# Node.js Installation Guide for F2 Testing

## Step 1: Check if Node.js is Already Installed

Checking common installation locations...

**Status:** Node.js not found in common locations or PATH

## Step 2: Install Node.js

### Download
1. Visit: https://nodejs.org/
2. Download the **LTS version** (Long Term Support)
3. Current LTS: v20.x.x or v22.x.x

### Install
1. Run the downloaded installer (`.msi` file)
2. Follow the installation wizard
3. **Important:** Make sure "Add to PATH" option is checked (usually checked by default)
4. Complete the installation

### Verify Installation
After installation, close and reopen PowerShell, then run:
```powershell
node --version
npm --version
```

Expected output:
```
v20.x.x
10.x.x
```

## Step 3: Install recharts

Once Node.js is installed, run:
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
npm install recharts
```

## Step 4: Start Frontend Server

```powershell
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 5: Test Temporal Patterns

1. Open browser: http://localhost:5173/temporal-patterns
2. Should see:
   - Hourly pattern chart
   - Weekly pattern chart
   - Forecast chart
   - Anomalies tab

## Troubleshooting

### If npm still not found after installing:
1. Close ALL PowerShell/terminal windows
2. Reopen PowerShell
3. Check PATH: `$env:PATH -split ';' | Where-Object { $_ -like '*node*' }`
4. If still not found, manually add to PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit PATH → Add: `C:\Program Files\nodejs`

### If installation fails:
- Make sure you have administrator rights
- Try installing as administrator
- Check Windows Defender/antivirus isn't blocking

## Current Status

✅ Backend server: Running on port 8000
✅ Backend endpoints: All working (200 OK)
✅ Code: All files created and fixed
⏳ Node.js: Needs to be installed
⏳ Frontend: Waiting for Node.js installation

## Next Steps After Installing Node.js

1. Install recharts: `npm install recharts`
2. Start frontend: `npm run dev`
3. Test the visualization: http://localhost:5173/temporal-patterns
4. Run through the 10 test checklist items

