import pandas as pd

lookup = pd.read_csv('Data/county_lookup.csv')

print('Delta county Location IDs from current mapping:')
delta_counties = ['Phillips', 'Lee', 'St Francis', 'Jefferson', 'Chicot', 'Desha', 'Crittenden']

for county in delta_counties:
    row = lookup[lookup['County Name'] == county]
    if len(row) > 0:
        print(f'{county:<15} Location ID: {row["Location ID"].values[0]}')
    else:
        print(f'{county:<15} NOT FOUND')
