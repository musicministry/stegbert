# =========================================================================== #
# Load required packages
from IPython.display import Markdown, display
from titlecase import titlecase
from tabulate import tabulate
from numbr import Cast as num
import numpy as np
import importlib
import requests
import yaml
import sys
import re

# =========================================================================== #
# Load video YAMLs from GitHub

# Hymns
hymn_yaml_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/main/hymns.yml'
hymn_videos = yaml.safe_load(requests.get(hymn_yaml_url).content)

# Mass Settings
mass_yaml_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/main/mass-settings.yml'
mass_videos = yaml.safe_load(requests.get(mass_yaml_url).content)

# Merge together
hymn_videos = hymn_videos | mass_videos

# =========================================================================== #
# Tools

def week(i):
    """Return integer `i` as ordinal word"""
    return num(i, target="Ordinal Word").capitalize()

def fmtdate(d):
    """Print date d"""
    return d.strftime("%B %-d, %Y")

def ra(page):
    """Print R&A with page"""
    return f'R&A p. {page}'

def keyify(string: str):
    """Convert human-readable titlecase to lowercase hyphen-separated string."""
    string = re.sub(r'[^a-zA-Z0-9]', ' ', string)
    return string.lower().replace('  ', ' ').replace(' ', '-')

def unkey(string: str):
    """Convert lowercase hyphen-separated string to human-readably titlecase."""
    return titlecase(string.replace('-', ' ').replace('_', ' '))

def md(hymn: str):
    """Display markdown hyperlink of `hymn` with URL"""
    return markdown_url(hymn)

def get_url(hymn, urls=hymn_videos):
    """Get video URL for 'hymn' from `urls` if available. Otherwise, returns None."""
    # Get notes, if any
    if "|" in hymn:
        hymn = hymn.split("|")[0].strip()
    # Remove punctuation and special characters
    hymn_key = re.sub('[^A-Za-z0-9 ]+', '', hymn.strip())
    # Replace spaces and make lowercase
    hymn_key = hymn_key.replace('  ', ' ').replace(' ', '-').lower()
    # print(hymn_key)
    # Get hyperlink
    if hymn_key in urls.keys():
        return urls[hymn_key]
    else:
        return None

def get_hymn_lists(file_name):
    """Get all hymn list dictionary objects from Python (*.py) `file_name`."""
    if file_name in sys.modules:
        del sys.modules[file_name]
    hymns = importlib.import_module(file_name)
    
    dicts = {}
    for name in dir(hymns):
        # Skip private/magic attributes
        if not name.startswith('_'):
            obj = getattr(hymns, name)
            # Check if it's a dictionary
            if isinstance(obj, dict):
                dicts[name] = obj
    
    return dicts

def markdown_url(hymn, urls=hymn_videos):
    """Create a markdown hyperlink for `hymn` with URL, if available."""
    # Check for note and separate out, if needed
    if "|" in hymn:
        hymn, note = hymn.split('|')
        hymn = hymn.strip()
        note = note.strip()
    else:
        note = None
    # Fetch the URL
    url = get_url(hymn, urls=urls)
    if url is not None:
        if note is not None:
            return f'[{hymn}]({url}) {note}'
        else:
            return f'[{hymn}]({url})'
    else:
        if note is not None:
            return f'{hymn} {note}'
        else:
            return hymn

def video_url(hymn, urls=hymn_videos):
    """Create a Quarto video inclusion link for `hymn` with URL, if available."""
    # Fetch the URL
    url = get_url(hymn, urls=urls)
    if url is not None:
        return f'{{{{< video {url} >}}}}'
    else:
        return "No video available."

def lityear(year):
    """Return the liturgical cycle for year `year`"""
    # Pick a starting year for cycle
    A, B, C = 2020, 2021, 2022
    # Array to index
    years = np.array(['A', 'B', 'C'])
    # Subtract the starting years from `year` and divide by 3
    ind = (year-np.array([A, B, C]))%3==0
    # Return the cycle year that is evenly divisible by 3
    return years[ind][0][0]

# =========================================================================== #
# Markdown tables

# def simple_table(hymns: dict, RA, mass):
#     """Create simple Markdown table from dictionary of hymns."""
    
#     display(Markdown(f'[**Mass Setting:** {mass}]{{style="float:right"}}'))
    
#     tbl = Markdown(
#         tabulate(
#             # Conditional for responsorial psalm
#             [["&emsp;", f"**{titlecase(k)}:**", f"[R&A p. {RA[0]}]({v})"] if "psalm" in k.lower() and "http" in v else
            
#             # Conditional for gospel acclamation
#             ["&emsp;", f"**{titlecase(k)}:**", f"[R&A p. {RA[1]}]({v})"] if "gospel" in k.lower() and "http" in v else
            
#             # Everything else
#             ["&emsp;", f"**{titlecase(k)}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] for k,v in hymns.items()],
#             tablefmt='simple'
            
#             # Add Mass setting and formatting
#             ) + '\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}' + '\n\n\\needspace{3\\baselineskip}'
#         )

#     return tbl

# def simple_table(hymn_dict: dict):
#     """Create simple Markdown table from dictionary of hymns."""
#     # Copy the dictionary to prevent modifying original and convert all keys to
#     # titlecase for querying
#     hymns = hymn_dict.copy()
#     hymns = {titlecase(k):v for k,v in hymns.items()}

#     # Mass setting
#     if 'Mass' in hymns.keys():
#         display(Markdown(f'[**Mass Setting:** [{hymns["Mass"]}](#{keyify(hymns["Mass"])})]{{style="float:right"}}'))
#         hymns.pop('Mass', None)
#     if 'Parts' in hymns.keys():
#         hymns.pop('Parts')
    
#     # Respond and Acclaim
#     RA = hymns['Ra'].copy()
#     hymns.pop('Ra', None)
    
#     tbl = Markdown(
#         tabulate(
#             # Conditional for responsorial psalm
#             [["&emsp;", f"**{k}:**", f"[R&A p. {RA[0]}]({v})"] if "psalm" in k.lower() and "http" in v else
            
#             # Conditional for gospel acclamation
#             ["&emsp;", f"**{k}:**", f"[R&A p. {RA[1]}]({v})"] if "gospel" in k.lower() and "http" in v else
            
#             # Everything else
#             ["&emsp;", f"**{k}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] for k,v in hymns.items()],
#             tablefmt='simple'
            
#             # Add Mass setting and formatting
#             ) + '\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}' + '\n\n\\needspace{3\\baselineskip}'
#         )

#     return tbl

def simple_table(hymn_dict: dict, file):
    """Create simple Markdown table from dictionary of hymns."""
    # Copy the dictionary to prevent modifying original and convert all keys to
    # titlecase for querying
    hymns = hymn_dict.copy()
    hymns = {titlecase(k):v for k,v in hymns.items()}

    # Mass setting
    if 'Mass' in hymns.keys():
        file.write(f'[**Mass Setting:** [{hymns["Mass"]}](#{keyify(hymns["Mass"])})]{{style="float:right"}}\n\n')
        hymns.pop('Mass', None)
    if 'Parts' in hymns.keys():
        hymns.pop('Parts')
    
    # Respond and Acclaim
    RA = hymns['Ra'].copy()
    hymns.pop('Ra', None)
    
    tbl = tabulate(
            # Conditional for responsorial psalm
            [["&emsp;", f"**{k}:**", f"[R&A p. {RA[0]}]({v})"] if "psalm" in k.lower() and "http" in v else
            
            # Conditional for gospel acclamation
            ["&emsp;", f"**{k}:**", f"[R&A p. {RA[1]}]({v})"] if "gospel" in k.lower() and "http" in v else
            
            # Everything else
            ["&emsp;", f"**{k}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] for k,v in hymns.items()],
            tablefmt='grid'
            
            # Add Mass setting and formatting
            ) + '\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}' + '\n\n\\needspace{3\\baselineskip}\n\n'

    return tbl


def massparts_table(setting:str, include:list, urls=hymn_videos):
    """Create simple Markdown table from dictionary of Mass parts."""

    include_keys = [f'{keyify(setting)}-{keyify(i)}' for i in include]

    display(Markdown(f"\n#### {titlecase(setting)}\n"))

    # Conditional for omitting Gloria in Advent and Lent (i.e., if not included
    # in parts list)
    if f'{keyify(setting)}-gloria' not in include_keys:
        gloria_entry = ["&emsp;", "**Gloria:**", "*Gloria is omitted.*"]
    else:
        gloria_entry = [" ", " ", " "]

    tbl = Markdown(
        tabulate(
            [gloria_entry] + [
            # Embed video, if available
            ["&emsp;", f"**{i}:**", markdown_url(f"{setting} {i}")] for i, k in zip(include, include_keys)],

            # Add table formatting
            tablefmt='simple', colalign=('center', 'right', 'left')
            )+'\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}'
        )
    return tbl

def video_table(hymns: dict, RA):
    """Create simple Markdown table from dictionary of hymns."""

    RAnote = " <br> Other video recordings from *Respond & Acclaim* for rehearsal purposes can usually be found on several private YouTube channels such as [Chris Brunelle](https://www.youtube.com/@ChrisBrunelle/videos), [Liturgical Music](https://www.youtube.com/@LiturgicalMusic), or [Music Ministry 101](https://www.youtube.com/@MusicMinistry101/videos)."

    tbl = Markdown(
        tabulate(            
            # Conditional for responsorial psalm
            [["&emsp;", f"**{titlecase(k)}:**", f"*Respond & Acclaim* p. {RA[0]} <br><br> {{{{< video {v} >}}}}"+RAnote] if "psalm" in k.lower() else
            
            # Conditional for gospel acclamation
            ["&emsp;", f"**{titlecase(k)}:**", f"*Respond & Acclaim* p. {RA[1]} <br><br> {{{{< video {v} >}}}}"] if "gospel" in k.lower() else
            
            # Everything else
            ["&emsp;", f"**{titlecase(k)}:**", v.replace('| ', '')+f" <br><br> {video_url(v.split(' - ')[1].strip())}"] for k,v in hymns.items()],
            tablefmt='simple', colalign=('center', 'right', 'left')
            
            # Add Mass setting and formatting
            )+'\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}'
        )
    return tbl

def massparts_video_table(season:str, setting:str, include:list, urls=hymn_videos):
    """Create simple Markdown table from dictionary of Mass parts."""

    include_keys = [f'{keyify(setting)}-{keyify(i)}' for i in include]

    display(Markdown(f"The Mass parts for {season} will be taken from *{setting}*: <rb><br>"))

    tbl = Markdown(
        tabulate(
            # Conditional for omitting Gloria in Advent and Lent
            [["&emsp;", f"**{i}:**", f"*{i} is omitted during {season}.* <br><br>"] if (i.lower()=='gloria' and (season.lower()=='advent' or season.lower()=="lent")) else
            
            # Embed video, if available
            ["&emsp;", f"**{i}:**", f"{{{{< video {urls[k]} >}}}}"] for i, k in zip(include, include_keys)],

            # Add table formatting
            tablefmt='simple', colalign=('center', 'right', 'left')
            )+'\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}'
        )
    return tbl
