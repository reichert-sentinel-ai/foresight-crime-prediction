# Testing on Android Phone - Step-by-Step Guide

## Goal
Access the crime heatmap from your Android phone to test mobile responsiveness.

---

## Step 1: Find Your Computer's IP Address

### On Windows (PowerShell):
```powershell
ipconfig
```

Look for **IPv4 Address** under your active network adapter (usually Wi-Fi or Ethernet).
Example: `192.168.1.100`

### On Windows (Command Prompt):
```cmd
ipconfig
```

---

## Step 2: Make Vite Dev Server Accessible on Network

The Vite dev server needs to be accessible from other devices on your local network.

### Option A: Update Vite Config (Recommended)
We need to modify `vite.config.js` to add `--host` flag.

### Option B: Start with --host Flag
Run the frontend with:
```powershell
npm.cmd run dev -- --host
```

---

## Step 3: Connect Phone to Same Network

**Important:** Your Android phone must be on the **same Wi-Fi network** as your computer.

1. Check your phone's Wi-Fi settings
2. Make sure it's connected to the same network as your computer
3. Note your phone's IP (optional, for debugging)

---

## Step 4: Access from Your Phone

### On Your Android Phone:
1. Open your web browser (Chrome, Firefox, etc.)
2. Go to: `http://YOUR_COMPUTER_IP:5173/crime-map`
   - Replace `YOUR_COMPUTER_IP` with your computer's IP address
   - Example: `http://192.168.1.100:5173/crime-map`

### If It Doesn't Load:
- Check firewall settings on your computer
- Make sure both devices are on the same network
- Try accessing: `http://YOUR_COMPUTER_IP:5173` (without /crime-map) first

---

## Step 5: Test Mobile Features

Once you can access the page on your phone:

### Test Checklist:
- [ ] Page loads correctly
- [ ] Filters stack vertically
- [ ] Map is visible and functional
- [ ] Legend is visible
- [ ] Info panel is visible
- [ ] No horizontal scrolling
- [ ] Text is readable
- [ ] Dropdowns work (tap to open)
- [ ] Map is zoomable/panable (pinch/zoom, drag)
- [ ] Hotspots are clickable (tap to see popup)
- [ ] Popups display correctly

---

## Troubleshooting

### Issue: Can't connect from phone
**Solution:**
1. Check Windows Firewall - allow port 5173
2. Verify both devices on same network
3. Try accessing from computer's browser: `http://localhost:5173` (should work)

### Issue: Page loads but backend doesn't work
**Solution:**
- Backend is still running on `localhost:8000`
- Need to update backend CORS or use proxy
- For now, test frontend responsiveness (layout, interactions)

### Issue: Slow connection
**Solution:**
- This is normal for dev server
- Production build would be faster

---

## Quick Commands

### Find IP Address:
```powershell
ipconfig | Select-String "IPv4"
```

### Start Frontend with Network Access:
```powershell
cd project\repo-foresight\frontend
$env:PATH += ";C:\Program Files\nodejs"
npm.cmd run dev -- --host
```

### Check if Port is Open:
```powershell
netstat -an | Select-String "5173"
```

---

## Alternative: Use Chrome DevTools Mobile Emulation

If you can't test on actual phone:
1. Open Chrome DevTools (F12)
2. Click "Toggle device toolbar" (Ctrl+Shift+M)
3. Select "Pixel 5" or "Galaxy S20" (Android sizes)
4. Test at different screen sizes

This is a good alternative for initial testing.

---

## Next Steps

After testing on your phone:
1. Complete TEST 7 checklist
2. Note any issues found
3. Report results

