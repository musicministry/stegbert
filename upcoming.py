# =============================================================================
# author: mgrossi
# date:   20 December 2025
#
# This script creates a Quarto markdown page containing music schedules from
# the date or feast passed to `start` through the date or feast passed to `end`
# for the calendar year passed to `year`. The output file name can optionally
# be set using the `-o, --output` flag and defaults to `upcoming.qmd` if no
# argument is passed. The music lists to populate the file are taken from `.py`
# files for each season (e.g., `advent.py`, `christmas.py`) containing 
# dictinaries (one per liturgy) where the keys specify the hymn in the Mass
# (e.g., "Professional") and the value is the name of the hymn. Each dictionary
# should also contain URLs for responsorial psalms and gospel acclamation, the
# name of the Mass setting to be used, and a list of Mass parts to include.
#
# To execute in terminal:
# python upcoming.py 2026 'advent01' 'advent04'
#
#     or
#
# python upcoming.py 2026 '2025-11-30' '2025-12-21'
#
# or a combination of date/feast.
#
# Feast names are taken from the name of the dictionaries containing the
# music schedules and must be a name found in the `name` column of the
# liturgical calendar dataframe.
#
# -----------------------------------------------------------------------------
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
    parser.add_argument('start', type=str,
                        help='First date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('end', type=str,
                        help='Last date (str: "YYYY-MM-DD") or feast (e.g., "advent01") to process')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='upcoming.qmd',
                        help='Name and directory of csv file to write. Default to "[pwd]/upcoming.qmd"')
    parser.add_argument('-c', '--callout', nargs='?', type=str,
                         help='Optional text to include in a callout at the top of the page')
    return parser.parse_args()

args = parse_args()

# =============================================================================
# Local development

# class Args:
#     def __init__(self, year, start, end, callout=None):
#         self.year = year
#         self.start = start
#         self.end = end
#         self.callout = callout

# args = Args(
#     year = 2026,
#     start = 'ot05',
#     end = 'lent05',
# )

# =============================================================================
# Main program

def main():
    # GitHub token
    u.load_env_file()
    token = os.environ.get('GITHUB_TOKEN')

    # Load hymn lists
    cycle = u.lityear(args.year)
    process_dir = f'{args.year}-{cycle}'
    sys.path.append(os.path.join(process_dir))

    lit_calendar = f'{args.year}-year{cycle.upper()}-liturgical-calendar.csv'
    cal = pd.read_csv(os.path.join(process_dir, lit_calendar),
                    parse_dates=['date'], index_col='date')

    # Start date and feast
    start = args.start
    end = args.end
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

    # Subset calendar
    df = cal[start_date:end_date]

    # Create a qmd file
    first_feast = df.loc[df['feast']==start, "name"].iloc[0]
    last_feast = df.loc[df['feast']==end, "name"].iloc[0]
    # first_date = dt.datetime.strftime(start_date, "%B %d, %Y")
    # last_date = dt.datetime.strftime(end_date, "%B %d, %Y")
    first_date = u.fmtdate(start_date)
    last_date = u.fmtdate(end_date)

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
        file.write("""All hymns are taken from the blue *Gather* hymnal unless otherwise noted. “R&A” indicates *Respond and Acclaim*. **Please note that the Mass setting is indicated for every week at the top of each list. Click its name to jump to links for Mass parts.** Click on any title to listen to a recording for rehearsal purposes, but note that the lyrics may not match our hymnal. Please practice the lyrics in the *Gather* hymnal, regardless of the video.\n\n""")

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

        # Empty dictionaries to fill:
        #   - mass_list -> compile all Mass settings used within the date range
        #   - linkcheck -> compile all song URLs to check video availability
        #   - ra_linkcheck -> compile all R&A URLs (not yet used)
        mass_list = {}
        linkcheck = {}
        ra_linkcheck = {}

        # Loop through the seasons that are encompassed in the `start`-`end` range
        for season in list(df['season'].unique()):
            # Subset the dataframe
            ss = df[df['season']==season]

            # Load the schedules and fix the keys
            hymn_lists = u.load_hymn_schedules(season)
            hymn_lists = {k.replace('_', '-'): v for k,v in hymn_lists.items()}

            # Get the Mass settings and parts
            masses = [hymn_lists[k]['Mass'] for k in hymn_lists.keys()]
            parts = [hymn_lists[k]['parts'] for k in hymn_lists.keys()]

            # Add Gloria omission if needed
            for part in parts:
                if all('gloria' not in p.lower() and (season == 'advent' or season == 'lent') for p in part):
                    part.insert(0, f'*Gloria omitted during {titlecase(season)}*')

            # Create a list of all unique Mass settings to include at the
            # bottom of the page (duplicate key:value pairs are ignored when
            # updating dictionaries)
            mass_list.update({k:v for k,v in zip(masses, parts)})

            # Loop through each week to check URLs and create the table
            for r in ss.itertuples():
                if r.feast in hymn_lists.keys():
                    # Create the header
                    file.write(f'#### {u.fmtdate(r.Index)} [{r.name}]{{style="float:right"}}\n\n')

                    # Compile the hymns and URLs
                    hymns = hymn_lists[r.feast]
                    for k,v in hymns.items():
                        # Ignore RA and Mass setting info
                        if (k.lower() == 'mass') or (k.lower() == 'ra'):
                            pass
                        # Handle Mass parts separately
                        elif k.lower() == 'parts':
                            urls = [u.get_url(i, swap=True) for i in v]
                            linkcheck.update({u.keyify(name):link for name, link in zip(v, urls)})
                        # Separate dict for R&A, since we don't need a repo issue for these
                        elif 'http' in v:
                            ra_linkcheck.update({' '.join([r.feast, k]): v})
                        # Otherwise, just keyify the hymn name and get the URL
                        else:
                            name = u.keyify(v.split(' - ')[-1].strip())
                            link = u.get_url(name)
                            linkcheck.update({name: link})

                    # Create the table
                    file.write(u.simple_table(hymns, file=file))
            file.write('\n')
        
        # Mass settings
        file.write(
            '::: {.titlered}\n' \
            '### &nbsp;&#x2720; Mass Parts\n' \
            ':::\n\n'
        )
        for mass, parts in mass_list.items():
            file.write(f'#### {mass}\n\n')

            for part in parts:
                try:
                    p, m = part.split(':')
                    index_entry = u.mass_index_lookup(part, swap=True)
                    if index_entry['number'] == 'NA':
                        number = '(Handout)'
                    else:
                        number = index_entry['number']
                    if m == mass:
                        file.write(f"- {number} - [{titlecase(p)}]({index_entry['url']})\n")
                    else:
                        file.write(f"- {number} - [{titlecase(m)}: {titlecase(p)}]({index_entry['url']})\n")
                except ValueError:
                    file.write(f"- {part}\n")
                
            file.write('\n')

    print(f'"{args.outfile}" file created.')

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
        if status.lower() != 'invalid url format' and 'ommited' not in k:
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
