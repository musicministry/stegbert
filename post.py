# =============================================================================
# author: mgrossi
# date:   12 February 2026
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
# To manually post a celebration that is not in the liturgical calendar (e.g.,
# Confirmation), use `--publish "occasions: occasion"` where `occasions.py` is
# the name of the file containing the music schedule(s) and `occasion` is the
# name of the celebration to post. In this use case, the hymn schedule dict
# requires `season` key indicating the liturgical season of the celebration and
# `date` of the format "YYYY-MM-DD HH:MM" specifying the date and time of the
# celebration.
#
# To execute in terminal:
# python post.py 2026
#
#     or
#
# python post.py 2026 --publish '2025-11-30'
#
#     or
#
# python post.py 2026 --publish 'advent01'
#
#     or
#
# python post.py 2026 -p 'occasions: confirmation'
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

args = parse_args()

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
#     publish = 'occasions: confirmation'
# )

# =========================================================================== #
# Main program

def main():
    # GitHub token
    u.load_env_file()
    token = os.environ.get('GITHUB_TOKEN')

    # Path for hymn list files
    cycle = u.lityear(args.year)
    process_dir = f'{args.year}-{cycle}'
    sys.path.append(os.path.join(process_dir))

    # Manual postings
    if ":" in args.publish:

        # Get feast and schedule file name from `--publish` argument
        year = args.year
        season = args.publish.split(':')[0].strip()
        feast = args.publish.split(':')[1].strip()
        print(f'Loading {titlecase(feast)} from {season}.py')
    
    # Pull from liturgical calendar
    else:

        lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
        cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                        parse_dates=['date'], index_col='feast')

        # Get next Sunday, if needed
        if args.publish.lower() == 'next':
            today = dt.datetime.today()
            next_sun = u.next_sunday(from_date=today)
            publish = str(next_sun)
            print(f'Publishing next Sunday {u.fmtdate(next_sun)}')
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

        # Subset calendar
        df = cal.loc[feast]
        season = df['season']
        feast_name = df['name']
        year = df['year']
        day = str(df['day']).zfill(2)

    # Load the schedules and fix the keys
    hymn_lists = u.load_hymn_schedules(season)
    hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}
    hymns = hymn_lists[feast]

    # Check for lists before proceeding
    u.check_for_lists(hymns, context="hymn dictionary")

    # Check video availability
    linkcheck = {}
    ra_linkcheck = {}
    for k,v in hymns.items():
        # Ignore RA, Mass setting info, season, and date, if provided
        if (k.lower() == 'mass') or (k.lower() == 'ra') or (k.lower() == 'season') or (k.lower() == 'date'):
            pass
        # Handle Mass parts separately
        elif k.lower() == 'parts':
            names = [' '.join(i.split(': ')[::-1]) for i in v]
            urls = [u.get_url(i) for i in names]
            linkcheck.update({u.keyify(name):link for name, link in zip(names, urls)})
        # Separate dict for R&A, since we don't need a repo issue for these
        elif 'http' in v:
            ra_linkcheck.update({' '.join([feast, k]): v})
        # Otherwise, just keyify the hymn name and get the URL
        else:
            name = u.keyify(v.split(' - ')[-1].strip())
            link = u.get_url(name)
            linkcheck.update({name: link})

    # Parse the dictionary
    mass = hymns['Mass']
    parts = hymns['parts']
    hymns.pop('Mass')
    hymns.pop('parts')

    if ":" in args.publish:
        feast_name = titlecase(feast)
        date = dt.datetime.strptime(hymns['date'], "%Y-%m-%d %H:%M")
        day = str(date.day).zfill(2)
        season = hymns['season']
        hymns.pop('season')
        hymns.pop('date')

    # Add Gloria omission if needed
    if all('gloria' not in p.lower() and (season == 'advent' or season == 'lent') for p in parts):
        parts.insert(0, f'Gloria: *Gloria omitted during {titlecase(season)}*')

    # File name
    if args.outfile.lower() == 'auto':
        outfile = os.path.join('posts', f'{str(date.date())}-{feast}.qmd')
    else:
        outfile = os.path.join('posts', args.outfile)

    with open(outfile, 'w') as file:
        # Header
        file.write('---\n')
        file.write(f'title: {feast_name}\n')
        file.write(f'last-updated: {str(date.date()-dt.timedelta(days=5))}\n')
        file.write(f'description: {u.fmtdate(date)}\n')
        file.write('categories:\n')
        file.write(f'  - {titlecase(u.unkey(season))} {year}\n')
        file.write(f'image: /_images/dates/{dt.datetime.strftime(date, format="%b").lower()}/{day}.png\n')
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

        file.write(u.video_table(hymns=hymns))

        # Mass parts
        file.write('### Mass Parts\n\n')

        file.write(f'The Mass parts for {u.unkey(season)} will be taken from *{mass}*:\n\n')

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
        # Only check YouTube videos
        if status.lower() != 'invalid url format' and 'omitted' not in k:
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
            print("✗ Failed to create issue for unavailable videos")
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
            print("✗ Failed to create issue for missing videos")
    else:
        print("✓ No missing video URLs found")

    print("="*60 + "\n")

if __name__ == "__main__":
    main()
