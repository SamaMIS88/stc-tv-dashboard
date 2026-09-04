import pandas as pd 
df = pd.read_excel('stc_raw_events.xlsb', engine='pyxlsb')
print(df.shape) 