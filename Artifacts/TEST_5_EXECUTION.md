# TEST 5: Filters Update Map Data Dynamically

## Current Status: 4 of 7 Tests Complete (3 Remaining)

### ✅ Completed
- TEST 1: Backend Endpoint Returns Valid Heatmap Data - **PASSED**
- TEST 2: Map Renders with Correct Center Coordinates - **PASSED**
- TEST 3: Hotspots Display with Proper Color Coding - **PASSED**
- TEST 4: Popups Show Detailed Prediction Information - **PASSED**

### ⏳ Remaining (3 tests)
- **TEST 5:** Filters Update Map Data Dynamically ← **YOU ARE HERE**
- TEST 6: Legend Displays Correctly
- TEST 7: Responsive Design Works on Different Screen Sizes

---

## TEST 5: Step-by-Step Execution

### Goal
Verify filters trigger API calls and update map dynamically when changed.

---

### Step 5.1: Open Network Tab

**Action:**
1. Open browser DevTools (Press F12)
2. Click "Network" tab
3. Clear existing requests (click trash icon or right-click → Clear)
4. Keep Network tab open

**What to Look For:**
- ✅ Network tab is open
- ✅ Ready to see API calls
- ✅ Previous requests cleared

**Check:** ✅ Network tab ready

---

### Step 5.2: Test City Filter

**Action:**
1. Find the "City" dropdown (top of page)
2. Change from "Chicago" to "New York" (or another city)
3. Watch Network tab

**What to Look For:**
- ✅ New request appears in Network tab
- ✅ Request URL: `/api/crime-map/hotspots?city=new-york&...`
- ✅ Map updates (may re-center on new city)
- ✅ Hotspots update
- ✅ Loading indicator appears briefly

**Check in Network Tab:**
- ✅ Request appears in list
- ✅ Status: 200 OK
- ✅ Request URL includes `city=new-york` (or other city)

**Check:** ✅ City filter triggers API call

---

### Step 5.3: Test Crime Type Filter

**Action:**
1. Find the "Crime Type" dropdown
2. Change from "All Crimes" to "Theft"
3. Watch Network tab

**What to Look For:**
- ✅ New request appears
- ✅ Request URL includes `crime_type=theft`
- ✅ Map updates
- ✅ Hotspot count may change
- ✅ Hotspots update

**Check in Network Tab:**
- ✅ Request URL: `/api/crime-map/hotspots?city=...&crime_type=theft&...`
- ✅ Status: 200 OK
- ✅ Response time < 500ms

**Test Multiple Values:**
1. "All Crimes" → Should show all hotspots
2. "Theft" → Should filter to theft only
3. "Assault" → Should filter to assault only
4. "Burglary" → Should filter to burglary only

**Check:** ✅ Crime type filter works

---

### Step 5.4: Test Time Window Filter

**Action:**
1. Find the "Time Window" dropdown
2. Change from "Next 24 Hours" to "Next 7 Days"
3. Watch Network tab

**What to Look For:**
- ✅ New request appears
- ✅ Request URL includes `time_window=7d`
- ✅ Map updates
- ✅ Data refreshes

**Test All Options:**
1. "Next 24 Hours" (24h)
2. "Next 7 Days" (7d)
3. "Next 30 Days" (30d)

**Check in Network Tab:**
- ✅ Request URL includes `time_window=7d`
- ✅ Status: 200 OK

**Check:** ✅ Time window filter works

---

### Step 5.5: Test Multiple Filters Together

**Action:**
1. Set City: "Chicago"
2. Set Crime Type: "Theft"
3. Set Time Window: "Next 7 Days"
4. Watch Network tab

**What to Look For:**
- ✅ Single API call (not multiple)
- ✅ Request URL includes all parameters: `?city=chicago&crime_type=theft&time_window=7d`
- ✅ Map updates with all filters applied
- ✅ Hotspots reflect all filters

**Check in Network Tab:**
```
Request URL: /api/crime-map/hotspots?city=chicago&crime_type=theft&time_window=7d
Status: 200 OK
```

**Verify Response:**
- ✅ Response is valid JSON
- ✅ Hotspots match all filter criteria
- ✅ Count is appropriate for filters

**Check:** ✅ Multiple filters work together

---

### Step 5.6: Check Loading State

**Action:**
1. Change a filter
2. Watch for loading indicator

**What to Look For:**
- ✅ Loading spinner appears (briefly)
- ✅ Spinner disappears when map updates
- ✅ No flickering or white screen
- ✅ Smooth transition

**Visual Check:**
- ✅ Spinner visible during API call
- ✅ Spinner disappears when map updates
- ✅ Smooth transition (no flash)

**Check:** ✅ Loading state displays

---

### Step 5.7: Verify No Full Page Reload

**Action:**
1. Change a filter
2. Observe page behavior

**What to Look For:**
- ✅ Page doesn't reload (URL doesn't change)
- ✅ Only map updates (not entire page)
- ✅ No page flash or white screen
- ✅ Smooth update

**Check:**
- ✅ URL stays the same (no page refresh)
- ✅ Only map area updates
- ✅ No full page reload

**Check:** ✅ No full page reload

---

## TEST 5 Checklist

- [ ] **5.1** City filter triggers API call
- [ ] **5.2** Crime type filter works
- [ ] **5.3** Time window filter works
- [ ] **5.4** Multiple filters work together
- [ ] **5.5** Loading state displays
- [ ] **5.6** No full page reload
- [ ] **5.7** API calls have correct parameters

---

## Quick Test Script

Run this in browser console (F12) while testing filters:

```javascript
// Test 5: Filter Updates
console.log('=== TEST 5: Filters ===');
console.log('1. Open Network tab (F12 → Network)');
console.log('2. Change City dropdown → Check Network tab for API call');
console.log('3. Change Crime Type dropdown → Check Network tab');
console.log('4. Change Time Window dropdown → Check Network tab');
console.log('5. Verify request URLs include correct parameters');
```

**Network Tab Check:**
- Look for requests to `/api/crime-map/hotspots`
- Check query parameters in request URL
- Verify status is 200 OK

---

## Expected Results Summary

- ✅ Filters trigger API calls
- ✅ Request URLs include correct parameters
- ✅ Map updates when filters change
- ✅ Loading state displays
- ✅ No full page reload
- ✅ All filters work independently and together
- ✅ API calls complete successfully (200 OK)

---

## Next Steps

After completing TEST 5:
- **TEST 6:** Legend Displays Correctly
- Then 1 more test remains

---

## Progress: 4/7 Complete (57%)

**Current:** TEST 5 - Filters  
**Remaining:** 3 tests (6, 7)

