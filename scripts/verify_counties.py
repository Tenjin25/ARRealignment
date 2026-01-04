import json

data = json.load(open('Data/arkansas_county_election_results.json'))

# Check structure
pres_2024 = data['results_by_year']['2024']['presidential']
print(f"2024 Presidential contests: {len(pres_2024)}")
print(f"Keys: {list(pres_2024.keys())}")

# Get the first (and only) key
contest_key = list(pres_2024.keys())[0]
contest = pres_2024[contest_key]
print(f"\nContest: {contest['contest_name']}")

polk = next(c for c in contest['results'] if c['county'] == 'Polk')
print('\nPolk County 2024 Presidential:')
print(f"  Trump: {polk['rep_votes']:,} ({polk['rep_pct']:.1f}%)")
print(f"  Harris: {polk['dem_votes']:,} ({polk['dem_pct']:.1f}%)")
print(f"  Competitiveness: {polk['competitiveness']}")

fulton = next(c for c in contest['results'] if c['county'] == 'Fulton')
print('\nFulton County 2024 Presidential:')
print(f"  Trump: {fulton['rep_votes']:,} ({fulton['rep_pct']:.1f}%)")
print(f"  Harris: {fulton['dem_votes']:,} ({fulton['dem_pct']:.1f}%)")
print(f"  Competitiveness: {fulton['competitiveness']}")
