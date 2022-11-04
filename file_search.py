#!/usr/bin/env python3
"""
File name: file_search.py
Description: Performs a simple file search given a starting directory and 
    a search string. Can optionally return only the newest file (latest modified 
    timestamp) in a directory if multiple files are found within that directory.
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-22

"""

import sys
import argparse
import logging
import pathlib
import re

def find_files(search_dir: pathlib.Path, search_string: str, newest_only: bool = False) -> list[str]:
    """
    Search for file containing search_string. Return a list of file names.

    Parameters
    ----------
    search_dir : pathlib.Path
        The directory to start searching.
    search_string : str
        The string to match in the file name.
    newest_only : bool
        For each directory, only return the file with the latest modified timestamp.

    Returns
    -------
    list[str]
        A list of file name strings.
    """
    # Find the files
    file_match = re.compile(re.escape(search_string), re.IGNORECASE)
    file_list = []
    for dir in pathlib.Path(search_dir).glob('**/'): # recursively get directories one at a time
        latest_file = None
        #for file in dir.glob(search_string):
        for file in dir.iterdir():
            if file.is_file() and file_match.search(file.name):
                if newest_only:
                    if not latest_file:
                        latest_file = file
                    elif file.stat().st_mtime > latest_file.stat().st_mtime:
                        latest_file = file
                else:
                    file_list.append(str(file))
        if newest_only and latest_file:
            file_list.append(str(latest_file))

    return file_list

def main() -> 1:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    parser.add_argument('-d', '--search_dir', default=pathlib.Path().cwd(), type=pathlib.Path,
        help='The directory from where to start the search for matching files')
    parser.add_argument('-s', '--search_string', required=True, type=str,
        help='The string to search in the file names')
    parser.add_argument('-n', '--newest_only', action='store_true',
        help='For each directory, only return the file with the newest modified timestamp')
    args = parser.parse_args()
    # Validate command line arguments (if necessary)
    if not args.search_string.isascii() or '/' in args.search_string or '\\' in args.search_string:
        logging.critical('--search_string is restricted to the ASCII character set, and cannot include "/" or "\\"')
        return 1
    # Set up logging
    if args.log_file:
        # Note: filemode is set to clobber by default
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)

    # Functionality starts here
    file_list = find_files(args.search_dir, args.search_string, args.newest_only)
    if not file_list:
        print("No files found")
    else:
        for f in file_list:
            print(f)
    return 0

if __name__ == '__main__':
    raise sys.exit(main())