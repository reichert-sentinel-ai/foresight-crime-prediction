# F2 Testing - Step by Step Guide

## ✅ STEP 1: Backend Server Started
Backend server is running in the background on port 8000.

## ✅ STEP 2: Verify Backend Endpoints

Open a new terminal and run:

```powershell
cd project/repo-foresight
python test_f2_quick.py
```

Expected output: All 4 backend tests should pass ✅

Or test manually:
- Visit: http://localhost:8000/docs
- Look for "temporal-patterns" section
- Try the endpoints directly

## STEP 3: Test Frontend

### Option A: If you have npm installed

```powershell
cd project/repo-foresight/frontend
npm install recharts
npm run dev
```

Then visit: http://localhost:5173/temporal-patterns

### Option B: Manual Testing Checklist

1. **Open browser:** http://localhost:5173/temporal-patterns

2. **Test 1: Backend endpoints return valid temporal data**
   - Open DevTools (F12) → Network tab
   - Refresh page
   - Should see 3 API calls returning 200

3. **Test 2: Hourly pattern chart displays correctly**
   - Should see bar chart with 24 bars
   - Red line overlay for severity
   - Peak hours badges below

4. **Test 3: Day of week patterns**
   - Click "Weekly" tab
   - Should see 7 bars with trend badges

5. **Test 4: Time series forecast**
   - Click "Forecast" tab
   - Should see area chart with confidence bands

6. **Test 5: Anomaly detection**
   - Click "Anomalies" tab
   - Should see orange alert cards

7. **Test 6: Forecast table**
   - On Forecast tab, scroll down
   - Should see 7-day forecast table

8. **Test 7: Tab switching**
   - Click each tab → should switch smoothly

9. **Test 8: Filters**
   - Change crime type dropdown → charts update
   - Change location dropdown → charts update

10. **Test 9: Responsiveness**
    - Resize browser → charts resize

11. **Test 10: Tooltips**
    - Hover over chart elements → tooltips appear

## Current Status

✅ Backend server: Running on port 8000
⏳ Backend tests: Ready to run (`python test_f2_quick.py`)
⏳ Frontend: Need to start (`npm run dev`)

## Troubleshooting

If backend endpoints return 404:
1. Check if server is running: http://localhost:8000/health
2. Check API docs: http://localhost:8000/docs
3. Look for "temporal-patterns" section in docs

If frontend shows errors:
1. Check browser console (F12)
2. Verify recharts is installed: `npm list recharts`
3. Check Network tab for API call errors

