# Quick Test 3 - Color Coding

## 🎯 TEST 3: Hotspots Display with Proper Color Coding

**Time:** ~2 minutes  
**Status:** 2 of 7 complete (5 remaining)

---

## Quick Visual Checks (1 minute)

### 1. Color Identification
Look at the map and identify:
- [ ] **Red circles** = Critical hotspots (darkest)
- [ ] **Orange circles** = High risk hotspots
- [ ] **Amber/yellow circles** = Medium risk hotspots
- [ ] **Light yellow circles** = Low risk hotspots (lightest)

### 2. Size Correlation
- [ ] Larger circles have higher intensity (darker colors)
- [ ] Smaller circles have lower intensity (lighter colors)

### 3. Click Test
Click on different colored hotspots:
- [ ] Red hotspot → intensity > 80% in popup
- [ ] Orange hotspot → intensity 60-80% in popup
- [ ] Yellow hotspot → intensity < 30% in popup

### 4. Opacity Check
- [ ] Circles are semi-transparent (can see map underneath)
- [ ] Not completely opaque or transparent

---

## Console Script (Copy & Paste)

Open browser console (F12) and run:

```javascript
// Quick Test 3: Color Coding
fetch('/api/crime-map/hotspots')
  .then(r => r.json())
  .then(data => {
    const risks = {critical: 0, high: 0, medium: 0, low: 0};
    data.hotspots.forEach(h => risks[h.risk_level]++);
    
    console.log('✅ Color Distribution:');
    console.log('  Critical (red):', risks.critical);
    console.log('  High (orange):', risks.high);
    console.log('  Medium (amber):', risks.medium);
    console.log('  Low (yellow):', risks.low);
    
    const sample = data.hotspots.find(h => h.risk_level === 'critical');
    if (sample) {
      console.log('\n✅ Sample Critical:');
      console.log('  Intensity:', sample.intensity, '(should be > 0.8)');
      console.log('  Match:', sample.intensity > 0.8);
    }
  });
```

---

## Color Reference

| Color | Risk Level | Intensity Range | Expected Look |
|-------|-----------|-----------------|---------------|
| Red | Critical | > 0.8 (>80%) | Dark red, largest circles |
| Orange | High | 0.6-0.8 (60-80%) | Orange, medium-large circles |
| Amber | Medium | 0.3-0.6 (30-60%) | Amber/yellow, medium circles |
| Yellow | Low | ≤ 0.3 (<30%) | Light yellow, smaller circles |

---

## Expected Results

- ✅ Multiple colors visible (red, orange, amber, yellow)
- ✅ Colors match risk levels
- ✅ Circle sizes correlate with intensity
- ✅ Semi-transparent (can see map)

---

## Next Test

**TEST 4:** Popups Show Detailed Prediction Information  
**Time:** ~1 minute

---

**Progress: 2/7 tests complete (29%)**

