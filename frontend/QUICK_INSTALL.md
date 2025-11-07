# Quick Fix: Install recharts

## Node.js Found! ✅
Node.js is installed at: `C:\Program Files\nodejs\node.exe`

## Solution: Use Full Path to npm

Run this command in PowerShell:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
& "C:\Program Files\nodejs\npm.cmd" install recharts
```

## Or Add npm to PATH (Better Long-term Solution)

### Option 1: Add to PATH for Current Session
```powershell
$env:PATH += ";C:\Program Files\nodejs"
npm install recharts
```

### Option 2: Add to PATH Permanently
1. Press `Win + X` → System
2. Advanced System Settings → Environment Variables
3. Under "User variables", find "Path" → Edit
4. Click "New" → Add: `C:\Program Files\nodejs`
5. Click OK on all windows
6. **Close and reopen PowerShell**
7. Then run: `npm install recharts`

## After Installing recharts

1. Verify installation:
```powershell
Test-Path "node_modules\recharts"
```

2. Start frontend:
```powershell
& "C:\Program Files\nodejs\npm.cmd" run dev
```

Or if you added to PATH:
```powershell
npm run dev
```

3. Visit: http://localhost:5173/temporal-patterns

## Summary

✅ Node.js installed
✅ npm available at: `C:\Program Files\nodejs\npm.cmd`
⏳ Need to install recharts
⏳ Need to start frontend server

**Quick Command:**
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
& "C:\Program Files\nodejs\npm.cmd" install recharts
& "C:\Program Files\nodejs\npm.cmd" run dev
```

