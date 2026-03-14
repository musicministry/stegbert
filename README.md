# St. Egbert Music Ministry

This repository contains an unofficial [website](https://musicministry.github.io/stegbert/) built for disseminating information about St. Egbert's music ministry program. It is experimental and will be built out if or as needed.

## Site Overview

#### Music Schedules

[This page](https://musicministry.github.io/stegbert/schedules.html) contains a collection posts, one per liturgical celebration, which lists the hymns and mass parts for each liturgy. Each song includes a YouTube video for practice purposes; these videos are embedded in the post for convenience. All posts for the week ahead, including, for example, any holy days of obligation, are published automatically each Sunday evening of the upcoming week. For example, the music lineup for the Second Sunday of Advent will be released on the evening of the First Sunday of Advent.

#### Looking Ahead

[This page](https://musicministry.github.io/stegbert/upcoming.html) contains schedules of music out several weeks in advance to faciliate planning and practice. Each song is a hyperlink to a YouTube video for practice. The Mass setting is indicated for each weekend and the Mass are listed with video links at the bottom of the page. This page is updated periodically throughout the year.

A PDF version of the page is also available for download and printing using the "PDF (hymn-schedule)" link under "Other Formats" at the bottom of the Table of Contents on the right side of the page. While printing from the website will often result in hymn lists getting split between two pages, this PDF template is specially designed to prevent page breaks within lists.

#### Cantors

[This page](https://musicministry.github.io/stegbert/cantors.html) contains an embedded Google calendar containing cantor schedules. The `Lookup` tab provides a simple web widget that allows users to search by name or Mass time to quickly find any upcoming liturgies for which they are scheduled to cantor.

### Disclaimer

This website is for general informational purposes only and is intended to be a resource for St. Egbert parish musicians. It is not the official parish website, which can be found [here](https://www.stegbertcatholicchurch.org/), nor does it constitute official communication of St. Egbert Catholic Church or the Catholic Diocese of Raleigh, North Carolina.

## How to use

The maintenance of this site is mostly automated to alleviate as much administrive burden as possible from the music coordinator. Setup and use instructions are provided below. Basic knowledge of using command line applications (platform-specific) is assumed. Knowledge of [Quarto](https://quarto.org/) and [Python](https://www.python.org/) is helpful but not necessarily required to make everything work.

### Setup

#### Initial site setup

Initial set up is easy. The instructions that follow will assume a parish named St. Cecilia for illustrative purposes.

After cloning the template repository (coming soon), simply set the parish name in the `_website.yml` file using the `church` keyword:

```yml
church: "Saint Cecilia Church"
```

This will then be used throughout the site, such as in PDF headers. Other places to specify the church name include:

* Title and subtitle of `index.qmd`, which controls the site home page. These are set in the frontmatter YML at the top of the file:

    ```yml
    ---
    title: "St. Cecilia"
    subtitle: "City, State"
    ---
    ```

* Body of `index.qmd`, if needed
* Title and body of `about.qmd`

Page content can be modified in any of the `qmd` files, and new pages can be added by creating new `qmd` files. New pages need to be manually added to the site navigation bar in `_website.yml` using the existing:

```yml
navbar:
  left:
    - about.qmd
    - text: "Music Schedules"
      href: schedules.qmd
    - text: "Looking Ahead"
      href: upcoming.qmd
```

More information about site configuration and customization options can be found in the [Quarto docs](https://quarto.org/docs/guide/).

#### Python setup

::: {.callout-note}
All commands below should be executed from within the project's parent directory, which we will assume to be `musicministry-site` located in `path/to/stcecilia` but this will be unique to your system and file structure.
:::

Python scripts are used to create and update content throughout the site. The repo contains everything you need, but some initial configuration is required.

First, make sure you have [Python](https://www.python.org/) installed. The tools were created using Python 3.14. Earlier versions may be supported but have not been tested.

In a command terminal, navigate to the parent project directory create a Python virtual environment . We'll call it `.venv` but it can be named anything. Just remember what you call it, as it will be needed later:

```bash
cd path/to/stcecilia/musicministry-site

python -m venv .venv
```

Now we need to activate the virtual environment and install the package dependencies, which are listed in `requirements.txt`.

To activate the virtual environment on Windows:

```bash
# In cmd.exe
venv\Scripts\activate.bat

# In PowerShell
venv\Scripts\Activate.ps1
```

Or, or Mac or Linux:

```bash
source .venv/bin/activate
```

See the [Python docs](https://python.land/virtual-environments/virtualenv) for more info or for troubleshooting.

Then install the package dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

That's it! Virtual environment creation and package installation only needs to be done once. You will, however, need to activate the virtual environment each time you want to use any of the scripts. If you do not do so, the packages will not be found.

### Maintenance: Populating Content

#### Creating hymn lists

Both the weekly post pages and the upcoming lineup pages pull content from JSON-formatted lists. These are stored in `.py` files in a directory called `YYYY-X`, where `YYYY` is the calendar year and `X` is the liturgical cycle, for example, `2026-A`. For convenience and organization purposes, there should be one file for each liturgical season:

```bash
`2026-a/`
|_ `advent.py`
|_ `christmas.py`
|_ `lent.py`
|_ `holy-week.py`
|_ `easter.py`
|_ `orderinary-time.py` # (includes all of Ordinary Time, both winter and summer)
|_ `occasions.py`       # (optional, for special occasions throughout the year)
```

Within each of these files are repeated JSON blocks formatted as follows:

```json
seasonNN = {
    "Mass": "Name of Mass Setting",
    "parts": ["Holy: Name of Mass Setting",
              "Memorial Acclamation A: Name of Mass Setting",
              "Amen: Name of Mass Setting",
              "Lamb of God: Name of Mass Setting"],

    "Processional":         "### - Name of Processional Hymn",

    "Responsorial Psalm":   "### - Name of Responsorial Psalm",
    "Gospel Acclamation":   "### - Name of Gospel Acclamation",

    "Preparation of Gifts": "### - Name of Preparation of Gifts Hymn",
    "Communion":            "### - Name of Communion Hymn",
    "Recessional":          "### - Name of Recessional Hymn"
}
```

where `seasonNN` is the liturgical season and zero-padded two-digit week number, `Mass` contains the name of the Mass setting used, and `parts` contains a list (comma-separated, in brackets, as shown) of the Mass parts to include. Repeating the Mass name after each Mass part in `parts` (note the mandatory colon separator) allows the flexibility of mixing and matching Mass parts from different settings. Note, however, that the value of `Mass` is always used in "Upcoming" at the top of each week list and to name the list of Mass parts at the bottom of the page, so this should indicate which Mass setting is used most when parts are mix-matched. "Gloria" should be omitted during Advent and Lent; the scripts will then automatically include a statement "Gloria is omitted during ____" in the weekly post. Be sure to specify which Memorial Acclamation (A, B, or C) is being used in order for the automated URL retrieval to function properly.

List the hymns in the liturgy in chronological order. They will appear in the lists in the same order they appear here. These keys can be modified. For example, if "Opening" is preferred over "Processional", simply change that, but remember to keep the quotation marks. Similarly, other songs can be added or subtracted as needed, as long as the same formatting convention is followed. For example, a meditation hymn can be inserted after communion:

```json
{
    ...
    "Meditaton": "### - Name of Meditation Hymn"
    ...
}
```

or a Sequence can be added for the Solemnities of Easter, Pentecost, or Corpus Christi:

```json
{
    ...
    "Sequence": "### - Name of Sequence"
    ...
}
```

:::{.callout-important title="Be careful!"}
Format and naming conventions matter throughout these instructions. Deviations or mistakes may lead to unintentional behavior or cause scripts to crash.
:::

In the example above, the Responsorial Psalm and Gospel Acclamation are assumed to be taken from the same hymnal. Currently, *Respond and Acclaim* (R&A) by OCP is also supported using the following structure:

```json
{
    ...
    "Responsorial Psalm":   "R&A p. 4 - URL",
    "Gospel Acclamation":   "R&A p. 5 - URL",
    ...
}
```

where "URL" is the URL to a YouTube video for rehearsal purposes, if desired.

Putting this all together, the music selection for the First Sunday of Advent might look like this:

```json
advent01 = {
    "Mass": "Missa Emmanuel",
    "parts": ["Holy: Missa Emmanuel",
              "Memorial Acclamation A: Missa Emmanuel",
              "Amen: Missa Emmanuel",
              "Lamb of God: Missa Emmanuel"],

    "Processional":         "577 - Sing Out, Earth and Skies!",

    "Responsorial Psalm":   "R&A p. 4 - https://youtu.be/4yPHj2DFoC4?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 5 - https://youtu.be/6JGogB_Mb-I?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "423 - Awake! Awake, and Greet the New Morn",
    "Communion":            "397 - Maranatha, Lord Messiah",
    "Recessional":          "766 - City of God"
}
```

This same block would be repeated in `advent.py` with appropriate variable names `advent02`, `advent03`, and `advent04`.

##### Automation Option

These blocks can be created automatically using `create-list.py` in the `scripts` directory *if a properly formatted music planning book is available* (description coming soon). To run the script in a command terminal:

```bash
python scripts/create-list.py YYYY advent01 advent04 
```

where "YYYY" is the current year followed by the first and last liturgical celebration to be retrieved. In order for this to work, these celebrations must have the same names as the JSON blocks above.

This script has the option to exclude lower priority feasts by passing the number of the lowest-desired celebration priority to `-p, --priority`:

* 2 for Sundays and holy days of obligation
* 1 for important days that are not holy days (e.g., Ash Wednesday)
* 0 otherwise

This is useful because the music planning book contains feasts that do not usually require music (*e.g.*, when they fall during the week). If the priority flag is not passed, all celebrations will be pulled.

The output file name defaults to `next-lists.py`, which can be changed using the optional `-o, --outfile` flag. Most of it will be populated automatically: numbers and video URLs for both hymnal and R&A will be retrieved from the appropriate index *as long as the hymn names match exactly*. Importantly, *this output file needs human review before proceeding*:

1. When the script is unsure of a listing, "⚠️VERIFY⚠️" will be appended to alert the user. This can refer to the number, hymn name, or URL. Check the entry, fix if if needed, and manually delete the "⚠️VERIFY⚠️" text.

2. When multiple hymn options are found in the music planning book, they will all be pulled over as a list and labeled by priority. Review the options and select the desired one by deleting the others and removing the surrounding brackets to remove the list. For example:
  
    ```json
    {
      "Processional": [
        "[preferred] ### - Name of Preferred Hymn ⚠️VERIFY⚠️",
        "[optional] ### - Name of Optional Hymn ⚠️VERIFY⚠️"
        ]
    }
    ```

    might become

    ```json
    {
      "Processional": "### - Name of Preferred Hymn",
    }
    ```

3. As of a result of the behavior in (2) above, even when there is only one hymn option, the hymn number will be prefaced by "[required]". Manually delete these prefaces.

::: {.callout-important}
If the output file is not named according to the [seasons listed above](#creating-hymn-lists), manually rename the file after reviewing. The automation will not find files named anything else. This is by design, not a bug.
:::

#### Looking Ahead

The "Looking Ahead" page is populated automatically using the [hymn lists above](#creating-hymn-lists) and the `upcoming.py` script:

```bash
python scripts/upcoming.py YYYY advent01 advent04
```

where "YYYY" is the year to process followed by the first and last feast to include on the page. Note that these feasts need not be in the same liturgical season. 

```bash
python scripts/upcoming.py YYYY advent01 baptism
```

will include all of the Advent and Christmas seasons.

An option exists to include a red alert banner at the top of the page. This could be useful to highlight a change in Mass setting, for example. To implement this, use a `-c, --callout` flag followed by the desired message in quotes. For example:

```bash
python scripts/upcoming.py YYYY advent01 advent04 --callout "The Gloria is omitted during Advent but resumes Christmas Eve"
```

will add the following banner to the top of the page after the generic instructions but before the hymn list:

::: {.callout-important title="Take heed!"}
The Gloria is omitted during Advent but resumes Christmas Eve
:::

The output file name defaults to `upcoming.qmd`, as expected by the website by default, but this can be changed using the `-o, --outfile` flag. This is useful for testing or creating additional lists that you don't want released on the website.

::: {.callout-tip}
The file extension must be `qmd` (Quarto Markdown). If you change the file name and want it to be included in the site, change the `href` value for "Looking Ahead" in `_website.yml`.
:::

#### Weekly Music Schedule Posts

`post-week.py`
`post.py`

#### Cantor Schedules

The Cantor Schedules page currently contains two tabset panels.

##### Calendar

The first panel, `Calendar`, is an embedded read-only Google calendar dedicated to cantors and other need-to-know events, like major solemnities or feast days. To embed your own Gmail calendar, open Google Calendar. Under "My calendars" on the left sidebar, find the calendar you want to embed and click the three dots next to the calendar name and select "Settings and sharing". On the page that opens, click "Integrate calendar" on the left sidebar under "Settings for my calendar" and the calendar name you want to embed. Copy the "Public URL to this calendar" URL and paste it in the `cantors.qmd` file as the source link for the calendar iframe:

```html
<iframe src="paste-URL-here"...>
```

Be sure to enclose it in quotation marks. Other display settings can be adjusted on the Google side using the "Customize" button or on the music ministry site side in this iframe block. Please consult the necessary documentation (Google or html syntax resources) to learn what is possible and how to do it. You only need to do this once to set up the site.

This calendar is updated directly in the Google account that owns it. Since this is a dynamic link, this calendar always shows the most recent version of the Google calendar and updates in real time. It is a public calendar, meaning anyone with the site link or calendar link can view it, but this is significantly easier to than manually granting access to different people, especially those without Gmail accounts, which Google does not support well.

##### Lookup

`cantors.py`
`cantor-counts.py`