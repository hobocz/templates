"""
File name: pandas_example.py
Description: Reads a csv file of baseball statistics and 
    produces some simple analyses and charts
Author: Chris Zaleski
Python Version: 3.x
Date: 2022-11-08

This script requires that "pandas" be installed within the Python
environment you are running this script in.

File: "MLB Player Batting 2022.csv" is credited to www.baseball-reference.com
"""

import sys
import argparse
import logging
import pathlib
import pandas as pd

def main() -> 1:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Please use command line options in the form --commands')
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='DEBUG', choices=log_levels, 
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

    # NOTE: The 'queries' of the Dataframe shown below intentionally attempt
    # to show a variety of pandas functionality
    team_count = PBDF['Team'].nunique()
    player_count = PBDF['Player'].nunique()
    print('=' * 50)
    print('The file contains', team_count, 'teams and', player_count, 'players')
    print('=' * 50)
    print('Here is the mean On-base Plus Slugging and Home Runs for each\n',
        'team, but only including players with at least 50 games:', sep='')
    result = (PBDF[PBDF['G'] >= 50].groupby('Team').mean(numeric_only=True)[['OPS', 'HR']]
        .sort_values(by='OPS', ascending=False)).round({'OPS':3, 'HR':1})
    print('-' * 50)
    print(result.to_string())

    print('=' * 50)
    print('Here are the top 10 Battting Averages for players with at\n',
        'least 200 Plate Appearances:', sep='')
    # We must group by player to account for players who played for multiple teams
    result = (PBDF[['PA', 'Player', 'BA']].groupby('Player').agg({'PA':'sum', 'BA':'mean'})
        .query('PA > 200').nlargest(10, 'BA')['BA'])
    print('-' * 50)
    print(result.to_string())

    print('=' * 50)
    print('Here are the top 10 Home Run to Strike Out Ratios for players\n',
        'with at least 50 Plate Appearances:', sep='')
    # We must group by player to account for players who played for multiple teams
    result = (PBDF.loc[lambda df: df['PA'] >= 50].groupby('Player').agg({'HR':'sum', 'SO':'sum'})
        .eval('HSRatio=HR/SO').nlargest(10, 'HSRatio')).round({'HSRatio':3})
    print('-' * 50)
    print(result.to_string())

    return 0

if __name__ == '__main__':
    raise SystemExit(main())