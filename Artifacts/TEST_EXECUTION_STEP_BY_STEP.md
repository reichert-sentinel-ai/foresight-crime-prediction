# Step-by-Step Test Execution Guide

## Prerequisites

Before starting, ensure:
- Backend server is running on `http://localhost:8000`
- Frontend server is running on `http://localhost:5173`
- Browser DevTools open (F12) with Console and Network tabs visible

---

## TEST 1: Backend Endpoint Returns Valid Heatmap Data

### Step 1.1: Test Basic Endpoint

**Action:**
```bash
# Open terminal and run:
curl http://localhost:8000/api/crime-map/hotspots
```

**Expected Output:**
```json
{
  "hotspots": [...],
  "prediction_date": "2024-01-15",
  "model_version": "v2.3.1",
  "coverage_area": {...},
  "grid_resolution": "2km",
  "total_predicted_incidents": 123
}
```

**Check:**
- ✅ Status code should be 200 (check HTTP status)
- ✅ Response is valid JSON (no parse errors)
- ✅ Response contains all required fields

---

### Step 1.2: Verify Response Structure

**Action:**
```bash
# Run with JSON formatting:
curl http://localhost:8000/api/crime-map/hotspots | python -m json.tool
```

**Check each field:**
- ✅ `hotspots` exists and is an array
- ✅ `prediction_date` is a string (YYYY-MM-DD format)
- ✅ `model_version` is present
- ✅ `coverage_area` is an object with `center` and `radius_km`
- ✅ `grid_resolution` is present
- ✅ `total_predicted_incidents` is a number

**Expected:**
```json
{
  "hotspots": [
    {
      "lat": 41.8781,
      "lng": -87.6298,
      "intensity": 0.85,
      ...
    }
  ],
  ...
}
```

---

### Step 1.3: Validate Hotspot Fields

**Action:**
```bash
# Extract first hotspot to inspect:
curl -s http://localhost:8000/api/crime-map/hotspots | python -m json.tool | head -30
```

**Check the first hotspot has:**
- ✅ `lat` - float between 41.0 and 42.0 (Chicago area)
- ✅ `lng` - float between -88.0 and -87.0 (Chicago area)
- ✅ `intensity` - float between 0.0 and 1.0
- ✅ `crime_type` - string
- ✅ `predicted_incidents` - integer
- ✅ `confidence` - float between 0.0 and 1.0
- ✅ `grid_id` - string (format: "grid_X_Y")
- ✅ `risk_level` - one of: "low", "medium", "high", "critical"

**Visual Check:**
```bash
# Quick validation script:
curl -s http://localhost:8000/api/crime-map/hotspots | python3 -c "
import json, sys
data = json.load(sys.stdin)
hotspot = data['hotspots'][0]
print(f'lat: {hotspot[\"lat\"]} (valid: {41.0 <= hotspot[\"lat\"] <= 42.0})')
print(f'lng: {hotspot[\"lng\"]} (valid: {-88.0 <= hotspot[\"lng\"] <= -87.0})')
print(f'intensity: {hotspot[\"intensity\"]} (valid: {0 <= hotspot[\"intensity\"] <= 1})')
print(f'risk_level: {hotspot[\"risk_level\"]} (valid: {hotspot[\"risk_level\"] in [\"low\", \"medium\", \"high\", \"critical\"]})')
"
```

---

### Step 1.4: Test Query Parameters

**Test City Parameter:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?city=chicago"
```

**Check:**
- ✅ Response has `coverage_area.center.lat` = 41.8781
- ✅ Response has `coverage_area.center.lng` = -87.6298

**Test Crime Type Parameter:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?crime_type=theft"
```

**Check:**
- ✅ All hotspots have `crime_type` = "theft"
- ✅ Response is valid

**Test Time Window Parameter:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?time_window=24h"
```

**Check:**
- ✅ Response is valid
- ✅ Data structure unchanged

**Test Date Parameter:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?date=2024-01-15"
```

**Check:**
- ✅ `prediction_date` = "2024-01-15"
- ✅ Response is valid

**Test Multiple Parameters:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?city=chicago&crime_type=theft&time_window=24h"
```

**Check:**
- ✅ All parameters applied
- ✅ Response is valid

---

### Step 1.5: Check Response Time

**Action:**
```bash
# Measure response time:
time curl -s http://localhost:8000/api/crime-map/hotspots > /dev/null
```

**Check:**
- ✅ Response time < 500ms (0.5 seconds)
- ✅ Acceptable for real-time updates

**Alternative (using curl with timing):**
```bash
curl -w "@-" -o /dev/null -s http://localhost:8000/api/crime-map/hotspots <<'EOF'
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_total:  %{time_total}\n
EOF
```

**Expected:** `time_total` should be < 0.5

---

## TEST 2: Map Renders with Correct Center Coordinates

### Step 2.1: Open Crime Map Page

**Action:**
1. Open browser
2. Navigate to: `http://localhost:5173/crime-map`
3. Wait for page to load

**Check:**
- ✅ Page loads without errors
- ✅ No 404 errors in console
- ✅ No network errors

---

### Step 2.2: Verify Map Container Renders

**Action:**
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors

**Check:**
- ✅ No red error messages
- ✅ No Leaflet-related errors
- ✅ Map container element exists

**Verify in Console:**
```javascript
// Run in browser console:
const mapElement = document.querySelector('.leaflet-container');
console.log('Map exists:', !!mapElement);
console.log('Map visible:', mapElement?.offsetHeight > 0);
console.log('Map dimensions:', mapElement?.offsetWidth, 'x', mapElement?.offsetHeight);
```

**Expected:**
- Map exists: `true`
- Map visible: `true`
- Map dimensions: Should be > 600px wide and tall

---

### Step 2.3: Check Center Coordinates

**Action:**
1. Inspect map center visually
2. Check if map shows Chicago area

**Check in Console:**
```javascript
// Get map center from API response
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    console.log('Expected center:', data.coverage_area.center);
    console.log('Chicago center:', { lat: 41.8781, lng: -87.6298 });
  });
```

**Visual Check:**
- ✅ Map shows Chicago area (downtown Chicago visible)
- ✅ Map is centered, not off to the side
- ✅ Map tiles load correctly (no broken images)

---

### Step 2.4: Verify Map Tiles Load

**Action:**
1. Look at the map
2. Check for broken images or gray squares

**Check:**
- ✅ Map shows street map tiles
- ✅ No broken image icons
- ✅ Tiles load smoothly when panning
- ✅ Attribution text visible at bottom-right

---

### Step 2.5: Test Map Interactivity

**Action:**
1. Click and drag to pan the map
2. Scroll to zoom in/out
3. Try double-click to zoom

**Check:**
- ✅ Map responds to mouse drag
- ✅ Map zooms with scroll wheel
- ✅ Map is smooth (no lag)
- ✅ Map doesn't jump or glitch

---

### Step 2.6: Verify Map Bounds Fit Hotspots

**Action:**
1. Wait for hotspots to load
2. Observe if all hotspots are visible

**Check:**
- ✅ All hotspots are visible on initial load
- ✅ Map doesn't need manual adjustment to see hotspots
- ✅ Hotspots are within visible map bounds

**Test in Console:**
```javascript
// Check if map auto-fits to hotspots
setTimeout(() => {
  const circles = document.querySelectorAll('[data-testid="circle"]');
  console.log('Hotspots rendered:', circles.length);
  console.log('All visible:', circles.length > 0);
}, 2000);
```

---

## TEST 3: Hotspots Display with Proper Color Coding

### Step 3.1: Observe Hotspots on Map

**Action:**
1. Look at the map
2. Identify colored circles (hotspots)

**Check:**
- ✅ Hotspots are visible as circles
- ✅ Circles are semi-transparent (can see through them)
- ✅ Circles overlap properly (no z-index issues)

---

### Step 3.2: Verify Color Coding

**Action:**
1. Identify different colored hotspots
2. Match colors to intensity levels

**Color Reference:**
- **Red (#dc2626)** = Critical (intensity > 0.8)
- **Orange (#ea580c)** = High (intensity > 0.6)
- **Amber (#f59e0b)** = Medium (intensity > 0.3)
- **Yellow (#facc15)** = Low (intensity ≤ 0.3)

**Check in Console:**
```javascript
// Get hotspot data and verify colors
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    data.hotspots.forEach(h => {
      let expectedColor;
      if (h.intensity > 0.8) expectedColor = '#dc2626';
      else if (h.intensity > 0.6) expectedColor = '#ea580c';
      else if (h.intensity > 0.3) expectedColor = '#f59e0b';
      else expectedColor = '#facc15';
      
      console.log(`Grid ${h.grid_id}: intensity=${h.intensity}, risk=${h.risk_level}, expected color=${expectedColor}`);
    });
  });
```

**Visual Check:**
- ✅ Red circles for high-intensity hotspots
- ✅ Orange circles for medium-high intensity
- ✅ Amber/yellow circles for lower intensity
- ✅ Colors are distinct and recognizable

---

### Step 3.3: Verify Circle Size

**Action:**
1. Compare sizes of different hotspots
2. Larger circles should have higher intensity

**Check:**
- ✅ Larger circles have higher intensity values
- ✅ Circle size correlates with intensity
- ✅ Size difference is visible

**Test in Console:**
```javascript
// Check circle sizes match intensity
const circles = document.querySelectorAll('[data-testid="circle"]');
circles.forEach(circle => {
  const radius = parseFloat(circle.getAttribute('data-radius'));
  const intensity = parseFloat(circle.getAttribute('data-intensity'));
  console.log(`Radius: ${radius}, Intensity: ${intensity}, Match: ${Math.abs(radius - (intensity * 500)) < 50}`);
});
```

---

### Step 3.4: Check Opacity

**Action:**
1. Look at hotspot circles
2. Verify they're semi-transparent

**Check:**
- ✅ Circles are see-through (can see map underneath)
- ✅ Fill opacity is around 0.6
- ✅ Stroke opacity is around 0.8

**Visual Check:**
- ✅ Not completely opaque (can see map)
- ✅ Not completely transparent (can see colors)

---

### Step 3.5: Verify All Hotspots Visible

**Action:**
1. Pan around the map
2. Check if hotspots are visible

**Check:**
- ✅ All hotspots are visible (not hidden)
- ✅ No hotspots are completely obscured
- ✅ Overlapping hotspots are visible

---

### Step 3.6: Test Hotspot Updates on Filter Change

**Action:**
1. Change a filter (e.g., crime type)
2. Observe hotspot colors

**Check:**
- ✅ Hotspots update when filter changes
- ✅ Colors change appropriately
- ✅ No flickering or glitches

---

## TEST 4: Popups Show Detailed Prediction Information

### Step 4.1: Click on a Hotspot

**Action:**
1. Click on any colored hotspot circle
2. Wait for popup to appear

**Check:**
- ✅ Popup appears immediately on click
- ✅ Popup is positioned near the hotspot
- ✅ Popup doesn't obscure the hotspot

---

### Step 4.2: Verify Popup Content

**Action:**
1. Read the popup content
2. Check each piece of information

**Required Information:**
- ✅ Grid ID (e.g., "Grid: grid_0_0")
- ✅ Risk level badge (Critical/High/Medium/Low)
- ✅ Predicted incidents count (e.g., "Predicted Incidents: 8")
- ✅ Intensity percentage (e.g., "Intensity: 85%")
- ✅ Confidence percentage (e.g., "Confidence: 92%")
- ✅ Crime type (e.g., "Crime Type: theft")

**Check:**
- ✅ All fields are present
- ✅ Values are readable
- ✅ Formatting is clear

---

### Step 4.3: Verify Risk Level Badge

**Action:**
1. Click on different colored hotspots
2. Check badge color matches hotspot color

**Check:**
- ✅ Red hotspot → Red badge (Critical)
- ✅ Orange hotspot → Orange badge (High)
- ✅ Amber hotspot → Amber badge (Medium)
- ✅ Yellow hotspot → Yellow badge (Low)

**Test Multiple Hotspots:**
1. Click on a red hotspot → Verify badge says "CRITICAL"
2. Click on an orange hotspot → Verify badge says "HIGH"
3. Click on an amber hotspot → Verify badge says "MEDIUM"
4. Click on a yellow hotspot → Verify badge says "LOW"

---

### Step 4.4: Verify Data Accuracy

**Action:**
1. Click on a hotspot
2. Note the values in popup
3. Check API response for same hotspot

**Test in Console:**
```javascript
// Get hotspot data from API
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const hotspot = data.hotspots[0];
    console.log('API Data:', {
      grid_id: hotspot.grid_id,
      predicted_incidents: hotspot.predicted_incidents,
      intensity: hotspot.intensity,
      confidence: hotspot.confidence,
      risk_level: hotspot.risk_level
    });
    console.log('Check popup matches these values');
  });
```

**Check:**
- ✅ Popup values match API response
- ✅ Grid ID matches
- ✅ Intensity percentage matches (intensity * 100)
- ✅ Confidence percentage matches (confidence * 100)

---

### Step 4.5: Test Popup Closing

**Action:**
1. Open a popup
2. Click outside the popup (on map)
3. Popup should close

**Check:**
- ✅ Popup closes when clicking map
- ✅ Popup closes when clicking another hotspot
- ✅ Popup doesn't stay open indefinitely

---

### Step 4.6: Test Multiple Popups

**Action:**
1. Click on one hotspot
2. Click on another hotspot
3. Observe popup behavior

**Check:**
- ✅ Only one popup open at a time
- ✅ New popup replaces old popup
- ✅ Popups don't overlap incorrectly

---

### Step 4.7: Verify Popup Readability

**Action:**
1. Read popup text
2. Check formatting

**Check:**
- ✅ Text is readable (proper font size)
- ✅ Text has good contrast (readable on white background)
- ✅ Information is well-organized
- ✅ Labels are clear (e.g., "Predicted Incidents:")

---

## TEST 5: Filters Update Map Data Dynamically

### Step 5.1: Test City Filter

**Action:**
1. Find the "City" dropdown
2. Change from "Chicago" to another city (if available)
3. Observe map behavior

**Check:**
- ✅ Dropdown changes value
- ✅ API call is triggered (check Network tab)
- ✅ Map re-centers on new city
- ✅ Hotspots update for new city

**Network Tab Check:**
1. Open DevTools → Network tab
2. Change city filter
3. Look for new request to `/api/crime-map/hotspots`
4. Check request parameters include new city

**Expected Request:**
```
GET http://localhost:8000/api/crime-map/hotspots?city=new-york&crime_type=all&time_window=24h
```

---

### Step 5.2: Test Crime Type Filter

**Action:**
1. Find the "Crime Type" dropdown
2. Change from "All Crimes" to "Theft"
3. Observe map behavior

**Check:**
- ✅ Dropdown changes value
- ✅ API call is triggered
- ✅ Hotspots update (count may change)
- ✅ Map doesn't flicker or jump

**Network Tab Check:**
- ✅ Request includes `crime_type=theft`
- ✅ Response time is acceptable (< 500ms)

**Test Multiple Values:**
1. "All Crimes" → Should show all hotspots
2. "Theft" → Should filter to theft only
3. "Assault" → Should filter to assault only
4. "Burglary" → Should filter to burglary only

---

### Step 5.3: Test Time Window Filter

**Action:**
1. Find the "Time Window" dropdown
2. Change from "Next 24 Hours" to "Next 7 Days"
3. Observe map behavior

**Check:**
- ✅ Dropdown changes value
- ✅ API call is triggered
- ✅ Data updates (may show different predictions)
- ✅ Map updates smoothly

**Network Tab Check:**
- ✅ Request includes `time_window=7d`
- ✅ Response is valid

**Test All Options:**
1. "Next 24 Hours" (24h)
2. "Next 7 Days" (7d)
3. "Next 30 Days" (30d)

---

### Step 5.4: Test Multiple Filters Together

**Action:**
1. Set City: "Chicago"
2. Set Crime Type: "Theft"
3. Set Time Window: "Next 7 Days"
4. Observe map behavior

**Check:**
- ✅ All three filters apply
- ✅ Single API call with all parameters
- ✅ Map updates correctly
- ✅ Hotspots reflect all filters

**Network Tab Check:**
```
GET http://localhost:8000/api/crime-map/hotspots?city=chicago&crime_type=theft&time_window=7d
```

**Verify Response:**
- ✅ Response is valid
- ✅ Hotspots match all filter criteria
- ✅ Count is appropriate for filters

---

### Step 5.5: Check Loading State

**Action:**
1. Change a filter
2. Watch for loading indicator

**Check:**
- ✅ Loading spinner/indicator appears
- ✅ Loading indicator disappears when data loads
- ✅ Map doesn't show stale data during loading

**Visual Check:**
- ✅ Spinner visible during API call
- ✅ Spinner disappears when map updates
- ✅ Smooth transition (no flash)

---

### Step 5.6: Verify No Full Page Reload

**Action:**
1. Change a filter
2. Observe page behavior

**Check:**
- ✅ Page doesn't reload (URL doesn't change)
- ✅ Only map updates (not entire page)
- ✅ No page flash or white screen
- ✅ Smooth update

---

### Step 5.7: Test Filter State Persistence

**Action:**
1. Set filters to specific values
2. Navigate away and back
3. Check if filters reset

**Note:** This may depend on implementation. Check if:
- ✅ Filters persist in URL parameters
- ✅ Filters reset to defaults
- ✅ Filters are remembered

---

## TEST 6: Legend Displays Correctly

### Step 6.1: Locate Legend

**Action:**
1. Look at the bottom-right corner of the map
2. Find the legend box

**Check:**
- ✅ Legend is visible
- ✅ Legend is positioned correctly (bottom-right)
- ✅ Legend doesn't obstruct map interaction

---

### Step 6.2: Verify Legend Content

**Action:**
1. Read legend text
2. Check for all risk levels

**Required Items:**
- ✅ "Risk Levels" title
- ✅ Critical (>80%) with red indicator
- ✅ High (60-80%) with orange indicator
- ✅ Medium (30-60%) with amber indicator
- ✅ Low (<30%) with yellow indicator

**Check:**
- ✅ All four levels are shown
- ✅ Text is readable
- ✅ Formatting is clear

---

### Step 6.3: Verify Color Matching

**Action:**
1. Compare legend colors to hotspot colors
2. Verify they match

**Check:**
- ✅ Legend red matches hotspot red
- ✅ Legend orange matches hotspot orange
- ✅ Legend amber matches hotspot amber
- ✅ Legend yellow matches hotspot yellow

**Visual Comparison:**
1. Find a red hotspot on map
2. Compare to red indicator in legend
3. Colors should match exactly

---

### Step 6.4: Test Legend Positioning

**Action:**
1. Pan the map
2. Check if legend stays in position

**Check:**
- ✅ Legend stays in bottom-right corner
- ✅ Legend doesn't move with map pan
- ✅ Legend is always visible (not off-screen)

---

### Step 6.5: Verify Legend Readability

**Action:**
1. Read legend text
2. Check contrast and font size

**Check:**
- ✅ Text is readable (not too small)
- ✅ Good contrast (readable on white background)
- ✅ Font size is appropriate
- ✅ Text is not cut off

---

### Step 6.6: Test Legend Interaction

**Action:**
1. Try to interact with legend
2. Check if it interferes with map

**Check:**
- ✅ Legend doesn't block map clicks
- ✅ Can still pan/zoom map
- ✅ Legend is clickable (if interactive)

---

## TEST 7: Responsive Design Works on Different Screen Sizes

### Step 7.1: Test Desktop View (1920x1080)

**Action:**
1. Open browser DevTools (F12)
2. Set viewport to 1920x1080
3. Refresh page

**Check:**
- ✅ Map fills available space
- ✅ Filters are in horizontal layout (4 columns)
- ✅ All elements are visible
- ✅ No horizontal scrolling
- ✅ Text is readable

**Visual Check:**
- ✅ Layout is clean and organized
- ✅ Elements are properly spaced
- ✅ No overlapping elements

---

### Step 7.2: Test Tablet View (768x1024)

**Action:**
1. Set viewport to 768x1024
2. Refresh page

**Check:**
- ✅ Map adapts to screen size
- ✅ Filters stack or wrap appropriately
- ✅ Legend remains accessible
- ✅ Popups are readable
- ✅ No horizontal scrolling

**Visual Check:**
- ✅ Layout is usable
- ✅ Touch targets are adequate size
- ✅ Text remains readable

---

### Step 7.3: Test Mobile View (375x667)

**Action:**
1. Set viewport to 375x667 (iPhone size)
2. Refresh page

**Check:**
- ✅ Map is still usable
- ✅ Filters are mobile-friendly (stack vertically)
- ✅ Popups fit on screen
- ✅ Legend is accessible
- ✅ Touch interactions work
- ✅ No horizontal scrolling

**Touch Test:**
1. Try tapping on hotspots (should open popup)
2. Try tapping on filters (should open dropdown)
3. Try pinch-to-zoom on map
4. Try dragging to pan map

**Check:**
- ✅ Touch targets are large enough (44px minimum)
- ✅ No accidental clicks
- ✅ Interactions feel responsive

---

### Step 7.4: Test Window Resizing

**Action:**
1. Start with desktop size (1920x1080)
2. Gradually resize browser window
3. Observe layout changes

**Check:**
- ✅ Map resizes smoothly
- ✅ No layout breaks
- ✅ Elements reposition correctly
- ✅ No elements overflow
- ✅ Layout adapts at breakpoints

**Breakpoints to Test:**
- Desktop → Tablet transition (~1024px)
- Tablet → Mobile transition (~768px)

---

### Step 7.5: Verify Text Readability

**Action:**
1. Test at different screen sizes
2. Check text size and contrast

**Check:**
- ✅ Text is readable at all sizes
- ✅ Font size doesn't get too small
- ✅ Text doesn't overflow containers
- ✅ Good contrast (readable on backgrounds)

---

### Step 7.6: Test Interactive Elements

**Action:**
1. Test at mobile size
2. Try all interactive elements

**Check:**
- ✅ Dropdowns work on mobile
- ✅ Buttons are touch-friendly
- ✅ Map interactions work
- ✅ Popups are touch-friendly
- ✅ No accidental clicks

---

## Final Verification

After completing all tests:

1. **Run Automated Tests:**
   ```bash
   # Backend
   cd project/repo-foresight
   pytest tests/test_crime_map_api.py -v
   
   # Frontend
   cd frontend
   npm test
   ```

2. **Check Browser Console:**
   - No errors
   - No warnings (or acceptable warnings)

3. **Check Network Tab:**
   - All API calls succeed (200 status)
   - Response times acceptable

4. **Document Results:**
   - Mark each test as PASS/FAIL
   - Note any issues found
   - Take screenshots of any problems

---

## Quick Test Script

Run this in browser console on the crime map page to verify everything:

```javascript
// Comprehensive test script
async function runAllTests() {
  console.log('=== TESTING CRIME HEATMAP ===\n');
  
  // Test 1: API Response
  console.log('Test 1: Backend API...');
  try {
    const response = await fetch('http://localhost:8000/api/crime-map/hotspots');
    const data = await response.json();
    console.log('✅ API Response:', {
      status: response.status,
      hasHotspots: Array.isArray(data.hotspots),
      hotspotCount: data.hotspots.length,
      hasCoverageArea: !!data.coverage_area
    });
  } catch (e) {
    console.log('❌ API Error:', e.message);
  }
  
  // Test 2: Map Element
  console.log('\nTest 2: Map Rendering...');
  const mapElement = document.querySelector('.leaflet-container');
  console.log(mapElement ? '✅ Map exists' : '❌ Map missing');
  if (mapElement) {
    console.log('  Dimensions:', mapElement.offsetWidth, 'x', mapElement.offsetHeight);
  }
  
  // Test 3: Hotspots
  console.log('\nTest 3: Hotspots...');
  const circles = document.querySelectorAll('[data-testid="circle"], .leaflet-interactive');
  console.log(circles.length > 0 ? `✅ ${circles.length} hotspots rendered` : '❌ No hotspots');
  
  // Test 4: Filters
  console.log('\nTest 4: Filters...');
  const filters = document.querySelectorAll('select, button[role="button"]');
  console.log(filters.length > 0 ? `✅ ${filters.length} filters found` : '❌ No filters');
  
  // Test 5: Legend
  console.log('\nTest 5: Legend...');
  const legend = document.querySelector('.legend, [class*="legend"]');
  console.log(legend ? '✅ Legend visible' : '❌ Legend missing');
  
  // Test 6: Responsive
  console.log('\nTest 6: Responsive Design...');
  const width = window.innerWidth;
  console.log(`Screen width: ${width}px`);
  if (width < 768) {
    console.log('  Mobile view detected');
  } else if (width < 1024) {
    console.log('  Tablet view detected');
  } else {
    console.log('  Desktop view detected');
  }
  
  console.log('\n=== TESTING COMPLETE ===');
}

// Run tests
runAllTests();
```

This script will give you a quick overview of all test categories!

