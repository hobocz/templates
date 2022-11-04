#!/usr/bin/env python3
"""
File name: foobar.py
Description: Does some amazing things, then some more amazing
    things, then some more. Wow it's amazing.
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-03

This script requires that "some_module" be installed within the Python
environment you are running this script in.
"""

import sys
import argparse
import logging
import pathlib

def example_function(parameter_a: int = 1) -> str:
    """
    Do <this> and return <that>.

    Parameters
    ----------
    parameter_a : int
        The number of times to print a message.

    Returns
    -------
    str
        A string saying something cool.
    """
    for x in range(parameter_a):
        logging.error('Test Error message ' + str(x+1))
    return 'Did it!'

def main() -> 1:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    args = parser.parse_args()
    # Set up logging
    if args.log_file:
        # Note: filemode is set to clobber by default
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)
    # Validate command line arguments (if necessary)


    # Functionality starts here
    logging.info('Started script - %s', 'newScript.py')
    print(example_function(3))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())