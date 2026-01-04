import json

with open('Data/arkansas_county_election_results.json') as f:
    data = json.load(f)

gov = data['results_by_year']['2022']['governor']['governor']

print(f"2022 Governor - Total counties: {len(gov)}")
print(f"Sanders counties: {sum(1 for c in gov.values() if c.get('winner_party') == 'Republican')}")
print(f"Jones counties: {sum(1 for c in gov.values() if c.get('winner_party') == 'Democratic')}")

print(f"\nDelta counties:")
for county in ['Jefferson', 'Lee', 'St. Francis', 'Phillips']:
    if county in gov:
        print(f"  {county}: {gov[county]['winner_party']} ({gov[county]['democratic_pct']:.1f}% Dem)")
    else:
        print(f"  {county}: MISSING")

print(f"\nPolk County (should be Republican):")
if 'Polk' in gov:
    print(f"  Polk: {gov['Polk']['winner_party']} ({gov['Polk']['democratic_pct']:.1f}% Dem)")
else:
    print(f"  Polk: MISSING")

print(f"\nPulaski County (Little Rock - should be Democratic):")
if 'Pulaski' in gov:
    print(f"  Pulaski: {gov['Pulaski']['winner_party']} ({gov['Pulaski']['democratic_pct']:.1f}% Dem)")
