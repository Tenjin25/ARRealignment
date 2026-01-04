"""
Download 2024 Arkansas election data from MIT Election Lab
Source: https://github.com/MEDSL/2024-elections-official
Arkansas was added: 2025-11-07
"""
import requests
from pathlib import Path
import pandas as pd

# MIT Election Lab GitHub repository - try different paths
GITHUB_RAW_URL = "https://raw.githubusercontent.com/MEDSL/2024-elections-official/main"
GITHUB_RELEASE_URL = "https://github.com/MEDSL/2024-elections-official/releases/latest/download"

# Files to download - try different naming patterns
FILES_TO_DOWNLOAD = [
    ("AR.csv", GITHUB_RAW_URL),  # Try direct from main branch
    ("arkansas.csv", GITHUB_RAW_URL),  # Try lowercase
    ("ar_gen_2024.csv", GITHUB_RAW_URL),  # Try with year
    ("2024-ar-precinct-general.csv", GITHUB_RELEASE_URL),  # Try release
]

# Create output directory
output_dir = Path("Data/2024/counties")
output_dir.mkdir(parents=True, exist_ok=True)

print("Downloading 2024 Arkansas Election Data from MIT Election Lab")
print("=" * 60)
print(f"Source: {GITHUB_RAW_URL}")
print(f"Output: {output_dir}")
print()

for filename, base_url in FILES_TO_DOWNLOAD:
    url = f"{base_url}/{filename}"
    output_path = output_dir / f"MIT_{filename}"
    
    print(f"Downloading {filename}...")
    print(f"  URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✓ Downloaded: {len(response.content):,} bytes")
        print(f"  ✓ Saved to: {output_path}")
        
        # Load and preview the data
        df = pd.read_csv(output_path)
        print(f"  ✓ Rows: {len(df):,}")
        print(f"  ✓ Columns: {', '.join(df.columns.tolist())}")
        print()
        
        # Show sample data
        print("  Sample data (first 5 rows):")
        print(df.head().to_string(index=False))
        print()
        
        # Show unique offices
        if 'office' in df.columns:
            print(f"  Offices in dataset: {', '.join(df['office'].unique())}")
            print()
        
        # Show unique counties
        if 'county_name' in df.columns:
            unique_counties = df['county_name'].unique()
            print(f"  Counties: {len(unique_counties)}")
            print(f"  County list: {', '.join(sorted(unique_counties))}")
            print()
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"  ✗ File not found (404)")
            print(f"  Note: Arkansas data may not be available yet or filename may differ")
            print(f"  Check: https://github.com/MEDSL/2024-elections-official")
        else:
            print(f"  ✗ HTTP Error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()

print("=" * 60)
print("Download complete!")
print()
print("NEXT STEPS:")
print("1. Review the downloaded data in:", output_dir)
print("2. Convert MIT format to match your existing 2018/2020/2022 format")
print("3. Re-run create_county_election_json.py to include 2024 data")
