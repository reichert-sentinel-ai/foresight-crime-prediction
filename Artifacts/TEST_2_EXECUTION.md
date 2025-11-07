# TEST 2: Map Renders with Correct Center Coordinates

## Current Status: 1 of 7 Tests Complete (6 Remaining)

### ✅ Completed
- TEST 1: Backend Endpoint Returns Valid Heatmap Data - **PASSED**

### ⏳ Remaining (6 tests)
- **TEST 2:** Map Renders with Correct Center Coordinates ← **YOU ARE HERE**
- TEST 3: Hotspots Display with Proper Color Coding
- TEST 4: Popups Show Detailed Prediction Information
- TEST 5: Filters Update Map Data Dynamically
- TEST 6: Legend Displays Correctly
- TEST 7: Responsive Design Works on Different Screen Sizes

---

## TEST 2: Step-by-Step Execution

### Goal
Verify the map displays correctly centered on Chicago with proper coordinates.

---

### Step 2.1: Visual Check - Map Shows Chicago Area

**Action:**
1. Look at the map on `http://localhost:5173/crime-map`
2. Visually identify if it shows Chicago area

**What to Look For:**
- ✅ Map shows Chicago area (downtown Chicago visible)
- ✅ Streets visible (not satellite view)
- ✅ Map is centered, not off to the side
- ✅ Map tiles load correctly (no broken images)

**Expected Result:**
- Map should show Chicago's street grid
- Downtown Chicago should be visible
- Map should be centered, not showing random location

**Check:** ✅ Map shows Chicago area

---

### Step 2.2: Browser Console Check

**Action:**
1. Open browser DevTools (Press F12)
2. Click "Console" tab
3. Look for any red error messages

**What to Look For:**
- ✅ No red error messages
- ✅ Maybe some warnings (yellow) - these are OK
- ✅ If you see errors, note them

**Check in Console:**
```javascript
// Run this in browser console:
const mapElement = document.querySelector('.leaflet-container');
console.log('Map exists:', !!mapElement);
console.log('Map visible:', mapElement?.offsetHeight > 0);
console.log('Map dimensions:', mapElement?.offsetWidth, 'x', mapElement?.offsetHeight);
```

**Expected Output:**
```
Map exists: true
Map visible: true
Map dimensions: [some number > 600] x [some number > 600]
```

**Check:** ✅ No critical errors in console

---

### Step 2.3: Verify Map Element Exists

**Action:**
1. In browser console (F12), run the script above
2. Check the output

**What to Look For:**
- ✅ `Map exists: true`
- ✅ `Map visible: true`
- ✅ Dimensions: Should be > 600px x 600px

**Check:** ✅ Map element exists and is visible

---

### Step 2.4: Verify Map Shows Chicago Coordinates

**Visual Check:**
1. Look at the map
2. Does it show Chicago area? (downtown Chicago with streets)

**Coordinate Check:**
The map should be centered on Chicago:
- **Latitude:** ~41.8781°N (Chicago)
- **Longitude:** ~87.6298°W (Chicago)

**Check in Console:**
```javascript
// Get the expected center from API
fetch('/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    console.log('Expected center:', data.coverage_area.center);
    console.log('Chicago center:', { lat: 41.8781, lng: -87.6298 });
    console.log('Match:', 
      Math.abs(data.coverage_area.center.lat - 41.8781) < 0.1 &&
      Math.abs(data.coverage_area.center.lng - (-87.6298)) < 0.1
    );
  });
```

**Expected Output:**
```
Expected center: {lat: 41.8781, lng: -87.6298}
Chicago center: {lat: 41.8781, lng: -87.6298}
Match: true
```

**Check:** ✅ Center coordinates match Chicago

---

### Step 2.5: Test Map Interactivity

**Action:**
1. Click and drag on the map → Map should pan
2. Scroll mouse wheel → Map should zoom
3. Double-click on map → Map should zoom in

**What to Look For:**
- ✅ Map responds to mouse drag
- ✅ Map zooms smoothly with scroll wheel
- ✅ Map is smooth (no lag or stuttering)
- ✅ Map doesn't jump or glitch

**Check:** ✅ Map is interactive

---

### Step 2.6: Verify Hotspots Are Visible

**Visual Check:**
1. Look at the map
2. Do you see colored circles? (these are hotspots)

**What to Look For:**
- ✅ Colored circles visible on map
- ✅ Circles are semi-transparent (can see map underneath)
- ✅ Circles are distributed across Chicago area
- ✅ All hotspots are visible (not hidden)

**Check:** ✅ Hotspots are visible

---

## TEST 2 Checklist

- [ ] **2.1** Map shows Chicago area visually
- [ ] **2.2** No console errors
- [ ] **2.3** Map element exists and is visible
- [ ] **2.4** Center coordinates match Chicago (41.8781, -87.6298)
- [ ] **2.5** Map is interactive (pan/zoom works)
- [ ] **2.6** Hotspots are visible on map

---

## Quick Test Commands

Run these in browser console (F12):

```javascript
// Test 2.3: Map element
const mapElement = document.querySelector('.leaflet-container');
console.log('✅ Map exists:', !!mapElement);
console.log('✅ Map visible:', mapElement?.offsetHeight > 0);

// Test 2.4: Center coordinates
fetch('/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const center = data.coverage_area.center;
    console.log('✅ Center:', center.lat, center.lng);
    console.log('✅ Chicago match:', 
      Math.abs(center.lat - 41.8781) < 0.1 && 
      Math.abs(center.lng - (-87.6298)) < 0.1
    );
  });
```

---

## Expected Results Summary

- ✅ Map displays Chicago area
- ✅ No console errors
- ✅ Map element exists (600px+ dimensions)
- ✅ Center coordinates: ~41.8781°N, ~87.6298°W
- ✅ Map is interactive (pan/zoom works)
- ✅ Hotspots visible as colored circles

---

## Next Steps

After completing TEST 2:
- **TEST 3:** Hotspots Display with Proper Color Coding
- Then 4 more tests remain

---

## Progress: 1/7 Complete (14%)

**Current:** TEST 2 - Map Rendering  
**Remaining:** 6 tests (3, 4, 5, 6, 7)

