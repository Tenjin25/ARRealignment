# Arkansas Election Realignment Project

An interactive visualization tool for analyzing Arkansas county-level election results from 2002-2024. This project tracks political realignment trends across all 75 Arkansas counties through multiple election cycles, featuring a Mapbox-powered interactive map with competitiveness analysis and historical comparison.

## Overview

This project provides comprehensive county-level election data for Arkansas spanning over 20 years, allowing researchers, journalists, and political enthusiasts to explore voting patterns, partisan shifts, and electoral competitiveness across the state.

## Features

- **Interactive Map**: Visualize Arkansas counties with color-coded election results
- **Competitiveness Analysis**: 15-category classification system from "Annihilation" to "Tossup"
- **Complete County Coverage**: All 75 Arkansas counties for recent election cycles (2018-2024)
- **Historical Data**: Election results spanning 2002-2024
- **Wikipedia-Style Margins**: Formatted as "R+XX.XX" or "D+XX.XX"
- **Multiple Office Types**: Presidential, US Senate, Governor, Lieutenant Governor, and other statewide offices
- **MIT Election Lab Format Support**: Integrated 2024 precinct-level data

## Data Coverage

### Election Years
- **2002**: Governor, Lt. Governor, US Senate, Statewide offices
- **2008**: President, US Senate
- **2010**: Governor, Lt. Governor, US Senate, Statewide offices
- **2012**: President
- **2014**: Governor, Lt. Governor, US Senate, Statewide offices
- **2016**: US Senate
- **2018**: Governor, Lt. Governor, Statewide offices
- **2020**: President (all 75 counties)
- **2022**: Governor, Lt. Governor, US Senate, Statewide offices (all 75 counties, including Phillips County)
- **2024**: President, State Treasurer (all 75 counties, 214,708 precinct records)

### Data Formats
The project handles three different data formats:
1. **Legacy Format** (2002-2016): Location ID-based with Contest Name
2. **OpenElections Format** (2018-2022): County/precinct with office names
3. **MIT Election Lab Format** (2024): Standardized precinct-level data

## Data Processing

The project includes a comprehensive Python script that processes election data from multiple CSV formats:

- Converts raw election data into a unified JSON format
- Calculates competitiveness metrics and margins
- Normalizes candidate names
- Identifies party affiliations from multiple sources
- Filters for statewide races only (excludes US House, state legislature, local offices)
- Aggregates precinct data to county level

## File Structure

```
ARRealignment/
├── Data/
│   ├── 2018/counties/             # 2018 precinct-level data (75 counties)
│   ├── 2020/counties/             # 2020 precinct-level data (75 counties)
│   ├── 2022/counties/             # 2022 precinct-level data (75 counties)
│   │   └── 20221108__ar__general__phillips__precinct.csv  # Phillips County (restored)
│   ├── 2024/counties/             # 2024 precinct-level data (75 counties, MIT format)
│   │   └── 20241105__ar__general__all_counties__precinct.csv
│   ├── 20*__ar__general*.csv      # Historical election CSVs (2002-2016)
│   ├── arkansas_county_election_results.json  # Processed comprehensive data
│   ├── county_lookup.csv          # County ID to name mappings
│   └── tl_2020_05_county20.geojson  # Arkansas county boundaries (TIGER/Line)
├── scripts/
│   ├── create_county_election_json.py  # Main data processing script
│   ├── download_2024_mit.py       # Download 2024 data from MIT Election Lab
│   ├── download_2022_counties.py  # Download 2022 data from OpenElections
│   ├── check_ar24.py              # Validate 2024 data structure
│   ├── map.js                     # Map visualization logic
│   └── common.js                  # Shared utilities
├── styles/
│   ├── main.css                   # Main application styles
│   └── common.css                 # Common component styles
├── index.html                     # Main application page
└── README.md                      # This file
```

## Setup

### Prerequisites
- **Python 3.x** with the following packages:
  - pandas
  - requests (for data downloads)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)
- **Mapbox API key** (optional, for enhanced map visualization)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tenjin25/ARRealignment.git
   cd ARRealignment
   ```

2. **Install Python dependencies:**
   ```bash
   pip install pandas requests
   ```

3. **Process the data (if needed):**
   ```bash
   python scripts/create_county_election_json.py
   ```
   This generates `Data/arkansas_county_election_results.json` from all CSV files.

### Running the Visualization

**Option 1: Simple File Open**
- Open `index.html` directly in your web browser

**Option 2: Local Web Server (Recommended)**
```bash
# Using Python's built-in server
python -m http.server 8000

# Or using Node.js
npx http-server
```
Then navigate to `http://localhost:8000`

## Data Sources

### Primary Sources
1. **MIT Election Data and Science Lab (MEDSL)**
   - 2024 precinct-level data
   - Standardized format with party identification
   - Source: https://github.com/MEDSL/2024-elections-official

2. **OpenElections Project**
   - 2018, 2020, 2022 county precinct data
   - Arkansas historical election data
   - Source: https://github.com/openelections/openelections-data-ar

3. **Arkansas Secretary of State**
   - Official certified results
   - County-level aggregations
   - Source: https://results.enr.clarityelections.com/AR/

### Data Updates
- **Phillips County 2022**: Manually acquired and converted to match OpenElections format
- **2024 Data**: Downloaded from MIT Election Lab on 2026-01-03

## Competitiveness Categories

The project uses a 15-category classification system based on margin percentage:

### Republican Categories (margin = Republican % - Democratic %)
- **Annihilation R**: >40% margin (Color: #67000d)
- **Dominant R**: 30-40% margin (Color: #a50f15)
- **Stronghold R**: 20-30% margin (Color: #cb181d)
- **Safe R**: 10-20% margin (Color: #ef3b2c)
- **Likely R**: 5.5-10% margin (Color: #fb6a4a)
- **Lean R**: 1-5.5% margin (Color: #fcae91)
- **Tilt R**: 0.5-1% margin (Color: #fee8c8)

### Tossup
- **Tossup**: <0.5% margin either way (Color: #f7f7f7)

### Democratic Categories (margin = Democratic % - Republican %)
- **Tilt D**: 0.5-1% margin (Color: #e1f5fe)
- **Lean D**: 1-5.5% margin (Color: #c6dbef)
- **Likely D**: 5.5-10% margin (Color: #9ecae1)
- **Safe D**: 10-20% margin (Color: #6baed6)
- **Stronghold D**: 20-30% margin (Color: #3182bd)
- **Dominant D**: 30-40% margin (Color: #08519c)
- **Annihilation D**: >40% margin (Color: #08306b)

## Known Issues & Limitations

- **2024 Data**: Only includes Presidential and State Treasurer races (other statewide races not yet in MIT Lab dataset)
- **2016 Data**: Limited to US Senate race only
- **US House Races**: Excluded due to varying district boundaries across years
- **Local Races**: Excluded to focus on statewide competitiveness
- **Early/Absentee/Election Day Breakdown**: Not available for all years

## Future Enhancements

- [ ] Add state legislative data
- [ ] Include turnout analysis
- [ ] Add demographic overlays
- [ ] Implement time-series trend analysis
- [ ] Add export functionality for charts/maps
- [ ] Include primary election data
## Contributing

Contributions are welcome! If you have:
- Additional election data sources
- Bug fixes or enhancements
- Improved visualization ideas
- Data corrections

Please open an issue or submit a pull request.

## Acknowledgments

- **MIT Election Data and Science Lab**: For comprehensive 2024 precinct-level data
- **OpenElections Project**: For standardized historical Arkansas election data
- **Arkansas Secretary of State**: For official certified results
- **Mapbox**: For mapping visualization capabilities
- **U.S. Census Bureau TIGER/Line**: For county boundary shapefiles

## Contact

Project maintained by Tenjin25
- GitHub: https://github.com/Tenjin25/ARRealignment

## License

MIT License - See LICENSE file for details

## Citation

If you use this data in research or publications, please cite:
```
Arkansas Election Realignment Project (2026)
Data sources: MIT Election Lab, OpenElections, Arkansas Secretary of State
GitHub: https://github.com/Tenjin25/ARRealignment
```
