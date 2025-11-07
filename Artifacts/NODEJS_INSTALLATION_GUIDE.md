# Node.js Installation Guide

## Current Status

❌ **Node.js is not installed** - Required for frontend development

---

## Quick Installation Steps

### Step 1: Download Node.js

1. **Go to:** https://nodejs.org/
2. **Click:** Download the **LTS version** (recommended)
   - LTS = Long Term Support (more stable)
   - Current recommended version: v20.x.x or v18.x.x

### Step 2: Install Node.js

1. **Run the installer** you just downloaded
2. **Follow the installation wizard:**
   - Click "Next" through the setup
   - Accept the license agreement
   - Keep default installation path (usually `C:\Program Files\nodejs\`)
   - **Important:** Make sure "Add to PATH" is checked (should be by default)
   - Click "Install"
   - Wait for installation to complete

### Step 3: Verify Installation

**Close and reopen your PowerShell terminal**, then run:

```powershell
node --version
npm --version
```

**Expected output:**
```
v20.x.x  (or v18.x.x)
10.x.x   (npm version)
```

If you see version numbers, Node.js is installed correctly! ✅

---

## After Installation

Once Node.js is installed, come back and I'll help you run:

```powershell
cd project\repo-foresight\frontend
npm install
npm run dev
```

---

## Troubleshooting

### "node: command not found" after installation

**Solution:** Restart your terminal/PowerShell
- Close the current PowerShell window
- Open a new PowerShell window
- Try `node --version` again

### Still not working after restart

**Solution:** Check PATH environment variable
1. Open System Properties → Environment Variables
2. Check if `C:\Program Files\nodejs\` is in PATH
3. If not, add it manually

### Installation fails

**Solution:** 
- Try running installer as Administrator
- Check if antivirus is blocking installation
- Download installer again

---

## Alternative: Use Node Version Manager (Advanced)

If you need to manage multiple Node.js versions:

**Windows:** Use `nvm-windows`
- Download from: https://github.com/coreybutler/nvm-windows/releases
- Install and use: `nvm install 20` then `nvm use 20`

---

## What Node.js Does

Node.js is a JavaScript runtime that allows you to:
- Run JavaScript on your computer (not just in browsers)
- Install and manage packages with npm
- Build and run frontend applications
- Use tools like Vite, React, etc.

---

## Next Steps After Installation

1. ✅ Install Node.js (see above)
2. ✅ Verify installation (`node --version`)
3. ⏳ Install frontend dependencies (`npm install`)
4. ⏳ Start frontend server (`npm run dev`)
5. ⏳ Open http://localhost:5173/crime-map
6. ⏳ Complete frontend tests (2-7)

---

## Quick Reference

**Download:** https://nodejs.org/  
**Install:** Run the installer  
**Verify:** `node --version` in new terminal  
**Then:** Come back and we'll continue with npm install

---

**Once Node.js is installed, let me know and I'll help you proceed!**

