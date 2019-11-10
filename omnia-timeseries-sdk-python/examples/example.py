from omnia_sdk import OmniaClient

client = OmniaClient()
ts = client.time_series.retrieve(id='bdc2e4aa-83de-458b-b989-675fa4e58aac')

df = ts.to_pandas()
print(df)


tsl = client.time_series.retrieve_multiple(
    ids=['bdc2e4aa-83de-458b-b989-675fa4e58aac',
         '16b569a6-e31a-4da6-b4f8-0b8354c33d2b',
         'd6f5e549-5766-4275-8024-f01084771dc1'
         ])
df = tsl.to_pandas()
print(df)


ts.plot(limit=100)