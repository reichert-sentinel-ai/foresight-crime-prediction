# Foresight API Render Deployment Checklist

## Current Status
❌ Backend API is returning 404 - Service not running or not deployed

## Steps to Deploy/Redeploy on Render

### 1. Check if Service Exists
- Go to https://dashboard.render.com
- Look for a service named `foresight-api` or similar
- If it doesn't exist, proceed to step 2
- If it exists, check its status (should be "Live")

### 2. Create New Service (if needed)
1. Click **"New"** → **"Web Service"**
2. Connect GitHub repository: `reichert-sentinel-ai/foresight-crime-prediction`
3. Render should auto-detect `render.yaml` in the `Artifacts` folder
4. If not auto-detected, configure manually:
   - **Name**: `foresight-api`
   - **Environment**: `Docker`
   - **Root Directory**: `Artifacts` (important!)
   - **Dockerfile Path**: `Dockerfile` (relative to root directory)
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes`

### 3. Verify Service Configuration
Check these settings in the Render dashboard:

**Settings Tab:**
- ✅ **Root Directory**: `Artifacts`
- ✅ **Environment**: `Docker`
- ✅ **Dockerfile Path**: `Dockerfile`
- ✅ **Health Check Path**: `/health`

**Environment Tab:**
- ✅ **PORT**: `8000` (or Render's auto-assigned port)

### 4. Check Deployment Logs
1. Go to **"Logs"** tab
2. Look for:
   - ✅ "Building Docker image..."
   - ✅ "Starting container..."
   - ✅ "Uvicorn running on..."
   - ❌ Any error messages

### 5. Common Issues & Fixes

#### Issue: "Cannot find Dockerfile"
- **Fix**: Set Root Directory to `Artifacts` in Render settings

#### Issue: "Module not found: src"
- **Fix**: Ensure `PYTHONPATH=/app` is set (should be in Dockerfile)

#### Issue: "Port already in use"
- **Fix**: Use Render's `$PORT` environment variable instead of hardcoded 8000

#### Issue: Service shows "Build Failed"
- **Fix**: Check logs for specific error, usually missing dependencies in requirements.txt

### 6. Test After Deployment
Once deployed, test these URLs:
- ✅ `https://foresight-api.onrender.com/` → Should return JSON with API info
- ✅ `https://foresight-api.onrender.com/health` → Should return `{"status": "healthy"}`
- ✅ `https://foresight-api.onrender.com/api/temporal/analysis` → Should return temporal data

### 7. Verify CORS is Working
After deployment, check browser console on frontend:
- ❌ Should NOT see CORS errors
- ✅ API calls should return 200 status
- ✅ Data should load in the UI

## Quick Deploy Command (if using Render CLI)
```bash
render deploy
```

## Manual Deploy Trigger
1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait 3-5 minutes for build to complete

## Expected Deployment Time
- First deployment: 5-10 minutes
- Subsequent deployments: 3-5 minutes

## After Successful Deployment
The frontend at `https://foresight-crime-prediction.vercel.app` should:
- ✅ Load without CORS errors
- ✅ Display data from the API
- ✅ All endpoints should work

