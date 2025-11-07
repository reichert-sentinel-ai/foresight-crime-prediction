# ✅ F2 Testing - Quick Instructions

## Backend Server Status

The backend server should be starting. Here's how to verify and test:

### Step 1: Verify Backend is Running

Open a NEW terminal window and run:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight
python test_f2_quick.py
```

**Expected Output:**
```
✅ Backend is running and healthy!
✅ All validations passed!
✅ All 4 backend tests should pass
```

### Step 2: If Backend Tests Fail (404 errors)

The server needs to be started from the project root. Run this in a NEW terminal:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: "Application startup complete"
Then press Ctrl+C to stop it (or leave it running)

### Step 3: Test Frontend

1. **Install recharts** (if not already):
   ```powershell
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
   npm install recharts
   ```

2. **Start frontend**:
   ```powershell
   npm run dev
   ```

3. **Open browser**: http://localhost:5173/temporal-patterns

4. **Test checklist**:
   - ✅ Page loads without errors
   - ✅ See 3 charts (Hourly, Weekly, Forecast)
   - ✅ Click tabs → charts switch
   - ✅ Change filters → charts update
   - ✅ Hover over charts → tooltips appear

## Quick Test Commands

**Test backend:**
```powershell
python test_f2_quick.py
```

**Check API docs:**
- Visit: http://localhost:8000/docs
- Look for "temporal-patterns" section

**Test endpoints directly:**
- http://localhost:8000/api/temporal/analysis
- http://localhost:8000/api/temporal/forecast
- http://localhost:8000/api/temporal/anomalies

## Summary

✅ Code is ready
✅ Backend router created
✅ Frontend component created
⏳ Need to start backend server
⏳ Need to start frontend server
⏳ Run tests

See `TESTING_CHECKLIST_F2.md` for detailed test instructions.
