import json

data = json.load(open('Data/arkansas_county_election_results.json'))

# Get 2024 Presidential contest
contest = data['results_by_year']['2024']['presidential']['us_president']
results = contest['results']

# Check Polk County
polk = results['POLK']
print('Polk County 2024 Presidential:')
print(f"  Trump: {polk['rep_votes']:,} ({polk['rep_votes']/polk['two_party_total']*100:.1f}%)")
print(f"  Harris: {polk['dem_votes']:,} ({polk['dem_votes']/polk['two_party_total']*100:.1f}%)")
print(f"  Winner: {polk['winner']}")
print(f"  Margin: {polk['margin_pct']:.1f}%")
print(f"  Competitiveness: {polk['competitiveness']['category']}")

# Check Fulton County
fulton = results['FULTON']
print('\nFulton County 2024 Presidential:')
print(f"  Trump: {fulton['rep_votes']:,} ({fulton['rep_votes']/fulton['two_party_total']*100:.1f}%)")
print(f"  Harris: {fulton['dem_votes']:,} ({fulton['dem_votes']/fulton['two_party_total']*100:.1f}%)")
print(f"  Winner: {fulton['winner']}")
print(f"  Margin: {fulton['margin_pct']:.1f}%")
print(f"  Competitiveness: {fulton['competitiveness']['category']}")
