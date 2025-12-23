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
    parser.add_argument('-p', '--publish', type=str,
                        help='Date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to publish')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='auto',
                        help='Name and directory of csv file to write. Default to "posts/YYYY-MM-DD-feast.qmd"')
    parser.add_argument('-c', '--callout', nargs='?', type=str,
                        help='Optional text to include in a callout at the top of the page')
    parser.add_argument('-nocommit', metavar='nocommit', action='store_true', 
                        help='Do not automatically commit to GitHub.')
    parser.add_argument('-nopush', metavar='nopush', action='store_true', 
                        help='Do not automatically push to GitHub.')
    return parser.parse_args()

class Args:
    def __init__(self, year, publish, outfile='auto', callout=None, nocommit=False, nopush=False):
        self.year = year
        self.publish = publish
        self.outfile = outfile
        self.callout = callout
        self.nocommit = nocommit
        self.nopush = nopush

args = Args(
    year = 2026,
    publish = 'advent01'
)

args = parse_args()

# --------------------------------------------------------------------------- #
# Main program

# Load hymn lists
cycle = u.lityear(args.year)
process_dir = f'{args.year}-{cycle}'
sys.path.append(os.path.join(process_dir))

lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                  parse_dates=['date'], index_col='feast')

# Date and feast
try:
    date = dt.datetime.strptime(args.publish, '%Y-%m-%d')
    feast = cal[cal['date']==args.publish].index
    if len(feast) > 1:
        raise IndexError(f'More than one liturgy was found for {dt.datetime.strftime(date.date(), format="%B %d")}. Please specify a feast to publish instead of a date and try again.')
except ValueError:
    feast = args.publish
    date = cal.loc[feast]['date']

# File name
if args.outfile.lower() == 'auto':
    outfile = os.path.join('posts', f'{str(date.date())}-{feast}.qmd')
else:
    outfile = os.path.join('posts', args.outfile)

# Subset calendar
df = cal.loc[feast]
season = df.season

# Load the schedules and fix the keys
hymn_lists = u.get_hymn_lists(season)
hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}

# Parse the dictionary
hymns = hymn_lists[feast]
mass = hymns['Mass']
parts = hymns['parts']
RA = hymns['RA']
hymns.pop('Mass')
hymns.pop('parts')
hymns.pop('RA')

# Add Gloria omission if needed
if all('gloria' not in p.lower() and (season == 'advent' or season == 'lent') for p in parts):
    parts.insert(0, f'Gloria: *Gloria omitted during {titlecase(season)}*')

with open(outfile, 'w') as file:
    # Header
    file.write('---\n')
    file.write(f'title: {df["name"]}\n')
    file.write(f'last-updated: {str(date.date()-dt.timedelta(days=5))}\n')
    file.write(f'description: {dt.datetime.strftime(date, format="%B %d, %Y")}\n')
    file.write('categories:\n')
    file.write(f'  - {df.year}\n')
    file.write(f'  - {titlecase(df.season)}\n')
    file.write(f'image: /_images/dates/{dt.datetime.strftime(date, format="%b").lower()}/{int(df["day"])}.png\n')
    file.write('---\n\n')

    # Callout
    if args.callout is not None:
        file.write(
            f'::: {{.callout-important title="Take heed!"}}\n' \
            f'{args.callout}\n' \
            ':::\n\n'
        )

    # Lineup
    file.write('### Hymns\n\n')
    
    file.write('All hymns are taken from the blue Gather hymnal unless otherwise noted. Note that the lyrics may not match our hymnal. Please practice the lyrics in the Gather hymnal, regardless of the video.\n\n')

    file.write(u.video_table(hymns=hymns, RA=RA))

    # Mass parts
    file.write('### Mass Parts\n\n')

    file.write(f'The Mass parts for {titlecase(season)} will be taken from *{mass}*:\n\n')

    file.write(u.massparts_video_table(season=season, setting=mass, include=parts))

    file.write('\n')

print(f'"{outfile}" file created.')

# Commit to Git: For clarity, get the inverse of the arg flags, since they are
# used to supress the default behavior.
commit = not args.nocommit
push = not args.nopush
if commit:
    u.git_commit(
        file=outfile,
        message='Release next lineup'
        push=push)