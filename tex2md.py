#!/usr/local/bin/python3 

from datetime import datetime
import argparse
import glob
import os
import re

# Command line arguments
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(prog='tex2md.py',
                usage='%(prog)s [arguments]',
                description='Convert weekly LaTeX music list to markdown blog.')
    parser.add_argument('-f', '--file', metavar='file', type=str,
                        default=argparse.SUPPRESS,
                        help='Latex file to convert')
    parser.add_argument('-d', '--date', metavar='date', type=str,
                        default=argparse.SUPPRESS,
                        help='Optional date YYYY-MM-DD to publish post')
    return parser.parse_args()

def get_hymns(doc):
    """Extract hymn names, numbers, and video IDs from LaTex document 'doc'"""
    hymns = dict()
    for line in doc:
        if 'date' in line:
            # Get the date
            hymns['date'] = re.sub('{|}|\\\date|\\\MAROON|\\\\textbf', '',
            line.strip())
        elif '=' in line:
            # Get keys:values
            splits = re.split('=|}{|--', line)
            if len(splits) == 2:
                # Header info
                hymns[splits[0].strip()] = re.sub('{|}|,', '',
                                                  splits[1].strip())
            elif len(splits) == 5:
                # Hymns
                splits = [s.strip() for s in splits]
                hymn = splits[0]
                hymns[hymn] = {
                    'number': splits[1].replace('{',''),
                    'video': splits[3],
                    'name': splits[4].split('}}')[0]
                    }
    # Fix Ordinary Time, since this will show up in the title of the post
    if 'season' == 'ot':
        hymns['season'] = 'Ordinary Time'
    return hymns

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Use the date passed in command line for file name and post release,
    # if provided. Otherwise, use today's date.
    if "date" in args:
        post_date = args.date
    else:
        post_date = datetime.today().strftime('%Y-%m-%d')
    
    # Read in LaTeX file
    with open(args.file, 'r') as file:
        tex = file.readlines()
    
    # Ordinal dictionary for title
    ordDict = dict({
        '1': 'first', '2': 'second', '3': 'third', '4': 'fourth', '5': 'fifth',
        '6': 'sixth', '7': 'seventh', '8': 'eighth', '9': 'ninth',
        '10': 'tenth', '11': 'eleventh', '12': 'twelfth', '13': 'thirteenth',
        '14': 'fourteenth', '15': 'fifteenth', '16': 'sixteenth',
        '17': 'seventeenth', '18': 'eighteenth', '19': 'nineteenth',
        '20': 'twentieth', '21': 'twenty-first', '22': 'twenty-second',
        '23': 'twenty-third', '24': 'twenty-fourth', '25': 'twenty-fifth',
        '26': 'twenty-sixth', '27': 'twenty-seventh', '28': 'twenty-eighth',
        '29': 'twenty-ninth', '30': 'thirtieth', '31': 'thirty-first',
        '32': 'thirty-second', '33': 'thirty-third', '34': 'thirty-fourth'
    })

    # Extract hymn list from LaTeX document
    hymns = get_hymns(doc=tex)
    
    # Read in markdown template
    mdDir = '.'
    with open(os.path.join(mdDir, 'post-template.md')) as mdtempfile:
        mdtemp = mdtempfile.read()

    # Name of celebration
    if 'litweek' in hymns.keys():
        title = f'{ordDict[hymns["litweek"]].title()} '\
                f'Sunday in {hymns["season"]}'
    else:
        title = hymns['solemnity']

    # Fill in template
    md = mdtemp.replace(
             'POSTDATE', post_date
         ).replace(
             'DATE', datetime.strptime(hymns['date'], '%A, %B %d, %Y')\
                             .strftime('%B %d, %Y')
         ).replace(
             'OCCASION', title
         ).replace(
             'SEASON', hymns['season']
         ).replace(
             'PROCESSIONALHYMN (N)',
             f'{hymns["processional"]["name"]} ({hymns["processional"]["number"]})'
         ).replace(
             'PROCESSIONALVIDEOID',
             hymns["processional"]["video"]
         ).replace(
             'OFFERTORYHYMN (N)',
             f'{hymns["offertory"]["name"]} ({hymns["offertory"]["number"]})'
         ).replace(
             'OFFERTORYVIDEOID',
             hymns["offertory"]["video"]
         ).replace(
             'COMMUNIONHYMN (N)',
             f'{hymns["communion"]["name"]} ({hymns["communion"]["number"]})'
         ).replace(
             'COMMUNIONVIDEOID',
             hymns["communion"]["video"]
         ).replace(
             'RECESSIONALHYMN (N)',
             f'{hymns["recessional"]["name"]} ({hymns["recessional"]["number"]})'
         ).replace(
             'RECESSIONALVIDEOID',
             hymns["recessional"]["video"]
         ).replace(
             'MASSSETTING',
             hymns["holy"]["name"]
         ).replace(
             'HOLYVIDEOID',
             hymns["holy"]["video"]
         ).replace(
             'MEMACCVIDEOID',
             hymns["memacc"]["video"]
         ).replace(
             'AMENVIDEOID',
             hymns["amen"]["video"]
         ).replace(
             'LAMBOFGODVIDEOID',
             hymns["lambofgod"]["video"]
         )

    # Conditional for Gloria
    if hymns['season'].lower() == 'advent' or hymns['season'].lower() == 'lent':
        md = md.replace(
            'GLORIAVIDEOID',
            f'*Gloria is omitted during {hymns["season"].title()}.*'
        )
    else:
        md = md.replace(
            'GLORIAVIDEOID',
            '{{% include youtube.html id="{}" %}} <br>'.format(hymns['gloria']['video'])
        )

    # Conditional for Responsorial Psalm
    if isinstance(hymns['psalm'], dict):
        md = md.replace(
            'PSALMVIDEOID',
            '{{% include youtube.html id="{}" %}} <br>'.format(hymns['psalm']['video'])
        )
    else:
        md = md.replace(
            'PSALMVIDEOID',
            "Handout from **Respond and Acclaim** "\
            "([OCP](https://www.ocp.org/en-us)). Video recordings for "\
            "rehearsal purposes can usually be found on several private "\
            "YouTube channels such as [Music Ministry 101]"\
            "(https://www.youtube.com/@MusicMinistry101/videos) or "\
            "[Chris Brunelle](https://www.youtube.com/@ChrisBrunelle/videos)."
        )
    
    # Conditional for Gospel Acclamation
    if isinstance(hymns['gospelacc'], dict):
        md = md.replace(
            'GOSPELACCVIDEOID',
            '{{% include youtube.html id="{}" %}} <br>'\
            .format(hymns['gospelacc']['video'])
        )
    else:
        md = md.replace(
            'GOSPELACCVIDEOID',
            "Handout from **Respond and Acclaim** "\
            "([OCP](https://www.ocp.org/en-us)). Video recordings for "\
            "rehearsal purposes can usually be found on several private "\
            "YouTube channels such as [Music Ministry 101]"\
            "(https://www.youtube.com/@MusicMinistry101/videos) or "\
            "[Chris Brunelle](https://www.youtube.com/@ChrisBrunelle/videos)."
        )
    
    # Conditional for Meditation Hymn
    if 'meditation' in hymns.keys():
        md = md.replace(
            'MEDITATIONVIDEOID',
            f'\n---\n\n### Meditation Hymn: {hymns["meditation"]["name"]} '\
            f'({hymns["meditation"]["number"]})\n\n'\
            '{{% include youtube.html id="{}" %}} <br>\n'\
            .format(hymns['meditation']['video'])
        )
    else:
        md = md.replace(
            'MEDITATIONVIDEOID', ''
        )

    # Conditional for Sequence
    if 'sequence' in hymns.keys():
        md = md.replace(
            'SEQUENCEVIDEOID',
            f'\n---\n\n### Sequence: {hymns["sequence"]["name"]} '\
            f'({hymns["sequence"]["number"]})\n\n'\
            '{{% include youtube.html id="{}" %}} <br>\n'\
            .format(hymns['sequence']['video'])
        )
    else:
        md = md.replace(
            'SEQUENCEVIDEOID', ''
        )

    # Switch repo branch
    os.system('git checkout gh-pages')

    # Write out post
    # Update existing post for the given weekend if it already exists
    if 'litweek' in hymns.keys():
        mdfname = glob.glob(f"_posts/*{hymns['season']}"\
                            f"{hymns['litweek'].zfill(2)}.md")
    else:
        mdfname = glob.glob(f"_posts/*{hymns['solemnity'].replace(' ', '')}.md")
    # If no post exist yet, create a new one
    if len(mdfname) == 0:
        if 'litweek' in hymns.keys():
            mdfname = f'{post_date}-{hymns["season"]}{hymns["litweek"].zfill(2)}.md'
        else:
            mdfname = f'{post_date}-{hymns["solemnity"].replace(" ", "")}.md'
        print(f'No existing post found. Creating {mdfname}.')
    else:
        mdfname = os.path.basename(mdfname[0])
        if "date" in args:
            # If a date was passed to command line but the file already exists,
            # replace the existing date with the date passed. Use this to change
            # post release date.
            mdfnameNew = args.date + mdfname[10:]
            print(f'Renaming post to {mdfname} with new publish date.')
            os.system(f'mv _posts/{mdfname} _posts/{mdfnameNew}')
            mdfname = mdfnameNew
        else:
            # Otherwise, just update the post
            print(f'Updating {mdfname}.')
    # Write post to file
    postfile = os.path.join("_posts", mdfname)
    with open(postfile, 'w') as mdout:
        mdout.write(md)
        
    # Commit and push new file to gh-pages branch
    os.system(f'git add {postfile}')
    os.system('git commit -m "Automatically generated by tex2md"')
    os.system('git push origin gh-pages')
    os.system('git checkout main')
    
if __name__ == '__main__':
    main()