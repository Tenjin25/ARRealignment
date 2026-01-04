import pandas as pd
from pathlib import Path
import re

# Define the TSV files and their corresponding office names
tsv_files = {
    'Data/2006 Gov.tsv': 'Governor',
    'Data/2006 Lt Gov.tsv': 'Lieutenant Governor',
    'Data/2006 Atty Gen..tsv': 'Attorney General',
    'Data/2006 SOS.tsv': 'Secretary of State',
    'Data/2006 State Auditor.tsv': 'State Auditor',
    'Data/2006 State Treasurer.tsv': 'State Treasurer',
    'Data/2006 Land Commissioner.tsv': 'Land Commissioner'
}

# Store all converted records
all_records = []

for tsv_file, office_name in tsv_files.items():
    print(f"\nProcessing {tsv_file}...")
    
    # Read the TSV file, skipping first row (office name)
    df = pd.read_csv(tsv_file, sep='\t', skiprows=1)
    
    # Get county column (first column)
    county_col = df.columns[0]
    
    # Get candidate columns (exclude Grand Totals, Registered Voters, Voter Turnout)
    metadata_cols = ['Grand Totals', 'Registered Voters', 'Voter Turnout']
    candidate_cols = [col for col in df.columns[1:] if col not in metadata_cols]
    
    print(f"  Found {len(candidate_cols)} candidates")
    
    # Process each county
    for idx, row in df.iterrows():
        county_name = row[county_col]
        
        # Skip header-like rows, totals, empty counties
        if pd.isna(county_name) or county_name == county_col or 'Total' in str(county_name) or county_name == '':
            continue
        
        # Clean county name
        county_name = county_name.strip()
        if county_name.endswith(' County'):
            county_name = county_name[:-7]  # Remove ' County' suffix
        
        # Process each candidate
        for candidate_info in candidate_cols:
            votes = row[candidate_info]
            
            # Skip if no votes or invalid
            if pd.isna(votes) or votes == 0:
                continue
            
            # Skip percentages (voter turnout)
            if isinstance(votes, str) and '%' in votes:
                continue
            
            # Convert votes to int (remove commas if present)
            if isinstance(votes, str):
                votes = int(votes.replace(',', ''))
            else:
                votes = int(votes)
            
            # Parse candidate name and party from column header
            # Format examples:
            # "Asa Hutchinson Republican"
            # "Attorney General Mike Beebe Democrat"
            # "Rod Bryan Independent"
            # "Jim Lendall Green Party"
            
            candidate_text = candidate_info.strip()
            
            # Extract party (last word or two words like "Green Party")
            party = 'Unknown'
            candidate_name = candidate_text
            
            if 'Republican' in candidate_text:
                party = 'Republican'
                candidate_name = candidate_text.replace('Republican', '').strip()
            elif 'Democrat' in candidate_text:
                party = 'Democratic'
                candidate_name = candidate_text.replace('Democrat', '').strip()
            elif 'Independent' in candidate_text:
                party = 'Independent'
                candidate_name = candidate_text.replace('Independent', '').strip()
            elif 'Green Party' in candidate_text:
                party = 'Green'
                candidate_name = candidate_text.replace('Green Party', '').strip()
            elif 'Write-In' in candidate_text or 'Write In' in candidate_text:
                party = 'Write-In'
                candidate_name = candidate_text.replace('Write-In', '').replace('Write In', '').strip()
            
            # Clean up candidate name (remove titles, extra spaces)
            candidate_name = re.sub(r'\s+', ' ', candidate_name)  # Normalize spaces
            candidate_name = candidate_name.replace('Attorney General ', '')
            candidate_name = candidate_name.replace('Secretary of State ', '')
            
            # Create record
            record = {
                'county': county_name,
                'office': office_name,
                'candidate': candidate_name,
                'party': party,
                'votes': votes
            }
            all_records.append(record)
            
    print(f"  Extracted {len([r for r in all_records if r['office'] == office_name])} records")

# Create DataFrame from all records
output_df = pd.DataFrame(all_records)

# Sort by county and office
output_df = output_df.sort_values(['county', 'office', 'votes'], ascending=[True, True, False])

# Save to CSV
output_file = 'Data/20061107__ar__general__precinct.csv'
output_df.to_csv(output_file, index=False)

print(f"\n✅ Conversion complete!")
print(f"Total records: {len(output_df)}")
print(f"Output file: {output_file}")
print(f"\nRecords by office:")
print(output_df.groupby('office').size())
print(f"\nCounties covered: {output_df['county'].nunique()}")
