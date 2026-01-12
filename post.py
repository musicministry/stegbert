# =============================================================================
# author: mgrossi
# date:   20 December 2025
#
# This script creates a Quarto markdown page containing the music lineup for a
# single liturgy in calendar year `year`. (Note that for Advent and Christmas,
# `year` should be the next calendar year.) A specific date or feast can be
# processed by passing the date or feast to `-p, --process`; otherwise, the
# next Sunday following script execution will be processed. The output file
# name can optionally be set using the `-o, --output` flag and defaults to
# `[pwd]/posts/YYYY-MM-DD-feast.qmd` if no argument is passed, where
# "YYYY-MM-DD" is the date of the liturgy and "feast" is the celebration for
# that date. An optional callout can be added to the top of the page using the
# `-c, --callout` flag.
# 
# The music list to populate the file are taken from `.py` files for each
# season (e.g., `advent.py`, `christmas.py`) containing dictinaries (one per
# liturgy) where the keys specify hymn in the Mass (e.g., "Professional") and
# the value is the name of the hymn. Each dictionary should also contain URLs
# for responsorial psalms and gospel acclamations, the name of the Mass
# setting to be used, and a list of Mass parts to include.
#
# To execute in terminal:
# python post.py 2026
#
#     or
#
# python upcoming.py 2026 --publish '2025-11-30'
#
#     or
#
# python upcoming.py 2026 --publish 'advent01'
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
    parser.add_argument('year', metavar='year', type=int,
                        help='Four-digit year to process')
    parser.add_argument('-p', '--publish', type=str, default='next',
                        help='Date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to publish. Defaults to next Sunday.')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='auto',
                        help='Name and directory of csv file to write. Default to "posts/YYYY-MM-DD-feast.qmd"')
    parser.add_argument('-c', '--callout', nargs='?', type=str,
                        help='Optional text to include in a callout at the top of the page')
    return parser.parse_args()

# =========================================================================== #
# Local development

# class Args:
#     def __init__(self, year, publish='next', outfile='auto', callout=None):
#         self.year = year
#         self.publish = publish
#         self.outfile = outfile
#         self.callout = callout

# args = Args(
#     year = 2026,
#     publish = 'baptism'
# )

# =========================================================================== #

# Command line arguments
args = parse_args()

# GitHub token
u.load_env_file()
token = os.environ.get('GITHUB_TOKEN')

# --------------------------------------------------------------------------- #
# Main program

def main():
    # Load hymn lists
    cycle = u.lityear(args.year)
    process_dir = f'{args.year}-{cycle}'
    sys.path.append(os.path.join(process_dir))

    lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
    cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                    parse_dates=['date'], index_col='feast')

    # Get next Sunday, if needed
    if args.publish.lower() == 'next':
        today = dt.datetime.today()
        next_sun = u.next_sunday(from_date=today)
        publish = str(next_sun)
        print(f'Publishing next Sunday {dt.datetime.strftime(next_sun, format="%B %d, %Y")}')
    else:
        publish = args.publish

    # Date and feast
    try:
        date = dt.datetime.strptime(publish, '%Y-%m-%d')
        feast = cal[cal['date']==publish].index
        if len(feast) > 1:
            raise IndexError(f'More than one liturgy was found for {dt.datetime.strftime(date.date(), format="%B %d")}. Please specify a feast to publish instead of a date and try again.')
        feast = feast[0]
    except ValueError:
        feast = publish
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
    hymns = hymn_lists[feast]

    # Check video availability
    linkcheck = {}
    ra_linkcheck = {}
    for k,v in hymns.items():
        # Ignore RA and Mass setting info
        if (k.lower() == 'mass') or (k.lower() == 'ra'):
            pass
        # Handle Mass parts separately
        elif k.lower() == 'parts':
            names = [' '.join(i.split(': ')[::-1]) for i in v]
            urls = [u.get_url(i) for i in names]
            linkcheck.update({u.keyify(n):l for n,l in zip(names, urls)})
        # Separate dict for R&A, since we don't need a repo issue for these
        elif 'http' in v:
            ra_linkcheck.update({' '.join([feast, k]): v})
        # Otherwise, just keyify the hymn name and get the URL
        else:
            name = u.keyify(v.split('-')[-1].strip())
            url = u.get_url(name)
            linkcheck.update({name: url})

    # Parse the dictionary
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
        file.write(f'  - {titlecase(df.season)} {df.year}\n')
        file.write(f'image: /_images/dates/{dt.datetime.strftime(date, format="%b").lower()}/{str(df["day"]).zfill(2)}.png\n')
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

    # Check URLs for video availability
    # Currently, no action is taken for R&A videos, since these are not
    # contained in the `song-urls` repo and these videos will have been
    # manually retrieved very recently.
    print('Checking video availability...')
    unavailable_videos = []
    missing_videos = []
    for k,v in linkcheck.items():
        has_url, is_available, status, title = u.check_video_availability(v)
        if not has_url:
            # Missing URL - needs to be added
            missing_videos.append({
                'hymn': k,
                'url': v,
                'status': status
            })
        elif not is_available:
            # URL exists but video unavailable
            unavailable_videos.append({
                'hymn': k,
                'url': v,
                'status': status
            })

    # Create GitHub issue for any unavailable video extracted from the
    # `musicministry/song-urls` repo
    if unavailable_videos or missing_videos:
        success, unavail_url, missing_url, skip_unavail, skip_missing = u.create_github_issues(
            unavailable_videos=unavailable_videos,
            missing_videos=missing_videos,
            token=token,
            owner='musicministry',
            target_repo='song-urls'
        )

    # Print summary
    print("\n" + "="*60)
    print("VIDEO CHECK SUMMARY")
    print("-"*60)

    # Unavailable videos (broken URLs)
    if unavailable_videos:
        new_unavail = len(unavailable_videos) - skip_unavail
        if unavail_url:
            print(f"✓ Created issue for {new_unavail} unavailable video(s)")
            print(f"  Issue: {unavail_url}")
        elif (skip_unavail != 0) and (skip_unavail == len(unavailable_videos)):
            print(f"⚠ All {len(unavailable_videos)} unavailable video(s) already flagged")
        else:
            print(f"✗ Failed to create issue for unavailable videos")
    else:
        print("✓ No unavailable videos found")

    # Missing videos (no URLs)
    if missing_videos:
        new_missing = len(missing_videos) - skip_missing
        if missing_url:
            print(f"✓ Created issue for {new_missing} missing video URL(s)")
            print(f"  Issue: {missing_url}")
        elif (skip_missing !=0) and (skip_missing == len(missing_videos)):
            print(f"⚠ All {len(missing_videos)} missing video(s) already flagged")
        else:
            print(f"✗ Failed to create issue for missing videos")
    else:
        print("✓ No missing video URLs found")

    print("="*60 + "\n")

if __name__ == "__main__":
    main()
