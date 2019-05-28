#!/usr/bin/env python3
from os import getcwd, sep
from os.path import isabs, islink, dirname, join


def extend_file_path_to_absolute(file_path, separator=sep):
    """Extend a relative file path to an absolute file path by extending
    `.` and `..` from the file path

    Args:
        file_path (str): The relative file path that needs to be extended
        separator (str): The separator between parts of the file path.
            Default is the separator from os.sep.

    Returns:
        str: The absolute file path derived from the relative file path
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a str type object")
    # Return the file path if it's already an absolute file path
    if isabs(file_path):
        return file_path
    # Split the file path using the separator
    path_component = file_path.split(separator)
    current_directory = getcwd()
    """
    Continuously reduce the current directory string till no . or .. is found
    at the beginning of the file path
    """
    try:
        while path_component[0] in (".", ".."):
            if path_component[0] == "..":
                current_directory = dirname(current_directory)
            path_component.pop(0)
    except IndexError:
        pass
    """
    Return the joined path of current directory and the rest of the
    components from the original file path
    """
    return join(current_directory, *path_component)
