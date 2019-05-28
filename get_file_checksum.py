#!/usr/bin/env python3
from hashlib import md5
from os import open as os_open, read as os_read, close as os_close
from os import O_RDONLY
from os.path import isabs, getsize


def get_file_checksum(file_path_name, size=-1):
    """Get the checksum of the content of a file

    Args:
        file_path_name (str): The absolute path of the file
        size (int): The amount of bytes read from the file that will
            be hashed. 0 and negative numbers will result in reading
            the whole file. Default is -1

    Returns:
        str: The hash value of the content of the file. Will be empty
            if there is any errors happens during the handling of the
            file content

    Raises:
        ValueError: When the file_path_name is not corrrectly formated as
            an absolute path.

    """
    if not isinstance(file_path_name, str):
        raise TypeError("file_path_name must be a str type object")
    elif not isinstance(size, int) and size is not None:
        raise TypeError(
            "size must be either left unspecified or is an int type object"
        )
    elif not isabs(file_path_name):
        raise ValueError("file_path_name must be an absolute path")
    try:
        if size <= 0:
            size = getsize(file_path_name)
        # Generate hash algorithm
        hash_algorithm = md5()
        # Open, read, generate hash value
        file_descriptor = os_open(file_path_name, O_RDONLY)
        content = os_read(file_descriptor, size)
        os_close(file_descriptor)
        hash_algorithm.update(content)
        return hash_algorithm.hexdigest()
    except OSError:
        return ""
