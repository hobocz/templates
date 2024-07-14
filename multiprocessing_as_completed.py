#!/usr/bin/env python3
"""
File name: multiprocessing_example.py
Description: A simple starter template for the 'use as completed' 
    multiprocessing pattern. NOTE: This implementation uses
    ProcessPoolExecutor and as_completed from concurrent.futures.
    I found this to be a simple, intuitive and robust choice
    however there are certainly other options.
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-05
"""

import sys
import argparse
import logging
import pathlib
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from time import sleep
import random

def a_job(job_id: int = 1, max_time: int = 2) -> str:
    """
    Waits for a random interval to simulate work. Returns a string.

    Parameters
    ----------
    job_id : int
        A unique job number.
    max_time : int
        The maximum time for the job to wait (in seconds).

    Returns
    -------
    str
        A string indicating it's result.
    """
    interval = random.randint(1, max_time)
    sleep(interval)
    return f'Job #{str(job_id)}, interval: {str(interval)}'

def main() -> 1:
    # --------------------------------------------------
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    parser.add_argument('-n', '--num_jobs', type=int, default=10,
        help='The number of jobs to run.')
    parser.add_argument('-m', '--max_time', type=int, default=2,
        help='The maximum time for each job to sleep.')
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
    with ProcessPoolExecutor() as PPE:
        job_future_list = [PPE.submit(a_job, n, args.max_time) for n in range(args.num_jobs)]
        for job_future in as_completed(job_future_list):
            print(job_future.result())
            
    return 0

if __name__ == '__main__':
    sys.exit(main())
