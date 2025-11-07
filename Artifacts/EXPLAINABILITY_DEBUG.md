# Quick Test Script for Explainability API

## Test if Backend is Running

Open PowerShell and run:

```powershell
# Test if backend is accessible
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET

# Test explainability endpoint
Invoke-WebRequest -Uri "http://localhost:8000/api/explainability/explain-prediction?location_id=grid_5_7" -Method GET
```

## If Backend is Not Running

1. Start backend server:
```powershell
cd project/repo-foresight/src/api
python -m uvicorn main:app --reload --port 8000
```

2. Verify explainability router is registered:
   - Check `main.py` includes: `from src.api.routers import explainability`
   - Check `main.py` includes: `app.include_router(explainability.router)`

## Frontend Fix Applied

The component now:
- ✅ Shows error message if API fails
- ✅ Displays helpful troubleshooting steps
- ✅ Has retry button
- ✅ Better loading state with message

## Quick Test Checklist

1. [ ] Backend server running on port 8000
2. [ ] Backend returns 200 for `/health`
3. [ ] Backend returns 200 for `/api/explainability/explain-prediction`
4. [ ] Frontend shows error message (not infinite spinner)
5. [ ] Browser console shows actual error details

