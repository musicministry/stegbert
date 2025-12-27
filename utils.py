# =========================================================================== #
# Load required packages
from IPython.display import Markdown, display
from titlecase import titlecase
from tabulate import tabulate
from numbr import Cast as num
from pathlib import Path
import datetime as dt
import numpy as np
import subprocess
import importlib
import requests
import yaml
import sys
import re
import os

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

def next_sunday(from_date):
    """Return the next Sunday after `from_date`, not counting `from_date` if
    `from_date` itself is a Sunday.
    
    Arguments
    ---------
    `from_date` : str or datetime object
        Date from which to find the next Sunday. If str, must be of the format 
        `YYYY-mm-dd`.
    
    Returns
    -------
        datetime object of the next Sunday
    """
    # Convert to datetime if `from_date` is a string
    if isinstance(from_date, str):
        start_date = dt.datetime.strptime(from_date, "%Y-%m-%d").date()
    else:
        start_date = from_date
    
    # Find the first Sunday after the start date
    days_ahead = 6 - start_date.weekday()  # 6 is Sunday
    if days_ahead == 0:  # If today is Sunday, get the next one
        days_ahead += 7
    next_sunday = start_date + dt.timedelta(days=days_ahead)
    return next_sunday.date()

def git_commit(file, message, push=True):
    """Commit file `file` to GitHub with message `message`, push if `push` is
    True.
    """
    subprocess.run(['git', 'add', file])
    subprocess.run(['git', 'commit', '-m', message])
    if push:
        subprocess.run(['git', 'push', 'origin', 'quarto'])

# The following were created with the assistance of claude.ai

def get_file_path(filename):
    """Get full path to qmd file `filename` in source repo."""
    # Set dir
    try:
        planning_book = Path(__file__).parent.parent / 'planning-book'
    except NameError:
        planning_book = Path.cwd().parent / 'planning-book'

    # Filename includes subdirectory (e.g., 'ordinary-time/ot02.qmd')
    qmd_file = planning_book / 'content' / filename
    
    # Return the file, if it exists.
    if qmd_file.exists():
        return qmd_file
    
    raise FileNotFoundError(f"Could not find {filename} in {planning_book}")

def get_hymn_list(file_path, lit_year):
    """Extract frontmatter dictionary for liturgical year `lit_year` from the appropriate qmd file `file_path`."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the str block called "frontmatter" in the qmd file
    pattern = r'frontmatter\s*=\s*"""(.*?)"""'
    match = re.search(pattern, content, re.DOTALL)
    
    # Return the hymns for the desired liturgical year
    if match:
        results = yaml.safe_load(match.group(1))
        key = list(results.keys())[0]
        try:
            return results[key][lit_year.lower()]
        except KeyError:
            return results[key]['abc']
    return None

def process_week_range(start, end, df, lit_year):
    """
    Process frontmatter for files between start and end filenames (inclusive).
    
    Args:
        start: Starting feast (e.g., 'ot02')
        end: Ending feast (e.g., 'ot04.qmd')
        df: DataFrame with columns: weekday, feast, season, name, priority, year, 
            month, day, dayofweek, filename, date
        lit_year: liturgical year to extract, 'a', 'b', or 'c'
    
    Returns:
        dict: Mapping of filename to dict containing frontmatter + metadata
    """
    # Get slice of dataframe between the two files
    start_idx = df[df['feast'] == start].index[0]
    end_idx = df[df['feast'] == end].index[0]
    week_range = df.loc[start_idx:end_idx]
    
    # Extract frontmatter for each file
    results = {}
    for _, row in week_range.iterrows():
        # Hymn list file name
        filename = row['filename']
        # Mass setting file name (season-dependent)
        if row['season'] == 'ordinary-time':
            if bool(row['date'] < df[df['feast']=='ash-wednesday']['date'].values):
                mass_filename = os.path.join(row['season'], 'ot-winter.qmd')
            else:
                mass_filename = os.path.join(row['season'], 'ot-summer.qmd')
        else:
            mass_filename = os.path.join(row['season'], row['season'])
        # Get the hymn and Mass parts lists
        try:
            file_path = get_file_path(filename)
            mass_file_path = get_file_path(mass_filename)
            params = get_hymn_list(file_path, lit_year)
            masses = get_hymn_list(mass_file_path, lit_year)
            
            if params:
                # Include dataframe metadata with frontmatter
                results[filename] = {
                    'lit_year': lit_year,
                    'date': row['date'],
                    'weekday': row['weekday'],
                    'season': row['season'],
                    'name': row['name'],
                    'feast': row['feast'],
                    'priority': row['priority'],
                    'mass': masses,
                    'frontmatter': params
                }
            else:
                print(f"Warning: No frontmatter found in {filename}")
                
        except FileNotFoundError as e:
            print(f"Error: {e}")
    
    return results

def flatten_frontmatter_to_dict(frontmatter, feast_name, season, lit_year, mass_setting=None):
    """
    Convert nested frontmatter structure to flat dictionary format.
    
    Args:
        frontmatter: Nested dict from QMD file
        feast_name: Name for the dictionary variable (e.g., 'christmas_day')
        mass_setting: Optional mass setting name
    
    Returns:
        dict: Flat dictionary with priority placeholders in specific order
    """
    # Prioritization
    priority_order = {'required': 0, 'preferred': 1, 'optional': 2}
    
    # Use ordered dict to preserve structure
    result = {}
    
    # 1. Add mass setting if provided
    if mass_setting:
        result['Mass'] = mass_setting['holy-holy-holy']['list'][0]['name']
    
    # 2. Add mass parts
    mass_parts = ['Gloria', 'Holy', f'Memorial Acclamation {lit_year.upper()}', 'Amen', 'Lamb of God']
    if season.lower() == 'advent' or season.lower() == 'lent':
        mass_parts.remove('Gloria')
    result['parts'] = [f'{p}: {result["Mass"]}' for p in mass_parts]
    
    # 3. Processional
    if 'processional' in frontmatter:
        result['Processional'] = format_hymn_options(frontmatter['processional'], priority_order)
    
    # 4. RA placeholder
    result['RA'] = ['[psalm_page]', '[gospel_page]']
    
    # 5. Responsorial Psalm
    if 'psalm' in frontmatter:
        result['Responsorial Psalm'] = format_hymn_options(frontmatter['psalm'], priority_order)
    
    # 6. Gospel Acclamation placeholder
    result['Gospel Acclamation'] = '[required] -- URL'
    
    # 7. Preparation of Gifts
    if 'offertory' in frontmatter:
        result['Preparation of Gifts'] = format_hymn_options(frontmatter['offertory'], priority_order)
    
    # 8. Communion
    if 'communion' in frontmatter:
        result['Communion'] = format_hymn_options(frontmatter['communion'], priority_order)
    
    # 9. Meditation
    if 'meditation' in frontmatter:
        result['Meditation'] = format_hymn_options(frontmatter['meditation'], priority_order)
    
    # 10. Recessional
    if 'recessional' in frontmatter:
        result['Recessional'] = format_hymn_options(frontmatter['recessional'], priority_order)
    
    return result

def format_hymn_options(moment_data, priority_order, is_gospel=False):
    """
    Format hymn options with priority labels.
    
    Args:
        moment_data: Dict with 'list' of hymns
        priority_order: Priority ranking dict
        is_gospel: If True, format as URL placeholder
    
    Returns:
        str or list: Formatted hymn(s)
    """
    # Sort hymn options by priority when applicable
    sorted_hymns = sorted(moment_data['list'], 
                         key=lambda h: priority_order.get(h.get('priority', 'optional'), 3))
    
    # If only one hymn, return as string
    if len(sorted_hymns) == 1:
        hymn = sorted_hymns[0]
        name = hymn['name']
        composer = f" ({hymn['composer']})" if 'composer' in hymn else ""
        priority = hymn.get('priority', 'optional')
        
        if is_gospel:
            return f"[{priority}] -- URL"
        else:
            return f"[{priority}] - {name}{composer}"
    
    # If multiple hymns, return as list
    else:
        options = []
        for hymn in sorted_hymns:
            name = hymn['name']
            composer = f" ({hymn['composer']})" if 'composer' in hymn else ""
            priority = hymn.get('priority', 'optional')
            
            if is_gospel:
                options.append(f"[{priority}] -- URL")
            else:
                options.append(f"[{priority}] - {name}{composer}")
        
        return options

def format_dict_as_python(dict_data, var_name):
    """
    Format dictionary as Python code string for writing to .py file.
    
    Argsuments
    ----------
        dict_data: Dictionary to format
        var_name: Variable name for the dictionary
    
    Returns:
        str: Formatted Python code
    """
    # Define the dictionary name in the .py file
    lines = [f"{var_name} = {{"]
    
    # Loop through the dictionary items to build the new code string
    for key, value in dict_data.items():
        if key.lower() == 'processional' or key.lower() == 'gospel acclamation':
            if isinstance(value, list):
                # Format lists with proper indentation
                lines.append(f'    "{key}": [')
                for item in value:
                    lines.append(f'        "{item}",')
                # Remove trailing comma from last item
                if lines[-1].endswith(','):
                    lines[-1] = lines[-1][:-1]+'\n'
                lines.append('    ],')
            else:
                lines.append(f'    "{key}": "{value}",\n')
        else:
            if isinstance(value, list):
                # Format lists with proper indentation
                lines.append(f'    "{key}": [')
                for item in value:
                    lines.append(f'        "{item}",')
                # Remove trailing comma from last item
                if lines[-1].endswith(','):
                    lines[-1] = lines[-1][:-1]
                lines.append('    ],')
            else:
                lines.append(f'    "{key}": "{value}",')

    # Remove trailing comma from last item
    if lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]
    
    lines.append('}')
    
    return '\n'.join(lines)

def process_and_export_to_py(results, output_file='hymn_data.py'):
    """
    Process all weeks and export to Python file with dictionary definitions.
    
    Args:
        results: Dict from process_week_range()
        output_file: Path to output .py file
    """
    with open(output_file, 'w') as f:
        # File header and metadata
        f.write('# =============================================================================\n')
        f.write(f'# {unkey(results[list(results.keys())[0]]["season"])} {results[list(results.keys())[0]]["date"].year}\n')
        f.write(f'# {results[list(results.keys())[0]]["name"]} through {results[list(results.keys())[-1]]["name"]}\n')
        f.write(f'# Liturgical Year {results[list(results.keys())[0]]["lit_year"].upper()}\n')
        f.write('#\n')
        f.write(f'# Updated {dt.datetime.strftime(dt.datetime.today(), format="%B %Y")}\n')
        f.write('#\n')
        f.write('# Auto-generated hymn data dictionaries\n')
        f.write('#\n')
        f.write('# =============================================================================\n')
        f.write('# Entry template:\n')
        f.write('#\n')
        f.write('#     seasonNN = {\n')
        f.write('#         "Mass": "Mass setting",\n')
        f.write('#         "parts": ["Gloria", "Holy", "Memorial Acclamation A", "Amen",\n')
        f.write('#                   "Lamb of God"],\n')
        f.write('#\n')
        f.write('#         "Processional":         "NNN - Song Title",\n')
        f.write('#\n')
        f.write('#         "RA": [N, N],\n')
        f.write('#         "Responsorial Psalm":   "YouTube video URL",\n')
        f.write('#         "Gospel Acclamation":   "YouTube video URL",\n')
        f.write('#\n')
        f.write('#         "Preparation of Gifts": "NNN - Song Title",\n')
        f.write('#         "Communion":            "NNN - Song Title",\n')
        f.write('#         "Recessional":          "NNN - Song Title",\n')
        f.write('#     }\n')
        f.write('#\n')
        f.write('# Repeat this YAML block for each liturgy -- but be sure to give each block a\n# unique name that matches a `feast` name in the liturgical calendar dataframe.\n# "Mass" (str) and "parts" (list of strings) are required. Other keys can be\n# anything or as many as desired. These will be rendered in the order in which\n# they appear here. Replace N and NNN with page or hymnal song numbers.\n')
        f.write('#\n')
        f.write('# =============================================================================\n\n')

        # Build the file
        for filename, data in results.items():
            # Create variable name from feast code
            var_name = data['feast']

            # Flatten the frontmatter
            flat_dict = flatten_frontmatter_to_dict(
                data['frontmatter'],
                var_name,
                season=data['season'],
                lit_year=data['lit_year'],
                mass_setting=data['mass']
            )
            
            # Format and write
            py_code = format_dict_as_python(flat_dict, var_name)
            f.write(py_code)
            f.write('\n\n')

# =========================================================================== #
# Markdown tables

def simple_table_markdown(hymns: dict, RA, mass):
    """Create simple Markdown table from dictionary of hymns."""
    
    display(Markdown(f'[**Mass Setting:** {mass}]{{style="float:right"}}'))
    
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
            ) + '\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}' + '\n\n\\needspace{3\\baselineskip}'
        )

    return tbl

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

def video_table_markdown(hymns: dict, RA):
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

def video_table(hymns: dict, RA):
    """Create HTML table from dictionary of hymns. (Generated by claude.ai on 2025-12-23 due to rendering inconsistencies with Quarto grid tables and complex content.)
    """

    RAnote = " <br> Other video recordings from *Respond & Acclaim* for rehearsal purposes can usually be found on several private YouTube channels such as <a href='https://www.youtube.com/@ChrisBrunelle/videos'>Chris Brunelle</a>, <a href='https://www.youtube.com/@LiturgicalMusic'>Liturgical Music</a>, or <a href='https://www.youtube.com/@MusicMinistry101/videos'>Music Ministry 101</a>. <br><br>"

    # Start table with custom classes and column widths
    html = '<table class="hover normal" style="width: 100%;">\n<tbody>\n'
    
    for k, v in hymns.items():
        html += '<tr>'
        
        # First column (title) - right-aligned and top-aligned
        html += f'<td style="width: 25%; text-align: right; vertical-align: top; padding-right: 0.5em;"><strong>{titlecase(k)}:</strong></td>'
        
        # Second column (content) - conditional logic
        if "psalm" in k.lower() and 'http' in v:
            content = f"<em>Respond & Acclaim</em> p. {RA[0]} <br><br> {{{{< video {v} >}}}}{RAnote}"
        elif "gospel" in k.lower() and 'http' in v:
            content = f"<em>Respond & Acclaim</em> p. {RA[1]} <br><br> {{{{< video {v} >}}}}"
        else:
            content = v.replace('| ', '') + f"<br><br> {video_url(v.split(' - ')[1].strip())}"
        
        html += f'<td style="width: 75%;">{content}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n\n'
    
    return html
    
def massparts_video_table_markdown(season:str, setting:str, include:list, urls=hymn_videos):
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

def massparts_video_table(season:str, setting:str, include:list, urls=hymn_videos):
    """Create HTML table from dictionary of Mass parts. (Generated by claude.ai on 2025-12-23 due to rendering inconsistencies with Quarto grid tables and complex content.)
    """

    include_keys = [keyify(f'{i.split(": ")[1]} {i.split(": ")[0]}') if 'omitted' not in i else i for i in include]

    # Start table with custom classes and column widths
    html = '<table class="hover normal" style="width: 100%;">\n<tbody>\n'
    
    for i, k in zip(include, include_keys):
        html += '<tr>'
        
        # First column (title) - right-aligned and top-aligned
        html += f'<td style="width: 25%; text-align: right; vertical-align: top; padding-right: 0.5em;"><strong>{i.split(": ")[0]}:</strong></td>'
        
        # Second column (content) - conditional logic
        if 'gloria' in i.lower() and (season.lower() == 'advent' or season.lower() == "lent"):
            content = f"<em>{i.split(': ')[1]}</em> <br><br>"
        else:
            content = f"{{{{< video {urls[k]} >}}}}"
        
        html += f'<td style="width: 75%;">{content}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n\n'
    
    return html