#!/usr/bin/env python3
"""
File name: foobar.py
Description: Does some amazing things, then some more amazing
    things, then some more. Wow it's amazing.
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-08-22

This script requires that "some_module" be installed within the Python
environment you are running this script in.
"""

import sys
import argparse
import logging
import pathlib

def find_files(search_dir: pathlib.Path, search_string: str) -> list[str]:
    """
    Search for file containing search_string. Return a list of file names.

    Parameters
    ----------
    search_dir : pathlib.Path
        The directory to start searching.
    search_string : str
        The string to match in the file name.

    Returns
    -------
    list[str]
        A list of file name strings.
    """
    file_match = re.compile(search_string)
    file_list = []
    for dir in pathlib.Path(search_dir).glob('**/'): # recursively get directories
        latest_file = None
        for file in dir.glob('*'):
            if file_match.search(file):
                if not latest_file:
                    latest_file = file
                elif file.stat().st_mtime > latest_file.stat().st_mtime:
                    latest_file = file
        if latest_file:
            if '.xlsx' not in str(latest_file): # it is old '.xls' format
                print('### File Error:', str(latest_file), '\n    This file has newest modified stamp but is ".xls" format')
                err_count += 1
            else:
                file_list.append(latest_file)

    print(len(file_list), 'issues list files found')
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
        help='The directory from where to start the search for matching files')
    args = parser.parse_args()
    # Set up logging
    if args.log_file is not None:
        # Note: filemode is set to clobber by default
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)
    

    # Functionality goes here
    find_files(args.search_dir, args.search_string)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())