#!/usr/bin/env python3
"""
File name: decorator_example.py
Description: A simple template for implementing decorator functions. It
    prints a random list of numbers (each from 1-10) but the decorator
    ensures the numbers can only be odd.
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-04
"""

import sys
import argparse
import logging
import pathlib
import random

def only_odd(func):
    """
    Type hinting is not used here because of unknown compatibility
        with decorators (implemented in 3.10?)
    """
    def odd_func(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            if (result % 2) != 0:
                logging.info('@decorated: It\'s odd! I love odd numbers!')
                break
            else:
                logging.info('@decorated: It\'s even! Throw it away!')
        return result
    return odd_func

@only_odd
def get_a_number() -> int:
    """
    Returns a random integer from 1 to 10.

    Returns
    -------
    int
        Random integer.
    """
    num = random.randint(1, 10)
    logging.info('Got number: ' + str(num))
    return num

def main() -> 1:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    parser.add_argument('-t', '--total_numbers', type=int, default=5,
        help='The total random numbers you want.')
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
    odds_only = []
    for t in range(args.total_numbers):
        odds_only.append(get_a_number())
    print('Here\'s my final list of numbers:')
    print(odds_only)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())