import json

data = json.load(open('Data/arkansas_county_election_results.json'))
results = data['results_by_year']['2020']['presidential']['us_president']['results']

# Arkansas Delta counties (eastern Arkansas, historically Democratic due to Black population)
delta_counties = [
    'PHILLIPS',    # Helena - majority Black
    'LEE',         # Marianna - majority Black
    'ST FRANCIS',  # Forrest City - heavily Black
    'CRITTENDEN',  # West Memphis - mixed
    'DESHA',       # Southeast Delta
    'CHICOT',      # Lake Village - majority Black
    'JEFFERSON',   # Pine Bluff - majority Black, largest city in Delta
    'MONROE',      # Clarendon
    'CROSS',       # Wynne
    'WOODRUFF',    # Augusta
]

print("Arkansas Delta Counties - 2020 Presidential Results:")
print("="*80)
print(f"{'County':<15} {'Trump':<12} {'Biden':<12} {'Winner':<8} {'Margin':<10} {'Category':<15}")
print("-"*80)

for county in delta_counties:
    if county in results:
        r = results[county]
        trump_pct = r['rep_votes']/r['two_party_total']*100
        biden_pct = r['dem_votes']/r['two_party_total']*100
        print(f"{county:<15} {trump_pct:>5.1f}% ({r['rep_votes']:>5}) {biden_pct:>5.1f}% ({r['dem_votes']:>5}) {r['winner']:<8} {r['margin_pct']:>6.1f}% {r['competitiveness']['category']:<15}")

print("\n\nOther notable counties:")
print("-"*80)
other_counties = ['PULASKI', 'WASHINGTON', 'BENTON', 'SALINE']
for county in other_counties:
    if county in results:
        r = results[county]
        trump_pct = r['rep_votes']/r['two_party_total']*100
        harris_pct = r['dem_votes']/r['two_party_total']*100
        print(f"{county:<15} {trump_pct:>5.1f}% ({r['rep_votes']:>5}) {harris_pct:>5.1f}% ({r['dem_votes']:>5}) {r['winner']:<8} {r['margin_pct']:>6.1f}% {r['competitiveness']['category']:<15}")
