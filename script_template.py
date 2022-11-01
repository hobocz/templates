#!/usr/bin/env python3
# Description: 
# Author: Chris Zaleski
# Date: 

import sys
import argparse
import logging
import pathlib
    
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='WARNING', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    args = parser.parse_args()
    # Set up logging
    if args.log_file is not None:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)
    
    logging.info('Started script - %s', 'newScript.py')
    logging.error('Test Error message')


    return 0


if __name__ == '__main__':
    raise SystemExit(main())