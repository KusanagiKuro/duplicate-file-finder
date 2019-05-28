#!/usr/bin/env python3
from os import walk
from os.path import join, islink
from pathlib import Path
from utility import extend_file_path_to_absolute


def scan_files(root_path, ignore_link=True):
    """Scan and return the list of absolute paths of files inside
    the root directory. This scan will be recursive to the directories
    inside the root as well.

    Args:
        root_path (str): The (absolute/relative) path to the root directory
        ignore_link (bool): Whether symbolic link should be ignored
            during the scan or not

    Returns:
        list: A list of str represents the paths to the files inside
            the directory. Empty if root_path is not a directory or is not
            found
    """
    def get_full_path(root, file_name, ignore_link):
        """Get the full path for a file by joining the root and the file
        name.

        Args:
            root (str): The root directory
            file_name (str): The name of the file
            ignore_link (bool): Whether symbolic link will be ignored

        Returns:
            str: The joined path string between the root and the file
                name. If the path is a link and ignore_link is True,
                return empty string
        """
        file_path = join(root, file_name)
        if ignore_link and islink(file_path):
            return ""
        else:
            return file_path

    if not isinstance(root_path, str):
        raise TypeError("root_path must be a str type object")
    # Extend the root path to absolute path
    root_path = extend_file_path_to_absolute(root_path)
    try:
        # Return a list of absolute paths for files inside the directory
        return [
            file_path for file_path in [
                get_full_path(root, file_name, ignore_link)
                for root, _, files in walk(root_path)
                for file_name in files
            ]
            if file_path
        ]
    except (FileNotFoundError, PermissionError):
        return []
