# =============================================================================
# author: mgrossi
# date:   20 December 2025
#
# This script creates a Quarto markdown page containing music schedules from
# the date or feast passed to `-s, --start` through the date or feast passed to
# `-e, --end` for the calendar year passed to `-y, --year`. The output file
# name can optionally be set using the `-o, --output` flag and defaults to
# `upcoming.qmd` if no argument is passed. The music lists to populate the
# file are taken from `.py` files for each season (e.g., `advent.py`,
# `christmas.py`) containing dictinaries (one per liturgy) where the keys
# specify hymn in the Mass (e.g., "Professional") and the value is the name of
# the hymn. Each dictionary should also contain URLs for responsorial psalms
# and gospel acclamations, the name of the Mass setting to be used, and a list
# of Mass parts to include.
#
# To execute in terminal:
# python upcoming.py --year 2026 --start 'advent01' --end 'advent04'
#
#     or
#
# python upcoming.py --year 2026 --start '2025-11-30' --end '2025-12-21'
#
# or a combination of date/feast.
#
# Feast names are taken from the name of the dictionaries containing the
# music schedules and must be a name found in the `name` column of the
# liturgical calendar dataframe.
#
# --------------------------------------------------------------------------- #
# Packages
from titlecase import titlecase
import datetime as dt
import pandas as pd
import argparse
import sys
import os
import utils as u

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Function control parameters.',
        prog='upcoming',
        usage='%(prog)s [arguments]')
    parser.add_argument('-y', '--year', metavar='year', type=int,
                        help='Four-digit year to process')
    parser.add_argument('-s', '--start', type=str,
                        help='First date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('-e', '--end', type=str,
                        help='Last date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='upcoming.qmd',
                        help='Name and directory of csv file to write. Default to "[pwd]/upcoming.qmd"')
    parser.add_argument('-c', '--callout', nargs='?', type=str,
                         help='Optional text to include in a callout at the top of the page')
    return parser.parse_args()

# class Args:
#     def __init__(self, year, start, end, callout=None):
#         self.year = year
#         self.start = start
#         self.end = end
#         self.callout = callout

# args = Args(
#     year = 2026,
#     start = 'christmas-day',
#     end = 'baptism',
#     callout = 'The Mass setting changes for Advent, the Solemnity of the Immaculate Conception, and Christmas.'
# )

args = parse_args()
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

# Start date and feast
try:
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    start = cal.loc[start_date,'feast']
except ValueError as e:
    start_date = cal.loc[cal['feast']==start].index[0]

# End date and feast
try:
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    end = cal.loc[end_date,'feast']
except ValueError as e:
    end_date = cal.loc[cal['feast']==end].index[0]

# Subset calendar
df = cal[start_date:end_date]

# Create a qmd file
first_feast = df.loc[df['feast']==start, "name"].iloc[0]
last_feast = df.loc[df['feast']==end, "name"].iloc[0]
first_date = dt.datetime.strftime(start_date, "%B %d, %Y")
last_date = dt.datetime.strftime(end_date, "%B %d, %Y")

with open(args.outfile, 'w') as file:
    # Header
    file.write('---\n')
    file.write(f'first-feast: {first_feast}\n')
    file.write(f'first-date: {first_date}\n')
    file.write(f'last-feast: {last_feast}\n')
    file.write(f'last-date: {last_date}\n')
    file.write('title: Hymn Schedules\n')
    file.write(f'subtitle: "**{first_date}** ({first_feast}) through **{last_date}** ({last_feast})"\n')
    file.write('---\n\n')

    # Preface
    file.write("""All hymns are taken from the blue *Gather* hymnal unless otherwise noted. “R&A” indicates *Respond and Acclaim*. Christmas season Mass parts will be provided as handouts. Click on any title to listen to a recording for rehearsal purposes, but note that the lyrics may not match our hymnal. Please practice the lyrics in the *Gather* hymnal, regardless of the video.\n\n""")

    # Callout
    if args.callout is not None:
        file.write(
            f'::: {{.callout-important title="Take heed!"}}\n' \
            f'{args.callout}\n' \
            ':::\n\n'
        )
    
    # Hymn schedules
    file.write(
        ':::: {.content-visible when-format="html"}\n' \
        '::: {.titlered}\n' \
        '### &nbsp;&#x2720; Hymn Schedules\n' \
        ':::\n' \
        '::::\n\n'
    )

    # Loop through the seasons that are encompassed in the `start`-`end` range
    mass_list = {}
    for season in list(df['season'].unique()):
        # Subset the dataframe
        ss = df[df['season']==season]

        # Load the schedules and fix the keys
        hymn_lists = u.get_hymn_lists(season)
        hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}

        # Get the Mass settings and parts
        masses = [hymn_lists[k]['Mass'] for k in hymn_lists.keys()]
        parts = [hymn_lists[k]['parts'] for k in hymn_lists.keys()]

        # Add Gloria omission if needed
        for part in parts:
            if all('gloria' not in p.lower() and (season == 'advent' or season == 'lent') for p in part):
                part.insert(0, f'*Gloria omitted during {titlecase(season)}*')

        # Create a list of all unique Mass settings to include at the bottom of the
        # page (duplicate key:value pairs are ignored when updating dictionaries)
        mass_list.update({k:v for k,v in zip(masses, parts)})

        # Loop through each week and create the header and table
        for i, r in enumerate(ss.itertuples()):
            if r.feast in hymn_lists.keys():
                file.write(f'#### {u.fmtdate(r.Index)} [{r.name}]{{style="float:right"}}\n\n')

                hymns = hymn_lists[r.feast]
                file.write(u.simple_table(hymns, file=file))
        file.write('\n')
    
    # Mass settings
    file.write(
        '::: {.titlered}\n' \
        '### &nbsp;&#x2720; Mass Settings\n' \
        ':::\n\n'
    )
    for mass, parts in mass_list.items():
        file.write(f'#### {mass}\n\n')

        for part in parts:
            try:
                p, m = part.split(':')
                file.write(f"- {u.md(f'{m.strip()}: {p.strip()}')}\n")
            except ValueError:
                file.write(f"- {part}\n")
            
        file.write('\n')

print(f'"{args.outfile}" file created.')