# Sprint F3: Bias Analysis Dashboard - Testing Checklist

## Overview
Comprehensive testing checklist for the Bias Analysis Dashboard feature. This ensures all fairness metrics, visualizations, and ethical AI features work correctly.

---

## Pre-Testing Setup

### 1. Backend Server
```bash
cd project/repo-foresight
# Activate virtual environment if needed
cd src/api
uvicorn main:app --reload --port 8000
```

**Verify:** Backend starts without errors  
**Expected:** Server running on http://localhost:8000

### 2. Frontend Server
```bash
cd project/repo-foresight/frontend
npm run dev
```

**Verify:** Frontend starts without errors  
**Expected:** Server running on http://localhost:5173

### 3. API Endpoints Test
```bash
# Test bias analysis endpoint
curl http://localhost:8000/api/bias/analysis

# Test interventions endpoint
curl http://localhost:8000/api/bias/interventions

# Test with parameters
curl "http://localhost:8000/api/bias/analysis?model_version=v2.3.1&include_historical=true"
```

**Verify:** All endpoints return valid JSON  
**Expected:** Response with demographic_metrics, fairness_metrics, historical_trends

---

## Visual Testing Checklist

### ✅ 1. Fairness Score Display

**Location:** Top of dashboard, prominent card

**Test Steps:**
1. Navigate to http://localhost:5173/bias-analysis
2. Locate the "Overall Fairness Score" section
3. Check display elements

**Verification Points:**
- [ ] Score displays as "X/100" format (e.g., "85.0/100")
- [ ] Progress bar is visible and reflects score percentage
- [ ] Progress bar color is appropriate (blue gradient)
- [ ] Model version displays correctly (e.g., "v2.3.1")
- [ ] Analysis date displays in readable format
- [ ] Next audit date displays correctly
- [ ] Audit status badge shows "PASSED", "CONDITIONAL PASS", or "FAILED"
- [ ] Badge color matches status (green/yellow/red)
- [ ] Metrics status icons display for all 5 fairness metrics
- [ ] Icons show correct status (checkmark/warning/error)

**Expected Result:** All elements visible, properly formatted, and color-coded

---

### ✅ 2. Demographic Comparison Chart

**Location:** Demographics tab → "Demographic Parity Analysis" card

**Test Steps:**
1. Click "Demographics" tab
2. Locate the bar chart showing Population % vs Prediction %

**Verification Points:**
- [ ] Chart renders without errors
- [ ] X-axis shows all 4 demographic groups (White, Black, Hispanic, Asian)
- [ ] Two bars per group: "Population %" and "Prediction %"
- [ ] Bars are color-coded (gray for Population, blue for Prediction)
- [ ] Y-axis shows percentage scale (0-100%)
- [ ] Tooltip appears on hover showing exact values
- [ ] Legend displays both bar types
- [ ] Chart is responsive (resizes with window)
- [ ] Info box below chart explains ideal parity
- [ ] Info box is readable and properly styled

**Expected Result:** Chart clearly shows parity comparison, easy to interpret

**Data Validation:**
- [ ] Population percentages sum to ~100% (allow small rounding differences)
- [ ] Prediction percentages are within reasonable range (0-100%)
- [ ] Parity ratios can be calculated from displayed values

---

### ✅ 3. Fairness Metrics Status Badges

**Location:** Fairness Metrics tab

**Test Steps:**
1. Click "Fairness Metrics" tab
2. Review each metric card

**Verification Points for Each Metric:**

**Demographic Parity:**
- [ ] Card displays with correct status color background
- [ ] Status icon shows (checkmark/warning/error)
- [ ] Metric name displays: "Demographic Parity"
- [ ] Description text is visible and readable
- [ ] Current value displays as percentage (e.g., "85.0%")
- [ ] Threshold displays as percentage (e.g., "80%")
- [ ] Status badge shows "PASS", "WARNING", or "FAIL"
- [ ] Badge color matches status
- [ ] Progress bar shows value relative to threshold

**Equal Opportunity:**
- [ ] All above checks apply
- [ ] Value and threshold are appropriate for FNR parity

**Equalized Odds:**
- [ ] All above checks apply
- [ ] Value reflects combined FPR/FNR parity

**Predictive Parity:**
- [ ] All above checks apply
- [ ] Value reflects precision equality

**Calibration:**
- [ ] All above checks apply
- [ ] Value reflects probability calibration

**Overall:**
- [ ] All 5 metrics display correctly
- [ ] Status colors are consistent (green/orange/red)
- [ ] Icons are properly aligned
- [ ] Text is readable in both light and dark mode

**Expected Result:** Each metric clearly shows pass/warning/fail status with intuitive color coding

---

### ✅ 4. Radar Chart Performance Comparison

**Location:** Demographics tab → "Performance Comparison" card

**Test Steps:**
1. Click "Demographics" tab
2. Locate the radar chart (right side)

**Verification Points:**
- [ ] Radar chart renders without errors
- [ ] 4 axes visible: Accuracy, Precision, Recall, Parity
- [ ] 4 data series (one per demographic group)
- [ ] Each group has distinct color:
  - White: Blue (#3b82f6)
  - Black: Purple (#8b5cf6)
  - Hispanic: Green (#10b981)
  - Asian: Orange (#f59e0b)
- [ ] Legend displays all 4 groups with correct colors
- [ ] Tooltip shows values on hover
- [ ] Chart is responsive
- [ ] Values are within 0-100% range
- [ ] Overlapping areas show transparency (fillOpacity)
- [ ] Polar grid lines are visible

**Expected Result:** Multi-dimensional view clearly shows performance differences across groups

**Data Validation:**
- [ ] Each group shows 4 metrics (Accuracy, Precision, Recall, Parity)
- [ ] Values match the detailed metrics table
- [ ] Chart updates if data changes

---

### ✅ 5. Historical Trends (90-Day Progression)

**Location:** Historical Trends tab

**Test Steps:**
1. Click "Historical Trends" tab
2. Review the line chart

**Verification Points:**
- [ ] Line chart renders without errors
- [ ] X-axis shows dates (last 90 days, ~10-day intervals)
- [ ] Y-axis shows parity ratio percentage (60-100% range)
- [ ] 4 lines visible (one per demographic group)
- [ ] Each line has distinct color matching demographic colors
- [ ] Lines show trend progression (generally upward)
- [ ] Tooltip displays date, group, and parity value on hover
- [ ] Legend shows all 4 groups
- [ ] Grid lines are visible
- [ ] Chart is responsive
- [ ] "Positive Trend Detected" info box appears below chart
- [ ] Info box shows improvement percentage (~18%)
- [ ] Info box is properly styled (green background)

**Data Validation:**
- [ ] Approximately 9 data points per group (90 days / 10-day intervals)
- [ ] Dates are chronological
- [ ] Parity ratios generally increase over time
- [ ] All values are within 0-1 range (before percentage conversion)

**Expected Result:** Clear visualization of fairness improvements over time

---

### ✅ 6. Interventions Before/After Display

**Location:** Interventions tab

**Test Steps:**
1. Click "Interventions" tab
2. Review each intervention card

**Verification Points for Each Intervention:**

**Data Rebalancing (2024-08-15):**
- [ ] Card displays with proper styling
- [ ] Intervention type shows: "Data Rebalancing"
- [ ] Date displays: "8/15/2024" (or locale format)
- [ ] Improvement badge shows "+X%" (e.g., "+22.2%")
- [ ] Before value displays: "72%" (red color)
- [ ] After value displays: "88%" (green color)
- [ ] Affected groups show: "Black", "Hispanic" badges
- [ ] Badges are properly styled

**Feature Engineering Review (2024-09-01):**
- [ ] All above checks apply
- [ ] Shows improvement from 78% to 91%
- [ ] Affected group: "Asian"

**Threshold Calibration (2024-10-10):**
- [ ] All above checks apply
- [ ] Shows improvement from 81% to 93%
- [ ] Affected groups: All 4 groups

**Overall:**
- [ ] All 3 interventions display
- [ ] Before/after comparison is clear
- [ ] Improvement percentages are accurate
- [ ] Color coding is intuitive (red before, green after)
- [ ] Cards are properly spaced

**Expected Result:** Clear visualization of intervention impact with before/after comparison

---

### ✅ 7. Recommendations Categorized by Severity

**Location:** Recommendations tab

**Test Steps:**
1. Click "Recommendations" tab
2. Review recommendation alerts

**Verification Points:**

**CRITICAL Recommendations:**
- [ ] Display with red border and red background
- [ ] Alert icon is red warning triangle
- [ ] Text starts with "CRITICAL:"
- [ ] Message describes critical issue
- [ ] Actionable steps are provided

**WARNING Recommendations:**
- [ ] Display with orange border and orange background
- [ ] Alert icon is orange warning triangle
- [ ] Text starts with "WARNING:"
- [ ] Message describes warning condition
- [ ] Actionable steps are provided

**General Recommendations:**
- [ ] Display with blue border and blue background
- [ ] Alert icon is blue lightbulb
- [ ] Text is informational
- [ ] Best practices are listed

**Ethical AI Best Practices Section:**
- [ ] Purple background section appears
- [ ] Shield icon displays
- [ ] Heading: "Ethical AI Best Practices"
- [ ] 4 bullet points with checkmark icons:
  - [ ] Community stakeholder engagement
  - [ ] Transparent documentation
  - [ ] Quarterly audits
  - [ ] Continuous monitoring

**Overall:**
- [ ] All recommendations display
- [ ] Severity categorization is clear
- [ ] Color coding matches severity (red/orange/blue)
- [ ] Text is readable
- [ ] Icons are properly aligned

**Expected Result:** Recommendations are clearly prioritized and actionable

---

### ✅ 8. Tab Switching Functionality

**Location:** Main dashboard tabs

**Test Steps:**
1. Navigate to dashboard
2. Click each tab sequentially

**Verification Points:**
- [ ] Click "Demographics" tab → Content loads, tab highlights
- [ ] Click "Fairness Metrics" tab → Content loads, tab highlights
- [ ] Click "Historical Trends" tab → Content loads, tab highlights
- [ ] Click "Interventions" tab → Content loads, tab highlights
- [ ] Click "Recommendations" tab → Content loads, tab highlights
- [ ] Only one tab is active at a time
- [ ] Active tab has white/dark background
- [ ] Inactive tabs are grayed out
- [ ] Transition is smooth (no jarring changes)
- [ ] Content loads immediately (no loading delays)
- [ ] Browser back/forward buttons work correctly
- [ ] Direct URL navigation works (e.g., /bias-analysis#demographics)

**Expected Result:** Smooth tab switching with visual feedback

---

### ✅ 9. Detailed Metrics Table Readability

**Location:** Demographics tab → "Detailed Performance Metrics by Demographic" card

**Test Steps:**
1. Click "Demographics" tab
2. Scroll to metrics table

**Verification Points:**

**Table Structure:**
- [ ] Table renders without errors
- [ ] Header row is visible with gray background
- [ ] Columns: Group, Accuracy, Precision, Recall, FPR, FNR, Parity Ratio
- [ ] Header text is bold and readable
- [ ] 4 data rows (one per demographic group)

**Data Display:**
- [ ] Group column shows colored dot + name
- [ ] Colored dots match chart colors
- [ ] Accuracy values show as percentage (e.g., "85.0%")
- [ ] Precision values show as percentage
- [ ] Recall values show as percentage
- [ ] FPR values show as percentage
- [ ] FNR values show as percentage
- [ ] Parity Ratio shows as badge with percentage

**Formatting:**
- [ ] Numbers are right-aligned
- [ ] Percentages have 1 decimal place
- [ ] High FPR (>15%) values are highlighted in red
- [ ] High FNR (>18%) values are highlighted in red
- [ ] Parity badges show correct color:
  - Green (≥85%)
  - Yellow (75-85%)
  - Red (<75%)

**Accessibility:**
- [ ] Table is scrollable horizontally on mobile
- [ ] Text is readable in light mode
- [ ] Text is readable in dark mode
- [ ] Row hover effect works
- [ ] Contrast ratio meets WCAG AA standards

**Expected Result:** Table is easy to read, well-formatted, and accessible

---

### ✅ 10. Color Coding and Accessibility

**Location:** Entire dashboard

**Test Steps:**
1. Review color usage throughout dashboard
2. Test dark mode toggle
3. Check color contrast

**Verification Points:**

**Color Consistency:**
- [ ] Demographic colors are consistent across all visualizations:
  - White: #3b82f6 (blue)
  - Black: #8b5cf6 (purple)
  - Hispanic: #10b981 (green)
  - Asian: #f59e0b (orange)
- [ ] Status colors are consistent:
  - Pass: Green
  - Warning: Orange/Yellow
  - Fail: Red
- [ ] Progress bars use blue
- [ ] Links use blue

**Dark Mode:**
- [ ] Toggle dark mode (theme toggle in nav)
- [ ] All components adapt to dark mode
- [ ] Text remains readable
- [ ] Charts adapt colors appropriately
- [ ] Backgrounds are dark (#0f0f0f, #1a1a1a)
- [ ] Borders are visible (#2a2a2a)
- [ ] Status colors maintain contrast

**Accessibility:**
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Icons have text labels where needed
- [ ] Focus states are visible (keyboard navigation)
- [ ] Screen reader friendly (semantic HTML)
- [ ] Color is not the only indicator (icons + text)

**Color Blindness:**
- [ ] Patterns/shapes differentiate groups (not just color)
- [ ] Text labels are always present
- [ ] Charts are readable in grayscale

**Expected Result:** Intuitive color coding, accessible in all modes

---

## Functional Testing

### API Integration Tests

**Test 1: Analysis Endpoint**
```bash
curl http://localhost:8000/api/bias/analysis
```

**Verify:**
- [ ] Returns 200 status
- [ ] JSON structure matches BiasAnalysisReport model
- [ ] All required fields present
- [ ] Demographic metrics array has 4 items
- [ ] Fairness metrics array has 5 items
- [ ] Historical trends array has ~36 items (9 per group × 4 groups)

**Test 2: Interventions Endpoint**
```bash
curl http://localhost:8000/api/bias/interventions
```

**Verify:**
- [ ] Returns 200 status
- [ ] Returns array of 3 interventions
- [ ] Each intervention has required fields
- [ ] Improvement percentages are calculated correctly

**Test 3: Disparity Report**
```bash
curl "http://localhost:8000/api/bias/disparity-report?metric_type=false_positive_rate"
```

**Verify:**
- [ ] Returns 200 status
- [ ] Contains rates_by_demographic object
- [ ] Disparity ratio is calculated correctly
- [ ] Status is "pass" or "fail"

---

### Error Handling Tests

**Test 1: Invalid Model Version**
```bash
curl "http://localhost:8000/api/bias/analysis?model_version=invalid"
```

**Verify:**
- [ ] Returns 200 (parameter is accepted as-is)
- [ ] Response includes provided model_version

**Test 2: Missing Historical Data**
```bash
curl "http://localhost:8000/api/bias/analysis?include_historical=false"
```

**Verify:**
- [ ] Returns 200
- [ ] historical_trends array is empty

**Test 3: Frontend Error Handling**
- [ ] Disconnect backend server
- [ ] Navigate to dashboard
- [ ] Verify: Loading spinner appears, then error message
- [ ] Reconnect backend
- [ ] Verify: Data loads successfully

---

## Cross-Browser Testing

**Test in:**
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile browser (iOS Safari)
- [ ] Mobile browser (Android Chrome)

**Verify:**
- [ ] Dashboard loads correctly
- [ ] Charts render properly
- [ ] Tabs work correctly
- [ ] Responsive layout works
- [ ] Dark mode toggle works

---

## Performance Testing

**Test:**
- [ ] Page loads in < 2 seconds
- [ ] Charts render in < 1 second
- [ ] Tab switching is instant (< 100ms)
- [ ] No memory leaks (check DevTools)
- [ ] API response time < 500ms

---

## Accessibility Testing

**Keyboard Navigation:**
- [ ] Tab through all interactive elements
- [ ] Enter/Space activates tabs
- [ ] Focus indicators are visible
- [ ] All content is reachable via keyboard

**Screen Reader:**
- [ ] Use screen reader (NVDA/JAWS/VoiceOver)
- [ ] Verify all content is announced
- [ ] Charts have alt text or descriptions
- [ ] Tables are properly labeled

---

## Final Checklist

### Visual Elements
- [ ] Fairness score displays correctly
- [ ] Demographic comparison chart shows parity
- [ ] All fairness metrics have proper status badges
- [ ] Radar chart renders performance comparison
- [ ] Historical trends show 90-day progression
- [ ] Interventions display before/after improvements
- [ ] Recommendations categorized by severity
- [ ] All tabs switch smoothly
- [ ] Detailed metrics table is readable
- [ ] Color coding is intuitive and accessible

### Functionality
- [ ] API endpoints return correct data
- [ ] Frontend fetches and displays data correctly
- [ ] Error handling works
- [ ] Loading states display properly
- [ ] Dark mode toggle works

### Code Quality
- [ ] No console errors
- [ ] No linting errors
- [ ] No TypeScript errors (if applicable)
- [ ] Components are properly structured
- [ ] Code follows project conventions

---

## Test Results Summary

**Date:** _______________  
**Tester:** _______________  
**Environment:** _______________

**Status:**
- [ ] All tests passed
- [ ] Some tests failed (see notes below)
- [ ] Blocking issues found

**Notes:**
_________________________________________________________
_________________________________________________________
_________________________________________________________

**Next Steps:**
- [ ] Fix identified issues
- [ ] Re-test after fixes
- [ ] Update documentation
- [ ] Deploy to staging

---

## Quick Test Commands

```bash
# Backend
cd project/repo-foresight/src/api
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd project/repo-foresight/frontend
npm run dev

# Test endpoints
curl http://localhost:8000/api/bias/analysis
curl http://localhost:8000/api/bias/interventions

# Open dashboard
open http://localhost:5173/bias-analysis
```

---

## Known Issues / Edge Cases

1. **Random Data:** Current implementation uses `np.random` - values will vary on each request
   - **Workaround:** Use fixed seed for testing consistency
   - **Future:** Replace with actual model predictions

2. **Historical Data:** Generated synthetic trends may not reflect real patterns
   - **Future:** Integrate with actual historical bias audit data

3. **Mobile Layout:** Some tables may need horizontal scroll on small screens
   - **Verified:** Responsive design handles this

---

**End of Testing Checklist**

