# Crime Heatmap Testing Checklist (F1)

## Pre-Testing Setup

- [ ] Backend server is running on `http://localhost:8000`
- [ ] Frontend server is running on `http://localhost:5173`
- [ ] All dependencies installed (`scipy`, `leaflet`, `react-leaflet`, etc.)
- [ ] Browser console is open to check for errors
- [ ] Network tab is open to monitor API calls

---

## Test 1: Backend Endpoint Returns Valid Heatmap Data

### Test Cases

- [ ] **1.1** GET `/api/crime-map/hotspots` returns 200 status
- [ ] **1.2** Response contains required fields:
  - [ ] `hotspots` array exists
  - [ ] `prediction_date` is valid date string
  - [ ] `model_version` is present
  - [ ] `coverage_area` object exists with `center` and `radius_km`
  - [ ] `grid_resolution` is present
  - [ ] `total_predicted_incidents` is a number
- [ ] **1.3** Each hotspot in array has required fields:
  - [ ] `lat` (float, valid latitude)
  - [ ] `lng` (float, valid longitude)
  - [ ] `intensity` (float, 0-1 range)
  - [ ] `crime_type` (string)
  - [ ] `predicted_incidents` (integer)
  - [ ] `confidence` (float, 0-1 range)
  - [ ] `grid_id` (string)
  - [ ] `risk_level` (one of: "low", "medium", "high", "critical")
- [ ] **1.4** Query parameters work correctly:
  - [ ] `?city=chicago` returns Chicago coordinates
  - [ ] `?crime_type=theft` filters correctly
  - [ ] `?time_window=24h` applies time filter
  - [ ] `?date=2024-01-15` uses custom date
- [ ] **1.5** Response times are acceptable (< 500ms)

### Manual Test Steps

```bash
# Test basic endpoint
curl http://localhost:8000/api/crime-map/hotspots

# Test with query parameters
curl "http://localhost:8000/api/crime-map/hotspots?city=chicago&crime_type=theft&time_window=24h"

# Verify response structure
curl -s http://localhost:8000/api/crime-map/hotspots | jq '.hotspots[0]'
```

### Expected Results

- Status code: `200 OK`
- Content-Type: `application/json`
- Response time: < 500ms
- Hotspots array contains 50-200 items
- All hotspots have valid coordinates within Chicago area

---

## Test 2: Map Renders with Correct Center Coordinates

### Test Cases

- [ ] **2.1** Map container renders without errors
- [ ] **2.2** Map centers on correct coordinates:
  - [ ] Default: Chicago (41.8781, -87.6298)
  - [ ] Matches `coverage_area.center` from API
- [ ] **2.3** Initial zoom level is appropriate (zoom 12)
- [ ] **2.4** Map tiles load correctly (OpenStreetMap)
- [ ] **2.5** Map is interactive (can pan and zoom)
- [ ] **2.6** Map bounds fit all hotspots when data loads

### Manual Test Steps

1. Navigate to `http://localhost:5173/crime-map`
2. Wait for map to load
3. Check browser console for errors
4. Verify map shows Chicago area
5. Check coordinates in map center

### Expected Results

- Map renders without console errors
- Center coordinates: ~41.8781°N, ~87.6298°W
- Map is interactive and responsive
- No broken tile images

---

## Test 3: Hotspots Display with Proper Color Coding

### Test Cases

- [ ] **3.1** Hotspots render as circles on map
- [ ] **3.2** Color coding matches intensity:
  - [ ] Red (#dc2626) for intensity > 0.8 (Critical)
  - [ ] Orange (#ea580c) for intensity > 0.6 (High)
  - [ ] Amber (#f59e0b) for intensity > 0.3 (Medium)
  - [ ] Yellow (#facc15) for intensity ≤ 0.3 (Low)
- [ ] **3.3** Circle size correlates with intensity (larger = higher intensity)
- [ ] **3.4** Circles have appropriate opacity (0.6 fill, 0.8 stroke)
- [ ] **3.5** All hotspots are visible (not hidden behind each other)
- [ ] **3.6** Hotspots update when filters change

### Manual Test Steps

1. Load crime map page
2. Observe hotspot colors on map
3. Click on hotspots to verify popup data
4. Change filters and verify colors update
5. Check browser console for rendering errors

### Expected Results

- Hotspots are clearly visible with distinct colors
- Color intensity matches risk level
- No overlapping issues that obscure hotspots
- Colors update correctly when filters change

---

## Test 4: Popups Show Detailed Prediction Information

### Test Cases

- [ ] **4.1** Clicking hotspot opens popup
- [ ] **4.2** Popup contains all required information:
  - [ ] Grid ID
  - [ ] Risk level badge (Critical/High/Medium/Low)
  - [ ] Predicted incidents count
  - [ ] Intensity percentage
  - [ ] Confidence percentage
  - [ ] Crime type
- [ ] **4.3** Risk level badge color matches hotspot color
- [ ] **4.4** Popup data matches API response data
- [ ] **4.5** Popup closes when clicking outside or map
- [ ] **4.6** Multiple popups don't overlap incorrectly
- [ ] **4.7** Popup is readable and well-formatted

### Manual Test Steps

1. Click on different colored hotspots
2. Verify popup content matches hotspot data
3. Check badge colors match risk levels
4. Verify all numeric values are displayed correctly
5. Test closing popups by clicking map

### Expected Results

- Popups open smoothly on click
- All information is accurate and readable
- Badge colors match hotspot colors
- Popups close properly
- No layout issues or overflow

---

## Test 5: Filters Update Map Data Dynamically

### Test Cases

- [ ] **5.1** City filter updates map:
  - [ ] Changing city triggers API call
  - [ ] Map re-centers on new city
  - [ ] Hotspots update for new city
- [ ] **5.2** Crime type filter works:
  - [ ] "All Crimes" shows all hotspots
  - [ ] Specific crime types filter correctly
  - [ ] Hotspot count updates
- [ ] **5.3** Time window filter works:
  - [ ] "24h" shows next 24 hours
  - [ ] "7d" shows next 7 days
  - [ ] "30d" shows next 30 days
- [ ] **5.4** Multiple filters work together:
  - [ ] City + Crime Type + Time Window
  - [ ] All filters apply simultaneously
- [ ] **5.5** Loading state displays during filter change
- [ ] **5.6** Map updates without full page reload
- [ ] **5.7** Filter state persists during navigation

### Manual Test Steps

1. Change city dropdown → verify map updates
2. Change crime type → verify hotspots update
3. Change time window → verify data refreshes
4. Combine multiple filters → verify all apply
5. Check Network tab for API calls
6. Verify loading indicator appears

### Expected Results

- Filters trigger API calls with correct parameters
- Map updates smoothly without flickering
- Loading state is visible during updates
- All filters work independently and together
- No duplicate API calls

---

## Test 6: Legend Displays Correctly

### Test Cases

- [ ] **6.1** Legend is visible on map
- [ ] **6.2** Legend shows all risk levels:
  - [ ] Critical (>80%) with red indicator
  - [ ] High (60-80%) with orange indicator
  - [ ] Medium (30-60%) with amber indicator
  - [ ] Low (<30%) with yellow indicator
- [ ] **6.3** Legend colors match hotspot colors
- [ ] **6.4** Legend is positioned correctly (bottom-right)
- [ ] **6.5** Legend is readable (proper contrast)
- [ ] **6.6** Legend doesn't obstruct map interaction
- [ ] **6.7** Legend styling is consistent

### Manual Test Steps

1. Check legend visibility on page load
2. Verify all four risk levels are shown
3. Compare legend colors with hotspot colors
4. Check legend positioning
5. Test map interaction near legend

### Expected Results

- Legend is clearly visible
- Colors match hotspot colors exactly
- Legend doesn't interfere with map
- Text is readable and well-formatted

---

## Test 7: Responsive Design Works on Different Screen Sizes

### Test Cases

- [ ] **7.1** Desktop view (1920x1080):
  - [ ] Map fills available space
  - [ ] Filters are in horizontal layout
  - [ ] All elements are visible
  - [ ] No horizontal scrolling
- [ ] **7.2** Tablet view (768x1024):
  - [ ] Map adapts to screen size
  - [ ] Filters stack vertically or wrap
  - [ ] Legend remains accessible
  - [ ] Popups are readable
- [ ] **7.3** Mobile view (375x667):
  - [ ] Map is still usable
  - [ ] Filters are mobile-friendly
  - [ ] Popups fit on screen
  - [ ] Legend is accessible
  - [ ] Touch interactions work
- [ ] **7.4** Window resizing:
  - [ ] Map resizes smoothly
  - [ ] No layout breaks
  - [ ] Elements reposition correctly
- [ ] **7.5** Text is readable at all sizes
- [ ] **7.6** Interactive elements are touch-friendly

### Manual Test Steps

1. Test on desktop (full screen)
2. Resize browser window to tablet size
3. Use browser dev tools device emulation
4. Test on actual mobile device (if available)
5. Check all breakpoints:
   - Desktop: > 1024px
   - Tablet: 768px - 1024px
   - Mobile: < 768px

### Expected Results

- Layout adapts to all screen sizes
- No horizontal scrolling
- All features remain accessible
- Touch targets are adequate size
- Text remains readable

---

## Additional Tests

### Performance

- [ ] Map loads in < 3 seconds
- [ ] API calls complete in < 500ms
- [ ] Smooth map interactions (no lag)
- [ ] No memory leaks during filter changes
- [ ] Efficient re-rendering (only updates when needed)

### Accessibility

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible
- [ ] Alt text for icons/images

### Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

### Error Handling

- [ ] Network errors handled gracefully
- [ ] Invalid API responses handled
- [ ] Empty data states handled
- [ ] Loading states display correctly
- [ ] Error messages are user-friendly

---

## Test Execution Template

```
Date: ___________
Tester: ___________
Browser: ___________
OS: ___________

Test Results:
[ ] Test 1: Backend Endpoint - PASS / FAIL
[ ] Test 2: Map Rendering - PASS / FAIL
[ ] Test 3: Color Coding - PASS / FAIL
[ ] Test 4: Popups - PASS / FAIL
[ ] Test 5: Filters - PASS / FAIL
[ ] Test 6: Legend - PASS / FAIL
[ ] Test 7: Responsive Design - PASS / FAIL

Issues Found:
1. ___________________________
2. ___________________________
3. ___________________________

Notes:
________________________________
________________________________
```

---

## Quick Test Script

Run this in browser console on crime map page:

```javascript
// Test 1: Check API response
fetch('http://localhost:8000/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    console.log('API Test:', {
      hasHotspots: Array.isArray(data.hotspots),
      hotspotCount: data.hotspots?.length,
      hasCoverageArea: !!data.coverage_area,
      firstHotspot: data.hotspots?.[0]
    });
  });

// Test 2: Check map element
const mapElement = document.querySelector('.leaflet-container');
console.log('Map Test:', {
  exists: !!mapElement,
  visible: mapElement?.offsetHeight > 0,
  width: mapElement?.offsetWidth,
  height: mapElement?.offsetHeight
});

// Test 3: Check filters
const filters = document.querySelectorAll('select, button[role="button"]');
console.log('Filters Test:', {
  count: filters.length,
  visible: Array.from(filters).every(f => f.offsetHeight > 0)
});
```

---

## Automated Test Files

See:
- `tests/test_crime_map_api.py` - Backend API tests
- `frontend/src/__tests__/CrimeHeatmap.test.jsx` - Frontend component tests

