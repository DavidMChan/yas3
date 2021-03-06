from typing import Any, Optional, Generator
import warnings
import pathlib
import filetype

import boto3

from yas3.utils import guess_mimetype, load_to_bytes_if_filepath
from yas3.aws import test_aws_acl


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

    # Utilities
    def _set_to_default_bucket_if_none(self, bucket):
        if bucket is None:
            if self._default_bucket is None:
                raise ValueError('Bucket must be specified if default bucket was not specified in connection.')
            bucket = self._default_bucket
        return bucket

    # Bucket Operations
    def list_buckets(self,) -> Generator[str, None, None]:
        for b in self._s3_client.list_buckets()['Buckets']:
            yield b['Name']

    def list_files(self, bucket: Optional[str] = None) -> Generator[str, None, None]:
        bucket = self._set_to_default_bucket_if_none(bucket)
        c_token = None

        while True:
            response = self._s3_client.list_objects_v2(Bucket=bucket, ContinuationToken=c_token)
            for elem in response['Contents']:
                yield elem['Key']
            if not response['IsTruncated']:
                break
            c_token = response['NextContinuationToken']

    # File Operations
    def upload(self,
               data_or_file_path: Any,
               key: str,
               bucket: Optional[str] = None,
               mimetype: Optional[str] = None,
               permissions: str = 'private') -> None:

        data = load_to_bytes_if_filepath(data_or_file_path)
        ftype = guess_mimetype(data, mimetype)
        bucket = self._set_to_default_bucket_if_none(bucket)
        test_aws_acl(permissions)

        self._s3_client.put_object(Key=key, Body=data, ACL=permissions, ContentType=ftype, Bucket=bucket)

    def download(self,
                 key: str,
                 download_path: str,
                 bucket: Optional[str] = None,
                 chunk_size: int = 1024) -> None:
        bucket = self._set_to_default_bucket_if_none(bucket)
        with open(download_path, 'wb') as ofile:
            for chunk in self._s3_client.get_object(Key=key, Bucket=bucket)['Body'].iter_chunks(chunk_size):
                ofile.write(chunk)

    def get(self, key: str, bucket: Optional[str] = None) -> bytes:
        bucket = self._set_to_default_bucket_if_none(bucket)
        return self._s3_client.get_object(Key=key, Bucket=bucket)['Body'].read()

    def delete(self, key: str, bucket: Optional[str] = None, version_id: Optional[str] = None) -> None:
        bucket = self._set_to_default_bucket_if_none(bucket)
        self._s3_client.delete_object(Key=key, Bucket=bucket, VersionId=version_id)

    def copy(self, from_key: str, to_key: str, from_bucket: Optional[str] = None, to_bucket: Optional[str] = None ) -> None:
        from_bucket = self._set_to_default_bucket_if_none(from_bucket)
        to_bucket = from_bucket if to_bucket is None else to_bucket
        self._s3_client.copy_object(CopySource={'Bucket': from_bucket, 'Key': from_key}, Bucket=to_bucket, Key=to_key, )

    def move(self, from_key: str, to_key: str, from_bucket: Optional[str], to_bucket: Optional[str]) -> None:
        from_bucket = self._set_to_default_bucket_if_none(from_bucket)
        to_bucket = from_bucket if to_bucket is None else to_bucket
        self.copy(from_key=from_key, to_key=to_key, from_bucket=from_bucket, to_bucket=to_bucket)
        self.delete(key=from_key, bucket=from_bucket)

    # Context management
    # NOTE: This is primarily just to make people feel better about using the code. There's really no context in the
    # BOTO3 clients, since everything is done by REST API calls.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
