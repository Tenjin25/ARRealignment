// --- Global status update function ---
// --- Global variables ---
var currentMode = 'county'; // Default mode

function updateStatus(msg) {
    // Try to update a status area in the DOM, fallback to console
    let el = document.getElementById('status-message');
    if (el) {
        el.textContent = msg;
    }
    console.log('[STATUS]', msg);
}

// Show county details panel when a county is clicked
// Robust global showCountyDetails function
function showCountyDetails(countyName) {
    console.log('[showCountyDetails] Called for county:', countyName);
    // Get selected contest (format: "year|contest")
    const contestValue = document.getElementById('contest').value;
    if (!contestValue) {
        updateStatus('❌ Please select a contest!');
        return;
    }
    const [year, contestType] = contestValue.split('|');
    if (!electionData || !electionData.results || !electionData.results[year]) {
        updateStatus(`❌ No data for year ${year}`);
        return;
    }
    // Find the contest key in this county that matches the normalized contestType
    const countyContests = electionData.results[year][countyName];
    if (!countyContests) {
        updateStatus(`❌ No data for county ${countyName} in ${year}`);
        // Show a friendly card in the sidebar
        const infoContent = document.getElementById('county-info-content');
        if (infoContent) {
            infoContent.innerHTML = `
                <div style="border-radius:10px;border:2px solid #e5e7ef;background:#f9fafb;box-shadow:0 2px 8px rgba(0,0,0,0.06);padding:18px 18px 10px 18px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                        <h3 style="margin:0;font-size:20px;font-weight:700;color:#1f2937;">${countyName} County</h3>
                        <span style="background:#f7f7f7;color:#64748b;padding:6px 14px;border-radius:6px;font-weight:600;font-size:14px;">No Data</span>
                    </div>
                    <div style="font-size:15px;color:#374151;margin-bottom:8px;"><b>${contestType} (${year})</b></div>
                    <div style="font-size:15px;color:#64748b;">No election data available for this county in the selected contest and year.</div>
                </div>
            `;
        }
        const detailsDiv = document.getElementById('county-details');
        if (detailsDiv) detailsDiv.style.display = 'block';
        // Optionally, scroll sidebar into view or open it if minimized
        const sidebar = document.getElementById('sidebar');
        if (sidebar && sidebar.classList.contains('minimized')) {
            toggleSidebar();
        }
        return;
    }
    const normalizedContestType = normalizeContestName(contestType);
    const foundKey = Object.keys(countyContests).find(
        key => normalizeContestName(key) === normalizedContestType
    );
    if (!foundKey) {
        updateStatus(`❌ No contest "${contestType}" found for ${countyName} in ${year}`);
        return;
    }
    const result = countyContests[foundKey];
    // --- FLMap-style county analysis layout and color scheme ---
    // Determine winner, margin, and color
    const demVotes = result.dem_votes || 0;
    const repVotes = result.rep_votes || 0;
    const totalVotes = result.total_votes || (demVotes + repVotes);
    const demPct = totalVotes ? (demVotes / totalVotes * 100) : 0;
    const repPct = totalVotes ? (repVotes / totalVotes * 100) : 0;
    const margin = (result.margin != null) ? result.margin : (demVotes - repVotes);
    const marginPct = (result.margin_pct != null) ? result.margin_pct : (totalVotes ? Math.abs(demVotes - repVotes) / totalVotes * 100 : 0);
    const winner = (margin > 0) ? 'Democratic' : (margin < 0 ? 'Republican' : 'Tie');
    const winnerShort = (margin > 0) ? 'D' : (margin < 0 ? 'R' : 'T');
    const winnerColor = (margin > 0) ? '#2563eb' : (margin < 0 ? '#dc2626' : '#64748b');
    const winnerIcon = (margin > 0) ? '🟦' : (margin < 0 ? '🟥' : '⚪');
    const marginText = (margin > 0 ? 'D+' : margin < 0 ? 'R+' : '') + marginPct.toFixed(2) + '%';
    // FLMap-style competitiveness category and color
    let competitiveness = '';
    let compColor = '#f7f7f7';
    if (marginPct >= 40) {
        competitiveness = winner === 'Democratic' ? 'Annihilation Democratic' : 'Annihilation Republican';
        compColor = winner === 'Democratic' ? '#08306b' : '#67000d';
    } else if (marginPct >= 30) {
        competitiveness = winner === 'Democratic' ? 'Dominant Democratic' : 'Dominant Republican';
        compColor = winner === 'Democratic' ? '#08519c' : '#a50f15';
    } else if (marginPct >= 20) {
        competitiveness = winner === 'Democratic' ? 'Stronghold Democratic' : 'Stronghold Republican';
        compColor = winner === 'Democratic' ? '#3182bd' : '#cb181d';
    } else if (marginPct >= 10) {
        competitiveness = winner === 'Democratic' ? 'Safe Democratic' : 'Safe Republican';
        compColor = winner === 'Democratic' ? '#6baed6' : '#ef3b2c';
    } else if (marginPct >= 5.5) {
        competitiveness = winner === 'Democratic' ? 'Likely Democratic' : 'Likely Republican';
        compColor = winner === 'Democratic' ? '#9ecae1' : '#fb6a4a';
    } else if (marginPct >= 1) {
        competitiveness = winner === 'Democratic' ? 'Lean Democratic' : 'Lean Republican';
        compColor = winner === 'Democratic' ? '#c6dbef' : '#fcae91';
    } else if (marginPct >= 0.5) {
        competitiveness = winner === 'Democratic' ? 'Tilt Democratic' : 'Tilt Republican';
        compColor = winner === 'Democratic' ? '#e1f5fe' : '#fee8c8';
    } else {
        competitiveness = 'Tossup';
        compColor = '#f7f7f7';
    }

        // FLMap-style panel layout, pixel-perfect match
        const demName = result.dem_name || 'Democratic';
        const repName = result.rep_name || 'Republican';
        let panelHtml = `
        <div style="border-radius:10px;border:2px solid #e5e7ef;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.06);padding:18px 18px 18px 18px;">
            <h3 style="margin:0 0 14px 0;font-size:20px;font-weight:700;color:#1f2937;">${countyName} County</h3>
            <div style="font-size:15px;color:#64748b;font-weight:600;margin-bottom:2px;">📊 Election Results</div>
            <div style="font-size:15px;color:#374151;margin-bottom:2px;"><b>${contestType} (${year})</b></div>
            <div style="font-size:15px;color:#374151;margin-bottom:10px;">Total Votes: <b>${totalVotes.toLocaleString()}</b></div>
            <div style="font-size:15px;color:#64748b;font-weight:600;margin-bottom:2px;">🏆 Winner</div>
            <div style="font-size:17px;font-weight:700;color:${winnerColor};margin-bottom:10px;">${winner === 'Tie' ? 'Tie' : (winner === 'Democratic' ? `${demName} (D)` : `${repName} (R)` )}</div>
            <div style="font-size:15px;color:#64748b;font-weight:600;margin-bottom:2px;">📈 Margin</div>
            <div style="font-size:17px;font-weight:700;color:${winnerColor};">${marginText}</div>
            <div style="font-size:13px;color:#64748b;margin-bottom:10px;">(${Math.abs(margin).toLocaleString()} vote margin)</div>
            <div style="font-size:15px;color:#64748b;font-weight:600;margin-bottom:2px;">🗳️ Vote Breakdown</div>
            <div style="font-size:15px;margin-bottom:0;"><span style="color:#2563eb;font-weight:600;">${demName} (D)</span></div>
            <div style="font-size:15px;margin-bottom:0;">${demPct.toFixed(2)}%</div>
            <div style="font-size:15px;margin-bottom:8px;color:#64748b;">${demVotes.toLocaleString()} votes</div>
            <div style="font-size:15px;margin-bottom:0;"><span style="color:#dc2626;font-weight:600;">${repName} (R)</span></div>
            <div style="font-size:15px;margin-bottom:0;">${repPct.toFixed(2)}%</div>
            <div style="font-size:15px;margin-bottom:10px;color:#64748b;">${repVotes.toLocaleString()} votes</div>
            <div style="font-size:15px;color:#64748b;font-weight:600;margin-bottom:2px;">🎯 Competitiveness</div>
            <div style="font-size:16px;font-weight:700;color:${compColor};">${competitiveness}</div>
        </div>
        `;
    // Show in your sidebar or details panel
    const infoContent = document.getElementById('county-info-content');
    if (infoContent) infoContent.innerHTML = panelHtml;
    const detailsDiv = document.getElementById('county-details');
    if (detailsDiv) detailsDiv.style.display = 'block';
    // Optionally, scroll sidebar into view or open it if minimized
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebar.classList.contains('minimized')) {
        toggleSidebar();
    }
    // Debug log
    console.log('[showCountyDetails] Panel created for', countyName);
}

// ...existing code...
console.log('map.js loaded - version debug1');
// Global variables

// Toggle main controls minimize/expand
function toggleMainControls() {
    const controls = document.getElementById('main-controls');
    const btn = document.getElementById('controls-minimize-btn');
    
    if (controls.classList.contains('minimized')) {
        controls.classList.remove('minimized');
        btn.textContent = '−';
    } else {
        controls.classList.add('minimized');
        btn.textContent = '+';
    }
}

// Toggle sidebar minimize/expand
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const btn = document.getElementById('sidebar-minimize-btn');
    const floatingBtn = document.getElementById('floating-expand-btn');
    const mapElement = document.getElementById('map');
    const body = document.body;
    // The rest of the function is present below and ends with a closing brace
    
    if (sidebar.classList.contains('minimized')) {
        sidebar.classList.remove('minimized');
        mapElement.classList.remove('sidebar-minimized');
        body.classList.remove('sidebar-minimized');
        btn.textContent = '−';
        floatingBtn.style.display = 'none';
        setTimeout(() => map.resize(), 300);
    } else {
        sidebar.classList.add('minimized');
        mapElement.classList.add('sidebar-minimized');
        body.classList.add('sidebar-minimized');
        btn.textContent = '+';
        floatingBtn.style.display = 'flex';
        setTimeout(() => map.resize(), 300);
    }
}

// Toggle legend minimize/expand
function toggleLegend() {
    const legend = document.getElementById('legend');
    const btn = document.getElementById('legend-minimize-btn');
    
    if (legend.classList.contains('minimized')) {
        legend.classList.remove('minimized');
        btn.textContent = '−';
    } else {
        legend.classList.add('minimized');
        btn.textContent = '+';
    }
}

// Calculate and display statewide results
function updateStatewideResults(results) {
    let demTotal = 0, repTotal = 0, totalVotes = 0;
    
    Object.values(results).forEach(result => {
        if (result.dem_votes && result.rep_votes) {
            demTotal += result.dem_votes;
            repTotal += result.rep_votes;
            totalVotes += result.dem_votes + result.rep_votes;
        }
    });
    
    if (totalVotes === 0) {
        document.getElementById('statewide-content').innerHTML = 
            '<p>No statewide data available for this contest.</p>';
        return;
    }
    const demPercent = (demTotal / totalVotes * 100);
    const repPercent = (repTotal / totalVotes * 100);
    const margin = Math.abs(demPercent - repPercent);
    const winner = demPercent > repPercent ? 'Democratic' : 'Republican';
    const winnerPercent = Math.max(demPercent, repPercent);
    const loserPercent = Math.min(demPercent, repPercent);
    
    let category;
    if (margin >= 40) {
        category = `Annihilation ${winner}`;
    } else if (margin >= 30) {
        category = `Dominant ${winner}`;
    } else if (margin >= 20) {
        category = `Stronghold ${winner}`;
    } else if (margin >= 10) {
        category = `Safe ${winner}`;
    } else if (margin >= 5.5) {
        category = `Likely ${winner}`;
    } else if (margin >= 1) {
        category = `Lean ${winner}`;
    } else if (margin >= 0.5) {
        category = `Tilt ${winner}`;
    } else {
        category = 'Tossup';
    }
    
    const marginText = `${winner} +${margin.toFixed(1)}%`;
    
    document.getElementById('statewide-content').innerHTML = `
        <div class="statewide-margin">
            <div class="margin-text" style="color: ${winner === 'Democratic' ? '#1e40af' : '#dc2626'}">${marginText}</div>
            <div class="margin-details">
                ${winnerPercent.toFixed(1)}% vs ${loserPercent.toFixed(1)}% • ${category}
            </div>
            <div class="margin-details">
                ${demTotal.toLocaleString()} D, ${repTotal.toLocaleString()} R • ${totalVotes.toLocaleString()} total votes
            </div>
        </div>
    `;
}

function setMode(mode) {
    console.log(`Setting mode to: ${mode}`);
    currentMode = mode;
    document.getElementById('county-mode').classList.toggle('active', mode === 'county');
    document.getElementById('precinct-mode').classList.toggle('active', mode === 'precinct');
    
    if (mode === 'county') {
        updateStatus(`Switched to County Results mode - shows actual county winners`);
    } else {
        updateStatus(`Switched to Precinct Patterns mode - shows dominant precinct categories`);
    }
    
    if (currentElectionResults) {
        console.log('Reapplying categories after mode change');
        const contest = document.getElementById('contest').value;
        console.log(`Current contest: ${contest}`);
        applyCategories();
    } else {
        console.log('No election results loaded yet');
    }
}

function applyCategories() {
    updateStatus('🟡 applyCategories called');
    if (!electionData || !countiesLoaded) {
        updateStatus('❌ Data not ready yet!');
        return;
    }
    if (!mapLoaded) {
        updateStatus('❌ Map not ready yet! Please wait for the map to finish loading.');
        console.warn('applyCategories: mapLoaded is false, aborting coloring.');
        return;
    }
    const contestElement = document.getElementById('contest');
    if (!contestElement) {
        updateStatus('❌ Contest dropdown not found!');
        return;
    }
    const contest = contestElement.value;
    if (!contest) {
        updateStatus('❌ Please select a contest!');
        return;
    }
    // TN: contest value format "year|contest" (e.g., "2004|President")
    const [year, contestType] = contest.split('|');
    console.log('applyCategories: contest value:', contest, 'year:', year, 'contestType:', contestType);
    updateStatus(`🔍 Loading ${year} county data for ${contestType}...`);
    if (!electionData.results[year]) {
        updateStatus(`❌ No data for year ${year}`);
        return;
    }
    // Gather results for all counties for the selected contest
    const results = {};
    let debugCount = 0;
    const normalizedContestType = normalizeContestName(contestType);
    Object.entries(electionData.results[year]).forEach(([county, contests]) => {
        if (debugCount < 5) {
            console.log(`County: ${county}, contest keys:`, Object.keys(contests));
            debugCount++;
        }
        // Find the contest key in this county that matches the normalized contestType
        const foundKey = Object.keys(contests).find(
            key => normalizeContestName(key) === normalizedContestType
        );
        if (foundKey) {
            results[county] = contests[foundKey];
        }
    });
    currentElectionResults = results;
    const countyCount = Object.keys(results).length;
    console.log(`applyCategories: Found ${countyCount} counties for ${contestType} ${year}`);
    updateStatus(`📊 Processing ${countyCount} counties for ${contestType} ${year}...`);
    updateStatewideResults(results);
    if (currentMode === 'county') {
        updateStatus('🟢 Calling applyCountyCategories...');
        applyCountyCategories(results, contestType, year);
    } else {
        updateStatus('🟢 Calling applyPrecinctCategories...');
        applyPrecinctCategories(results, contestType, year);
    }
}

// Stub functions for county/precinct categories (to avoid reference errors)
function applyCountyCategories(results, contestType, year) {
    updateStatus('🟣 applyCountyCategories called');
    // FLMap color palette for competitiveness
    const FLMAP_COLORS = {
        'Annihilation Republican': '#67000d',
        'Dominant Republican': '#a50f15',
        'Stronghold Republican': '#cb181d',
        'Safe Republican': '#ef3b2c',
        'Likely Republican': '#fb6a4a',
        'Lean Republican': '#fcae91',
        'Tilt Republican': '#fee8c8',
        'Tossup': '#f7f7f7',
        'Tilt Democratic': '#e1f5fe',
        'Lean Democratic': '#c6dbef',
        'Likely Democratic': '#9ecae1',
        'Safe Democratic': '#6baed6',
        'Stronghold Democratic': '#3182bd',
        'Dominant Democratic': '#08519c',
        'Annihilation Democratic': '#08306b'
    };
    // Get county names from the map layer source for comparison
    const layer = map.getLayer('tn-counties-fill');
    if (!layer) {
        updateStatus('❌ Map layer "tn-counties-fill" not found!');
        console.error('Map layer "tn-counties-fill" not found!');
        return;
    }
    const source = map.getSource('tn-counties');
    let geojsonCounties = [];
    if (source && source._data && source._data.features) {
        geojsonCounties = source._data.features.map(f => f.properties.NAME);
    } else {
        updateStatus('❌ Could not get county names from GeoJSON source.');
        return;
    }
    // Build a match expression: [ 'match', ['get', 'NAME'], county1, color1, county2, color2, ... , defaultColor ]
    const matchExpr = ['match', ['get', 'NAME']];
    let coloredCount = 0;
    const missingCounties = [];
    // Build a map of normalized GeoJSON county names to actual names
    const geojsonCountyMap = {};
    geojsonCounties.forEach(name => {
        geojsonCountyMap[name.toLowerCase().replace(/[^a-z]/g, '')] = name;
    });
    Object.entries(results).forEach(([county, data]) => {
        // Compute competitiveness and color using FLMap logic
        const demVotes = data.dem_votes || 0;
        const repVotes = data.rep_votes || 0;
        const totalVotes = data.total_votes || (demVotes + repVotes);
        const margin = (data.margin != null) ? data.margin : (demVotes - repVotes);
        const marginPct = (data.margin_pct != null) ? data.margin_pct : (totalVotes ? Math.abs(demVotes - repVotes) / totalVotes * 100 : 0);
        const winner = (margin > 0) ? 'Democratic' : (margin < 0 ? 'Republican' : 'Tie');
        let competitiveness = '';
        if (marginPct >= 40) {
            competitiveness = winner === 'Democratic' ? 'Annihilation Democratic' : 'Annihilation Republican';
        } else if (marginPct >= 30) {
            competitiveness = winner === 'Democratic' ? 'Dominant Democratic' : 'Dominant Republican';
        } else if (marginPct >= 20) {
            competitiveness = winner === 'Democratic' ? 'Stronghold Democratic' : 'Stronghold Republican';
        } else if (marginPct >= 10) {
            competitiveness = winner === 'Democratic' ? 'Safe Democratic' : 'Safe Republican';
        } else if (marginPct >= 5.5) {
            competitiveness = winner === 'Democratic' ? 'Likely Democratic' : 'Likely Republican';
        } else if (marginPct >= 1) {
            competitiveness = winner === 'Democratic' ? 'Lean Democratic' : 'Lean Republican';
        } else if (marginPct >= 0.5) {
            competitiveness = winner === 'Democratic' ? 'Tilt Democratic' : 'Tilt Republican';
        } else {
            competitiveness = 'Tossup';
        }
        const color = FLMAP_COLORS[competitiveness] || '#e0e7ef';
        const normCounty = county.toLowerCase().replace(/[^a-z]/g, '');
        const geojsonName = geojsonCountyMap[normCounty];
        if (geojsonName) {
            matchExpr.push(geojsonName, color);
            coloredCount++;
        } else {
            matchExpr.push(county, color); // fallback, may not match
            missingCounties.push(county);
        }
    });
    matchExpr.push('#e0e7ef'); // default color
    map.setPaintProperty('tn-counties-fill', 'fill-color', matchExpr);
    map.setPaintProperty('tn-counties-fill', 'fill-opacity', 0.38);
    // Move the fill layer to the top to ensure it's visible
    try {
        map.moveLayer('tn-counties-fill');
    } catch (e) {
        console.warn('Could not move tn-counties-fill layer:', e);
    }
    updateStatus(`🗺️ Coloring ${coloredCount} of ${geojsonCounties.length} counties for ${contestType} ${year}`);
    if (missingCounties.length > 0) {
        console.warn('Counties in results but not in GeoJSON:', missingCounties);
    }
}
function applyPrecinctCategories(results, contestType, year) {
    // TODO: Implement precinct category logic
    console.log('applyPrecinctCategories called', results, contestType, year);
}

// TN: Normalize contest name for consistent matching
function normalizeContestName(name) {
    return name.toLowerCase().replace(/[^a-z]/g, '');
}


// TN: Populate contest dropdown from JSON structure
function populateContestDropdown() {
    try {
        console.log('ENTERED populateContestDropdown');
        const contestSelect = document.getElementById('contest');
        if (!electionData || !electionData.results) {
            console.log('Election data or results missing:', electionData);
            return;
        }
        if (!contestSelect) {
            updateStatus('❌ Contest dropdown element with id "contest" not found in DOM!');
            return;
        }
        let options = '<option value="">Select a Contest...</option>';
        // Collect all unique contest names from all counties in all years, as year|contest
        const allContests = new Set();
        Object.entries(electionData.results).forEach(([year, counties]) => {
            Object.keys(counties).forEach(county => {
                Object.keys(counties[county]).forEach(contest => {
                    allContests.add(`${year}|${contest}`);
                });
            });
        });
        const allContestsArr = Array.from(allContests);
        allContestsArr.sort();
        allContestsArr.forEach(contestKey => {
            const splitKey = contestKey.split('|');
            console.log('contestKey:', contestKey, 'split:', splitKey);
            const [year, contest] = splitKey;
            options += `<option value="${contestKey}">${year} - ${contest}</option>`;
        });
        console.log('Final options HTML:', options);
    contestSelect.innerHTML = options;
    console.log('Dropdown now has', contestSelect.options.length, 'options.');
    // Add event listener to trigger applyCategories on change
    contestSelect.removeEventListener('change', applyCategories); // Remove if already attached
    contestSelect.addEventListener('change', applyCategories);
    } catch (err) {
        console.error('Error in populateContestDropdown:', err);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Ensure Mapbox GL JS is loaded
    if (typeof mapboxgl === 'undefined') {
        updateStatus('❌ Mapbox GL JS library not loaded!');
        return;
    }
    // Ensure map container exists
    if (!document.getElementById('map')) {
        updateStatus('❌ Map container with id "map" not found!');
        return;
    }
    // Initialize map
    mapboxgl.accessToken = 'pk.eyJ1Ijoic2hhbWFyZGF2aXMiLCJhIjoiY21kcW8yeDB2MDhvbTJzb29qeGp1aDZmZCJ9.Zw_i6U-dL7_bEKRHTUh7yg';
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v11',
        center: [-86.5, 35.8], // Centered on Tennessee
        zoom: 6.5
    });

    map.on('load', function() {
        fetch('VTDs/TN_counties.geojson')
            .then(response => response.json())
            .then(geojson => {
                map.addSource('tn-counties', {
                    type: 'geojson',
                    data: geojson
                });
                map.addLayer({
                    id: 'tn-counties-fill',
                    type: 'fill',
                    source: 'tn-counties',
                    layout: {},
                    paint: {
                        'fill-color': '#e0e7ef',
                        'fill-opacity': 0.5
                    }
                });
                map.addLayer({
                    id: 'tn-counties-outline',
                    type: 'line',
                    source: 'tn-counties',
                    layout: {},
                    paint: {
                        'line-color': '#333',
                        'line-width': 1
                    }
                });
                map.addLayer({
                    id: 'tn-county-labels',
                    type: 'symbol',
                    source: 'tn-counties',
                    layout: {
                        'text-field': ['get', 'NAME'],
                        'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                        'text-size': 12,
                        'text-anchor': 'center'
                    },
                    paint: {
                        'text-color': '#222',
                        'text-halo-color': '#fff',
                        'text-halo-width': 1
                    }
                });
                // Enable county click toggle
    map.on('click', 'tn-counties-fill', function(e) {
        const countyName = e.features[0].properties.NAME;
        console.log('[Map Click] County clicked:', countyName);
        updateStatus('Clicked county: ' + countyName);
        if (countyName) {
            if (window.showCountyDetails) {
                window.showCountyDetails(countyName);
            } else {
                console.warn('window.showCountyDetails is not defined!');
            }
        }
    });
    window.showCountyDetails = showCountyDetails;
    countiesLoaded = true;
    mapLoaded = true; // Set mapLoaded to true after all layers are added
    updateStatus('✅ TN counties loaded.');
});
        // Now fetch election data and populate dropdown
        fetch('Election_Data/standardized/tn_legacy_comprehensive_by_county_with_party_updated.json')
            .then(response => response.json())
            .then(json => {
                electionData = json;
                countiesLoaded = true;
                // Debug: log structure of loaded election data
                console.log('Loaded electionData:', electionData);
                if (electionData && electionData.results) {
                    console.log('Available years:', Object.keys(electionData.results));
                    const firstYear = Object.keys(electionData.results)[0];
                    if (firstYear) {
                        console.log('First year:', firstYear);
                        console.log('Available counties in first year:', Object.keys(electionData.results[firstYear]));
                        const firstCounty = Object.keys(electionData.results[firstYear])[0];
                        if (firstCounty) {
                            console.log('First county:', firstCounty);
                            console.log('Contests in first county:', Object.keys(electionData.results[firstYear][firstCounty]));
                        }
                    }
                } else {
                    console.warn('No results key in electionData');
                }
                console.log('About to call populateContestDropdown:', typeof populateContestDropdown);
                console.log('Calling populateContestDropdown now');
                // Ensure dropdown exists before calling
                if (document.getElementById('contest')) {
                    populateContestDropdown();
                } else {
                    console.error('Dropdown element with id "contest" not found in DOM at time of population!');
                }
                updateStatus('✅ TN election data loaded.');
            });
    });
});
