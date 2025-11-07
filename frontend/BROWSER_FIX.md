# Fix for Blank White Page

## Issue
The page shows blank white after refresh, likely due to cached CSS or build errors.

## Quick Fix Steps

### Step 1: Hard Refresh Browser
1. **Chrome/Edge (Windows):**
   - Press `Ctrl + Shift + R` OR
   - Press `Ctrl + F5` OR
   - Open DevTools (F12) → Right-click refresh button → "Empty Cache and Hard Reload"

2. **Android Chrome:**
   - Open Chrome menu (3 dots)
   - Settings → Privacy → Clear browsing data
   - Select "Cached images and files"
   - Clear data
   - Reload page

### Step 2: Restart Vite Dev Server
1. Stop the current frontend server (Ctrl+C in terminal)
2. Restart it:
   ```powershell
   cd project\repo-foresight\frontend
   $env:PATH += ";C:\Program Files\nodejs"
   npm.cmd run dev
   ```

### Step 3: Check Browser Console
1. Open DevTools (F12)
2. Check Console tab for errors
3. Check Network tab - verify CSS files load (status 200)

### Step 4: Clear Browser Cache Completely
If still not working:
1. **Chrome:** Settings → Privacy → Clear browsing data → All time
2. **Or:** Use Incognito/Private window to test

## Expected Behavior
- Page should load with light theme by default
- Navigation bar should be visible
- Theme toggle button (moon/sun icon) should be in top-right
- Clicking toggle should switch between light and dark themes

## If Still Not Working
1. Check terminal for Vite errors
2. Check browser console for JavaScript errors
3. Verify backend server is running on port 8000
4. Try accessing: `http://localhost:5173/` (without /crime-map)

