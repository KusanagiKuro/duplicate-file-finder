#!/usr/bin/env python3
from os.path import isabs, isfile, islink
from get_file_checksum import get_file_checksum


def group_files_by_checksum(file_path_names):
    """Split the files whose paths are specified in a list
    into groups based on their checksum hashes

    Args:
        file_path_names (list): Contains string represents
            the absolute paths of the files

    Returns:
        list: Contains lists of file paths whose files have
            the same hash

    Raises:
        ValueError: If the file_path_names list contains elements that
            are either not string or not in absolute file path format
    """
    if not isinstance(file_path_names, list):
        raise TypeError("file_path_names must be a list type object")
    elif not all([isinstance(file_path, str) and isabs(file_path)
                  for file_path in file_path_names]):
        raise ValueError(
            "Not all elements in file_path_names are correcly formatted"
        )
    """
    Initialize dictionary that holds all files with same hash as value
    and their hash value as key
    """
    hash_dict = {}
    for file_path_name in file_path_names:
        # Ignore path that resolves into a directory
        if not isfile(file_path_name):
            continue
        # Get the hash value of the file and add to group accordingly
        hash_value = get_file_checksum(file_path_name)
        try:
            hash_dict[hash_value].append(file_path_name)
        except KeyError:
            hash_dict[hash_value] = [file_path_name]
    # Return the list of groups of files with same hash value
    return [
        value for key, value in hash_dict.items()
        if key and len(value) > 1
    ]
