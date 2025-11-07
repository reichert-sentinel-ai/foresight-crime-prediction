# Fixed Backend Startup Issue

## Problem Fixed
The backend was failing with `ModuleNotFoundError: No module named 'src'` because Python couldn't find the `src` module when running from `src/api/` directory.

## Solution Applied
Changed imports in `main.py` to use relative imports for routers, which works when running from the `src/api/` directory.

## Start Backend Server (Corrected)

Run from the project root:

```powershell
cd project/repo-foresight
python -m uvicorn src.api.main:app --reload --port 8000
```

OR run from src/api directory (now fixed):

```powershell
cd project/repo-foresight/src/api
python -m uvicorn main:app --reload --port 8000
```

## Verify It's Working

After starting, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX]
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then test:
- `http://localhost:8000/health` - Should return JSON
- `http://localhost:8000/docs` - Should show Swagger UI

## Refresh Frontend

Once backend is running:
1. Refresh explainability page
2. Should load successfully!

