# ARRealignment<<<<<<< HEAD

# new-project

Arkansas Election Realignment Visualization Project

A new Node.js project scaffolded for development.

## Overview

## Getting Started

An interactive visualization tool for analyzing Arkansas county-level election results from 2002-2024. The project features a Mapbox-powered interactive map with competitiveness analysis, historical election data, and political realignment trends.

Install dependencies:

## Features```bash

npm install

- **Interactive Map**: Visualize Arkansas counties with election results```

- **Competitiveness Analysis**: 15-category classification system from "Annihilation" to "Tossup"

- **Historical Data**: Election results spanning 2002-2024Run the project:

- **Wikipedia-Style Margins**: Formatted as "R+XX.XX" or "D+XX.XX"```bash

- **Multiple Office Types**: Presidential, US Senate, Governor, Lieutenant Governor, and other statewide officesnode src/index.js

```

## Data Processing=======

# ARRealignment

The project includes a Python script that processes election data from multiple CSV formats:>>>>>>> 577aceb7f6854713ce7e787f18fbb1c7da101af2

- Converts raw election data into a comprehensive JSON format
- Calculates competitiveness metrics and margins
- Normalizes candidate names
- Filters for statewide races only (excludes US House, state legislature, local offices)

## File Structure

```
ARRealignment/
├── Data/                          # Election data files
│   ├── 2018/                     # 2018 county-level results
│   ├── 2020/                     # 2020 county-level results
│   ├── *__ar__general*.csv       # Historical election CSVs
│   ├── arkansas_county_election_results.json  # Processed comprehensive data
│   ├── county_lookup.csv         # County ID mappings
│   └── tl_2020_05_county20.geojson  # Arkansas county boundaries
├── scripts/
│   ├── create_county_election_json.py  # Data processing script
│   ├── map.js                    # Map visualization logic
│   └── common.js                 # Shared utilities
├── styles/
│   ├── main.css                  # Main styles
│   └── common.css                # Common styles
└── index.html                    # Main application page
```

## Setup

### Prerequisites
- Python 3.x with pandas library
- Modern web browser
- Mapbox API key (for map visualization)

### Data Processing
```bash
python scripts/create_county_election_json.py
```

### Running the Visualization
Simply open `index.html` in a web browser or serve it using a local web server.

## Competitiveness Categories

The project uses a 15-category classification system:

**Republican Categories:**
- Annihilation (>50% margin)
- Dominant (40-50% margin)
- Stronghold (30-40% margin)
- Safe (20-30% margin)
- Likely (15-20% margin)
- Lean (10-15% margin)
- Tilt (5-10% margin)

**Tossup:** (<5% margin)

**Democratic Categories:**
- Tilt (5-10% margin)
- Lean (10-15% margin)
- Likely (15-20% margin)
- Safe (20-30% margin)
- Stronghold (30-40% margin)
- Dominant (40-50% margin)
- Annihilation (>50% margin)

## License

MIT License - See LICENSE file for details

## Data Sources

Election data sourced from the OpenElections project and Arkansas Secretary of State.
