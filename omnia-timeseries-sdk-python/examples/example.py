from omnia_sdk import OmniaClient


client = OmniaClient()
ts = client.time_series.retrieve(id='bdc2e4aa-83de-458b-b989-675fa4e58aac')
dps = ts.data()

print(type(dps))
print(dps.count)
print(dps)


