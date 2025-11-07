# Frontend Setup Guide - Crime Heatmap

## Quick Start

### Option 1: Use the Setup Script (Recommended)

```powershell
cd project\repo-foresight\frontend
.\start-frontend.ps1
```

### Option 2: Manual Setup

```powershell
# Navigate to frontend directory
cd project\repo-foresight\frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

---

## Prerequisites

- **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
- **npm** - Comes with Node.js
- **Backend server running** - Port 8000

---

## Verification

### Check Node.js Installation

```powershell
node --version
npm --version
```

Should show versions like:
- Node.js: v18.x.x or higher
- npm: 9.x.x or higher

### Check Backend Server

```powershell
curl.exe http://localhost:8000/health
```

Should return: `{"status":"healthy",...}`

---

## After Starting Frontend

1. **Open Browser:**
   - Navigate to: `http://localhost:5173/crime-map`
   - Or: `http://localhost:5173` (home page)

2. **Open DevTools:**
   - Press F12
   - Go to Console tab (for errors)
   - Go to Network tab (for API calls)

3. **Start Testing:**
   - Follow `TEST_WALKTHROUGH.md` for step-by-step tests
   - Or use `TEST_EXECUTION_CHECKLIST.md` for quick reference

---

## Troubleshooting

### Issue: "npm: command not found"

**Solution:** Install Node.js from [nodejs.org](https://nodejs.org/)

### Issue: "Port 5173 already in use"

**Solution:** 
```powershell
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: "Cannot find module"

**Solution:**
```powershell
cd project\repo-foresight\frontend
rm -r node_modules  # Remove if exists
npm install
```

### Issue: "Backend connection error"

**Solution:**
1. Make sure backend is running:
   ```powershell
   cd project\repo-foresight
   python -m uvicorn src.api.main:app --port 8000
   ```

2. Check CORS is enabled in backend (already configured)

### Issue: "Module not found: leaflet"

**Solution:**
```powershell
cd project\repo-foresight\frontend
npm install leaflet react-leaflet
```

---

## Expected Output

When you run `npm run dev`, you should see:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Then open `http://localhost:5173/crime-map` in your browser.

---

## Files Created

- `frontend/start-frontend.ps1` - Setup and start script
- `frontend/package.json` - Dependencies configuration
- `frontend/vite.config.js` - Vite build configuration
- `frontend/src/App.jsx` - Main React application
- `frontend/src/components/CrimeHeatmap.jsx` - Crime map component

---

## Next Steps

Once frontend is running:

1. ✅ Verify backend is running (port 8000)
2. ✅ Verify frontend is running (port 5173)
3. ✅ Open `http://localhost:5173/crime-map`
4. ✅ Follow test guide: `TEST_WALKTHROUGH.md`

---

## Quick Test Commands

```powershell
# Test backend
curl.exe http://localhost:8000/api/crime-map/hotspots

# Test frontend (in browser)
http://localhost:5173/crime-map

# Check both are running
Test-NetConnection -ComputerName localhost -Port 8000
Test-NetConnection -ComputerName localhost -Port 5173
```

