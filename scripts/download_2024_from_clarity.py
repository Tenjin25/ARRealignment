"""
Download 2024 county precinct files from Arkansas Secretary of State
Uses the Clarity Elections API
"""
import requests
import csv
from pathlib import Path
import time

# Arkansas 2024 General Election ID
# Try both Clarity and Total Results systems
ELECTION_ID_CLARITY = "115556"
ELECTION_ID_TOTAL_RESULTS = "1846"
BASE_URL_CLARITY = f"https://results.enr.clarityelections.com/AR/{ELECTION_ID_CLARITY}"
BASE_URL_TOTAL_RESULTS = "https://enr.totalresults.com/arkansas/api"
BASE_URL = BASE_URL_TOTAL_RESULTS  # Try Total Results first based on user's URL

# Arkansas counties (75 total)
COUNTIES = [
    "Arkansas", "Ashley", "Baxter", "Benton", "Boone", "Bradley", "Calhoun", "Carroll",
    "Chicot", "Clark", "Clay", "Cleburne", "Cleveland", "Columbia", "Conway", "Craighead",
    "Crawford", "Crittenden", "Cross", "Dallas", "Desha", "Drew", "Faulkner", "Franklin",
    "Fulton", "Garland", "Grant", "Greene", "Hempstead", "Hot Spring", "Howard", "Independence",
    "Izard", "Jackson", "Jefferson", "Johnson", "Lafayette", "Lawrence", "Lee", "Lincoln",
    "Little River", "Logan", "Lonoke", "Madison", "Marion", "Miller", "Mississippi", "Monroe",
    "Montgomery", "Nevada", "Newton", "Ouachita", "Perry", "Phillips", "Pike", "Poinsett",
    "Polk", "Pope", "Prairie", "Pulaski", "Randolph", "Saline", "Scott", "Searcy",
    "Sebastian", "Sevier", "Sharp", "St. Francis", "Stone", "Union", "Van Buren",
    "Washington", "White", "Woodruff", "Yell"
]

# Create output directory
output_dir = Path("Data/2024/counties")
output_dir.mkdir(parents=True, exist_ok=True)

print("Arkansas 2024 General Election - County Data Downloader")
print("=" * 60)
print(f"Election ID (Total Results): {ELECTION_ID_TOTAL_RESULTS}")
print(f"Election ID (Clarity): {ELECTION_ID_CLARITY}")
print(f"Output directory: {output_dir}")
print(f"Counties to process: {len(COUNTIES)}")
print()

# First, let's get the contest/office information
print("Fetching election summary from Total Results...")
try:
    summary_url = f"{BASE_URL_TOTAL_RESULTS}/election/{ELECTION_ID_TOTAL_RESULTS}"
    response = requests.get(summary_url, timeout=10)
    response.raise_for_status()
    print(f"✓ Total Results API accessible: Status {response.status_code}")
    print()
except Exception as e:
    print(f"⚠ Total Results not accessible: {e}")
    print("Trying Clarity Elections...\n")
    try:
        summary_url = f"{BASE_URL_CLARITY}/json/en/summary.json"
        response = requests.get(summary_url, timeout=10)
        response.raise_for_status()
        summary = response.json()
        print(f"✓ Clarity Elections: {summary.get('ElectionName', 'Unknown')}")
        print()
    except Exception as e2:
        print(f"⚠ Could not access Clarity either: {e2}")
        print("Will try individual county downloads...\n")

# Try to download precinct-level data for each county
successful = 0
failed = []

for i, county in enumerate(COUNTIES, 1):
    county_safe = county.lower().replace(" ", "_")
    output_file = output_dir / f"20241105__ar__general__{county_safe}__precinct.csv"
    
    print(f"[{i}/{len(COUNTIES)}] {county} County...")
    
    try:
        # Try different URL patterns that Clarity Elections might use
        # Pattern 1: Direct JSON endpoint
        json_url = f"{BASE_URL}/json/{county.replace(' ', '%20')}.json"
        
        response = requests.get(json_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Downloaded JSON data")
            
            # TODO: Parse JSON and convert to CSV format
            # For now, save the raw JSON
            json_output = output_dir / f"{county_safe}_raw.json"
            with open(json_output, 'w') as f:
                import json
                json.dump(data, f, indent=2)
            print(f"  ✓ Saved raw JSON to {json_output}")
            successful += 1
        else:
            failed.append(county)
            print(f"  ✗ HTTP {response.status_code}")
        
        # Be nice to the server
        time.sleep(0.5)
        
    except Exception as e:
        failed.append(county)
        print(f"  ✗ Error: {e}")

print()
print("=" * 60)
print(f"Download complete: {successful} succeeded, {len(failed)} failed")
if failed:
    print(f"Failed counties: {', '.join(failed)}")

print()
print("NOTES:")
print("- Clarity Elections data structure may require additional parsing")
print("- You may need to manually export CSVs from the web interface")
print("- Alternative: https://results.enr.clarityelections.com/AR/115556/")
print("  Click on each county and use the 'Reports' > 'Detail CSV' option")
