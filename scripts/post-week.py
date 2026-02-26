# =============================================================================
# author: mgrossi
# date:   24 Jan 2025
#
# This script checks for any celebrations during the next week inclusive of the
# next Sunday in the calendar year `year`. For any feasts that occur during the
# upcoming week, it will first check the hymn lists for a hymn schedule. If one
# exists, `post.py` will be executed to publish a post for it. Otherwise, no 
# music schedule implies the feast or solemnity is not being celebrated (or, if
# it is, there will be no music for it), and a notification is printed for
# awareness. If `--pdf` is passed, PDF documents will also be generated.
#
# To execute in terminal:
# python post-week.py 2026
#
# -----------------------------------------------------------------------------
# Packages
import datetime as dt
import pandas as pd
import argparse
import os
import sys
import subprocess
import utils as u
from pathlib import Path

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Function control parameters.',
        prog='upcoming',
        usage='%(prog)s [arguments]')
    parser.add_argument('year', metavar='year', type=int,
                        help='Four-digit year to process')
    parser.add_argument('--pdf', action='store_true',
                        help='Produce a PDF of the post page for distribution.')
    return parser.parse_args()

args = parse_args()

# =============================================================================
# Local development

# class Args:
#     def __init__(self, year):
#         self.year = year
# args = Args(
#     year = 2026
# )

# =============================================================================
# Main program

def main():
    # Project home directory
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    # Load liturgical calendar
    cycle = u.lityear(args.year)
    process_dir = os.path.join(PROJECT_ROOT, f'{args.year}-{cycle}')
    sys.path.append(os.path.join(process_dir))

    lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
    cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                      parse_dates=['date'], index_col='date')

    # Check for feasts this week including next Sunday
    today = dt.datetime.today()
    next_sun = u.next_sunday(from_date=today)
    ss = cal.loc[today:next_sun]
    seasons = ss['season'].unique()

    # Load the hymn list(s) to see if music is scheduled
    for season in seasons:
        hymn_lists = u.load_hymn_schedules(season)
        hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}

        # There may be more than one feast (e.g., Christmas Eve, Christmas Day)
        # Check each feast for scheduled music and, if there is a scheduled
        # line up, publish it.
        for feast in ss['feast']:
            if feast in hymn_lists.keys():
                print(f"Posting for {ss[ss['feast']==feast]['name'].values[0]}")
                if args.pdf:
                    subprocess.run(['python3', 'scripts/post.py', str(args.year),
                                    '--publish', feast, '--pdf'])
                else:
                    subprocess.run(['python3', 'scripts/post.py', str(args.year),
                                    '--publish', feast])
            else:
                print(f"{ss[ss['feast']==feast]['name'].values[0]} occurs this week but no music schedule was found. Nothing to process.")

if __name__ == "__main__":
    main()