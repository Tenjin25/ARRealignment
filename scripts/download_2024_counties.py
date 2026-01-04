"""
Download 2024 county precinct files from OpenElections GitHub
"""
import requests
import os
from pathlib import Path

# GitHub API URL for the 2024/counties directory
api_url = "https://api.github.com/repos/openelections/openelections-data-ar/contents/2024/counties"

# Create output directory
output_dir = Path("Data/2024/counties")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Fetching file list from: {api_url}")

try:
    # Get the directory listing
    response = requests.get(api_url)
    response.raise_for_status()
    
    files = response.json()
    
    # Check if it's an error message (directory doesn't exist)
    if isinstance(files, dict) and 'message' in files:
        print(f"\n⚠ {files['message']}")
        print("\nThe 2024/counties directory may not exist yet on OpenElections.")
        print("\nAlternative options:")
        print("1. Check the main 2024 directory for available files")
        print("2. Download directly from Arkansas Secretary of State")
        print("3. Wait for OpenElections to publish county-level data")
        
        # Try the main 2024 directory instead
        print("\n" + "="*60)
        print("Checking main 2024 directory...")
        api_url_2024 = "https://api.github.com/repos/openelections/openelections-data-ar/contents/2024"
        response_2024 = requests.get(api_url_2024)
        response_2024.raise_for_status()
        files_2024 = response_2024.json()
        
        if isinstance(files_2024, list):
            print(f"\nFound {len(files_2024)} items in 2024 directory:")
            for item in files_2024:
                print(f"  - {item['name']} ({'folder' if item['type'] == 'dir' else 'file'})")
        exit(0)
    
    csv_files = [f for f in files if f['name'].endswith('.csv')]
    
    print(f"Found {len(csv_files)} CSV files to download\n")
    
    # Download each file
    for i, file_info in enumerate(csv_files, 1):
        filename = file_info['name']
        download_url = file_info['download_url']
        output_path = output_dir / filename
        
        print(f"[{i}/{len(csv_files)}] Downloading {filename}...")
        
        file_response = requests.get(download_url)
        file_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(file_response.content)
        
        print(f"  ✓ Saved to {output_path}")
    
    print(f"\n✓ Downloaded {len(csv_files)} files to {output_dir}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    print("\nIf OpenElections doesn't have 2024 data yet, you can:")
    print("1. Visit: https://results.enr.clarityelections.com/AR/115556/")
    print("2. Download county-by-county CSV exports manually")
    print("3. Check back later as OpenElections typically publishes data within months after election")
