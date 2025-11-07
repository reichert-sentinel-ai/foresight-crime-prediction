# F2 Temporal Pattern Visualization - Testing Guide

## Overview
This document provides step-by-step testing instructions for Sprint F2: Temporal Crime Pattern Visualization feature.

**Total Test Cases: 10**

---

## Test Setup

### Prerequisites
1. Backend server running on `http://localhost:8000`
2. Frontend dev server running (typically `http://localhost:5173`)
3. Dependencies installed:
   - Backend: FastAPI, numpy, pandas, pydantic
   - Frontend: React, recharts, axios

### Starting Services

**Terminal 1 - Backend:**
```bash
cd project/repo-foresight/src/api
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd project/repo-foresight/frontend
npm install  # If recharts not installed yet
npm run dev
```

---

## Test Cases

### Test 1: Backend Endpoints Return Valid Temporal Data ✅

**Objective:** Verify all API endpoints return properly structured data

**Steps:**
1. Navigate to `http://localhost:8000/docs` (FastAPI Swagger UI)
2. Test each endpoint:

   **a) `/api/temporal/analysis`**
   - Click "Try it out"
   - Use default parameters or set:
     - crime_type: "all"
     - location: "downtown"
     - days_back: 30
   - Click "Execute"
   - **Expected:** Status 200, response contains:
     - `hourly_patterns`: Array of 24 objects with hour, incidents, avg_response_time, severity_score
     - `day_of_week_patterns`: Array of 7 objects with day, day_num, incidents, trend
     - `time_series`: Array of 30 objects with timestamp, actual_incidents, predicted_incidents, confidence_lower, confidence_upper, accuracy
     - `peak_times`: Object with "hours" and "days" arrays
     - `insights`: Array of strings
     - `seasonality_detected`: Boolean

   **b) `/api/temporal/forecast`**
   - Click "Try it out"
   - Use default parameters or set:
     - crime_type: "all"
     - location: "downtown"
     - forecast_days: 7
   - Click "Execute"
   - **Expected:** Status 200, response contains:
     - `forecast_period`: String
     - `generated_at`: ISO timestamp
     - `location`: String
     - `crime_type`: String
     - `forecasts`: Array of 7 objects with date, day_of_week, predicted_incidents, confidence, risk_level, recommended_patrol_units
     - `total_predicted`: Number
     - `avg_daily_incidents`: Number

   **c) `/api/temporal/anomalies`**
   - Click "Try it out"
   - Use default parameters or set:
     - days_back: 30
     - threshold: 2.0
   - Click "Execute"
   - **Expected:** Status 200, response contains:
     - `analysis_period_days`: Number
     - `threshold_std_dev`: Number
     - `anomalies_detected`: Number
     - `anomalies`: Array of objects with date, expected_incidents, actual_incidents, deviation, severity, possible_causes, similar_historical_events
     - `recommendation`: String

**Automated Test:**
```bash
cd project/repo-foresight
python test_temporal_api.py
```

**Pass Criteria:**
- ✅ All endpoints return 200 status
- ✅ Response structure matches expected schema
- ✅ All required fields present
- ✅ Data types are correct

---

### Test 2: Hourly Pattern Chart Displays Correctly ✅

**Objective:** Verify the 24-hour crime pattern chart renders with proper data visualization

**Steps:**
1. Navigate to `http://localhost:5173/temporal-patterns`
2. Wait for data to load (loading spinner should disappear)
3. Ensure "Hourly" tab is selected (default)
4. **Verify Chart Elements:**
   - Chart displays with 24 bars (one per hour)
   - Bars show incident counts (blue bars)
   - Line overlay shows severity scores (red line)
   - X-axis shows hours from 0:00 to 23:00
   - Left Y-axis labeled "Incidents"
   - Right Y-axis labeled "Severity"
   - Grid lines visible
   - Legend shows "Incidents" and "Severity"
5. **Verify Peak Hours Summary:**
   - Below chart, see "Peak Crime Hours" section
   - Badges display top 5 peak hours (e.g., "20:00 - 21:00")
   - Badges are red/destructive style

**Visual Checks:**
- ✅ Chart fills container width
- ✅ Bars are properly spaced
- ✅ Colors are distinct (blue bars, red line)
- ✅ Peak hours badges match highest incident hours

**Data Verification:**
- ✅ Highest bars typically in evening/night hours (18:00-23:00)
- ✅ Lower bars in morning hours (6:00-12:00)
- ✅ Severity line follows similar pattern to incidents

---

### Test 3: Day of Week Patterns Show Proper Trends ✅

**Objective:** Verify weekly pattern visualization displays correct trends

**Steps:**
1. Navigate to `/temporal-patterns`
2. Click on "Weekly" tab
3. **Verify Chart:**
   - Bar chart displays 7 bars (Monday through Sunday)
   - Bars are purple/violet colored
   - X-axis shows day names
   - Y-axis shows incident counts
   - Tooltip appears on hover
4. **Verify Weekly Summary Cards:**
   - Below chart, see grid of 7 cards (2 columns on mobile, 4 on desktop)
   - Each card shows:
     - Day name (small text)
     - Incident count (large, bold)
     - Trend badge (increasing/stable/decreasing)
   - Weekend days (Saturday, Sunday) should show higher incident counts
   - Weekday trend badges should show "decreasing" for Monday/Tuesday
   - Weekend trend badges should show "increasing"

**Visual Checks:**
- ✅ Weekend bars are taller than weekday bars
- ✅ Trend badges use correct colors:
  - Red (destructive) for "increasing"
  - Gray (secondary) for "stable"
  - Blue (default) for "decreasing"
- ✅ Cards are properly aligned in grid

**Data Verification:**
- ✅ Saturday and Sunday typically have highest incident counts
- ✅ Friday shows increasing trend
- ✅ Monday/Tuesday show decreasing trend

---

### Test 4: Time Series Shows Actual vs Predicted with Confidence Bands ✅

**Objective:** Verify time series forecast visualization with confidence intervals

**Steps:**
1. Navigate to `/temporal-patterns`
2. Click on "Forecast" tab
3. **Verify Area Chart:**
   - Chart displays time series data (last 14 days)
   - **Confidence Band:**
     - Light gray area shows confidence interval
     - Upper bound visible as shaded area
     - Lower bound creates the band effect
   - **Actual Line:**
     - Blue solid line shows actual incidents
     - Dots on line for data points
   - **Predicted Line:**
     - Green dashed line shows predicted incidents
     - Smooth curve following trend
4. **Verify Chart Elements:**
   - X-axis shows dates (formatted as "Jan 15", "Jan 16", etc.)
   - Y-axis shows incident counts
   - Legend shows "Actual", "Predicted", "Upper Confidence", "Lower Confidence"
   - Tooltip shows all values when hovering

**Visual Checks:**
- ✅ Actual line stays within confidence band (most points)
- ✅ Predicted line follows general trend of actual
- ✅ Confidence band is clearly visible but not overwhelming
- ✅ Lines are distinct (solid blue vs dashed green)

**Data Verification:**
- ✅ Confidence upper bound >= predicted >= confidence lower bound
- ✅ Actual values fluctuate around predicted
- ✅ Weekend dates show higher predicted values

---

### Test 5: Anomaly Detection Highlights Unusual Spikes ✅

**Objective:** Verify anomaly detection alerts display correctly

**Steps:**
1. Navigate to `/temporal-patterns`
2. Click on "Anomalies" tab
3. **Verify Anomaly Cards:**
   - Each anomaly displayed as an Alert card
   - Orange/yellow background (warning variant)
   - Alert triangle icon visible
4. **Verify Anomaly Details:**
   For each anomaly card, verify:
   - **Header:**
     - Full date (e.g., "Monday, January 15, 2024")
     - Severity badge (red "HIGH" badge)
   - **Metrics Grid:**
     - Expected incidents (number)
     - Actual incidents (number, highlighted in orange)
     - Deviation (e.g., "3.2σ")
   - **Possible Causes:**
     - List of badges showing possible causes
     - Examples: "Major sporting event", "Holiday weekend", "Increased foot traffic"
5. **Verify Recommendation:**
   - Bottom section shows recommendation text
   - Blue background
   - Actionable text (e.g., "Increase patrol presence during similar upcoming events")

**Visual Checks:**
- ✅ Anomaly cards stand out (orange/warning styling)
- ✅ High severity anomalies have red badges
- ✅ Actual incidents are highlighted differently from expected
- ✅ Cause badges are clearly readable

**Data Verification:**
- ✅ Actual incidents > Expected incidents (anomaly spike)
- ✅ Deviation values are reasonable (typically 2-4 standard deviations)
- ✅ Dates are in the past (within last 30 days)
- ✅ At least 2-3 anomalies displayed

---

### Test 6: Forecast Table Displays Upcoming Predictions ✅

**Objective:** Verify 7-day forecast table is accurate and readable

**Steps:**
1. Navigate to `/temporal-patterns`
2. Click on "Forecast" tab
3. Scroll down to "Next 7 Days Forecast" section
4. **Verify Table Structure:**
   - Table has 5 columns:
     - Date (formatted date)
     - Day (day of week name)
     - Predicted (number, right-aligned, bold)
     - Risk (centered badge)
     - Patrol Units (right-aligned number)
5. **Verify Table Data:**
   - 7 rows (one per day)
   - Dates are sequential (next 7 days from today)
   - Day names match dates correctly
   - Predicted incidents are reasonable numbers (80-200 range)
   - Risk levels:
     - "high" = red badge (predicted > 160)
     - "medium" = yellow badge (120 < predicted <= 160)
     - "low" = gray badge (predicted <= 120)
   - Patrol units calculated (typically 5-8 units)

**Visual Checks:**
- ✅ Table is responsive (scrollable on mobile)
- ✅ Header row has gray background
- ✅ Risk badges use correct colors
- ✅ Numbers are properly aligned
- ✅ Table is readable and well-spaced

**Data Verification:**
- ✅ Weekend days show higher predicted incidents
- ✅ Risk levels match predicted values correctly
- ✅ Patrol units scale with predicted incidents
- ✅ Dates are future dates (not past)

---

### Test 7: All Tabs Switch Smoothly ✅

**Objective:** Verify tab navigation works correctly

**Steps:**
1. Navigate to `/temporal-patterns`
2. **Test Tab Switching:**
   - Click "Hourly" tab → Chart changes to hourly view
   - Click "Weekly" tab → Chart changes to weekly view
   - Click "Forecast" tab → Chart changes to forecast view
   - Click "Anomalies" tab → View changes to anomalies list
3. **Verify Tab States:**
   - Active tab has white background
   - Active tab text is dark
   - Inactive tabs are gray
   - Icons appear next to tab labels
4. **Verify Content Loading:**
   - Each tab shows correct content
   - No content from previous tab visible
   - No flickering or delay when switching

**Visual Checks:**
- ✅ Active tab is clearly highlighted
- ✅ Smooth transitions between tabs
- ✅ Icons are visible and correctly sized
- ✅ Tab bar spans full width

**Functional Checks:**
- ✅ Clicking tab immediately shows new content
- ✅ No console errors when switching tabs
- ✅ URL doesn't change (single-page app)

---

### Test 8: Filters Update All Visualizations ✅

**Objective:** Verify crime type and location filters affect all visualizations

**Steps:**
1. Navigate to `/temporal-patterns`
2. **Test Crime Type Filter:**
   - Change crime type from "All Crimes" to "Theft"
   - **Expected:** Loading spinner appears briefly
   - **Verify updates:**
     - Hourly chart data changes
     - Weekly chart data changes
     - Forecast chart data changes
     - Forecast table updates
     - Insights panel updates
     - Peak hours may change
   - Change to "Assault", "Burglary", "Robbery" → same behavior
3. **Test Location Filter:**
   - Change location from "Downtown" to "North Side"
   - **Expected:** Loading spinner appears briefly
   - **Verify updates:**
     - All charts update
     - Forecast table updates
     - Insights update
   - Change to "South Side", "West Side" → same behavior
4. **Test Combined Filters:**
   - Set crime type to "Theft" and location to "North Side"
   - Verify all visualizations reflect both filters

**Visual Checks:**
- ✅ Loading spinner appears when filters change
- ✅ Charts update smoothly (no jarring transitions)
- ✅ Data values change appropriately

**Functional Checks:**
- ✅ API calls made with correct parameters
   - Check browser Network tab: requests include `crime_type` and `location` params
- ✅ No duplicate API calls
- ✅ Error handling works (try invalid filter values)

---

### Test 9: Charts Are Responsive and Interactive ✅

**Objective:** Verify charts adapt to screen size and respond to user interaction

**Steps:**
1. Navigate to `/temporal-patterns`
2. **Test Responsiveness:**
   - **Desktop (1920x1080):**
     - Charts fill container width
     - All elements visible and readable
   - **Tablet (768px width):**
     - Resize browser window to tablet size
     - Charts scale down appropriately
     - Text remains readable
     - Weekly summary cards show 2 columns
   - **Mobile (375px width):**
     - Resize to mobile size
     - Charts scroll horizontally if needed
     - Tab bar wraps if necessary
     - Forecast table scrolls horizontally
3. **Test Interactivity:**
   - **Hover on Chart Elements:**
     - Hourly chart: Hover over bars → tooltip shows hour, incidents, severity
     - Weekly chart: Hover over bars → tooltip shows day, incidents
     - Forecast chart: Hover over lines → tooltip shows date, actual, predicted, confidence bounds
   - **Tooltip Details:**
     - Tooltips appear on hover
     - Show formatted values
     - Include proper labels
     - Position correctly near cursor

**Visual Checks:**
- ✅ Charts resize smoothly when window resizes
- ✅ No horizontal scrolling on desktop
- ✅ Text doesn't overflow containers
- ✅ Charts maintain aspect ratio

**Functional Checks:**
- ✅ Tooltips trigger on hover
- ✅ Tooltips show correct data
- ✅ Tooltips disappear when mouse leaves
- ✅ Charts remain interactive at all sizes

---

### Test 10: Tooltips Show Detailed Information ✅

**Objective:** Verify tooltips provide comprehensive data on hover

**Steps:**
1. Navigate to `/temporal-patterns`
2. **Test Hourly Chart Tooltips:**
   - Hover over any bar in hourly chart
   - **Expected Tooltip:**
     - Header: "Hour: XX:00"
     - Incidents: [number]
     - Severity: [number]
     - Formatted correctly
3. **Test Weekly Chart Tooltips:**
   - Hover over any bar in weekly chart
   - **Expected Tooltip:**
     - Day name
     - Incidents count
     - Clean formatting
4. **Test Forecast Chart Tooltips:**
   - Hover over actual line (blue)
   - **Expected:** Shows date, actual incidents
   - Hover over predicted line (green dashed)
   - **Expected:** Shows date, predicted incidents
   - Hover over confidence area
   - **Expected:** Shows upper/lower confidence bounds
5. **Verify Tooltip Formatting:**
   - Values are formatted as numbers (no decimals for counts)
   - Dates formatted as readable dates
   - Labels are clear and descriptive
   - Colors match chart elements

**Visual Checks:**
- ✅ Tooltips appear near cursor
- ✅ Tooltips don't overflow viewport
- ✅ Tooltips have readable font size
- ✅ Tooltips have proper background/padding

**Functional Checks:**
- ✅ Tooltips update in real-time as cursor moves
- ✅ Tooltips show correct data for hovered element
- ✅ Multiple tooltips work (when hovering close elements)

---

## Automated Testing

### Running Backend API Tests

```bash
cd project/repo-foresight
python test_temporal_api.py
```

**Expected Output:**
```
============================================================
TEMPORAL PATTERNS API TEST SUITE
============================================================

============================================================
Testing /api/temporal/analysis endpoint
============================================================
✅ All validations passed!
   - Hourly patterns: 24 entries
   - Day patterns: 7 entries
   - Time series points: 30 entries
   - Peak hours: [20, 21, 19, 22, 23]
   - Peak days: ['Saturday', 'Sunday', 'Friday']
   - Insights: 5 items

============================================================
Testing /api/temporal/forecast endpoint
============================================================
✅ All validations passed!
   - Forecast period: 7 days
   - Number of forecasts: 7
   - Total predicted incidents: 840
   - Average daily incidents: 120.0

============================================================
Testing /api/temporal/anomalies endpoint
============================================================
✅ All validations passed!
   - Analysis period: 30 days
   - Threshold: 2.0σ
   - Anomalies detected: 3
   - Recommendation: Increase patrol presence during similar upcoming events

============================================================
Testing query parameter variations
============================================================
✅ All query parameter variations work correctly!

============================================================
TEST SUMMARY
============================================================
✅ PASSED: Temporal Analysis
✅ PASSED: Forecast
✅ PASSED: Anomalies
✅ PASSED: Query Parameters

Total: 4/4 tests passed

🎉 All tests passed! Backend endpoints are working correctly.
```

---

## Test Checklist Summary

| # | Test Case | Type | Status |
|---|-----------|------|--------|
| 1 | Backend endpoints return valid temporal data | API | ⬜ |
| 2 | Hourly pattern chart displays correctly | UI | ⬜ |
| 3 | Day of week patterns show proper trends | UI | ⬜ |
| 4 | Time series shows actual vs predicted with confidence bands | UI | ⬜ |
| 5 | Anomaly detection highlights unusual spikes | UI | ⬜ |
| 6 | Forecast table displays upcoming predictions | UI | ⬜ |
| 7 | All tabs switch smoothly | UI | ⬜ |
| 8 | Filters update all visualizations | Functional | ⬜ |
| 9 | Charts are responsive and interactive | Responsive | ⬜ |
| 10 | Tooltips show detailed information | UI | ⬜ |

**Total: 10 Test Cases**

---

## Common Issues & Solutions

### Issue: Charts not displaying
**Solution:** Check browser console for errors. Verify recharts is installed: `npm install recharts`

### Issue: API calls failing
**Solution:** Verify backend is running on port 8000. Check CORS settings in main.py.

### Issue: Tooltips not appearing
**Solution:** Verify mouse events are working. Check recharts version compatibility.

### Issue: Filter changes not updating charts
**Solution:** Check browser Network tab to verify API calls are being made. Verify useEffect dependencies.

### Issue: Responsive layout breaking
**Solution:** Check Tailwind CSS classes. Verify ResponsiveContainer from recharts is used.

---

## Success Criteria

All tests pass when:
- ✅ Backend returns valid data structures
- ✅ All charts render without errors
- ✅ Data visualizations are accurate
- ✅ Filters work correctly
- ✅ UI is responsive and accessible
- ✅ No console errors or warnings
- ✅ Performance is acceptable (< 2s load time)

---

## Next Steps After Testing

1. Document any bugs found
2. Create GitHub issues for failures
3. Update test cases if requirements change
4. Add automated E2E tests (optional)
5. Performance testing (optional)

