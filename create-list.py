# =============================================================================
# author: mgrossi
# date:   20 December 2025
#
# This script extracts hymn selections from the music planning book repo for
# all of the weeks between `start` and `end`, inclusive, for year `year`;
# re-formats them into more consolidated dictionaries, one per feast; and
# writes these to a single `.py` file to be processed by `upcomping.py`.
# Optionally exclude lower priority feasts by passing the number of the
# lowest-desired celebration priority to `-p, --priority`:
#     -> 2 for Sundays and holy days of obligation
#     -> 1 for important days that are not holy days (e.g., Ash Wednesday)
#     -> 0 otherwise
# If the priority flag is not passed, all celebrations will be pulled. The
# output file name defaults to `next-lists.py`, which can be changed using the
# optional `-o, --outfile` flag.
#
# Note that all hymn options are extracted when available and listed by
# priority (required, preferred, optional). The output file must be reviewed
# manually to whittle down these options to one per entry; otherwise,
# `upcoming.py` will fail. The output file name, if the default was used,
# should be changed after manual review to prevent it from getting overwritten
# in the future.
#
# To execute in terminal:
#
#     python create-list.py 2026 'advent01' 'advent04' --priority 1
#
# or
#
#     python create-list.py 2026 '2025-11-30' '2025-12-21'
#
# or a combination of date/feast. Feast names are taken from the name of the 
# dictionaries containing the music schedules and must be a name found in the
# `name` column of the liturgical calendar dataframe.
#
# --------------------------------------------------------------------------- #
# Packages
import datetime as dt
import pandas as pd
import argparse
import yaml
import sys
import os
import utils as u

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Function control parameters.',
        prog='upcoming',
        usage='%(prog)s [arguments]')
    parser.add_argument('year', metavar='year', type=int,
                        help='Four-digit year to process')
    parser.add_argument('start', type=str,
                        help='First date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('end', type=str,
                        help='Last date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('-p', '--priority', type=int, default=0,
                        help='Interger [0,2] indicating the lowest priority celebration to extract. Default to 0 to extract everything.')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='next-lists.py',
                        help='Name and directory of csv file to write. Default to "[pwd]/[yearDir]/next_lists.py"')
    return parser.parse_args()

args = parse_args()

# # For testing
# class Args:
#     def __init__(self, year, start, end, priority=0, outfile='next-lists.py'):
#         self.year = year
#         self.start = start
#         self.end = end
#         self.priority = priority
#         self.outfile = outfile

# args = Args(
#     year = 2026,
#     start = 'ot02',
#     end='ot06',
#     priority = 1,
# )

start = args.start
end = args.end

# --------------------------------------------------------------------------- #
# Main program

# Load hymn lists
cycle = u.lityear(args.year)
process_dir = f'{args.year}-{cycle}'
sys.path.append(os.path.join(process_dir))

lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                parse_dates=['date'], index_col='date')
cal = cal[cal['priority'] >= args.priority]

# Start date and feast
try:
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    start = cal.loc[start_date,'feast']
except ValueError:
    start_date = cal.loc[cal['feast']==start].index[0]

# End date and feast
try:
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    end = cal.loc[end_date,'feast']
except ValueError:
    end_date = cal.loc[cal['feast']==end].index[0]

def main():
    # Get hymns for desired range
    cal.reset_index(inplace=True)
    results = u.process_week_range(start=start, end=end, df=cal, lit_year=cycle)

    # Write to file
    u.process_and_export_to_py(
        results=results,
        output_file=os.path.join(process_dir, args.outfile)
        )
    print(f'{args.outfile} created.')

if __name__ == "__main__":
    main()