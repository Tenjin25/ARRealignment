import pandas as pd
import json
from pathlib import Path
import glob

# Load county lookup
county_lookup = pd.read_csv('Data/county_lookup.csv')
location_to_county = dict(zip(county_lookup['Location ID'], county_lookup['County Name']))

print(f"Loaded {len(location_to_county)} counties from lookup table")

# Find all CSV files in Data folder and subfolders
all_csv_files = []
data_path = Path('Data')

# Get all CSV files recursively
for csv_file in data_path.rglob('*.csv'):
    # Skip the lookup file and other non-election files
    if 'lookup' not in csv_file.name.lower() and csv_file.stat().st_size > 0:
        all_csv_files.append(csv_file)

print(f"\nFound {len(all_csv_files)} CSV files:")
for f in sorted(all_csv_files):
    print(f"  {f}")

# Known Democratic and Republican candidates for pattern matching
DEMOCRATIC_PATTERNS = [
    'harris', 'walz', 'biden', 'obama', 'kerry', 'gore',
    'james', 'natalie', 'clinton', 'hillary'
]

REPUBLICAN_PATTERNS = [
    'trump', 'vance', 'romney', 'mccain', 'bush', 
    'boozman', 'john', 'hutchinson', 'cotton'
]

# Competitiveness categorization system
CATEGORIZATION_SYSTEM = {
    "Republican": [
        {"category": "Annihilation", "min": 40, "max": float('inf'), "color": "#67000d"},
        {"category": "Dominant", "min": 30, "max": 40, "color": "#a50f15"},
        {"category": "Stronghold", "min": 20, "max": 30, "color": "#cb181d"},
        {"category": "Safe", "min": 10, "max": 20, "color": "#ef3b2c"},
        {"category": "Likely", "min": 5.5, "max": 10, "color": "#fb6a4a"},
        {"category": "Lean", "min": 1, "max": 5.5, "color": "#fcae91"},
        {"category": "Tilt", "min": 0.5, "max": 1, "color": "#fee8c8"}
    ],
    "Tossup": [
        {"category": "Tossup", "min": -0.5, "max": 0.5, "color": "#f7f7f7"}
    ],
    "Democratic": [
        {"category": "Tilt", "min": 0.5, "max": 1, "color": "#e1f5fe"},
        {"category": "Lean", "min": 1, "max": 5.5, "color": "#c6dbef"},
        {"category": "Likely", "min": 5.5, "max": 10, "color": "#9ecae1"},
        {"category": "Safe", "min": 10, "max": 20, "color": "#6baed6"},
        {"category": "Stronghold", "min": 20, "max": 30, "color": "#3182bd"},
        {"category": "Dominant", "min": 30, "max": 40, "color": "#08519c"},
        {"category": "Annihilation", "min": 40, "max": float('inf'), "color": "#08306b"}
    ]
}

def calculate_competitiveness(dem_votes, rep_votes):
    """Calculate competitiveness category and margin"""
    total = dem_votes + rep_votes
    if total == 0:
        return {
            'category': 'No Data',
            'margin': 0,
            'margin_pct': 'EVEN',
            'color': '#cccccc',
            'winner': None
        }
    
    dem_pct = (dem_votes / total) * 100
    rep_pct = (rep_votes / total) * 100
    margin_pct = abs(dem_pct - rep_pct)
    
    # Determine winner and margin direction
    if rep_pct > dem_pct:
        winner = 'Republican'
        margin = margin_pct
        margin_formatted = f"R+{margin:.2f}"
        
        # Find category
        for cat in CATEGORIZATION_SYSTEM['Republican']:
            if margin >= cat['min'] and margin < cat['max']:
                return {
                    'category': f"{cat['category']} Republican",
                    'margin': margin,
                    'margin_pct': margin_formatted,
                    'color': cat['color'],
                    'winner': 'Republican',
                    'dem_pct': round(dem_pct, 2),
                    'rep_pct': round(rep_pct, 2)
                }
    elif dem_pct > rep_pct:
        winner = 'Democratic'
        margin = margin_pct
        margin_formatted = f"D+{margin:.2f}"
        
        # Find category
        for cat in CATEGORIZATION_SYSTEM['Democratic']:
            if margin >= cat['min'] and margin < cat['max']:
                return {
                    'category': f"{cat['category']} Democratic",
                    'margin': margin,
                    'margin_pct': margin_formatted,
                    'color': cat['color'],
                    'winner': 'Democratic',
                    'dem_pct': round(dem_pct, 2),
                    'rep_pct': round(rep_pct, 2)
                }
    else:
        # Exact tie
        return {
            'category': 'Tossup',
            'margin': 0,
            'margin_pct': 'EVEN',
            'color': '#f7f7f7',
            'winner': 'Tossup',
            'dem_pct': round(dem_pct, 2),
            'rep_pct': round(rep_pct, 2)
        }
    
    # Fallback if no category matched
    return {
        'category': 'Unknown',
        'margin': margin_pct,
        'margin_pct': f"{'R' if winner == 'Republican' else 'D'}+{margin_pct:.2f}",
        'color': '#cccccc',
        'winner': winner,
        'dem_pct': round(dem_pct, 2),
        'rep_pct': round(rep_pct, 2)
    }

def identify_party(candidate_name, contest_type=''):
    """Identify party based on candidate name"""
    if pd.isna(candidate_name):
        return 'other'
    
    name_lower = str(candidate_name).lower()
    
    # Check Democratic patterns
    for pattern in DEMOCRATIC_PATTERNS:
        if pattern in name_lower:
            return 'dem'
    
    # Check Republican patterns
    for pattern in REPUBLICAN_PATTERNS:
        if pattern in name_lower:
            return 'rep'
    
    return 'other'

def categorize_office(office_name):
    """Categorize office into appropriate bucket"""
    office_lower = str(office_name).lower()
    
    # Presidential
    if 'president' in office_lower and 'vice' not in office_lower:
        return 'presidential'
    
    # US Senate
    if 'senate' in office_lower and ('u.s.' in office_lower or 'united states' in office_lower):
        return 'us_senate'
    
    # Skip US House/Congress
    if any(word in office_lower for word in ['congress', 'u.s. house', 'representative', 'district']) and 'state' not in office_lower:
        return None
    
    # Governor
    if 'governor' in office_lower and 'lieutenant' not in office_lower and 'lt' not in office_lower:
        return 'governor'
    
    # Lieutenant Governor
    if 'lieutenant governor' in office_lower or 'lt governor' in office_lower or 'lt. governor' in office_lower:
        return 'lt_governor'
    
    # Other statewide offices
    if any(word in office_lower for word in [
        'attorney general', 'secretary of state', 'treasurer', 
        'auditor', 'commissioner', 'land', 'superintendent'
    ]):
        return 'statewide'
    
    # Skip everything else (state legislature, local offices, courts, etc.)
    return None

def extract_year_from_filename(filename):
    """Extract year from filename like 20241105__ar__general.csv"""
    name = str(filename.name)
    # Handle formats like 20241105, 2024_General, etc.
    if name.startswith('20') and len(name) >= 4:
        return name[:4]
    # Handle subfolder structure
    if '2018' in str(filename):
        return '2018'
    elif '2020' in str(filename):
        return '2020'
    return None

def normalize_county_name(county_str):
    """Normalize county name for matching"""
    if pd.isna(county_str):
        return None
    county = str(county_str).strip().upper()
    # Remove " County" suffix if present
    county = county.replace(' COUNTY', '')
    return county

def normalize_candidate_name(candidate_str):
    """Normalize candidate name by removing titles and prefixes"""
    if pd.isna(candidate_str):
        return None
    
    name = str(candidate_str).strip()
    
    # Remove common titles and prefixes (case-sensitive for proper nouns)
    titles_to_remove = [
        'Senator ', 'Sen. ', 'Sen ', 
        'Congressman ', 'Congresswoman ',
        'Representative ', 'Rep. ', 'Rep ',
        'Governor ', 'Gov. ', 'Gov ',
        'President ', 'Vice President ',
        'Secretary ', 'Commissioner ',
        'Attorney General ', 'AG ',
        'Lieutenant Governor ', 'Lt. Governor ', 'Lt Governor ',
        'Treasurer ', 'Auditor '
    ]
    
    for title in titles_to_remove:
        if name.startswith(title):
            name = name[len(title):].strip()
    
    return name

def process_csv_file(csv_path, location_to_county):
    """Process a single CSV file and return structured data"""
    print(f"\nProcessing {csv_path.name}...")
    
    try:
        df = pd.read_csv(csv_path, on_bad_lines='skip', encoding='utf-8', encoding_errors='ignore')
        print(f"  Loaded {len(df)} rows")
        
        # Check if it's the aligned format (with Location ID) or old format (with county name)
        has_location_id = 'Location ID' in df.columns
        has_contest_name = 'Contest Name' in df.columns
        has_office = 'office' in df.columns
        has_county = 'county' in df.columns
        
        if not has_contest_name and not has_office:
            print(f"  ⚠️ Skipping - no contest/office column")
            return None
        
        results = {}
        
        if has_contest_name and has_location_id:
            # New format (2022, 2024)
            contests = df['Contest Name'].unique()
            print(f"  Found contests: {list(contests)[:3]}...")
            
            for contest_name in contests:
                if pd.isna(contest_name):
                    continue
                    
                contest_data = df[df['Contest Name'] == contest_name]
                
                # Determine category
                category = categorize_office(contest_name)
                if category is None:
                    continue  # Skip this contest
                
                if category not in results:
                    results[category] = {}
                
                contest_key = contest_name.replace(' ', '_').replace('.', '').replace(',', '').lower()
                
                results[category][contest_key] = {
                    'contest_name': contest_name,
                    'results': {}
                }
                
                # Process by county
                for location_id in contest_data['Location ID'].unique():
                    county_name = location_to_county.get(location_id)
                    if not county_name:
                        continue
                    
                    county_data = contest_data[contest_data['Location ID'] == location_id]
                    
                    county_result = {
                        'total_votes': int(county_data['Total Votes'].iloc[0]) if len(county_data) > 0 and pd.notna(county_data['Total Votes'].iloc[0]) else 0,
                        'dem_votes': 0,
                        'rep_votes': 0,
                        'other_votes': 0,
                        'dem_candidate': None,
                        'rep_candidate': None
                    }
                    
                    for _, row in county_data.iterrows():
                        candidate_name = row['Candidate Name']
                        votes = int(row['Candidate Votes']) if pd.notna(row['Candidate Votes']) else 0
                        
                        party = identify_party(candidate_name, contest_name)
                        
                        if party == 'dem':
                            county_result['dem_votes'] += votes
                            if not county_result['dem_candidate']:
                                county_result['dem_candidate'] = normalize_candidate_name(candidate_name)
                        elif party == 'rep':
                            county_result['rep_votes'] += votes
                            if not county_result['rep_candidate']:
                                county_result['rep_candidate'] = normalize_candidate_name(candidate_name)
                        else:
                            county_result['other_votes'] += votes
                    
                    # Add competitiveness calculation
                    comp_data = calculate_competitiveness(county_result['dem_votes'], county_result['rep_votes'])
                    county_result.update(comp_data)
                    
                    results[category][contest_key]['results'][county_name.upper()] = county_result
        
        elif has_office and has_county:
            # Old format (pre-2022) - has columns like: office, candidate, party, county, votes
            print(f"  Processing old format...")
            
            # Determine column names (they may vary)
            office_col = 'office' if 'office' in df.columns else None
            candidate_col = 'candidate' if 'candidate' in df.columns else None
            party_col = 'party' if 'party' in df.columns else ''
            county_col = 'county' if 'county' in df.columns else None
            votes_col = 'votes' if 'votes' in df.columns else None
            
            if not all([office_col, candidate_col, county_col, votes_col]):
                print(f"  ⚠️ Missing required columns")
                return None
            
            # Get unique offices
            offices = df[office_col].unique()
            print(f"  Found {len(offices)} offices")
            
            for office_name in offices:
                if pd.isna(office_name):
                    continue
                
                office_data = df[df[office_col] == office_name]
                
                # Determine category using new function
                category = categorize_office(office_name)
                if category is None:
                    continue  # Skip this office
                
                if category not in results:
                    results[category] = {}
                
                contest_key = office_name.replace(' ', '_').replace('.', '').replace(',', '').lower()
                
                results[category][contest_key] = {
                    'contest_name': office_name,
                    'results': {}
                }
                
                # Process by county
                for county_raw in office_data[county_col].unique():
                    county_norm = normalize_county_name(county_raw)
                    if not county_norm:
                        continue
                    
                    county_data = office_data[office_data[county_col] == county_raw]
                    
                    county_result = {
                        'total_votes': 0,
                        'dem_votes': 0,
                        'rep_votes': 0,
                        'other_votes': 0,
                        'dem_candidate': None,
                        'rep_candidate': None
                    }
                    
                    for _, row in county_data.iterrows():
                        candidate_name = row[candidate_col]
                        votes_raw = row[votes_col]
                        # Handle comma-separated vote counts
                        if pd.notna(votes_raw):
                            votes_str = str(votes_raw).replace(',', '')
                            try:
                                votes = int(float(votes_str))
                            except (ValueError, TypeError):
                                votes = 0
                        else:
                            votes = 0
                        
                        party_val = row[party_col] if party_col and party_col in row else ''
                        
                        county_result['total_votes'] += votes
                        
                        party = identify_party(candidate_name, party_val)
                        
                        if party == 'dem':
                            county_result['dem_votes'] += votes
                            if not county_result['dem_candidate']:
                                county_result['dem_candidate'] = normalize_candidate_name(candidate_name)
                        elif party == 'rep':
                            county_result['rep_votes'] += votes
                            if not county_result['rep_candidate']:
                                county_result['rep_candidate'] = normalize_candidate_name(candidate_name)
                        else:
                            county_result['other_votes'] += votes
                    
                    # Add competitiveness calculation
                    comp_data = calculate_competitiveness(county_result['dem_votes'], county_result['rep_votes'])
                    county_result.update(comp_data)
                    
                    results[category][contest_key]['results'][county_norm] = county_result
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error processing {csv_path.name}: {e}")
        return None

# Build results by year
results_by_year = {}

for csv_file in sorted(all_csv_files):
    year = extract_year_from_filename(csv_file)
    
    if not year:
        print(f"⚠️ Could not extract year from {csv_file.name}")
        continue
    
    if year not in results_by_year:
        results_by_year[year] = {}
    
    file_results = process_csv_file(csv_file, location_to_county)
    
    if file_results:
        # Merge results into year
        for category, contests in file_results.items():
            if category not in results_by_year[year]:
                results_by_year[year][category] = {}
            
            # Merge contests, combining data if contest appears in multiple files
            for contest_key, contest_data in contests.items():
                if contest_key not in results_by_year[year][category]:
                    results_by_year[year][category][contest_key] = contest_data
                else:
                    # Merge county results
                    for county, county_data in contest_data['results'].items():
                        if county not in results_by_year[year][category][contest_key]['results']:
                            results_by_year[year][category][contest_key]['results'][county] = county_data

# Create final JSON structure
output = {
    'results_by_year': results_by_year
}

# Save to JSON file
output_path = 'Data/arkansas_county_election_results.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Successfully created {output_path}")
print(f"\nTotal years: {len(results_by_year)}")
for year in sorted(results_by_year.keys()):
    categories = results_by_year[year]
    print(f"  {year}: {len(categories)} categories")
    for category, contests in sorted(categories.items()):
        print(f"    {category}: {len(contests)} contests")
