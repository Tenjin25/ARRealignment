"""
Download 2022 county precinct files from OpenElections GitHub
"""
import requests
import os
from pathlib import Path

# GitHub API URL for the 2022/counties directory
api_url = "https://api.github.com/repos/openelections/openelections-data-ar/contents/2022/counties"

# Create output directory
output_dir = Path("Data/2022/counties")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Fetching file list from: {api_url}")

# Get the directory listing
response = requests.get(api_url)
response.raise_for_status()

files = response.json()
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
