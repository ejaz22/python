# infer datetime
import pandas as pd
df = pd.read_csv('20180112-2.csv')
df['Month/Day'] = pd.to_datetime(df['Month/Day'], format = '%m/%d')
print(df)

#
df.columns.to_list() # or [*df]
