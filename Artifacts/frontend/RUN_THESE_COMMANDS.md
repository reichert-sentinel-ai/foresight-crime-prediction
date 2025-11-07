# Complete Setup Commands - Copy and Run These

## Step 1: Install recharts

Copy and paste this into PowerShell:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
& "C:\Program Files\nodejs\npm.cmd" install recharts
```

**Wait for installation to complete** (may take 1-2 minutes)

## Step 2: Verify Installation

```powershell
Test-Path "node_modules\recharts"
```

Should return: `True`

## Step 3: Start Frontend Server

```powershell
& "C:\Program Files\nodejs\npm.cmd" run dev
```

**Keep this terminal open** - the server will run here.

## Step 4: Test the Visualization

1. Open browser: http://localhost:5173/temporal-patterns
2. You should see:
   - ✅ Hourly pattern chart with 24 bars
   - ✅ Weekly tab with 7-day pattern
   - ✅ Forecast tab with time series
   - ✅ Anomalies tab with alert cards

## Alternative: Use Batch Script

I've created `install_and_run.bat` - you can double-click it to:
1. Install recharts
2. Start the frontend server automatically

## Troubleshooting

### If npm commands fail:
- Make sure you're in the frontend directory
- Try: `& "C:\Program Files\nodejs\npm.cmd" --version` to verify npm works

### If frontend doesn't start:
- Make sure backend is running on port 8000
- Check for port conflicts (another app using port 5173)

### If you see "recharts not found" error:
- Verify: `Test-Path "node_modules\recharts"`
- Try: `& "C:\Program Files\nodejs\npm.cmd" install` (installs all dependencies)

## Current Status

✅ Backend: Running on port 8000
✅ Backend endpoints: All working
✅ Node.js: Found and ready
⏳ recharts: Needs installation
⏳ Frontend: Waiting to start

**Run the commands above to complete setup!**

