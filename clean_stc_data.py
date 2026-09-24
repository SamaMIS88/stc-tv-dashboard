import pandas as pd

pd.set_option('display.max_columns', None)

df = pd.read_pickle('events_raw.pkl')

df['date_'] = pd.to_datetime(df['date_'], unit='D', origin='1899-12-30')
df['duration_hours'] = df['duration_seconds'] / 3600

print(df[['date_', 'duration_seconds', 'duration_hours']].head(10))
is_movie = df['program_class'] == 'MOVIE'
df.loc[is_movie, ['season', 'episode']] = None
print(df[df['program_class'] == 'MOVIE'][['program_class', 'season', 'episode']].head())
df['hd'] = df['hd'].astype(bool)
df['series_title'] = df['series_title'].astype(bool)
print(df[['hd', 'series_title']].head(10))
df['program_name'] = df['program_name'].str.strip()
df['program_class'] = df['program_class'].str.strip()
df['program_desc'] = df['program_desc'].str.strip()
df['program_genre'] = df['program_genre'].str.strip()
df['original_name'] = df['original_name'].str.strip()
print(df[['program_name', 'program_class', 'program_desc', 'program_genre', 'original_name']].head(10))
df['long_session_flag'] = df['duration_hours'] > 24
print(df['long_session_flag'].sum(), "sessions flagged as unrealistically long")

print("max ID:", df['Column1'].max())
print("actual row count:", len(df))
df = df.reset_index(drop=True)
df['row_id'] = df.index
df.to_csv('events_clean.csv', index=False)
print("saved!")
