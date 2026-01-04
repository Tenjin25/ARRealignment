# Arkansas County Location ID Mapping Issue

## Summary
The Arkansas Secretary of State election CSVs (2022-2024) use "Location ID" numbers (1-75) instead of county names. We need the official mapping between Location IDs and County Names to correctly analyze county-level election results.

## Problem
Without the correct mapping:
- Delta counties (Phillips, Lee, Jefferson, St. Francis, Chicot) which are majority-Black and should be Democratic are showing as heavily Republican
- Cannot trust any county-level analysis or visualization

## What We Know
- Location ID 1 = Pulaski County (verified - shows 61% Harris, matches Little Rock demographics)
- Location ID 9 appears to be Benton County (based on vote totals)
- Location IDs do NOT follow:
  - Alphabetical order by county name
  - FIPS code order
  - Population order

## Known Democratic Counties (for verification)
These Arkansas Delta counties should show Harris/Democratic majorities or near-majorities in 2024:
- Phillips County (Helena) - 53% Black population
- Lee County (Marianna) - 47% Black  
- Jefferson County (Pine Bluff) - 45% Black
- St. Francis County (Forrest City) - 55% Black
- Chicot County (Lake Village) - Majority Black

In the 2024 Presidential race, only 6 Location IDs showed Harris > 45%:
- Location ID 52, 10, 53, 25, 60, 46

## Request
Could you please provide the official mapping between Location IDs (1-75) and County Names as used in the Arkansas Secretary of State CSV downloads for 2022 and 2024 elections?

Alternative: If there's documentation about the Location ID system in the Clarity/TotalResults election reporting system, a link to that would be helpful.

## Contact
Elections Email: electionsemail@sos.arkansas.gov
Phone: 501-682-1010

## Files Analyzed
- Data/2024_General_Federal.csv
- Data/2022_General_Statewide.csv  
- Data/2022_General_Federal.csv

These CSVs all use Location IDs but do not include county names.
