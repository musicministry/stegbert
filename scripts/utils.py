# =========================================================================== #
# Load required packages
from rapidfuzz import process, fuzz
from titlecase import titlecase
from tabulate import tabulate
from numbr import Cast as num
from pathlib import Path
import datetime as dt
import numpy as np
import importlib
import requests
import time
import yaml
import sys
import re
import os

# =========================================================================== #
# Load video YAMLs from GitHub

# Gather index
gather_index_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/gather/gather.yml'
gather_index = yaml.safe_load(requests.get(gather_index_url).content)

# Mass settings index
mass_index_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/gather/mass-settings.yml'
mass_index = yaml.safe_load(requests.get(mass_index_url).content)

# Supplemental index (anthems, handouts, etc.)
supplemental_index_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/supplemental/supplemental.yml'
supplemental_index = yaml.safe_load(requests.get(supplemental_index_url).content)

# Combine
index = gather_index | supplemental_index | mass_index

# Respond and Acclaim index
ra_index_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/ra/ra-index.yml'
ra_index = yaml.safe_load(requests.get(ra_index_url).content)

# Respond and Acclaim YouTube videos and feast mapping
ra_videos_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/ra/ra-video-urls.yml'
ra_videos = yaml.safe_load(requests.get(ra_videos_url).content)

ra_feast_mapping_url = 'https://raw.githubusercontent.com/musicministry/song-urls/refs/heads/ra/feast-mapping.yml'
ra_feast_mapping = yaml.safe_load(requests.get(ra_feast_mapping_url).content)

# =========================================================================== #
# Tools

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

def week(i):
    """Return integer `i` as ordinal word"""
    return num(i, target="Ordinal Word").capitalize()

def unkey(string: str):
    """Convert lowercase hyphen-separated string to human-readably titlecase."""
    return titlecase(string.replace('-', ' ').replace('_', ' '))

def fmtdate(d, day_of_week=False):
    """Print date d"""
    if day_of_week:
        return d.strftime("%A, %B %-d, %Y")
    else:
        return d.strftime("%B %-d, %Y")

def keyify(string: str):
    """Convert human-readable titlecase to lowercase hyphen-separated string."""
    # Remove notes, if any
    if "|" in string:
        string = string.split("|")[0].strip()
    # Remove punctuation and special characters
    string = string.replace("'", "")
    string = re.sub(r'[^a-zA-Z0-9]', ' ', string).strip().lower()
    return '-'.join(string.split())

def get_url(name, swap=False):
    """Return the video URL for hymn or song `name`. If the `name` has a colon and needs to be swapped, for example, `Gloria: Heritage Mass` needs to become `Heritage Mass: Gloria`, use `swap = True`."""
    # Reverse the name, if needed
    if swap:
        name = ' '.join(name.split(': ')[::-1])

    # Extract the URL
    if keyify(name) in index.keys():
        return index[keyify(name)]['url']
    else:
        return None

def get_ra_video_url(celebration, get='psalm'):
    """Return the R&A video URL for `celebration`."""
    # Check the `get` string
    assert get.lower() in ['psalm', 'gospel acclamation'], '`get` parameter must be "psalm" or "gospel acclamation"'
    get = titlecase(get)
    return(ra_videos[ra_feast_mapping[celebration] + f' - {get}']['url'])

def check_for_lists(d, context=""):
    """Ensure all dictionary values are strings, not lists or other types."""
    # Get any entries that are not strings, except for 'parts'
    non_strings = [(k, type(v).__name__) for k, v in d.items() 
                   if not isinstance(v, str) and k.lower() != 'parts']
    
    # If there are any lists, require a selection be made first
    if non_strings:
        keys_and_types = ", ".join(f"{t} in {k}" for k, t in non_strings)
        context_msg = f" in {context}" if context else ""
        raise TypeError(f"Expected single string values{context_msg}, but found {keys_and_types}. Please make a selection and try again.")

def get_local_path(name, swap=False):
    """Return the local file path for hymn or song `name`. If the `name` has a colon and needs to be swapped, for example, `Gloria: Heritage Mass` needs to become `Heritage Mass: Gloria`, use `swap = True`."""
    # Reverse the name, if needed
    if swap:
        name = ' '.join(name.split(': ')[::-1])

    # Extract the URL
    if keyify(name) in index.keys():
        return index[keyify(name)]['local_path']
    else:
        return None

def mass_index_lookup(name, swap=False):
    """Return the number and video URL for Mass setting and part, formatted 'Mass Setting: Part', passed to `name`. If `swap = True`, `name` will be split at the colon and reversed. For example, 'Gloria: Heritage Mass' will become 'Heritage Mass: Gloria'."""
    # Reverse the Mass setting with part, if needed
    if swap:
        name = ' '.join(name.split(': ')[::-1])
    # Extract the URL
    if keyify(name) in index.keys():
        return index[keyify(name)]
    else:
        return None

def markdown_url(hymn):
    """Create a markdown hyperlink for `hymn` with URL, if available."""
    # Check for note and separate out, if needed
    if "|" in hymn:
        hymn, note = hymn.split('|')
        hymn = hymn.strip()
        note = " " + note.strip()
    else:
        note = ""
    # Fetch the URL
    url = get_url(hymn)
    if url is not None:
        return f'[{hymn}]({url}){note}'
    else:
        return hymn

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

def fuzzy_index_lookup(name, verbose=False):
    """Use fuzzy name matching to find the closest hymnal entry for the song `name`. If the match is not perfect a perfect match, an alert will be appended to the name.

    If `verbose` is True, the original name, matched name, and score will be printed.
    """

    # Extract the closest match
    index_name, score, _ = process.extractOne(keyify(name), index.keys())
    number = index[index_name]['number']
    display_name = index[index_name]['original_title']

    # Append alert for non-perfect matches
    if score < 100:
        display_name = display_name + f' ⚠️VERIFY ({round(score, 1)}%)⚠️'
    
    # Print results, if desired
    if verbose:
        print(f"{name} -> {display_name} (confidence: {round(score, 1)}%)")
    
    # Return contents
    return display_name, number

# -----------------------------------------------------------------------------
# Made by claude.ai

def fuzzy_ra_index_lookup(date, celebration_name, threshold=70):
    """
    Get page number using fuzzy matching on celebration name.
    
    Args:
        date: datetime.date or datetime.datetime object
        celebration_name: Name of the celebration (can be partial or slightly
            different)
        threshold: Minimum similarity score (0-100, default 70)
    
    Returns:
        tuple: (page_number, matched_key, score) or (None, None, 0) if no match
    
    Example:
        >>> get_page_fuzzy(date(2026, 1, 4), "Epiphany")
        (28, "January 04, 2026 - The Epiphany of the Lord", 100)
    """
    # Format date to match the index
    date_str = date.strftime("%B %d, %Y")
    
    # Filter to only entries for this date (some dates have multiple entries)
    candidates = {k: v for k, v in ra_index.items() if k.startswith(date_str)}
    if not candidates:
        return None, None, 0
    
    # If only one entry for this date, return it (common case)
    if len(candidates) == 1:
        key, page = list(candidates.items())[0]
        return page, key, 100
    
    # Multiple entries for this date - use fuzzy matching on celebration part
    # Extract just the celebration names (part after " - ")
    candidate_celebrations = {k: k.split(" - ", 1)[1] for k in candidates.keys()}
    
    # Find best match
    result = process.extractOne(
        celebration_name,
        candidate_celebrations.values(),
        scorer=fuzz.ratio,
        score_cutoff=threshold
    )
    
    # If a match is found, find the original key
    if result:
        matched_celebration, score = result[0], result[1]
        for key, celebration in candidate_celebrations.items():
            if celebration == matched_celebration:
                return candidates[key], key, score
    
    # Otherwise, return nothing
    return None, None, 0

def get_file_path(filename, hymnal):
    """Get full path to qmd file `filename` in source repo for hymnal `hymnal`."""
    # Set dir
    try:
        planning_book = Path(__file__).resolve().parent.parent.parent / f'planning-book-{hymnal.lower()}'
    except NameError:
        planning_book = Path.cwd().parent / f'planning-book-{hymnal.lower()}'

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

def process_week_range(start, end, df, lit_year, hymnal):
    """
    Process frontmatter for files between start and end filenames (inclusive).
    
    Args:
        start: Starting feast (e.g., 'ot02')
        end: Ending feast (e.g., 'ot04.qmd')
        df: DataFrame with columns: weekday, feast, season, name, priority, year, 
            month, day, dayofweek, filename, date
        lit_year: liturgical year to extract, 'a', 'b', or 'c'
        hymnal: hymnal from which to pull lists. Currently only 'gather' or
            'bb' (Breaking Bread) are supported.
    
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
            mass_filename = os.path.join(row['season'], f"{row['season']}.qmd")
        
        # Get the hymn and Mass parts lists
        try:
            file_path = get_file_path(filename=filename,
                                      hymnal=hymnal)
            mass_file_path = get_file_path(filename=mass_filename,
                                           hymnal=hymnal)
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

def process_and_export(results, hymnal, output_file='hymn_data.py'):
    """
    Process all weeks into dictionaries and export to a single Python file for review.
    
    Args:
        results: Dict from process_week_range()
        hymnal: Either 'gather' or 'bb' (Breaking Bread) indicating the hymnal
            to pull numbers from
        output_file: Path to output .py file
    """
    with open(output_file, 'w') as f:
        # File header and metadata
        f.write('# =============================================================================\n')
        f.write(f'# {unkey(results[list(results.keys())[0]]["season"])} {results[list(results.keys())[0]]["date"].year}\n')
        f.write(f'# {results[list(results.keys())[0]]["name"]} through {results[list(results.keys())[-1]]["name"]}\n')
        f.write(f'# Liturgical Year {results[list(results.keys())[0]]["lit_year"].upper()}\n')
        f.write('#\n')
        f.write(f'# Updated: {dt.datetime.strftime(dt.datetime.today(), format="%B %Y")}\n')
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
        f.write('#         "Responsorial Psalm":   "R&A p. n - YouTube video URL",\n')
        f.write('#         "Gospel Acclamation":   "R&A p. n - YouTube video URL",\n')
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
            flat_dict = flatten_frontmatter(
                frontmatter=data['frontmatter'],
                feast_name=var_name,
                date=data['date'],
                season=data['season'],
                lit_year=data['lit_year'],
                mass_setting=data['mass'],
                hymnal=hymnal
            )
            
            # Format and write
            py_code = format_dict_as_python(flat_dict, var_name)
            f.write(py_code)
            f.write('\n\n')

def format_hymn_options(song_data, priority_order, is_gospel=False):
    """
    Format hymn options with priority labels.
    
    Args:
        song_data: Dict with 'list' of hymns and options
        priority_order: Priority ranking dict
        is_gospel: If True, format as URL placeholder
    
    Returns:
        str or list: Formatted hymn(s)
    """
    # Sort hymn options by priority when applicable
    sorted_hymns = sorted(song_data['list'], 
                         key=lambda h: priority_order.get(h.get('priority', 'optional'), 3))
    
    # If only one hymn, return as string
    if len(sorted_hymns) == 1:
        hymn = sorted_hymns[0]
        name = hymn['name']
        if 'composer' in hymn.keys():
            name = f"{name} ({hymn['composer']})"
        priority = hymn.get('priority', 'optional')
        
        # Find entry in hymnal index using closest match
        display_name, number = fuzzy_index_lookup(name, verbose=False)

        if is_gospel:
            return f"[{priority}] -- URL"
        else:
            return f"[{priority}] {number} - {display_name}"
    
    # If multiple hymns, return as list
    else:
        options = []
        for hymn in sorted_hymns:
            name = hymn['name']
            if 'composer' in hymn.keys():
                name = f"{name} ({hymn['composer']})"
            priority = hymn.get('priority', 'optional')

            # Find entry in hymnal index using closest match
            display_name, number = fuzzy_index_lookup(name, verbose=False)

            if is_gospel:
                options.append(f"[{priority}] -- URL")
            else:
                options.append(f"[{priority}] {number} - {display_name}")
        
        return options

def format_psalm_options(song_data, priority_order, date, celebration, is_gospel=False):
    """
    Format psalm and gospel acclamation options with priority labels.
    
    Args:
        song_data: Dict with 'list' of psalm or gospel acclamation options
        priority_order: Priority ranking dict
        date: date of celebration, used for RA indexing
        celebration: name of celebration, used for RA indexing
        is_gospel: Boolean, whether to advance the page number by one
    
    Returns:
        str or list: Formatted entry or entries
    """
    # Sort options by priority when applicable
    sorted_entries = sorted(song_data['list'], 
                         key=lambda h: priority_order.get(h.get('priority', 'optional'), 3))
    
    # If only one entry, return as string
    if len(sorted_entries) == 1:
        entry = sorted_entries[0]
        priority = entry.get('priority', 'optional')

        # Handle RA differently from hymnal options
        numflag = False
        if entry['book'].lower() == 'ra':
            number, index_key, _ = fuzzy_ra_index_lookup(date=date, celebration_name=celebration)
            if number is None:
                numflag = True
            if is_gospel and number is not None:
                display_name = get_ra_video_url(index_key.split(' - ')[-1].strip(),
                                                get='gospel acclamation')
                number += 1
            else:
                display_name = get_ra_video_url(index_key.split(' - ')[-1].strip(),
                                                get='psalm')
            number = f'R&A p. {number}'
        # Appendices 
        elif 'app' in entry['book'].lower():
            display_name = 'URL'
            number = 'R&A p. None'
            numflag = True
        else:
            # Find entry in hymnal index using closest match
            name = entry['name']
            display_name, number = fuzzy_index_lookup(name, verbose=False)

        if numflag:
            return f"[{priority}] {number} - {display_name} ⚠️VERIFY⚠️"
        else:
            return f"[{priority}] {number} - {display_name}"
    
    # If multiple entries, return as list
    else:
        options = []
        for entry in sorted_entries:
            priority = entry.get('priority', 'optional')

            # Handle RA differently from hymnal options
            numflag = False
            if entry['book'].lower() == 'ra':
                number, index_key, _ = fuzzy_ra_index_lookup(date=date, celebration_name=celebration)
                display_name = get_ra_video_url(index_key.split(' - ')[-1].strip())
                if number is None:
                    numflag = True
                if is_gospel and number is not None:
                    number += 1
                number = f'R&A p. {number}'
            # Appendices 
            elif 'app' in entry['book'].lower():
                display_name = 'URL'
                number = 'R&A p. None'
                numflag = True
            else:
                # Find entry in hymnal index using closest match
                name = entry['name']
                numflag = False
                display_name, number = fuzzy_index_lookup(name, verbose=False)
                if number is None:
                    numflag = True

            if numflag:
                options.append(f"[{priority}] {number} - {display_name} ⚠️VERIFY⚠️")
            else:
                options.append(f"[{priority}] {number} - {display_name}")
        
        return options

def advance_psalm(text, step=1):
    # New number
    number = int(''.join(c for c in text if c.isdigit())) + step

    # Split the string
    text_list = text.split(' ')

    # Replace and reassemble
    text_list[3] = str(number)
    return ' '.join(text_list)

def flatten_frontmatter(frontmatter, feast_name, date, season, lit_year, hymnal, mass_setting=None):
    """
    Convert nested frontmatter structure to flat dictionary format.
    
    Args:
        frontmatter: Nested dict from QMD file
        feast_name: Name for the dictionary variable (e.g., 'christmas_day')
        date: Date of the feast, used for index lookup
        season: Liturgical season
        lit_year: Liturgical year from which to pull songs
        hymnal: Either 'gather' or 'bb' (Breaking Bread) to specify the hymnal
            to use for hymn numbers
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

    # 3. Add songs one at a time
    increase = 0
    for song in frontmatter.keys():
        # Handle responsorial psalm and gospel acclamation separately
        if 'psalm' in song.lower():
            if song.lower() == 'psalm':
                result['Responsorial Psalm'] = format_psalm_options(frontmatter[song], priority_order, date, feast_name)

                # If no gospel acclamation is provided, require R&A
                if 'gospel-acclamation' not in frontmatter.keys():
                    result['Gospel Acclamation'] = format_psalm_options(
                        {'list': [{'book': 'RA', 'priority': 'required'}]}, priority_order, date, feast_name, is_gospel=True)
            else:
                # Advance pages for multiple psalms (Easter Vigil and Pentecost
                # Vigil) - requires manual verification due to multiple options
                results = format_psalm_options(frontmatter[song], priority_order, date, feast_name)
                if isinstance(results, list):
                    for i, entry in enumerate(results):
                        results[i] = advance_psalm(entry, step=increase) + ' ⚠️VERIFY⚠️'
                        increase += 1
                    result[unkey(song)] = results
                else:
                   result[unkey(song)] = advance_psalm(results, step=increase) + ' ⚠️VERIFY⚠️'
                   increase += 1
        
        # Ignore anthems for now
        elif song.lower() == 'anthems':
            pass
        else:
            result[titlecase(song)] = format_hymn_options(frontmatter[song], priority_order)
    
    return result

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
    lines = [f"{var_name.replace('-', '_')} = {{"]
    
    # Loop through the dictionary items to build the new code string
    for key, value in dict_data.items():
        if key.lower() == 'parts' or key.lower() == 'processional' or key.lower() == 'gospel acclamation':
            if isinstance(value, list):
                # Format lists with proper indentation
                lines.append(f'    "{key}": [')
                for item in value:
                    lines.append(f'        "{item}",')
                # Remove trailing comma from last item
                if lines[-1].endswith(','):
                    lines[-1] = lines[-1][:-1]
                lines.append('    ],\n')
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

def load_env_file():
    """Load environment variables from .ghenv file."""
    # Get environment variable file
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    env_file = Path(f'{PROJECT_ROOT}/.ghenv')
    # If the file exists, load the variables
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def load_hymn_schedules(file_name):
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
    if 'Ra' in hymns.keys():
        hymns.pop('Ra', None)
    
    tbl = tabulate(
            # Conditional for responsorial psalm
            [["&emsp;", f"**{unkey(k)}:**", f"[{v.split('-')[0].strip()}]({v.split('-')[1].strip()})"] if ('psalm' in k.lower() or 'gospel' in k.lower()) and "http" in v else
            
            # Everything else
            ["&emsp;", f"**{unkey(k)}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] for k,v in hymns.items()],
            tablefmt='grid'
            
            # Add Mass setting and formatting
            ) + '\n: {.hover .normal tbl-colwidths="[2, 25, 73]"}' + '\n\n\\needspace{3\\baselineskip}\n\n'

    return tbl

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def get_existing_flagged_videos(token, owner, repo, label):
    """Get videos already flagged with a specific label."""
    # Repo issues URL
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # Metadata
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "state": "open",
        "labels": label
    }
    # Extract information from open issues
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        if label == "video-unavailable":
            # Extract YouTube URLs
            flagged = set()
            for issue in issues:
                body = issue.get('body', '')
                urls = re.findall(r'https://(?:www\.)?youtube\.com/watch\?v=[\w-]+', body)
                flagged.update(urls)
            return flagged
        
        elif label == "video-missing":
            # Extract hymn names from issue body
            flagged = set()
            for issue in issues:
                body = issue.get('body', '')
                # Extract hymn names between ** markers
                hymn_names = re.findall(r'\*\*([^*]+)\*\*', body)
                flagged.update(hymn_names)
            return flagged
        
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not fetch existing issues: {e}")
        return set()

def check_video_availability(url, retry_delay=2):
    """
    Check video availability using multiple free methods.
    
    Returns:
        tuple: (is_valid_url, is_available, status, title)
            - is_valid_url: True if URL format is valid
            - is_available: True if video exists and is accessible
            - status: Status message (e.g., "Available", "Private", "Invalid URL")
            - title: Video title or None
    """
    # Check for missing URL
    if url is None or url == '' or not isinstance(url, str):
        return False, False, "Missing URL", None
    
    # Check for valid YouTube URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return False, False, "Invalid URL format", None
    
    video_id = extract_video_id(url)
    if not video_id:
        return False, False, "Invalid URL format", None
    
    # URL is valid, now check availability
    # Method 1: YouTube oEmbed (fastest, most reliable)
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    
    try:
        response = requests.get(oembed_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return True, True, "Available", data.get('title', 'Unknown')
        elif response.status_code == 404:
            return True, False, "Unavailable or removed", None
        elif response.status_code == 401:
            return True, False, "Private", None
            
    except requests.RequestException:
        pass  # Fall through to next method
    
    # Method 2: Invidious API (fallback)
    time.sleep(retry_delay)  # Be nice to public instances
    
    invidious_instances = [
        "https://invidious.private.coffee",
        "https://inv.nadeko.net",
    ]
    
    for instance in invidious_instances:
        try:
            api_url = f"{instance}/api/v1/videos/{video_id}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('error'):
                    return True, False, data['error'], None
                return True, True, "Available", data.get('title', 'Unknown')
            elif response.status_code == 404:
                return True, False, "Not found", None
                
        except requests.RequestException:
            continue
    
    # If all methods fail - URL is valid but couldn't be verified
    return True, False, "Could not verify (all methods failed)", None

def create_issue(token, owner, target_repo, title, body, labels):
    """Helper function to create a GitHub issue."""
    # Repo issues URL
    url = f"https://api.github.com/repos/{owner}/{target_repo}/issues"
    
    # Metadata
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Data
    data = {
        "title": title,
        "body": body,
        "labels": labels,
        "assignees": [owner]
    }
    # Create the issue
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        issue_url = response.json()['html_url']
        print(f"✓ Issue created: {issue_url}")
        return issue_url
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to create issue: {e}")
        return None

def create_github_issues(unavailable_videos, missing_videos, token, owner, target_repo):
    """
    Create separate GitHub issues for unavailable videos vs missing video URLs.
    
    Args:
        unavailable_videos: List of videos with URLs that are unavailable
        missing_videos: List of entries where video URL is None/missing
        token: GitHub token
        owner: Repository owner
        target_repo: Target repository name
    
    Returns:
        tuple: (success, unavailable_issue_url, missing_issue_url, skipped_unavailable, skipped_missing)
    """
    # Keep track of unavailable and missing videos
    unavailable_issue_url = None
    missing_issue_url = None
    skipped_unavailable = 0
    skipped_missing = 0
    
    # Get already flagged issues
    print("Checking for open issues...")
    flagged_unavailable = get_existing_flagged_videos(
        token=token,
        owner=owner,
        repo=target_repo,
        label="video-unavailable")
    flagged_missing = get_existing_flagged_videos(
        token=token,
        owner=owner,
        repo=target_repo,
        label="video-missing")
    
    # ========== Handle Unavailable Videos ==========
    if unavailable_videos:
        # Filter out already flagged
        new_unavailable = [
            video for video in unavailable_videos 
            if video['url'] not in flagged_unavailable
        ]
        skipped_unavailable = len(unavailable_videos) - len(new_unavailable)
       
        # Report out
        if skipped_unavailable > 0:
            print(f"Skipping {skipped_unavailable} unavailable video(s) already flagged")
        
        # Create issue for new unavailable videos
        if new_unavailable:
            title = f"⚠️ {len(new_unavailable)} Unavailable Videos Detected"
            body = "The following videos are no longer available and need replacement:\n\n"
            
            for video in new_unavailable:
                body += f"- [ ] **{video.get('hymn', 'Unknown')}**\n"
                body += f"  - URL: {video['url']}\n"
                body += f"  - Status: {video['status']}\n"
                body += "\n"
            
            body += "\n---\n*Auto-generated: Video URLs exist but videos are unavailable*"
            
            unavailable_issue_url = create_issue(
                token=token,
                owner=owner,
                target_repo=target_repo,
                title=title,
                body=body,
                labels=["automated", "video-unavailable", "needs-replacement"]
            )
    
    # ========== Handle Missing Video URLs ==========
    if missing_videos:
        # Filter out already flagged (use hymn name as identifier)
        flagged_missing_names = flagged_missing
        new_missing = [
            video for video in missing_videos
            if video.get('hymn') not in flagged_missing_names
        ]
        skipped_missing = len(missing_videos) - len(new_missing)
        
        # Report out
        if skipped_missing > 0:
            print(f"Skipping {skipped_missing} missing video(s) already flagged")
        
        # Create issue for new missing videos
        if new_missing:
            title = f"🔍 {len(new_missing)} Missing Video URLs"
            body = "The following entries are missing video URLs and need to be added:\n\n"
            
            for video in new_missing:
                body += f"- [ ] **{video.get('hymn', 'Unknown')}**\n"
                body += "  - Status: No URL provided\n"
                if video.get('feast'):
                    body += f"  - Feast: {video['feast']}\n"
                if video.get('moment'):
                    body += f"  - Moment: {video['moment']}\n"
                body += "\n"
            
            body += "\n---\n*Auto-generated: Video URLs are missing from YAML data*"
            
            missing_issue_url = create_issue(
                token, owner, target_repo,
                title, body,
                ["automated", "video-missing", "needs-url"]
            )
    
    # Summary
    if not unavailable_issue_url and not missing_issue_url:
        if unavailable_videos or missing_videos:
            print("All issues already flagged in open issues")
        else:
            print("No unavailable or missing videos found")
    
    return True, unavailable_issue_url, missing_issue_url, skipped_unavailable, skipped_missing

def embed_multimedia(name, swap=False, try_local=False):
    """Embed multimedia into an HTML table.
    
    Parameters
    ----------
    name: Name of the song to embed
    swap: Set to True if the `name` has a colon and needs to be swapped, for
        example, `Gloria: Heritage Mass` --> `Heritage Mass: Gloria`. See
        ?get_url or ?get_local_path.
    local_path: If True, will first look for `local_path` key in the hymn index
        specifying a path to a local audio file. If found, that local file will
        be embedded instead of an online video. If the `local_path` key is not
        found, or if `try_local` is False (default), a video will be embedded
        using the `url` key in the index.
    """

    # Get URL
    if try_local:
        try:
            url = get_local_path(name, swap=swap)
        except KeyError:
            url = get_url(name, swap=swap)
    else:
        url = get_url(name, swap=swap)

    # If the URL is a local audio file, embed an audio player
    if 'http' not in url and '.mp3' in url:
        content = '<audio controls="">\n' +\
                f'  <source src="{url}" type="audio/wav"/>\n' +\
                '</audio>\n' +\
                '<br><br>'
    # If the URL is a YouTube video, embed a video
    elif 'http' in url and ('youtu.be' in url or 'youtube.com' in url):
        content = f"{{{{< video {url} >}}}}"
    # Otherwise, return the URL
    else:
        content = url

    return content

def video_table(hymns: dict):
    """Create HTML table from dictionary of hymns. (Generated by claude.ai on 2025-12-23 due to rendering inconsistencies with Quarto grid tables and complex content.)
    """

    RAnote = " <br> Other video recordings from *Respond & Acclaim* for rehearsal purposes can usually be found on several private YouTube channels such as <a href='https://www.youtube.com/@ChrisBrunelle/videos'>Chris Brunelle</a>, <a href='https://www.youtube.com/@LiturgicalMusic'>Liturgical Music</a>, or <a href='https://www.youtube.com/@MusicMinistry101/videos'>Music Ministry 101</a>. <br><br>"

    # Start table with custom classes and column widths
    html = '<table class="hover normal" style="width: 100%;">\n<tbody>\n'
    
    for k, v in hymns.items():
        html += '<tr>'
        
        # First column (title) - right-aligned and top-aligned
        html += f'<td style="width: 25%; text-align: right; vertical-align: top; padding-right: 0.5em;"><strong>{titlecase(unkey(k))}:</strong></td>'
        
        # Second column (content) - conditional logic
        if ('psalm' in k.lower() or 'gospel' in k.lower()) and 'http' in v:
            content = f"<em>Respond & Acclaim</em> {re.search('R&A (.+?) -', v).group(1)} <br><br> {{{{< video {v.split('- ')[-1]} >}}}}{RAnote}"
        else:
            content = v.replace('| ', '') + f"<br><br> {{{{< video {get_url(v.split(' - ')[1].strip())} >}}}}"
        
        html += f'<td style="width: 75%;">{content}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n\n'
    
    return html

def massparts_video_table(season:str, setting:str, include:list):
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
            content = embed_multimedia(name=k, swap=True, try_local=True)
        
        html += f'<td style="width: 75%;">{content}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n\n'
    
    return html

def get_page(date_celebration):
    """Get page number by exact date and celebration. Must be formatted
    'date - celebration'
    For example, `November 30, 2025 - First Sunday of Advent'
    """
    return ra_index.get(date_celebration)

def search_celebration(search_term):
    """Search for celebrations by partial name match."""
    search_lower = search_term.lower()
    return {k: v for k, v in ra_index.items()
            if search_lower in k.lower()}

def get_page_by_date(date_obj, celebration_substring="", fuzzy=False, threshold=70):
    """
    Get page number using a datetime object.
    
    Args:
        date_obj: datetime.date or datetime.datetime object
        celebration_substring: Substring or full name to match
        fuzzy: If True, use fuzzy matching; if False, use exact substring match
        threshold: Minimum similarity score for fuzzy matching (0-100)
    
    Returns:
        int: Page number, or None if not found
    
    Examples:
        >>> # Exact substring match
        >>> get_page_by_date(date(2026, 1, 4), "Epiphany")
        28
        
        >>> # Fuzzy match (handles typos, variations)
        >>> get_page_by_date(date(2026, 1, 4), "Epifany", fuzzy=True)
        28
    """
    # Use fuzzy matching, if indicated
    if fuzzy and celebration_substring:
        page, _, _ = fuzzy_ra_index_lookup(date_obj, celebration_substring, threshold)
        return page
    
    # Format date to match the index
    date_str = date_obj.strftime("%B %d, %Y")
    
    # Search the celebrations for one that contains the substring
    if celebration_substring:
        # Search for entries matching this date and celebration
        for key, page in ra_index.items():
            if key.startswith(date_str) and celebration_substring.lower() in key.lower():
                return page
    else:
        # Return first entry for this date
        for key, page in ra_index.items():
            if key.startswith(date_str):
                return page
    
    # Otherwise, return nothing
    return None

def get_all_pages_for_date(date):
    """
    Get all entries for a specific date.
    Useful when you need to see all options.
    
    Args:
        date: datetime.date or datetime.datetime object
    
    Returns:
        dict: {celebration_name: page_number}
    
    Example:
        >>> get_all_pages_for_date(date(2025, 12, 25))
        {
            'The Nativity of the Lord (Christmas): At the Mass during the Night': 18,
            'The Nativity of the Lord (Christmas): At the Mass at Dawn': 20,
            'The Nativity of the Lord (Christmas): At the Mass during the Day': 22
        }
    """
    # Format date to match the index
    date_str = date.strftime("%B %d, %Y")
    
    # Get all the entries (e.g., Christmas options)
    results = {}
    for key, page in ra_index.items():
        if key.startswith(date_str):
            celebration = key.split(" - ", 1)[1]
            results[celebration] = page
    
    return results

def arrange_songs(hymns, parts):
    """Arrange hymns, songs, and parts of the Mass in liturgical order"""

    def find_match(order_key, lookup):
        """Look up order keys to parts_dict keys using prefix matching.
        e.g., 'Memorial Acclamation' matches 'Memorial Acclamation A'."""
        if order_key in lookup:
            return order_key
        matches = [k for k in lookup if k.startswith(order_key)]
        return matches[0] if len(matches) == 1 else None

    # Order in which songs would appear
    order = [
        'Psalm After First Reading',
        'Psalm After Second Reading',
        'Psalm After Third Reading',
        'Psalm After Fourth Reading',
        'Psalm After Fifth Reading',
        'Psalm After Sixth Reading',
        'Psalm After Seventh Reading',
        'Psalm After Epistle',
        'Processional',
        'Kyrie',
        'Sprinkling',
        'Gloria',
        'Responsorial Psalm',
        'Sequence',
        'Gospel Acclamation',
        'Distribution of Ashes',
        'Washing of Feet',
        'Veneration of the Cross',
        'Litany of the Saints',
        'After each Baptism',
        'Sprinkling',
        'Offertory',
        'Holy',
        'Memorial Acclamation',
        'Amen',
        'Lamb of God',
        'Communion',
        'Meditation',
        'Recessional',
        'Transfer of the Blessed Sacrament',
    ]

    # Parse parts list into a dict: "Gloria: *Gloria omitted*" -> {"Gloria": "*Gloria omitted*"}
    parts_dict = dict(item.split(": ", maxsplit=1) for item in parts)

    # Merge: parts_dict takes priority over hymns for any key appearing in both
    combined = {**hymns, **parts_dict}

    # Extract rows in order, skipping parts not present in either source
    table = []
    for part in order:
        key = find_match(part, combined)
        if key:
            table.append((key, combined[key]))

    return table

def single_table(hymn_dict: dict, mass_parts: list):
    """Create a single Markdown table containing all songs in the Mass, including Mass parts, in order."""
    # Combine hymns and Mass parts in liturgical order
    combined = arrange_songs(hymns=hymn_dict, parts=mass_parts)

    tbl = tabulate(
        # Conditionals for R&A
        [[f"**{k.strip()}:**", f"[{v.split(' - ')[0].strip()}]({v.split(' - ')[1].strip()})<br><br>"] if ("https" in v and 'gospel' in k.lower()) else
        [f"**{k.strip()}:**", f"[{v.split(' - ')[0].strip()}]({v.split(' - ')[1].strip()})"] if "https" in v else

        # Hymns
        [f"**{k.strip()}:**", f"{v.split(' - ')[0].strip()} - {markdown_url(v.split(' - ')[-1].strip())}"] if " - " in v else

        # Mass parts
        [f"**{k.strip()}:**", f"[{v.strip()}]({get_url(k.strip()+': '+v.strip(), swap=True)})"] if 'omitted' not in v else
        [f"**{k.strip()}:**", f"{v.strip()}"]

        for k,v in combined],
        tablefmt='grid'
    
        # Formatting
        ) + '\n: {.hover .normal tbl-colwidths="[35, 65]"}' + '\n\n\\needspace{3\\baselineskip}\n\n'

    return tbl

def make_callout(message: str, title="Take heed!", type="important"):

    callout = '::: {.content-visible when-format="html"}\n' \
              f'::: {{.callout-{type} title="{title}"}}\n' \
              f'{message}\n' \
              ':::\n' \
              ':::\n\n' \
              '::: {.content-visible when-format="pdf"}\n' \
              f'::: {{.schedule-callout title="{title}"}}\n' \
              f'{message}\n' \
              ':::\n' \
              ':::\n\n'
    
    return callout
