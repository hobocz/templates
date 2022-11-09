"""
File name: pandas_example.py
Description: Reads a csv file of 2022 baseball batting
    statistics and produces some simple analyses
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-08

This script requires that "pandas" and "matplotlib" be installed 
within the Python environment you are running this script in.

File: "MLB Player Batting 2022.csv" is credited to www.baseball-reference.com
"""

import sys
import argparse
import logging
import pathlib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main() -> 1:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='WARNING', choices=log_levels, 
        help='Verbosity of logging: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--log_file', type=pathlib.Path, default=None,
        help='Log file location. If not specified, log messages will be printed to the screen.')
    parser.add_argument('-d', '--data_file', type=pathlib.Path, default='test_data/MLB Player Batting 2022.csv',
        help='Location of the "MLB Player Batting 2022.csv" file.')
    args = parser.parse_args()
    # Set up logging
    if args.log_file:
        # Note: filemode is set to clobber by default
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=args.log_file, filemode='w',
            level=args.log_level, datefmt='%Y/%m/%d %I:%M:%S')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
            level=args.log_level, stream=sys.stdout)

    # PBDF = Player Batting DataFrame
    PBDF = pd.read_csv(args.data_file)
    # Update some column names for readability
    PBDF = PBDF.rename(columns={'Name': 'Player', 'Tm': 'Team'})
    # Remove records where Team is 'TOT' (this is an aggregate and creates redundancy)
    PBDF = PBDF[PBDF['Team'] != 'TOT']
    # change default 'object' dtypes to pandas preferred string type
    PBDF[['Player', 'Team', 'Lg', 'Pos Summary', 'Name-additional']] = \
        PBDF[['Player', 'Team', 'Lg', 'Pos Summary', 'Name-additional']].astype(pd.StringDtype())

    matplotlib.style.use('ggplot')

    HOU = PBDF[(PBDF['Team'] == 'HOU') & (PBDF['G'] >= 50)][['Player', 'R']]
    run_vals = HOU['R']
    run_vals.plot.pie(labels=HOU['Player'], title = 'Astros: Runs per player with\nat least 50 games', 
        ylabel = '', legend = False, autopct=lambda x: '{:.0f}'.format(x*run_vals.sum()/100))

    corr_value = PBDF['HR'].corr(PBDF['SO'], method = 'pearson')
    title_str = 'Home Runs vs Strike Outs\nPearson Correlation: ' + str(round(corr_value, 2))
    PBDF.plot.scatter(x ='HR', y ='SO', title = title_str, xlabel = 'Home Runs', ylabel = 'Strike Outs')
    z = np.polyfit(PBDF['HR'], PBDF['SO'], 1)
    p = np.poly1d(z)
    plt.plot(PBDF['HR'],p(PBDF['HR']),"r--")

    PBDF[['Team','HR']].boxplot(by = 'Team', xlabel = 'Home Runs', ylabel = 'Teams', vert = False)
    plt.suptitle('')
    plt.title('Distribution of Home Runs by Team')

    plt.show()

    return 0

if __name__ == '__main__':
    raise SystemExit(main())