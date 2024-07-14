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
from data_class_module import Company, Employee

def main() -> 1:
    # --------------------------------------------------
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    args = parser.parse_args()
    # --------------------------------------------------
    # Set up logging
    if args.log_file:
        # Note: filemode is set to clobber by default
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)

    # --------------------------------------------------
    # Functionality starts here
    a = Employee('John', 'Doe', 30)
    print('A new employee:', a.full_name())
    b = Employee('Jane', 'Doe', 32, 62534, 'Accounting')
    print('A new employee:', b.full_name())
    c = Employee('Jane', 'Doe', 32, 62534, 'HR')
    print('Employee "c" changed her department:', c.dept)
    print('Same employee?:', b == c)
    comp = Company('FooBar', [a,b,c])
    print('The company', comp.name, 'has these employees:')
    for emp in comp.employees:
        print(f'{emp.full_name()}: {emp.dept}')

    return 0

if __name__ == '__main__':
    sys.exit(main())