from omnia_sdk import OmniaClient


client = OmniaClient()

tsl = client.time_series.retrieve_multiple(ids=['bdc2e4aa-83de-458b-b989-675fa4e58aac',
                                               'b51e1723-c25b-4847-825e-2da26409ff3c'])

print(type(tsl))
print(tsl.count)


