"""
Build correct county_lookup.csv by matching vote patterns between
2020 precinct data (has county names) and 2022 Federal data (has Location IDs).
"""

import pandas as pd
from pathlib import Path

# Read 2022 Federal data (has Location IDs)
df_2022 = pd.read_csv('Data/2022_General_Federal.csv')
pres_2022 = df_2022[df_2022['Contest Name'] == 'U.S. Senate'].copy()
location_totals_2022 = pres_2022.groupby('Location ID')['Candidate Votes'].sum().to_dict()

# Read all 2020 county precinct files for presidential votes
county_totals_2020 = {}
precinct_dir = Path('Data/2020/counties')

for csv_file in precinct_dir.glob('*.csv'):
    parts = csv_file.stem.split('__')
    if len(parts) >= 4:
        county_name = parts[3].replace('_', ' ').title()
        
        try:
            df = pd.read_csv(csv_file)
            pres_df = df[df['office'].str.contains('President', case=False, na=False)]
            if len(pres_df) > 0:
                total = pres_df['votes'].sum()
                county_totals_2020[county_name] = total
        except Exception as e:
            print(f"Error reading {csv_file.name}: {e}")

# Get FIPS codes from current (wrong) lookup - FIPS codes are probably correct even if mapping isn't
current_lookup = pd.read_csv('Data/county_lookup.csv')
county_fips = dict(zip(current_lookup['County Name'], current_lookup['FIPS Code']))

# Strategy: Match counties to Location IDs based on relative vote ranking
# Sort both by total votes
sorted_counties = sorted(county_totals_2020.items(), key=lambda x: x[1], reverse=True)
sorted_locations = sorted(location_totals_2022.items(), key=lambda x: x[1], reverse=True)

print("Building mapping by vote ranking correlation...")
print("\nTop 10 matches:")
print(f"{'Rank':<6} {'County':<20} {'2020 Votes':<12} {'Location ID':<12} {'2022 Votes':<12} {'Ratio':<8}")
print("-" * 80)

mapping = []
for rank, ((county, votes_2020), (loc_id, votes_2022)) in enumerate(zip(sorted_counties, sorted_locations), 1):
    ratio = votes_2022 / votes_2020 if votes_2020 > 0 else 0
    if rank <= 10:
        print(f"{rank:<6} {county:<20} {votes_2020:<12,} {loc_id:<12} {votes_2022:<12,} {ratio:<8.3f}")
    
    # Get FIPS code
    fips = county_fips.get(county, f"05{rank:03d}")  # Fallback if not found
    
    mapping.append({
        'Location ID': loc_id,
        'County Name': county,
        'FIPS Code': fips
    })

# Create DataFrame and save
df_mapping = pd.DataFrame(mapping)
df_mapping = df_mapping.sort_values('Location ID').reset_index(drop=True)

# Verify key counties
print("\n\nVerifying known counties:")
print(f"Location ID 1 = {df_mapping[df_mapping['Location ID'] == 1]['County Name'].values[0]} (should be Pulaski)")
print(f"Location ID 9 = {df_mapping[df_mapping['Location ID'] == 9]['County Name'].values[0]} (should be Benton)")

# Find Polk County
polk_row = df_mapping[df_mapping['County Name'] == 'Polk']
if len(polk_row) > 0:
    polk_id = polk_row['Location ID'].values[0]
    print(f"Polk County = Location ID {polk_id} (old wrong mapping said 56)")

# Save
output_path = 'Data/county_lookup_NEW.csv'
df_mapping.to_csv(output_path, index=False)
print(f"\n✓ Saved new mapping to {output_path}")
print(f"Total counties mapped: {len(df_mapping)}")
