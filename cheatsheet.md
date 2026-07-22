# Code Execution Cheat Sheet

### :book: Retrieve songs from planning book

Song lists are written to `next-lists.py`.

```bash
python scripts/create-list.py YYYY advent01 advent04 --priority 1
```

> [!NOTE]  
> :musical_note: The following next steps are not automated and must be carried out manually:
> 
> 1. Select one song when options exist.
> 2. Remove all "[Required] ", "[Preferred] ", , "[Flexible] ", and "[Optional] " prefaces. Be sure to include the trailing space.
> 3. Verify and correct, as needed, any songs marked "⚠️VERIFY⚠️". Remove the " ⚠️VERIFY⚠️" flag, including the leading space, when fixed.
> 4. Make any additional corrections as needed,
> 5. Copy and paste the corrected contents of `next-lists.py` into the appropriate liturgical season file(s) (*e.g.*, `advent.py`). Special occasions, such as Confirmation, should be added to `occasions.py`.

### :calendar: Weekly Lineups

To post one occasion:

```bash
python scripts/post.py YYYY --publish advent01
```

To post the next week:

```bash
python scripts/post-week.py YYYY
```

Use `--pdf` to generate individual PDF files for each post.

### :spiral_calendar: Looking Ahead

```bash
python upcoming.py YYYY 'advent01' 'advent04'
```
Both `html` and `pdf` versions are always created.

### :singer: Cantor Calendar

To start and end at specified dates:

```bash
python cantors.py --start 2026-03-01 --end 2026-03-31
```

### :bar_chart: Count Cantors

```bash
python scripts/cantor-counts.py --month 01
```