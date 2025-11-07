# Debugging: Infinite Spinner / Hanging Requests

## Issue
- Requests to `/health` and explainability endpoints hang indefinitely
- No errors in console or network tab
- Spinner keeps spinning

## Root Cause
Likely the backend server is not running or not accessible.

## Quick Fix Applied

1. **Added timeout to all axios requests** (10 seconds)
2. **Added health check before main requests**
3. **Better error detection** for timeout vs network errors
4. **Clear error messages** telling user what to do

## Test Steps

### Step 1: Verify Backend is Running

Open PowerShell and run:
```powershell
# Check if port 8000 is listening
netstat -ano | findstr :8000

# Or test directly
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
```

If you get "Connection refused" or timeout, backend is NOT running.

### Step 2: Start Backend Server

```powershell
cd project/repo-foresight/src/api
python -m uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Test Backend Directly

Open browser and go to:
- `http://localhost:8000/health` - Should return JSON with status
- `http://localhost:8000/docs` - Should show FastAPI docs
- `http://localhost:8000/api/explainability/explain-prediction?location_id=grid_5_7` - Should return prediction data

### Step 4: Check Frontend

With backend running, refresh the explainability page. It should now:
- Show loading message briefly
- Load data OR show clear error message
- NOT hang indefinitely

## Alternative: Check if Port is Already in Use

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill process if needed (replace PID with actual process ID)
taskkill /PID <PID> /F
```

## Debugging Network Tab

In browser DevTools Network tab:
1. Look for requests to `localhost:8000`
2. Check Status column:
   - `(pending)` = hanging (backend not running)
   - `200` = success
   - `404` = endpoint not found
   - `CORS error` = CORS issue
3. Check Timing:
   - If `Waiting (TTFB)` is very long = backend slow/not responding
   - If `Pending` = request never completed

## Expected Behavior After Fix

### Backend Running:
- ✅ Health check passes quickly
- ✅ API calls complete in < 1 second
- ✅ Dashboard loads with data

### Backend NOT Running:
- ✅ Health check fails after 3 seconds
- ✅ Shows error message immediately
- ✅ No infinite spinner

## Still Having Issues?

1. Check Windows Firewall blocking port 8000
2. Try different port: Change backend to port 8001 and update frontend
3. Check antivirus blocking localhost connections
4. Verify Python/uvicorn is installed correctly

