#!/usr/bin/env python3
from argparse import ArgumentParser
from os.path import isabs
from scan_files import scan_files
from group_files_by_size import group_files_by_size
from group_files_by_checksum import group_files_by_checksum
from group_files_by_read_buffer import group_files_by_read_buffers
from json import dumps


def find_duplicate_files(file_path_names, quick=False):
    """Find duplicate files from a list of absolute file path

    Args:
        file_path_names (list): Consists of str type objects represent
            the absolute file paths

    Returns:
        list: Consists of groups of absolute paths of files with the same
            content
    """
    if not isinstance(file_path_names, list):
        raise TypeError("file_path_names must be a list type object")
    elif not all([isinstance(file_path, str) and isabs(file_path)
                  for file_path in file_path_names]):
        raise ValueError(
            "Not all elements in file_path_names are correcly formatted"
        )
    # Split the files into groups with same size
    file_size_groups = group_files_by_size(file_path_names)
    duplicated_files = []
    # Split each size group into groups that has same content
    for file_path_name_group in file_size_groups:
        duplicated_files.extend(
            group_files_by_checksum(
                file_path_name_group
            ) if not quick else
            group_files_by_read_buffers(
                file_path_name_group
            )
        )
    # Return all the groups
    return duplicated_files


def main():
    """Main function to run the program
    """
    def parse_arguments():
        """Create a parser for the program and use it to parse arguments

        Returns:
            ArgumentParser: The argument parser of the program
        """
        parser = ArgumentParser()
        parser.add_argument("-p", "--path", required=True, nargs=1,
                            dest="file_path", type=str, action="store",
                            help="path to the root directory")
        parser.add_argument("-q", "--quick", action="store_true",
                            default=False, dest="quick",
                            help="Speed up the search or not")
        return parser.parse_args()
    try:
        arguments = parse_arguments()
        # Get all files in the root directory, ignoring symlink
        file_path_names = scan_files(arguments.file_path[0])
        # Get groups of duplicated files
        duplicated_file_groups = find_duplicate_files(
            file_path_names, arguments.quick
        )
        # Print those groups in json format
        print(dumps(duplicated_file_groups, indent=4, separators=("", "")))
    except (TypeError, ValueError):
        return


if __name__ == "__main__":
    main()
