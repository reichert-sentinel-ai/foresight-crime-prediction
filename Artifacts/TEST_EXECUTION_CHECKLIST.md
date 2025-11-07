# Test Execution Checklist - Quick Reference

Print this checklist and check off items as you test.

---

## TEST 1: Backend Endpoint Returns Valid Heatmap Data

### Terminal Commands to Run:

```bash
# 1.1 Basic endpoint
curl http://localhost:8000/api/crime-map/hotspots

# 1.2 Format JSON
curl http://localhost:8000/api/crime-map/hotspots | python -m json.tool

# 1.3 Check first hotspot
curl -s http://localhost:8000/api/crime-map/hotspots | python -m json.tool | head -30

# 1.4 Test query parameters
curl "http://localhost:8000/api/crime-map/hotspots?city=chicago"
curl "http://localhost:8000/api/crime-map/hotspots?crime_type=theft"
curl "http://localhost:8000/api/crime-map/hotspots?time_window=24h"
curl "http://localhost:8000/api/crime-map/hotspots?date=2024-01-15"

# 1.5 Check response time
time curl -s http://localhost:8000/api/crime-map/hotspots > /dev/null
```

### Checklist:

- [ ] **1.1** Status code is 200
- [ ] **1.2** Response has all required fields
- [ ] **1.3** Each hotspot has required fields
- [ ] **1.4** Query parameters work
- [ ] **1.5** Response time < 500ms

---

## TEST 2: Map Renders with Correct Center Coordinates

### Browser Actions:

1. Open: `http://localhost:5173/crime-map`
2. Open DevTools (F12) → Console tab
3. Run console check script

### Console Script:

```javascript
const mapElement = document.querySelector('.leaflet-container');
console.log('Map exists:', !!mapElement);
console.log('Map visible:', mapElement?.offsetHeight > 0);
```

### Checklist:

- [ ] **2.1** Page loads without errors
- [ ] **2.2** Map container exists
- [ ] **2.3** Center coordinates correct (Chicago: 41.8781, -87.6298)
- [ ] **2.4** Map tiles load correctly
- [ ] **2.5** Map is interactive (pan/zoom works)
- [ ] **2.6** Map bounds fit all hotspots

---

## TEST 3: Hotspots Display with Proper Color Coding

### Visual Check:

Look at the map and identify:
- Red circles = Critical (>80%)
- Orange circles = High (60-80%)
- Amber circles = Medium (30-60%)
- Yellow circles = Low (<30%)

### Console Script:

```javascript
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    data.hotspots.forEach(h => {
      let expectedColor;
      if (h.intensity > 0.8) expectedColor = '#dc2626';
      else if (h.intensity > 0.6) expectedColor = '#ea580c';
      else if (h.intensity > 0.3) expectedColor = '#f59e0b';
      else expectedColor = '#facc15';
      console.log(`Grid ${h.grid_id}: ${expectedColor} (intensity: ${h.intensity})`);
    });
  });
```

### Checklist:

- [ ] **3.1** Hotspots render as circles
- [ ] **3.2** Colors match intensity (red/orange/amber/yellow)
- [ ] **3.3** Circle size correlates with intensity
- [ ] **3.4** Opacity is correct (semi-transparent)
- [ ] **3.5** All hotspots visible
- [ ] **3.6** Hotspots update on filter change

---

## TEST 4: Popups Show Detailed Prediction Information

### Actions:

1. Click on any hotspot
2. Read popup content
3. Verify all fields present

### Checklist:

- [ ] **4.1** Popup opens on click
- [ ] **4.2** Popup has all required fields:
  - [ ] Grid ID
  - [ ] Risk level badge
  - [ ] Predicted incidents
  - [ ] Intensity percentage
  - [ ] Confidence percentage
  - [ ] Crime type
- [ ] **4.3** Badge color matches hotspot color
- [ ] **4.4** Data matches API response
- [ ] **4.5** Popup closes on outside click
- [ ] **4.6** Multiple popups handled correctly
- [ ] **4.7** Popup is readable

---

## TEST 5: Filters Update Map Data Dynamically

### Actions:

1. Change City dropdown → Watch map
2. Change Crime Type dropdown → Watch map
3. Change Time Window dropdown → Watch map
4. Change all filters together → Watch map
5. Check Network tab for API calls

### Network Tab Check:

- [ ] API calls triggered on filter change
- [ ] Request includes correct parameters
- [ ] Response time < 500ms

### Checklist:

- [ ] **5.1** City filter updates map
- [ ] **5.2** Crime type filter works
- [ ] **5.3** Time window filter works
- [ ] **5.4** Multiple filters work together
- [ ] **5.5** Loading state displays
- [ ] **5.6** No full page reload
- [ ] **5.7** Filter state persists (optional)

---

## TEST 6: Legend Displays Correctly

### Visual Check:

Look at bottom-right of map for legend box.

### Checklist:

- [ ] **6.1** Legend is visible
- [ ] **6.2** Legend shows all 4 risk levels:
  - [ ] Critical (>80%) with red
  - [ ] High (60-80%) with orange
  - [ ] Medium (30-60%) with amber
  - [ ] Low (<30%) with yellow
- [ ] **6.3** Legend colors match hotspot colors
- [ ] **6.4** Legend positioned correctly (bottom-right)
- [ ] **6.5** Legend is readable
- [ ] **6.6** Legend doesn't interfere with map

---

## TEST 7: Responsive Design Works on Different Screen Sizes

### DevTools Actions:

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test different sizes:
   - Desktop: 1920x1080
   - Tablet: 768x1024
   - Mobile: 375x667

### Checklist:

- [ ] **7.1** Desktop view (1920x1080):
  - [ ] Map fills space
  - [ ] Filters horizontal layout
  - [ ] All elements visible
  - [ ] No horizontal scroll
- [ ] **7.2** Tablet view (768x1024):
  - [ ] Map adapts
  - [ ] Filters stack/wrap
  - [ ] Legend accessible
  - [ ] Popups readable
- [ ] **7.3** Mobile view (375x667):
  - [ ] Map usable
  - [ ] Filters mobile-friendly
  - [ ] Popups fit on screen
  - [ ] Touch interactions work
- [ ] **7.4** Window resizing:
  - [ ] Map resizes smoothly
  - [ ] No layout breaks
  - [ ] Elements reposition correctly
- [ ] **7.5** Text readable at all sizes
- [ ] **7.6** Interactive elements touch-friendly

---

## Final Results

### Test Summary:

- [ ] Test 1: Backend Endpoint - ✅ PASS / ❌ FAIL
- [ ] Test 2: Map Rendering - ✅ PASS / ❌ FAIL
- [ ] Test 3: Color Coding - ✅ PASS / ❌ FAIL
- [ ] Test 4: Popups - ✅ PASS / ❌ FAIL
- [ ] Test 5: Filters - ✅ PASS / ❌ FAIL
- [ ] Test 6: Legend - ✅ PASS / ❌ FAIL
- [ ] Test 7: Responsive Design - ✅ PASS / ❌ FAIL

### Issues Found:

1. _________________________________
2. _________________________________
3. _________________________________

### Notes:

_________________________________
_________________________________
_________________________________

---

## Quick Test Script

Run this in browser console:

```javascript
async function runAllTests() {
  console.log('=== TESTING CRIME HEATMAP ===\n');
  
  // Test 1: API
  try {
    const r = await fetch('http://localhost:8000/api/crime-map/hotspots');
    const d = await r.json();
    console.log('✅ API:', r.status, d.hotspots.length, 'hotspots');
  } catch (e) {
    console.log('❌ API Error:', e.message);
  }
  
  // Test 2: Map
  const map = document.querySelector('.leaflet-container');
  console.log(map ? '✅ Map exists' : '❌ Map missing');
  
  // Test 3: Hotspots
  const circles = document.querySelectorAll('[data-testid="circle"], .leaflet-interactive');
  console.log(circles.length > 0 ? `✅ ${circles.length} hotspots` : '❌ No hotspots');
  
  // Test 4: Filters
  const filters = document.querySelectorAll('select, button[role="button"]');
  console.log(filters.length > 0 ? `✅ ${filters.length} filters` : '❌ No filters');
  
  // Test 5: Legend
  const legend = document.querySelector('.legend, [class*="legend"]');
  console.log(legend ? '✅ Legend visible' : '❌ Legend missing');
  
  // Test 6: Responsive
  console.log(`Screen: ${window.innerWidth}x${window.innerHeight}px`);
  
  console.log('\n=== COMPLETE ===');
}

runAllTests();
```

