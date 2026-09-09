import pandas as pd

pd.set_option('display.max_columns', None)

df = pd.read_pickle('events_raw.pkl')

df['date_'] = pd.to_datetime(df['date_'], unit='D', origin='1899-12-30')
df['duration_hours'] = df['duration_seconds'] / 3600

print(df[['date_', 'duration_seconds', 'duration_hours']].head(10))