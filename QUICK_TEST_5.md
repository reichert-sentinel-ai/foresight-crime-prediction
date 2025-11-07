# Quick Test 5 - Filters

## 🎯 TEST 5: Filters Update Map Data Dynamically

**Time:** ~2 minutes  
**Status:** 4 of 7 complete (3 remaining)

---

## Quick Checks (1 minute)

### 1. Network Tab Setup
- [ ] Open DevTools (F12)
- [ ] Click Network tab
- [ ] Clear existing requests

### 2. City Filter Test
- [ ] Change City dropdown → Watch Network tab
- [ ] New API call appears with `city=...`
- [ ] Map updates

### 3. Crime Type Filter Test
- [ ] Change Crime Type dropdown → Watch Network tab
- [ ] New API call appears with `crime_type=...`
- [ ] Map updates

### 4. Time Window Filter Test
- [ ] Change Time Window dropdown → Watch Network tab
- [ ] New API call appears with `time_window=...`
- [ ] Map updates

### 5. Multiple Filters Test
- [ ] Set all three filters → Watch Network tab
- [ ] Single API call with all parameters
- [ ] Map updates with all filters

### 6. Loading State Check
- [ ] Change filter → Loading spinner appears
- [ ] Spinner disappears when map updates

---

## Network Tab Checklist

When you change a filter, check Network tab:

- [ ] Request appears: `/api/crime-map/hotspots?city=...&crime_type=...&time_window=...`
- [ ] Status: **200 OK**
- [ ] Response time: < 500ms
- [ ] Parameters match your selection

---

## Expected Results

- ✅ Filters trigger API calls
- ✅ Request URLs include correct parameters
- ✅ Map updates dynamically
- ✅ Loading state appears
- ✅ No full page reload

---

## Quick Answer

1. Change a filter → Does API call appear in Network tab? (yes/no)
2. Does map update when filter changes? (yes/no)
3. Does loading spinner appear? (yes/no)

If all are yes → TEST 5 passes.

---

## Next Test

**TEST 6:** Legend Displays Correctly  
**Time:** ~30 seconds

---

**Progress: 4/7 tests complete (57%)**

