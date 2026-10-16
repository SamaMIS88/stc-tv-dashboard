import pandas as pd

# ---- T2: daily watch time ----
t2 = pd.read_excel('stc_raw_daily_watchtime.xlsx')
t2 = t2.drop(columns=[c for c in t2.columns if str(c).startswith('Unnamed')], errors='ignore')
t2 = t2.rename(columns={'date_': 'date', 'Total_watch_time_in_houres': 'total_watch_hours'})
t2['date'] = pd.to_datetime(t2['date'])
print(t2.head())
t2.to_csv('daily_watchtime_clean.csv', index=False)
print("T2 saved!")

# ---- T3: ratings ----
t3 = pd.read_excel('stc_raw_ratings.xlsx')
t3 = t3.drop(columns=[c for c in t3.columns if str(c).startswith('Unnamed')], errors='ignore')
t3['program_name'] = t3['program_name'].str.strip()
t3['program_genre'] = t3['program_genre'].str.strip()
t3['date_'] = pd.to_datetime(t3['date_'])
t3 = t3.rename(columns={'date_': 'date'})
t3 = t3.reset_index(drop=True)
t3['row_id'] = t3.index
print(t3.head())
t3.to_csv('ratings_clean.csv', index=False)
print("T3 saved!")