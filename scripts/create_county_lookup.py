"""
Create accurate county_lookup.csv by matching Location IDs from 2024 data
with county names from 2020 precinct-level data based on vote totals.
"""

import pandas as pd
from pathlib import Path

# Read 2024 Federal data (has Location IDs)
df_2024 = pd.read_csv('Data/2024_General_Federal.csv')

# Filter to US President contest
pres_2024 = df_2024[df_2024['Contest Name'] == 'U.S. President'].copy()

# Aggregate total votes by Location ID
location_totals = pres_2024.groupby('Location ID')['Candidate Votes'].sum().reset_index()
location_totals.columns = ['Location ID', 'Total Votes']

print("Location IDs with total votes:")
print(location_totals.head(10))
print(f"\nTotal locations: {len(location_totals)}")

# Read all 2020 county precinct files and aggregate PRESIDENTIAL votes only
county_totals_2020 = {}
precinct_dir = Path('Data/2020/counties')

for csv_file in precinct_dir.glob('*.csv'):
    # Extract county name from filename
    # Format: 20201103__ar__general__polk__precinct.csv
    parts = csv_file.stem.split('__')
    if len(parts) >= 4:
        county_name = parts[3].replace('_', ' ').title()
        
        # Read and filter to presidential race
        try:
            df = pd.read_csv(csv_file)
            # Filter to presidential race
            pres_df = df[df['office'].str.contains('President', case=False, na=False)]
            if len(pres_df) > 0 and 'votes' in pres_df.columns:
                total = pres_df['votes'].sum()
                county_totals_2020[county_name] = total
        except Exception as e:
            print(f"Error reading {csv_file.name}: {e}")

print(f"\n2020 counties found: {len(county_totals_2020)}")
print("Sample 2020 Presidential totals:")
for county, total in list(sorted(county_totals_2020.items()))[:10]:
    print(f"  {county}: {total:,}")

# Check if we have a statewide 2020 file with Location IDs
# If not, we'll use 2022 data instead (closer to 2020 than 2024)
df_2022 = pd.read_csv('Data/2022_General_Federal.csv')
pres_2022 = df_2022[df_2022['Contest Name'] == 'U.S. Senate'].copy()
location_totals_2022 = pres_2022.groupby('Location ID')['Candidate Votes'].sum().reset_index()
location_totals_2022.columns = ['Location ID', 'Total Votes 2022']

print("\n2022 Location ID totals (U.S. Senate):")
print(location_totals_2022.head(10))

# Now let's try to match. We know:
# - Pulaski County (Little Rock, biggest county) should have highest total
# - Polk County was showing wrong data - let's find its real Location ID

# Find largest totals in both datasets
print("\nTop 5 counties by votes in 2020 (Presidential):")
sorted_2020 = sorted(county_totals_2020.items(), key=lambda x: x[1], reverse=True)
for county, votes in sorted_2020[:5]:
    print(f"  {county}: {votes:,}")

print("\nTop 5 Location IDs by votes in 2022 (Senate):")
top_2022 = location_totals_2022.nlargest(5, 'Total Votes 2022')
print(top_2022)

# Check Polk County specifically
print(f"\nPolk County 2020 Presidential votes: {county_totals_2020.get('Polk', 'NOT FOUND'):,}")

# Let's check what Location ID the CURRENT (wrong) lookup says is Polk
current_lookup = pd.read_csv('Data/county_lookup.csv')
polk_wrong_id = current_lookup[current_lookup['County Name'] == 'Polk']['Location ID'].values[0]
print(f"\nCurrent (WRONG) lookup says Polk = Location ID {polk_wrong_id}")
print(f"Location ID {polk_wrong_id} 2024 Presidential total: {location_totals[location_totals['Location ID'] == polk_wrong_id]['Total Votes'].values[0]:,}")
print(f"Location ID {polk_wrong_id} 2022 Senate total: {location_totals_2022[location_totals_2022['Location ID'] == polk_wrong_id]['Total Votes 2022'].values[0]:,}")
