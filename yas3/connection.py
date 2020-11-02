from typing import Any, Optional
import warnings
import pathlib
import filetype

import boto3


class Connection():
    """Connection Object for managing S3 connections in boto.
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint: Optional[str] = None,
        region: Optional[str] = None,
        tls: bool = False,
        default_bucket: str = None,
    ):

        # Construct the endpoint if not passed in
        if endpoint is None:
            if region is None:
                # No region/endpoints specified
                raise NotImplementedError(
                    'Cannot specify no endpoint, and no region for connection. Please specify at least a region (for AWS).'
                )
            # Region is specified
            endpoint = f"{'https://' if tls else 'http://'}s3.{region}.amazonaws.com"
        else:
            if tls:
                warnings.warn('TLS is specified and endpoint is specified. Make sure that your endpoint uses https://')

        # Construct the boto3 client
        self._s3_client = boto3.client('s3',
                                       aws_access_key_id=access_key,
                                       aws_secret_access_key=secret_key,
                                       endpoint_url=endpoint)

        self._default_bucket = default_bucket

    def list_buckets(self,):
        return [b['Name'] for b in self._s3_client.list_buckets()['Buckets']]

    def upload(self,
               file_data_or_file_path: Any,
               target_path: str,
               bucket: Optional[str] = None,
               mimetype: Optional[str] = None,
               permissions: str = 'private') -> None:

        if isinstance(file_data_or_file_path, (str, pathlib.Path)):
            # Open the file for reading, and guess the mimetype
            with open(pathlib.Path(file_data_or_file_path).expanduser().absolute(), 'rb') as fbytes:
                data = fbytes.read()
        elif isinstance(file_data_or_file_path, bytes):
            # Use the file bytes
            data = file_data_or_file_path
        else:
            raise NotImplementedError('Unknown data type or path.')

        # Setup or guess the data type
        if mimetype is None:
            ftype = filetype.guess(data)
            if ftype is None:
                ftype = 'application/octet-stream'
            else:
                ftype = ftype.mime
        else:
            ftype = mimetype

        # Setup the bucket
        if bucket is None:
            if self._default_bucket is None:
                raise ValueError('Bucket must be specified if default bucket was not specified in connection.')
            _obj_bucket = self._default_bucket
        else:
            _obj_bucket = bucket

        # Test ACL
        if permissions not in ('private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read',
                               'bucket-owner-read', 'bucket-owner-full-control'):
            raise ValueError('Permission string must be one of: ',
                             ('private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read',
                              'bucket-owner-read', 'bucket-owner-full-control'))

        self._s3_client.put_object(Key=target_path, Body=data, ACL=permissions, ContentType=ftype, Bucket=_obj_bucket)

    def download(self,
                 file_path: str,
                 download_path: str,
                 bucket: Optional[str] = None,
                 chunk_size: int = 1024) -> None:

        # Setup the bucket
        if bucket is None:
            if self._default_bucket is None:
                raise ValueError('Bucket must be specified if default bucket was not specified in connection.')
            _obj_bucket = self._default_bucket
        else:
            _obj_bucket = bucket

        with open(download_path, 'wb') as ofile:
            for chunk in self._s3_client.get_object(Key=file_path, Bucket=_obj_bucket)['Body'].iter_chunks(chunk_size):
                ofile.write(chunk)

    def get(self, file_path: str, download_path: str, bucket: Optional[str] = None) -> bytes:

        # Setup the bucket
        if bucket is None:
            if self._default_bucket is None:
                raise ValueError('Bucket must be specified if default bucket was not specified in connection.')
            _obj_bucket = self._default_bucket
        else:
            _obj_bucket = bucket

        return self._s3_client.get_object(Key=file_path, Bucket=_obj_bucket)['Body'].read()

    # Context management
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return
