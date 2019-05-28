#!/usr/bin/env python3
from os.path import isabs, getsize, isfile, islink


def group_files_by_size(file_path_names):
    """Split the files whose paths are specified in a list
    into groups based on their sizes

    Args:
        file_path_names (list): Contains string represents
            the absolute paths of the files

    Returns:
        list: Contains lists of file paths whose files have
            the same size

    Raises:
        ValueError: If the file_path_names list contains elements that
            are either not string or not in absolute file path format
    """
    if not isinstance(file_path_names, list):
        raise TypeError("file_path_names must be a list type object")
    elif not all([isinstance(file_path_name, str) and isabs(file_path_name)
                  for file_path_name in file_path_names]):
        raise ValueError(
            "Not all elements in file_path_names are correcly formatted"
        )
    """
    Initialize dictionary that holds all files with same size as value
    and the size as key
    """
    size_dict = {}
    # Loop through files and split based on size
    for file_path_name in file_path_names:
        # Ignoring directory
        if not isfile(file_path_name):
            continue
        try:
            size = getsize(file_path_name)
        except OSError:
            continue
        try:
            size_dict[size].append(file_path_name)
        except KeyError:
            size_dict[size] = [file_path_name]
    # Return only the files whose sizes is larger than 0
    return [value for key, value in size_dict.items()
            if key and len(value) > 1]
