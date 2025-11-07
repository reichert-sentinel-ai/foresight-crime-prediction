# TEST 7: Mobile Testing Checklist (On Your Android Phone)

## ✅ Setup Complete
- ✅ Same network (confirmed)
- ✅ Chrome browser (confirmed)
- ✅ Page loads on phone: `http://192.168.1.161:5173/crime-map` (confirmed)

---

## TEST 7: Step-by-Step Mobile Testing

### Step 7.3: Mobile Layout Test

**On Your Android Phone:**

1. **Check Filter Layout:**
   - [ ] Filters stack vertically (one per row)
   - [ ] Each filter takes full width
   - [ ] Filters are not cramped or overlapping

2. **Check Map Display:**
   - [ ] Map is visible and fills the screen
   - [ ] Map is not cut off
   - [ ] Map is properly sized

3. **Check Legend:**
   - [ ] Legend is visible (bottom-right corner)
   - [ ] Legend is readable on mobile
   - [ ] Legend doesn't overlap with map controls

4. **Check Info Panel:**
   - [ ] Info panel is visible (top-left corner)
   - [ ] Info panel is readable on mobile
   - [ ] Info panel doesn't block important map areas

5. **Check Horizontal Scrolling:**
   - [ ] NO horizontal scrolling required
   - [ ] All content fits within screen width
   - [ ] No elements overflow horizontally

6. **Check Text Readability:**
   - [ ] All text is readable (not too small)
   - [ ] Labels are clear
   - [ ] No text is cut off

---

### Step 7.4: Mobile Interactions Test

**On Your Android Phone:**

1. **Test Dropdowns:**
   - [ ] Tap "City" dropdown → Opens and shows options
   - [ ] Tap "Crime Type" dropdown → Opens and shows options
   - [ ] Tap "Time Window" dropdown → Opens and shows options
   - [ ] Can select an option from each dropdown

2. **Test Map Interactions:**
   - [ ] Pinch to zoom IN → Map zooms in
   - [ ] Pinch to zoom OUT → Map zooms out
   - [ ] Drag to pan → Map moves
   - [ ] Double-tap to zoom → Map zooms

3. **Test Hotspots (if visible):**
   - [ ] Tap on a hotspot → Popup appears
   - [ ] Popup shows crime information
   - [ ] Can close popup (tap outside or X button)

**Note:** If page shows "No data available", that's OK - you can still test:
- ✅ Layout and responsiveness
- ✅ Text readability
- ✅ No horizontal scrolling
- ✅ Dropdown interactions
- ✅ Map zoom/pan interactions

---

## Quick Test Checklist

### Layout (Visual Check)
- [ ] Filters stack vertically
- [ ] Map fills screen
- [ ] Legend visible
- [ ] Info panel visible
- [ ] No horizontal scrolling
- [ ] Text readable

### Interactions (Touch Test)
- [ ] Dropdowns work (tap to open)
- [ ] Map zooms (pinch/zoom)
- [ ] Map pans (drag)
- [ ] Hotspots clickable (if visible)

---

## Expected Results

**Layout:**
- ✅ Filters stack vertically on mobile
- ✅ Map fills screen appropriately
- ✅ Legend and info panel remain visible
- ✅ No horizontal scrolling required
- ✅ Text is readable

**Interactions:**
- ✅ All dropdowns work with touch
- ✅ Map zoom/pan works with touch gestures
- ✅ Hotspots are tappable (if visible)

---

## If Page Shows "No Data Available"

**This is expected!** The backend API calls won't work from your phone because:
- Backend is on `localhost:8000` (only accessible from your computer)
- You can still test all frontend features:
  - ✅ Responsive layout
  - ✅ Mobile interactions
  - ✅ Text readability
  - ✅ No horizontal scrolling
  - ✅ Dropdown functionality

---

## TEST 7 Completion

**If all items are checked:**
- ✅ **TEST 7 PASSES**

**Report back:**
- Which items passed?
- Any issues found?
- Screenshots helpful (optional)

---

## Next: All Tests Complete! 🎉

After TEST 7 passes:
- **7/7 tests complete!**
- Crime heatmap feature is fully tested
- Ready for deployment

