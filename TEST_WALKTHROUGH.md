# Interactive Test Walkthrough - Follow Along

This guide walks you through each test step-by-step. Follow along in order.

---

## 🚀 SETUP (Do This First)

### Step 0: Start Services

**Terminal 1 - Backend:**
```bash
cd project/repo-foresight
python -m uvicorn src.api.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd project/repo-foresight/frontend
npm install  # If first time
npm run dev
```

**Terminal 3 - Testing:**
Keep this terminal open for running curl commands.

**Browser:**
Open Chrome/Firefox with DevTools open (F12)

---

## ✅ TEST 1: Backend Endpoint Returns Valid Heatmap Data

### 🎯 Goal: Verify API returns valid JSON with all required fields

### Step-by-Step:

**Step 1.1: Test Basic Endpoint**

In Terminal 3, run:
```bash
curl http://localhost:8000/api/crime-map/hotspots
```

**What to Look For:**
- ✅ You see JSON output (not error message)
- ✅ First line should be `{"hotspots":[...]`
- ✅ No "404 Not Found" or "Connection refused"

**Expected:** JSON response with hotspots array

---

**Step 1.2: Format JSON for Readability**

In Terminal 3, run:
```bash
curl http://localhost:8000/api/crime-map/hotspots | python -m json.tool
```

**What to Look For:**
- ✅ Formatted JSON (indented, readable)
- ✅ Top-level object has these keys:
  - `hotspots`
  - `prediction_date`
  - `model_version`
  - `coverage_area`
  - `grid_resolution`
  - `total_predicted_incidents`

**Check:** ✅ All fields present

---

**Step 1.3: Inspect First Hotspot**

In Terminal 3, run:
```bash
curl -s http://localhost:8000/api/crime-map/hotspots | python -m json.tool | grep -A 10 '"hotspots"'
```

**What to Look For:**
First hotspot in array should have:
- ✅ `"lat"`: number around 41.8 (Chicago latitude)
- ✅ `"lng"`: number around -87.6 (Chicago longitude)
- ✅ `"intensity"`: number between 0.0 and 1.0
- ✅ `"crime_type"`: string
- ✅ `"predicted_incidents"`: integer
- ✅ `"confidence"`: number between 0.0 and 1.0
- ✅ `"grid_id"`: string like "grid_0_0"
- ✅ `"risk_level"`: one of "low", "medium", "high", "critical"

**Check:** ✅ All fields present and valid

---

**Step 1.4: Test Query Parameters**

**Test City Parameter:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?city=chicago" | python -m json.tool | grep -A 2 "coverage_area"
```

**What to Look For:**
- ✅ `"center"` object has `"lat": 41.8781`
- ✅ `"center"` object has `"lng": -87.6298`

**Test Crime Type:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?crime_type=theft" | python -m json.tool | grep "crime_type"
```

**What to Look For:**
- ✅ Hotspots have `"crime_type": "theft"`

**Test Time Window:**
```bash
curl "http://localhost:8000/api/crime-map/hotspots?time_window=24h"
```

**What to Look For:**
- ✅ Response is valid JSON (no errors)

**Check:** ✅ All parameters work

---

**Step 1.5: Check Response Time**

In Terminal 3, run:
```bash
time curl -s http://localhost:8000/api/crime-map/hotspots > /dev/null
```

**What to Look For:**
- ✅ Real time: < 0.5 seconds (0.500s)
- ✅ If > 1 second, might be slow network

**Check:** ✅ Response time acceptable

---

## ✅ TEST 2: Map Renders with Correct Center Coordinates

### 🎯 Goal: Verify map displays correctly centered on Chicago

### Step-by-Step:

**Step 2.1: Open Crime Map Page**

In Browser:
1. Navigate to: `http://localhost:5173/crime-map`
2. Wait for page to load (3-5 seconds)

**What to Look For:**
- ✅ Page loads (no blank page)
- ✅ Map appears (not just white screen)
- ✅ No error messages on page

**Check:** ✅ Page loads successfully

---

**Step 2.2: Check Browser Console**

In Browser DevTools (F12):
1. Click "Console" tab
2. Look for red error messages

**What to Look For:**
- ✅ No red error messages
- ✅ Maybe some warnings (yellow) - these are OK
- ✅ If you see errors, note them

**Check:** ✅ No critical errors

---

**Step 2.3: Verify Map Element Exists**

In Browser Console, run:
```javascript
const mapElement = document.querySelector('.leaflet-container');
console.log('Map exists:', !!mapElement);
console.log('Map visible:', mapElement?.offsetHeight > 0);
console.log('Dimensions:', mapElement?.offsetWidth, 'x', mapElement?.offsetHeight);
```

**What to Look For:**
- ✅ `Map exists: true`
- ✅ `Map visible: true`
- ✅ Dimensions: Should be > 600px x 600px

**Check:** ✅ Map element exists and is visible

---

**Step 2.4: Verify Map Shows Chicago**

**Visual Check:**
1. Look at the map
2. Do you see Chicago area? (downtown Chicago with streets)

**What to Look For:**
- ✅ Map shows Chicago area (not random location)
- ✅ Streets visible (not satellite)
- ✅ Map tiles load correctly (no broken images)

**Check:** ✅ Map shows Chicago area

---

**Step 2.5: Test Map Interactivity**

**Actions:**
1. Click and drag on map → Map should pan
2. Scroll mouse wheel → Map should zoom
3. Double-click on map → Map should zoom in

**What to Look For:**
- ✅ Map responds to mouse drag
- ✅ Map zooms smoothly
- ✅ No lag or stuttering

**Check:** ✅ Map is interactive

---

**Step 2.6: Verify Hotspots Are Visible**

**Visual Check:**
1. Look at the map
2. Do you see colored circles? (these are hotspots)

**What to Look For:**
- ✅ Colored circles visible on map
- ✅ Circles are semi-transparent (can see map underneath)
- ✅ Circles are distributed across Chicago area

**Check:** ✅ Hotspots are visible

---

## ✅ TEST 3: Hotspots Display with Proper Color Coding

### 🎯 Goal: Verify hotspots have correct colors matching risk levels

### Step-by-Step:

**Step 3.1: Identify Hotspot Colors**

**Visual Check:**
Look at the map and identify:
- **Red circles** = Critical risk
- **Orange circles** = High risk
- **Amber/yellow circles** = Medium risk
- **Light yellow circles** = Low risk

**What to Look For:**
- ✅ At least 2-3 different colors visible
- ✅ Colors are distinct (not all same color)
- ✅ Red circles are darkest/most intense

**Check:** ✅ Multiple colors visible

---

**Step 3.2: Verify Color Mapping**

In Browser Console, run:
```javascript
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const colors = {
      critical: 0, high: 0, medium: 0, low: 0
    };
    data.hotspots.forEach(h => {
      if (h.intensity > 0.8) colors.critical++;
      else if (h.intensity > 0.6) colors.high++;
      else if (h.intensity > 0.3) colors.medium++;
      else colors.low++;
    });
    console.log('Color distribution:', colors);
    console.log('Expected: Red (critical), Orange (high), Amber (medium), Yellow (low)');
  });
```

**What to Look For:**
- ✅ Console shows distribution of risk levels
- ✅ At least some hotspots in each category

**Check:** ✅ Color distribution matches risk levels

---

**Step 3.3: Verify Circle Sizes**

**Visual Check:**
1. Compare different hotspot circles
2. Larger circles should have higher intensity

**What to Look For:**
- ✅ Circle sizes vary (not all same size)
- ✅ Larger circles tend to be red/orange
- ✅ Smaller circles tend to be yellow

**Check:** ✅ Circle size correlates with intensity

---

**Step 3.4: Click on Different Colored Hotspots**

**Actions:**
1. Click on a red hotspot → Note intensity value
2. Click on an orange hotspot → Note intensity value
3. Click on a yellow hotspot → Note intensity value

**What to Look For:**
- ✅ Red hotspots: intensity > 0.8 (80%)
- ✅ Orange hotspots: intensity 0.6-0.8 (60-80%)
- ✅ Yellow hotspots: intensity < 0.3 (<30%)

**Check:** ✅ Colors match intensity values

---

## ✅ TEST 4: Popups Show Detailed Prediction Information

### 🎯 Goal: Verify popups display all required information correctly

### Step-by-Step:

**Step 4.1: Click on a Hotspot**

**Actions:**
1. Click on any colored hotspot circle
2. Wait for popup to appear (should be instant)

**What to Look For:**
- ✅ Popup appears immediately
- ✅ Popup is positioned near the hotspot
- ✅ Popup doesn't cover the hotspot completely

**Check:** ✅ Popup opens on click

---

**Step 4.2: Verify Popup Content**

**Read the popup and check for:**

1. **Grid ID** (e.g., "Grid: grid_0_0")
   - ✅ Present
   - ✅ Format: "Grid: grid_X_Y"

2. **Risk Level Badge** (e.g., "CRITICAL", "HIGH", "MEDIUM", "LOW")
   - ✅ Present
   - ✅ Color matches hotspot color

3. **Predicted Incidents** (e.g., "Predicted Incidents: 8")
   - ✅ Present
   - ✅ Number is an integer

4. **Intensity** (e.g., "Intensity: 85%")
   - ✅ Present
   - ✅ Percentage format

5. **Confidence** (e.g., "Confidence: 92%")
   - ✅ Present
   - ✅ Percentage format

6. **Crime Type** (e.g., "Crime Type: theft")
   - ✅ Present
   - ✅ Text is readable

**Check:** ✅ All 6 fields present

---

**Step 4.3: Verify Badge Color Matches Hotspot**

**Actions:**
1. Click on a red hotspot
2. Check popup badge color
3. Badge should also be red

**Test Multiple:**
- Red hotspot → Red badge (CRITICAL)
- Orange hotspot → Orange badge (HIGH)
- Amber hotspot → Amber badge (MEDIUM)
- Yellow hotspot → Yellow badge (LOW)

**Check:** ✅ Badge colors match hotspot colors

---

**Step 4.4: Verify Data Accuracy**

**Actions:**
1. Click on a hotspot
2. Note the values in popup
3. In Console, run:

```javascript
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const hotspot = data.hotspots[0];
    console.log('API Data:', {
      grid_id: hotspot.grid_id,
      predicted_incidents: hotspot.predicted_incidents,
      intensity: (hotspot.intensity * 100).toFixed(0) + '%',
      confidence: (hotspot.confidence * 100).toFixed(0) + '%',
      risk_level: hotspot.risk_level
    });
    console.log('Compare with popup values');
  });
```

**What to Look For:**
- ✅ Popup values match API response
- ✅ Intensity percentage = intensity * 100
- ✅ Confidence percentage = confidence * 100

**Check:** ✅ Data is accurate

---

**Step 4.5: Test Popup Closing**

**Actions:**
1. Open a popup (click hotspot)
2. Click somewhere on the map (not on hotspot)
3. Popup should close

**What to Look For:**
- ✅ Popup closes when clicking map
- ✅ Popup closes when clicking another hotspot
- ✅ Popup doesn't stay stuck open

**Check:** ✅ Popup closes properly

---

## ✅ TEST 5: Filters Update Map Data Dynamically

### 🎯 Goal: Verify filters trigger API calls and update map

### Step-by-Step:

**Step 5.1: Open Network Tab**

In Browser DevTools:
1. Click "Network" tab
2. Clear existing requests (trash icon)
3. Keep tab open

**What to Look For:**
- ✅ Network tab is open
- ✅ Ready to see API calls

**Check:** ✅ Network tab ready

---

**Step 5.2: Test City Filter**

**Actions:**
1. Find "City" dropdown (top of page)
2. Change from "Chicago" to another city (if available)
3. Watch Network tab

**What to Look For:**
- ✅ New request appears in Network tab
- ✅ Request URL: `/api/crime-map/hotspots?city=...`
- ✅ Map updates (may re-center)
- ✅ Hotspots update

**Check:** ✅ City filter triggers API call

---

**Step 5.3: Test Crime Type Filter**

**Actions:**
1. Find "Crime Type" dropdown
2. Change from "All Crimes" to "Theft"
3. Watch Network tab

**What to Look For:**
- ✅ New request appears
- ✅ Request includes `crime_type=theft`
- ✅ Map updates
- ✅ Hotspot count may change

**Check:** ✅ Crime type filter works

---

**Step 5.4: Test Time Window Filter**

**Actions:**
1. Find "Time Window" dropdown
2. Change from "Next 24 Hours" to "Next 7 Days"
3. Watch Network tab

**What to Look For:**
- ✅ New request appears
- ✅ Request includes `time_window=7d`
- ✅ Map updates

**Check:** ✅ Time window filter works

---

**Step 5.5: Test Multiple Filters Together**

**Actions:**
1. Set City: "Chicago"
2. Set Crime Type: "Theft"
3. Set Time Window: "Next 7 Days"
4. Watch Network tab

**What to Look For:**
- ✅ Single API call (not multiple)
- ✅ Request URL includes all parameters: `?city=chicago&crime_type=theft&time_window=7d`
- ✅ Map updates with all filters applied

**Check:** ✅ Multiple filters work together

---

**Step 5.6: Check Loading State**

**Actions:**
1. Change a filter
2. Watch for loading indicator

**What to Look For:**
- ✅ Loading spinner appears (briefly)
- ✅ Spinner disappears when map updates
- ✅ No flickering or white screen

**Check:** ✅ Loading state displays

---

## ✅ TEST 6: Legend Displays Correctly

### 🎯 Goal: Verify legend is visible and matches hotspot colors

### Step-by-Step:

**Step 6.1: Locate Legend**

**Visual Check:**
1. Look at bottom-right corner of map
2. Find white box with "Risk Levels" text

**What to Look For:**
- ✅ Legend box visible
- ✅ Positioned in bottom-right
- ✅ Doesn't obstruct map

**Check:** ✅ Legend is visible

---

**Step 6.2: Verify Legend Content**

**Read legend and check for:**

1. **Title:** "Risk Levels"
   - ✅ Present

2. **Critical (>80%)** with red circle
   - ✅ Present
   - ✅ Red color matches red hotspots

3. **High (60-80%)** with orange circle
   - ✅ Present
   - ✅ Orange color matches orange hotspots

4. **Medium (30-60%)** with amber circle
   - ✅ Present
   - ✅ Amber color matches amber hotspots

5. **Low (<30%)** with yellow circle
   - ✅ Present
   - ✅ Yellow color matches yellow hotspots

**Check:** ✅ All 4 risk levels shown

---

**Step 6.3: Verify Color Matching**

**Visual Comparison:**
1. Find a red hotspot on map
2. Compare to red indicator in legend
3. Colors should match exactly

**Test All Colors:**
- Red hotspot → Red legend indicator
- Orange hotspot → Orange legend indicator
- Amber hotspot → Amber legend indicator
- Yellow hotspot → Yellow legend indicator

**Check:** ✅ Colors match exactly

---

## ✅ TEST 7: Responsive Design Works on Different Screen Sizes

### 🎯 Goal: Verify layout adapts to different screen sizes

### Step-by-Step:

**Step 7.1: Test Desktop View (1920x1080)**

**Actions:**
1. Open DevTools (F12)
2. Click device toolbar icon (or Ctrl+Shift+M)
3. Set dimensions to: 1920 x 1080
4. Refresh page

**What to Look For:**
- ✅ Map fills available space
- ✅ Filters are in horizontal row (4 columns)
- ✅ All elements visible
- ✅ No horizontal scrolling

**Check:** ✅ Desktop layout works

---

**Step 7.2: Test Tablet View (768x1024)**

**Actions:**
1. In DevTools, set dimensions to: 768 x 1024
2. Refresh page

**What to Look For:**
- ✅ Map adapts to screen size
- ✅ Filters stack or wrap (not horizontal)
- ✅ Legend still visible
- ✅ Popups fit on screen

**Check:** ✅ Tablet layout works

---

**Step 7.3: Test Mobile View (375x667)**

**Actions:**
1. In DevTools, set dimensions to: 375 x 667 (iPhone size)
2. Refresh page

**What to Look For:**
- ✅ Map is still usable
- ✅ Filters stack vertically
- ✅ Text is readable
- ✅ Touch targets are large enough

**Touch Test:**
1. Try tapping on hotspot (should open popup)
2. Try tapping on filter dropdown (should open)
3. Try dragging map (should pan)

**Check:** ✅ Mobile layout works

---

**Step 7.4: Test Window Resizing**

**Actions:**
1. Start with desktop size (1920x1080)
2. Gradually resize browser window
3. Watch layout adapt

**What to Look For:**
- ✅ Layout adapts smoothly
- ✅ No elements break or overflow
- ✅ Map resizes correctly

**Check:** ✅ Responsive resizing works

---

## 🎉 FINAL CHECKLIST

After completing all tests, verify:

- [ ] All 7 test categories completed
- [ ] No critical errors in console
- [ ] All API calls succeed (200 status)
- [ ] Map functions correctly
- [ ] Filters work properly
- [ ] Responsive design works

---

## 📝 Document Results

Record your results:

```
Date: ___________
Tester: ___________
Browser: ___________

Test Results:
[ ] Test 1: Backend Endpoint - PASS / FAIL
[ ] Test 2: Map Rendering - PASS / FAIL
[ ] Test 3: Color Coding - PASS / FAIL
[ ] Test 4: Popups - PASS / FAIL
[ ] Test 5: Filters - PASS / FAIL
[ ] Test 6: Legend - PASS / FAIL
[ ] Test 7: Responsive Design - PASS / FAIL

Issues Found:
1. _________________________________
2. _________________________________
```

---

**Congratulations!** You've completed all tests! 🎊

