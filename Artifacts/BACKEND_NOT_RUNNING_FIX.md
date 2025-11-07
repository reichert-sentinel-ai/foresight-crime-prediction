# Backend Server Not Running - Quick Fix

## Problem
- Health endpoint shows "(canceled)"
- Docs endpoint shows "(pending)"
- No backend server responding

## Solution: Start the Backend Server

### Option 1: Use the startup script (Recommended)

```powershell
cd project/repo-foresight
python start_backend.py
```

### Option 2: Manual start

```powershell
cd project/repo-foresight/src/api
python -m uvicorn main:app --reload --port 8000
```

### Option 3: Check if something is blocking port 8000

```powershell
# See what's using port 8000
netstat -ano | findstr :8000

# If something is using it, kill it (replace PID)
taskkill /PID <PID> /F
```

## Expected Output When Server Starts

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX]
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Verify It's Working

After starting, test in browser:
- `http://localhost:8000/health` - Should return JSON immediately
- `http://localhost:8000/docs` - Should load Swagger UI
- `http://localhost:8000/api/explainability/explain-prediction?location_id=grid_5_7` - Should return prediction data

## If Port 8000 is Already in Use

Try a different port:
```powershell
python -m uvicorn main:app --reload --port 8001
```

Then update frontend: Change `http://localhost:8000` to `http://localhost:8001` in:
- `frontend/src/components/PredictionExplainer.jsx`

## Common Issues

### Issue: "Module not found: uvicorn"
```powershell
pip install uvicorn fastapi
```

### Issue: "Module not found: src.api.main"
```powershell
# Make sure you're in the right directory
cd project/repo-foresight/src/api
python -m uvicorn main:app --reload --port 8000
```

### Issue: "Address already in use"
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## After Starting Backend

1. ✅ Keep the terminal window open (server runs in foreground)
2. ✅ Refresh the explainability page
3. ✅ Should load immediately (no more canceled/pending)

