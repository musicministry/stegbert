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
    parser.add_argument('-u', '--upcoming', action='store_true',
                        help='Updates "upcoming.pdf" file')
    return parser.parse_args()

def get_hymns(latexdoc):
    """Extract hymn names, numbers, and video IDs from LaTex document 'doc'"""
    hymns = dict()
    for line in latexdoc:
        if 'solemnity' in line:
            hymns['litweek'] = re.sub('{|}', '', line.strip())
        if 'date' in line:
            hymns['date'] = re.sub('{|}|\\\date|\\\MAROON|\\\\textbf', '',
            line.strip())
        elif '=' in line:
            splits = re.split('=|}{|--', line)
            if len(splits) == 2:
                hymns[splits[0].strip()] = re.sub('{|}|,', '', splits[1].strip())
            elif len(splits) == 5:
                splits = [s.strip() for s in splits]
                hymn = splits[0]
                hymns[hymn] = {
                    'number': splits[1].replace('{',''),
                    'video': splits[3],
                    'name': splits[4].split('}}')[0]
                    }
    # Fix Ordinary Time
    if 'season' in hymns.keys():
        if 'season' == 'ot':
            hymns['season'] = 'Ordinary Time'
    return hymns

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Read in LaTeX file
    # texDir = 'Documents/Liturgy/Music Ministry/_Schedules_StEgbert/YearB/Weekly'
    # with open(os.path.join(texDir, 'B-Advent03-2023.tex'), 'r') as file:
    #     tex = file.readlines()
    with open(args.file, 'r') as file:
        tex = file.readlines()
    
    # Update upcoming.pdf (optional)
    if args.upcoming:
        print('Creating and committing "upcoming.pdf"')
        texDir = os.path.dirname(args.file)
        pdfFile = args.file.replace('tex', 'pdf')
        newPdfFile = os.path.join(texDir, 'upcoming.pdf')
        os.system(f'cp {pdfFile} {newPdfFile}')
        os.system(f'git add {newPdfFile}')
        os.system('git commit -m "Automatically generated by tex2md"')
        os.system('git push origin main')

    # Ordinal dictionary
    ordDict = dict({
        '1': 'first', '2': 'second', '3': 'third', '4': 'fourth', '5': 'fifth',
        '6': 'sixth', '7': 'seventh', '8': 'eighth', '9': 'ninth', '10': 'tenth',
        '11': 'eleventh', '12': 'twelfth', '13': 'thirteenth', '14': 'fourteenth',
        '15': 'fifteenth', '16': 'sixteenth', '17': 'seventeenth',
        '18': 'eighteenth', '19': 'nineteenth', '20': 'twentieth',
        '21': 'twenty-first', '22': 'twenty-second', '23': 'twenty-third',
        '24': 'twenty-fourth', '25': 'twenty-fifth', '26': 'twenty-sixth',
        '27': 'twenty-seventh', '28': 'twenty-eighth', '29': 'twenty-ninth',
        '30': 'thirtieth', '31': 'thirty-first', '32': 'thirty-second',
        '33': 'thirty-third', '34': 'thirty-fourth'
    })

    # Extract hymn list
    hymns = get_hymns(latexdoc=tex)
    # Read in markdown template
    mdDir = '.'
    with open(os.path.join(mdDir, 'post-template.md')) as mdtempfile:
        mdtemp = mdtempfile.read()

    # Name of celebration
    if 'season' in hymns.keys():
        title = f'{ordDict[hymns["litweek"]].title()} '\
                f'Sunday in {hymns["season"]}'
    else:
        title = hymns['litweek']

    # Fill in template
    md = mdtemp.replace(
             'DATE', hymns['date']
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
            '{% include youtube.html id="" %} <br>'.format(hymns['gloria']['video'])
        )

    # Switch repo branch
    os.system('git checkout gh-pages')

    # Write out post
    # Update existing post for the given weekend if it already exists
    if 'season' in hymns.keys():
        mdfname = glob.glob(f"_posts/*{hymns['season']}"\
                            f"{hymns['litweek'].zfill(2)}.md")
    else:
        mdfname = glob.glob(f"_posts/*{hymns['litweek'].md}")
    if len(mdfname) == 0:
        if "date" in args:
            post_date = args.date
        else:
            post_date = datetime.today().strftime('%Y-%m-%d')
        if 'season' in hymns.keys():
            mdfname = f'{post_date}-{hymns["season"]}{hymns["litweek"].zfill(2)}.md'
        else:
            mdfname = f'{post_date}-{hymns["litweek"].md}'
        print(f'No existing post found. Creating {mdfname}.')
    else:
        mdfname = os.path.basename(mdfname[0])
        if "date" in args:
            mdfnameNew = args.date + mdfname[10:]
            print(f'Renaming post to {mdfname} with new publish date.')
            os.system(f'cp /_posts/{mdfname} /_posts{mdfnameNew}')
            mdfname = mdfnameNew
        else:
            print(f'Updating {mdfname}.')
    postfile = os.path.join("_posts", mdfname)
    with open(postfile, 'w') as mdout:
        mdout.write(md)
        
    # Commit and push new file
    os.system(f'git add {postfile}')
    os.system('git commit -m "Automatically generated by tex2md"')
    os.system('git push origin gh-pages')
    os.system('git checkout main')
    
if __name__ == '__main__':
    main()