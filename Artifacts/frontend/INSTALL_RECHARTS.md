# Installing recharts - npm Not Found

## Issue
npm is not recognized, which means Node.js/npm is either:
1. Not installed
2. Not in your PATH environment variable

## Solutions

### Option 1: Install Node.js (if not installed)
1. Download Node.js from: https://nodejs.org/
2. Choose the LTS version
3. Install it (this will add npm to your PATH automatically)
4. Restart your terminal/PowerShell
5. Then run: `npm install recharts`

### Option 2: Find npm if already installed
Try these locations:
- `C:\Program Files\nodejs\npm.cmd`
- `C:\Program Files (x86)\nodejs\npm.cmd`
- `%APPDATA%\npm\npm.cmd`

If you find it, you can:
1. Add it to PATH, OR
2. Use the full path: `C:\Program Files\nodejs\npm.cmd install recharts`

### Option 3: Manual Installation (if npm is available elsewhere)
If you have npm installed elsewhere, you can:
1. Navigate to the frontend directory
2. Run: `npm install recharts`

### Option 4: Check if you're using a different package manager
- yarn: `yarn add recharts`
- pnpm: `pnpm add recharts`

## Quick Check Commands
Run these to diagnose:
```powershell
# Check if Node.js is installed
node --version

# Check if npm is installed  
npm --version

# Check common install locations
Test-Path "C:\Program Files\nodejs\npm.cmd"
Test-Path "$env:APPDATA\npm\npm.cmd"
```

## After Installing npm
Once npm is available, run:
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend
npm install recharts
```

This will install recharts and resolve the import error.

