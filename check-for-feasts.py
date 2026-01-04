# =============================================================================
# author: mgrossi
# date:   23 December 2025
#
# This script checks for any celebrations during the next week before the next
# Sunday, since the next Sunday will be picked up by a separate GitHbub Action.
# The argument `-y, --year` specifies which liturgical calendar to load and use
# for checking. If any feasts do occur during the upcoming week, it will first
# check the hymn lists for a hymn schedule. If one exists, `post.py` will be
# executed to publish a post for it. Otherwise, a lack of music schedule
# implies the feast or solemnity is not being celebrated (or, if it is, there
# will be no music for it.)
#
# To execute in terminal:
# python check-for-feasts.py --year 2026
#
# =========================================================================== #
# Packages
import datetime as dt
import pandas as pd
import argparse
import os
import sys
import subprocess
import utils as u

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Function control parameters.',
        prog='upcoming',
        usage='%(prog)s [arguments]')
    parser.add_argument('-y', '--year', metavar='year', type=int,
                        help='Four-digit year to process')
    return parser.parse_args()

args = parse_args()

# # For testing
# class Args:
#     def __init__(self, year):
#         self.year = year
# args = Args(
#     year = 2026
# )

# --------------------------------------------------------------------------- #
# Main program

def main():
    # Load liturgical calendar
    cycle = u.lityear(args.year)
    process_dir = f'{args.year}-{cycle}'
    sys.path.append(os.path.join(process_dir))

    lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
    cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                      parse_dates=['date'], index_col='date')

    # Check for other feasts this week before next Sunday
    today = dt.datetime.today()
    next_sun = u.next_sunday(from_date=today)
    check = (cal.index > pd.to_datetime(today)) & \
            (cal.index < pd.to_datetime(next_sun))

    if int(sum(check)) > 0:
        # Extract any feasts this week (could be one or more)
        ss = cal[check]
        seasons = ss['season'].unique()

        # Load the hymn list(s) to see if music is scheduled
        for season in seasons:
            hymn_lists = u.get_hymn_lists(season)
            hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}

            # There may be more than one feast (e.g., Christmas Eve, Christmas Day)
            # Check each feast for scheduled music and, if there is a scheduled
            # line up, publish it.
            for feast in ss['feast']:
                if feast in hymn_lists.keys():
                    print(f"Posting for {ss[ss['feast']==feast]['name'].values[0]}")
                    subprocess.run(['python3', 'post.py', '--year', str(args.year),
                                    '--publish', feast])
                else:
                    print(f"{ss[ss['feast']==feast]['name'].values[0]} occurs this week but no music schedule was found. Nothing to process.")
    else:
        print("No occasions found.")
        return

if __name__ == "__main__":
    main()