"""
cantors.py
==========
Extracts events from Google calendar whose ID and authentication credentials 
are specified in `.env`.

Usage
-----
    python cantors.py --start 2026-03-01 --end 2026-03-31    
    python cantors.py --end 2026-03-31 --include_all_day

Arguments
---------
    -s, --start         First date to extract as string formatted "YYYY-MM-DD".
                        (optional, default: "today" for current day)
    -e, --end           Last date to extract as string formatted "YYYY-MM-DD".
                        (optional, default: "tomorrow" for next day)
    --include_all_day   Include all day events (default: False)
    -o, --outfile       CSV file to write (optional, default:
                        "[pwd]/calendars/cantors.csv")

Author: mgrossi
"""

# =============================================================================
#
# This script extracts events from Google calendar whose ID and authentication
# credentials are stored in `.env`. Results are saved as a dataframe using the
# file name and directory passed to `--outfile, -o`, which defaults to
# "[pwd]/calendars/cantors.csv" if empty. Optional start and end dates
#  formatted "YYYY-MM-DD" can be passed using `--start, -s` and `--end, -e`;
# if omitted, defaults to today and tomorrow, respectively. Note that unlike
# the Google API extraction method, this script returns events *inclusive* of
# `--end, -e`.
#
# See Google Calendar API docs:
# https://developers.google.com/workspace/calendar/api/quickstart/python
#
# =============================================================================
# Packages
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pathlib import Path
import datetime as dt
import pandas as pd
import utils as u
import argparse
import pytz
import json
import re
import os

# -----------------------------------------------------------------------------
# Local development

# class Args:
#     def __init__(self, start, end):
#         self.start = start
#         self.end = end

# args = Args(
#     start = 'today',
#     end = '2026-04-30'
# )

# PROJECT_ROOT = Path(os.getcwd())

# -----------------------------------------------------------------------------
# Command line execution

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        prog='calendar',
        usage='%(prog)s [arguments]',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--start', type=str, default='today',
                        help='First date to retrieve (str: "YYYY-MM-DD")')
    parser.add_argument('-e', '--end', type=str, default='tomorrow',
                        help='Last date to retrieve (str: "YYYY-MM-DD")')
    parser.add_argument('--include_all_day', action='store_true',
                        help='Include all day events in table (Default: False)')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, 
                        default='calendars/cantors.csv',
                        help='Name and directory of csv file to write. Default: "[pwd]/calendars/cantors.csv"')
    return parser.parse_args()

args = parse_args()

# -----------------------------------------------------------------------------
# Main program

def event_info(event_dict: dict, keys=['start', 'summary']):
    """Extract relevant information from event results.
    
    Parameters
    ----------
        event_dict: dictionary of event details from Google calendar API
        keys: list of keys from `event_dict` to be extracted.
            Default: ['start', 'summary']
    
    Returns
    -------
        Filtered calendar event detail dictionary containing only desired keys
    """
    # Subset `event_dict` using desired keys
    subset = {key:event_dict[key] for key in keys if key in event_dict}

    # Parse start date/time
    if 'start' in keys:
        # Handle events with times
        if 'dateTime' in event_dict['start'].keys():
            start = event_dict['start'].get('dateTime')
            start_date = dt.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').date()
            start_time = dt.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').time()
        # Handle all day events with no time
        else:
            start = event_dict['start'].get('date')
            start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()

            # Extract time from event name, if available
            if 'pm' in event_dict.get('summary').lower() or ' am' in event_dict.get('summary').lower():
                start_time = re.search('\\(([^)]+)', event_dict.get('summary')).group(1)
                start_time = dt.datetime.strptime(start_time, '%I:%M %p').time()
            else:
                start_time = dt.datetime.strptime(start, '%Y-%m-%d').time()

        # Update new dict
        subset['start'] = start
        subset['start_date'] = start_date
        subset['start_time'] = start_time

    return subset

def cantor_df(events: list, include_all_day=False):
    """Create a dataframe from a list of Google calendar event dictionaries.

    Parameters
    ----------
        events: list of event dictionaries to be converted to dataframe
        include_all_day: Bool, include all day events in the filtered dataframe
    
    Returns
    -------
        Dataframe containing Google calendar events
    """
    # Create a dataframe
    if include_all_day:
        df = pd.DataFrame([event_info(i) for i in events])
    else:
        df = pd.DataFrame([event_info(i) for i in events if 'dateTime' in i['start'].keys()])

    df.rename(columns={'summary': 'Name'}, inplace=True)
    df['start'] = pd.to_datetime(df['start_date'].astype(str) + df['start_time'].astype(str), format='%Y-%m-%d%H:%M:%S')
    df['Date'] = pd.to_datetime(df['start_date']).dt.strftime('%a %-m/%-d')
    df['Mass Time'] = pd.to_datetime(df['start']).dt.strftime('%-I:%M %p')

    return df

def main():
    # Project home directory
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    
    # Load calendar info
    CALENDAR_ID = os.environ["GOOGLE_CALENDAR_ID"]

    # Are we running in a GitHub Actions?
    in_ci = os.environ.get("GITHUB_OUTPUT") is not None
    
    # Load credentials from environment
    creds = None
    load_dotenv()

    TOKEN_PATH = os.environ.get("GOOGLE_TOKEN_PATH")
    token_json = os.environ.get("GOOGLE_TOKEN_JSON")
    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json), SCOPES
        )
    else:
        # Local: read from file
        token_path = PROJECT_ROOT / TOKEN_PATH
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This branch requires interactive login — only runs locally
            credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
            if credentials_json:
                flow = InstalledAppFlow.from_client_config(
                    json.loads(credentials_json), SCOPES
                )
            else:
                # Fallback for local dev with a file
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(PROJECT_ROOT, CREDENTIALS_PATH), SCOPES
                )
            creds = flow.run_local_server(port=0)

    # Write refreshed token to GitHub Actions output if running in CI
    if in_ci:
        # Write to GitHub Actions step output for the secret-update step
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"token_json={creds.to_json()}\n")
    else:
        # Update GOOGLE_TOKEN_JSON in .env
        env_path = PROJECT_ROOT / ".env"
        env_text = env_path.read_text()
        new_line = f'GOOGLE_TOKEN_JSON={creds.to_json()}'
        if "GOOGLE_TOKEN_JSON" in env_text:
            env_text = re.sub(r'GOOGLE_TOKEN_JSON=.*', new_line, env_text)
        else:
            env_text += f'\n{new_line}'
        env_path.write_text(env_text)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        tz = 'US/Eastern'
        if args.start.lower() == 'today':
            start = dt.datetime.now(tz=dt.timezone.utc).isoformat()
        else:
            start = pytz.timezone(tz).localize(dt.datetime.strptime(args.start, '%Y-%m-%d')).isoformat()
        
        # Need to add an extra day because retrieval excludes maxTime
        if args.end.lower() == 'tomorrow':
            end = dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(days=2)
            end = end.isoformat()
        else:
            end = pytz.timezone(tz).localize(dt.datetime.strptime(args.end, '%Y-%m-%d')) + dt.timedelta(days=1)
            end = end.isoformat()

        # Print formatted status, reverting end time back to original time
        print(f"Getting events from {dt.datetime.strftime(dt.datetime.strptime(start.split('T')[0], '%Y-%m-%d'), '%b %d, %Y')} to {dt.datetime.strftime(dt.datetime.strptime(end.split('T')[0], '%Y-%m-%d')-dt.timedelta(days=1), '%b %d, %Y')}")

        # List the events
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # If no events are found
        if not events:
            print("No upcoming events found.")
            return

        # Format output into dataframe
        df = cantor_df(events=events, include_all_day=args.include_all_day)
        # Remove placeholder events with no one scheduled
        dfss = df[df['Name'] != '-']
        if not dfss.equals(df):
            print(f"Omitting {df.shape[0]-dfss.shape[0]} events with no cantors scheduled.")

        # Write to file
        outfile = os.path.join(PROJECT_ROOT, args.outfile)
        dfss.to_csv(outfile)
        print(f"Events written to file: {outfile}")

        # Create HTML lookup widget
        widget_filename = "schedule_lookup.html"
        u.generate_lookup_widget(df=dfss, output_path=Path(f"{PROJECT_ROOT}/{widget_filename}"))
        print(f"Lookup widget created: {os.path.join(PROJECT_ROOT, widget_filename)}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()