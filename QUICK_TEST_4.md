# Quick Test 4 - Popups

## 🎯 TEST 4: Popups Show Detailed Prediction Information

**Time:** ~2 minutes  
**Status:** 3 of 7 complete (4 remaining)

---

## Quick Checks (1 minute)

### 1. Click Test
- [ ] Click on any hotspot → popup appears
- [ ] Popup positioned near hotspot
- [ ] Popup is visible and readable

### 2. Content Check
Read the popup and verify:
- [ ] **Grid ID** (e.g., "Grid: grid_0_0")
- [ ] **Risk Level Badge** (e.g., "CRITICAL", "HIGH", "MEDIUM", "LOW")
- [ ] **Predicted Incidents** (e.g., "Predicted Incidents: 8")
- [ ] **Intensity** (e.g., "Intensity: 85%")
- [ ] **Confidence** (e.g., "Confidence: 92%")
- [ ] **Crime Type** (e.g., "Crime Type: theft")

### 3. Badge Color Test
- [ ] Click red hotspot → red badge
- [ ] Click orange hotspot → orange badge
- [ ] Click yellow hotspot → yellow badge
- [ ] Badge color matches hotspot color

### 4. Close Test
- [ ] Click outside popup → popup closes
- [ ] Click another hotspot → popup switches
- [ ] Smooth transitions

---

## Console Script (Copy & Paste)

Open browser console (F12) and run:

```javascript
// Test 4: Popup Data Verification
fetch('/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const h = data.hotspots[0];
    console.log('✅ Expected Popup Content:');
    console.log('  Grid ID: Grid:', h.grid_id);
    console.log('  Risk Level:', h.risk_level.toUpperCase());
    console.log('  Predicted Incidents:', h.predicted_incidents);
    console.log('  Intensity:', (h.intensity * 100).toFixed(0) + '%');
    console.log('  Confidence:', (h.confidence * 100).toFixed(0) + '%');
    console.log('  Crime Type:', h.crime_type);
    console.log('\n✅ Compare with popup values');
  });
```

---

## Required Fields Checklist

When you click a hotspot, the popup should show:

1. ✅ **Grid ID** - "Grid: grid_X_Y"
2. ✅ **Risk Level Badge** - "CRITICAL/HIGH/MEDIUM/LOW" (colored)
3. ✅ **Predicted Incidents** - "Predicted Incidents: [number]"
4. ✅ **Intensity** - "Intensity: [percentage]%"
5. ✅ **Confidence** - "Confidence: [percentage]%"
6. ✅ **Crime Type** - "Crime Type: [type]"

---

## Expected Results

- ✅ Popup opens on click
- ✅ All 6 fields present
- ✅ Badge color matches hotspot
- ✅ Values match API data
- ✅ Popup closes properly

---

## Next Test

**TEST 5:** Filters Update Map Data Dynamically  
**Time:** ~1 minute

---

**Progress: 3/7 tests complete (43%)**

