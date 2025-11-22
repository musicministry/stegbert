from IPython.display import Markdown, display
from titlecase import titlecase
from tabulate import tabulate
from numbr import Cast as num
from pyhere import here
import yaml
import re

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

# Video links
# with open('../planning-book/_hymns.yml', 'r') as vf:
with open(here('_hymns.yml'), 'r') as vf:
    videos = yaml.safe_load(vf)

# def get_url(hymn, urls=videos):
#     """Get video URL for 'hymn' from `urls`. Returns Markdown syntax, `[hymn](url)`, if URL is available; otherwise, `hymn`."""
#     # Remove punctuation and special characters
#     hymn_key = re.sub('[^A-Za-z0-9 ]+', '', hymn.strip())
#     # Replace spaces and make lowercase
#     hymn_key = hymn_key.replace('  ', ' ').replace(' ', '-').lower()
#     # Add hyperlink if available
#     if hymn_key in urls.keys():
#         return f'[{hymn}]({urls[hymn_key]})'
#     else:
#         return hymn
def get_url(hymn, urls=videos):
    """Get video URL for 'hymn' from `urls` if available. Otherwise, returns None."""
    # Get notes, if any
    if "|" in hymn:
        hymn = hymn.split("|")[0].strip()
    # Remove punctuation and special characters
    hymn_key = re.sub('[^A-Za-z0-9 ]+', '', hymn.strip())
    # Replace spaces and make lowercase
    hymn_key = hymn_key.replace('  ', ' ').replace(' ', '-').lower()
    # Get hyperlink
    if hymn_key in urls.keys():
        return urls[hymn_key]
    else:
        return None

def markdown_url(hymn, urls=videos):
    # Check for note
    if "|" in hymn:
        hymn, note = hymn.split('|')
        hymn = hymn.strip()
        note = note.strip()
    else:
        note = None
    url = get_url(hymn, urls=videos)
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

def video_url(hymn, urls=videos):
    url = get_url(hymn, urls=videos)
    if url is not None:
        return f'{{{{< video {url} >}}}}'
    else:
        return "No video available."

def simple_table(hymns: dict, RA, mass):
    """Create simple Markdown table from dictionary of hymns."""
    tbl = Markdown(
        tabulate(
            # Conditional for responsorial psalm
            [["&emsp;", f"**{titlecase(k)}:**", f"[R&A p. {RA[0]}]({v})"] if "psalm" in k.lower() and "http" in v else
            # Conditional for gospel acclamation
            ["&emsp;", f"**{titlecase(k)}:**", f"[R&A p. {RA[1]}]({v})"] if "gospel" in k.lower() and "http" in v else
            # Everything else
            ["&emsp;", f"**{titlecase(k)}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] for k,v in hymns.items()],
            tablefmt='simple'
            # Add Mass setting and formatting
            )+f'\n: **Mass Setting:** {mass} {{.hover .normal tbl-colwidths="[2, 25, 73]"}}'
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

def massparts_table(parts: dict, season, setting):
    """Create simple Markdown table from dictionary of Mass parts."""

    display(Markdown(f"The Mass parts for {season} will be taken from *{setting}*: <rb><br>"))

    tbl = Markdown(
        tabulate(
            # # Embed video, if available
            # [["&emsp;", f"**{titlecase(k)}:**", f"{{{{< video {v} >}}}}"] if 'http' in v else
            # # Otherwise, display the value.
            # ["&emsp;", f"**{titlecase(k)}:**", f'{v} <br><br>'] for k,v in parts.items()],
            # Embed video, if available
            [["&emsp;", f"**{titlecase(k)}:**", f"*{k} is omitted during {season}.* <br><br>"] if 'omit' in v.lower() else
            ["&emsp;", f"**{titlecase(k)}:**", f"{video_url(v.split('-')[-1].strip())}"] for k,v in parts.items()],
            tablefmt='simple', colalign=('center', 'right', 'left')
            # Add Mass setting and formatting
            )+f'\n: {{.hover .normal tbl-colwidths="[2, 25, 73]"}}'
        )
    return tbl

def md(hymn: str):
    """Display markdown hyperlink of `hymn` with URL"""
    return Markdown(markdown_url(hymn))


