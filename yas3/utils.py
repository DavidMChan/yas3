
from typing import Optional, Union
import pathlib
import filetype


def guess_mimetype(data: Union[bytes, str, pathlib.Path], mimetype: Optional[str] = None) -> str:
    if mimetype is None:
        ftype = filetype.guess(data)
        if ftype is None:
            ftype = 'application/octet-stream'
        else:
            ftype = ftype.mime
    else:
        ftype = mimetype

    return ftype


def load_to_bytes_if_filepath(data_or_file_path: Union[bytes, str, pathlib.Path]) -> bytes:
    if isinstance(data_or_file_path, (str, pathlib.Path)):
        # Open the file for reading, and guess the mimetype
        with open(pathlib.Path(data_or_file_path).expanduser().absolute(), 'rb') as fbytes:
            data = fbytes.read()
    elif isinstance(data_or_file_path, bytes):
        # Use the file bytes
        data = data_or_file_path
    else:
        raise NotImplementedError('Unknown data type or path.')

    return data
