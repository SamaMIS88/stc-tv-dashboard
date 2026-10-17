STC TV Viewership Dashboard

An interactive Power BI dashboard built on about 1 million TV viewing sessions. The raw data was cleaned in Python (pandas), modelled in Power BI with DAX, and styled with a custom dark theme and HTML KPI cards.



What the dashboard shows
Metric	Value
Total watch time	358.5K hours
Unique viewers	11,578
Viewing sessions	1,048,575
Programs / genre labels	8,013 / 16
Period covered	14 Mar 2017 to 30 Apr 2018
Average rating	2.5 (scale 1 to 4)

The page has KPI cards, a daily watch-time trend, watch hours by genre, a top-programs table, active users by year, and slicers for genre and program class (movie or series).

Things the data shows
Four genres (Animation, Drama, Action, Comedy) make up about 83% of all watch hours.
Half of all sessions (50.1%) are shorter than 2 minutes, and the median session is about 2 minutes. That suggests a lot of the activity is quick browsing rather than sitting down to watch something.
Ratings are spread almost evenly across 1 to 4 (about 25% each), so the 2.5 average and the differences between genres carry little signal and shouldn't be over-read.
Data

Three raw files were provided in the STC x Misk data analytics workshop. They are not included in this repo.

File	What it is
stc_raw_events.xlsb	One row per viewing session: user, program, duration, genre, class, HD flag, date (1,048,575 rows, 13 columns)
stc_raw_ratings.xlsx	The same sessions with the user's rating (1,048,575 rows)
stc_raw_daily_watchtime.xlsx	Total watch hours per day (86 days between 1 Jan and 30 Apr 2018)
Data cleaning (Python)

Scripts are in scripts/.

Converted Excel serial dates to real dates.
Added duration_hours next to duration_seconds so units match the daily table.
Replaced the placeholder 0 in season and episode on movie rows with nulls.
Converted the hd and series_title 0/1 columns to booleans.
Trimmed whitespace in all text columns.
Flagged sessions longer than 24 hours with long_session_flag instead of deleting them: 663 sessions, 33.3K hours (9.3% of the total).
Compared the source row IDs with the row count (see limitations below).
Added a row_id to the events and ratings tables so they can be joined.
Data model and DAX
events_clean and ratings_clean are joined one-to-one on row_id. Before joining, I checked that all 1,048,575 rows match across the two files on user, program, date and genre.
daily_watchtime_clean is loaded in the model but no visual uses it. It is an exact roll-up of the events data for 86 days, so it adds nothing new.

Main measures:

dax
Total Watch Hours     = SUM(events_clean[duration_hours])
Active Users          = DISTINCTCOUNT(events_clean[user_id_maped])
Average Rating        = AVERAGE(ratings_clean[rating])
Average Session Duration = AVERAGE(events_clean[duration_hours])
Flagged Long Sessions = COUNTROWS(FILTER(events_clean, events_clean[long_session_flag] = TRUE()))

The three KPI cards are built with the HTML Content custom visual. Each card is a DAX measure that returns an HTML string, so the cards update with the slicers like any other visual.

Theme

dashboard/stc-theme.json is a Power BI theme (dark background, purple data colors, Segoe UI). Import it from View, then Themes, then Browse for themes.

Data quality notes and limitations
Gaps in the source IDs. The row IDs in the events file run up to 1,247,852, but only 1,048,575 rows are present. About 16% of IDs are missing, spread evenly through the file, so rows were removed before this file was made. The row count also equals Excel's row limit exactly, so the file may be cut off at the end as well. I couldn't confirm either way.
Damaged program names. Some titles are missing their first "S" (for example "100 treets", "The Amazing pider-Man"). I left them as they are, so a few programs are split or mis-grouped.
Placeholder genres. NOT_DEFINED_IN_UMS and SERIES_NOT_ADDED_UNDER_ANY_GENRE are hidden from the genre chart. They hold about 466 hours (0.1%).
Placeholder program names. Four time-slot style names ("24 :00 AM - :00 AM" and similar) cover 6,061 sessions and about 5.2K hours (1.4%). The top-programs table hides the two largest; the other visuals include them.
Long sessions are flagged, not removed, so the headline total includes them.
Uneven years. 2017 covers 14 Mar to 31 Dec and 2018 covers 1 Jan to 30 Apr, so the year-by-year comparison is not like for like.
Ratings only use the values 1 to 4.
Repo structure
dashboard/     Power BI report and theme
scripts/       Python cleaning scripts
screenshots/   Dashboard image used in this README
Reproduce

Requires Python 3 with pandas, pyxlsb and openpyxl, and Power BI Desktop (Windows).

Put the three raw files in the project root with the names above.
Convert the large events file once, because it is slow to read (about a minute or two):
python
   import pandas as pd
   pd.read_excel('stc_raw_events.xlsb', engine='pyxlsb').to_pickle('events_raw.pkl')
From the project root, run:
   python scripts/clean_stc_data.py
   python scripts/clean_t2_t3.py

This writes events_clean.csv, ratings_clean.csv and daily_watchtime_clean.csv. 4. Open dashboard/stc-tv-dashboard.pbix and point the data sources at those CSV files.

Tools

Python (pandas, pyxlsb, openpyxl), Power BI Desktop, DAX, HTML Content visual, Git and GitHub, VS Code.

Built by Sama Alshehri.
