# Quick Test 2 - Map Rendering

## 🎯 Test 2: Map Renders with Correct Center Coordinates

**Time:** ~2 minutes  
**Status:** 1 of 7 complete (6 remaining)

---

## Quick Checks (30 seconds)

### 1. Visual Check
- [ ] Map shows Chicago area (not random location)
- [ ] Map is centered (not off to the side)
- [ ] Map tiles load (no broken images)

### 2. Console Check
Press **F12** → Console tab:
- [ ] No red errors
- [ ] Map element exists

### 3. Interactive Check
- [ ] Can pan map (drag)
- [ ] Can zoom map (scroll)
- [ ] Smooth interaction (no lag)

### 4. Hotspots Check
- [ ] See colored circles on map
- [ ] Circles are semi-transparent
- [ ] Circles distributed across Chicago

---

## Console Script (Copy & Paste)

Open browser console (F12) and run:

```javascript
// Quick Test 2 Verification
console.log('=== TEST 2: Map Rendering ===');

// Check map element
const map = document.querySelector('.leaflet-container');
console.log('✅ Map exists:', !!map);
console.log('✅ Map visible:', map?.offsetHeight > 0);

// Check center coordinates
fetch('/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const center = data.coverage_area.center;
    const isChicago = Math.abs(center.lat - 41.8781) < 0.1 && 
                      Math.abs(center.lng - (-87.6298)) < 0.1;
    console.log('✅ Center:', center.lat, center.lng);
    console.log('✅ Chicago coordinates:', isChicago);
    console.log('✅ Hotspots:', data.hotspots.length);
  });

console.log('\n=== Visual Checks ===');
console.log('1. Map shows Chicago area?');
console.log('2. Can pan/zoom map?');
console.log('3. See colored hotspots?');
```

---

## Expected Results

- ✅ Map shows Chicago
- ✅ No console errors
- ✅ Map interactive
- ✅ Hotspots visible

---

## Next Test

**TEST 3:** Hotspots Display with Proper Color Coding  
**Time:** ~1 minute

---

**Progress: 1/7 tests complete (14%)**

