# F2 Testing - Quick Start Guide

## Current Status
✅ Backend server is running (health check passed)
❌ Temporal endpoints returning 404 - server needs restart to load new router

## Solution: Restart Backend Server

The backend server needs to be restarted to load the new temporal_patterns router.

### Steps:

1. **Stop the current backend server** (Ctrl+C in the terminal running uvicorn)

2. **Restart the backend:**
   ```powershell
   cd project/repo-foresight/src/api
   uvicorn main:app --reload
   ```

3. **Verify router is loaded:**
   - Visit: http://localhost:8000/docs
   - Look for "temporal-patterns" section in the API docs
   - Should see 3 endpoints:
     - GET /api/temporal/analysis
     - GET /api/temporal/forecast  
     - GET /api/temporal/anomalies

4. **Run tests again:**
   ```powershell
   cd project/repo-foresight
   python test_f2_quick.py
   ```

## After Backend Restart - Test Checklist

### Backend Tests (Automated)
```powershell
python test_f2_quick.py
```

Expected: All 4 tests should pass ✅

### Frontend Tests (Manual)

1. **Install recharts** (if not already):
   ```powershell
   cd project/repo-foresight/frontend
   npm install recharts
   ```

2. **Start frontend:**
   ```powershell
   npm run dev
   ```

3. **Open browser:** http://localhost:5173/temporal-patterns

4. **Test each item:**

   ✅ **Test 1: Backend endpoints return valid temporal data**
   - Open browser DevTools (F12) → Network tab
   - Refresh page
   - Should see 3 API calls:
     - `/api/temporal/analysis` → Status 200
     - `/api/temporal/forecast` → Status 200
     - `/api/temporal/anomalies` → Status 200

   ✅ **Test 2: Hourly pattern chart displays correctly**
   - Should see bar chart with 24 bars
   - Red line overlay for severity
   - Peak hours badges below chart

   ✅ **Test 3: Day of week patterns show proper trends**
   - Click "Weekly" tab
   - Should see 7 bars (Monday-Sunday)
   - Trend badges below chart

   ✅ **Test 4: Time series shows actual vs predicted**
   - Click "Forecast" tab
   - Should see area chart with confidence bands
   - Blue line (actual) and green dashed line (predicted)

   ✅ **Test 5: Anomaly detection highlights unusual spikes**
   - Click "Anomalies" tab
   - Should see orange alert cards
   - Each shows date, expected vs actual, deviation

   ✅ **Test 6: Forecast table displays upcoming predictions**
   - Still on "Forecast" tab
   - Scroll down to table
   - Should see 7 rows with dates, predictions, risk levels

   ✅ **Test 7: All tabs switch smoothly**
   - Click each tab: Hourly → Weekly → Forecast → Anomalies
   - Should switch instantly without flickering

   ✅ **Test 8: Filters update all visualizations**
   - Change "Crime Type" dropdown
   - Should see loading spinner, then charts update
   - Change "Location" dropdown
   - Charts should update again

   ✅ **Test 9: Charts are responsive and interactive**
   - Resize browser window
   - Charts should resize smoothly
   - Hover over chart elements → tooltips appear

   ✅ **Test 10: Tooltips show detailed information**
   - Hover over bars/lines in charts
   - Tooltips should show:
     - Hourly: hour, incidents, severity
     - Weekly: day, incidents
     - Forecast: date, actual, predicted, confidence

## Troubleshooting

### Issue: Backend endpoints still 404 after restart
- Check that `temporal_patterns.py` exists in `src/api/routers/`
- Verify `main.py` includes: `app.include_router(temporal_patterns.router)`
- Check for import errors in backend console

### Issue: Frontend shows "Error fetching temporal data"
- Verify backend is running on port 8000
- Check CORS settings in main.py
- Check browser console for errors

### Issue: Charts not displaying
- Verify recharts is installed: `npm list recharts`
- Check browser console for React errors
- Verify data is loading (check Network tab)

### Issue: Import errors in backend
- Install dependencies: `pip install fastapi numpy pandas pydantic`

## Quick Test Commands

**Backend API Test:**
```powershell
python test_f2_quick.py
```

**Check endpoints manually:**
- http://localhost:8000/api/temporal/analysis
- http://localhost:8000/api/temporal/forecast  
- http://localhost:8000/api/temporal/anomalies

**Check API docs:**
- http://localhost:8000/docs

