#!/usr/bin/env python3
from os import read as os_read, open as os_open, O_RDONLY,\
               close as os_close, stat as os_stat
from os.path import getsize, isabs
from stat import S_ISREG, S_IRUSR


READ_SIZE = 2048


def group_files_by_read_buffers(file_path_names, size=0):
    """Split the files whose paths are specified in a list
    into groups by reading and compare part-to-part of their content

    Args:
        file_path_names (list): Contains string represents
            the absolute paths of the files
        size (int): The size of each reading part

    Returns:
        list: Contains lists of file paths whose files are duplicated

    Raises:
        ValueError: If the file_path_names list contains elements that
            are either not string or not in absolute file path format
    """
    def read_and_compare(file1, file2):
        """Read and compare two files

        Returns:
            bool: True if two files have same contents, False if either
                size is different, content is different or error occured
        """
        # If file sizes are different, return False
        if getsize(file1) != getsize(file2):
            return False
        try:
            fd1 = open(file1, "rb")
        except OSError:
            return False
        try:
            fd2 = open(file2, "rb")
        except OSError:
            # Remove invalid file path from the file path list
            file_path_names.remove(file2)
            return False
        # Read till end of file or differents are spotted
        while True:
            # Read part of the file
            content1 = fd1.read(size)
            content2 = fd2.read(size)
            # If these parts are different, return False
            if content1 != content2:
                fd1.close()
                fd2.close()
                return False
            # If end of file is reached, return True
            if not content1:
                return True

    def check_for_duplicate():
        """Check for duplicate of the first element in the
        file path list and group them together

        Returns:
            list: Contains file path of files with same content as
                the first element in the path
        """
        equal_list = [file_path_names[0]]
        for _, file_path in enumerate(file_path_names[1:]):
            if read_and_compare(file_path, equal_list[0]):
                equal_list.append(file_path)
        return equal_list

    if not isinstance(file_path_names, list):
        raise TypeError("file_path_names must be a list type object")
    elif not all(isinstance(file_path_name, str) and isabs(file_path_name)
                 for file_path_name in file_path_names):
        raise ValueError(
            "Not all elements in file_path_names are correctly formatted"
        )
    # If size is negative or 0, set it to default read size
    if size <= 0:
        size = READ_SIZE
    duplicated_files = []
    # Loop till all file paths have been removed from original list
    while file_path_names:
        # Group all duplicate files into a list
        equal_list = check_for_duplicate()
        file_path_names = [item for item in file_path_names
                           if item not in equal_list]
        # Add the new duplicate group to the duplicate list
        if len(equal_list) > 1:
            duplicated_files.append(equal_list)
    return duplicated_files
