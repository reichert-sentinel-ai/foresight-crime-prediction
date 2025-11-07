# Quick Phone Connection Test

## Issue: Phone Can't Connect

### Most Likely Cause: Windows Firewall

**Quick Fix:**

### Option 1: Allow Port 5173 in Firewall (Recommended)

**Manual Method:**
1. Press `Win + R`
2. Type: `wf.msc`
3. Press Enter
4. Click "Inbound Rules" → "New Rule"
5. Select "Port" → Next
6. Select "TCP" → Enter "5173" → Next
7. Select "Allow the connection" → Next
8. Check all (Domain, Private, Public) → Next
9. Name: "Vite Dev Server" → Finish

**PowerShell Method (Run as Administrator):**
```powershell
New-NetFirewallRule -DisplayName "Vite Dev Server" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

Or run the script:
```powershell
.\fix-firewall.ps1
```

---

### Option 2: Test Connection Steps

**Step 1: Verify Server is Running**
- Check terminal shows: `Network: http://192.168.1.161:5173/`
- If not, restart frontend server

**Step 2: Test from Computer First**
- Open browser on computer
- Go to: `http://192.168.1.161:5173/crime-map`
- Should load (if not, firewall issue)

**Step 3: Test from Phone**
- Same Wi-Fi network as computer
- Open Chrome on phone
- Go to: `http://192.168.1.161:5173/crime-map`
- Should load after firewall fix

---

### Option 3: Alternative - Use Chrome DevTools Mobile Emulation

If phone connection still doesn't work:

1. Open Chrome on computer
2. Press F12 (DevTools)
3. Click "Toggle device toolbar" (Ctrl+Shift+M)
4. Select "Pixel 5" or "Galaxy S20" (Android sizes)
5. Test all mobile features

**This works for:**
- ✅ Responsive layout testing
- ✅ Mobile interactions (simulated)
- ✅ Text readability
- ✅ No horizontal scrolling
- ✅ Touch interactions (simulated)

---

## Quick Checklist

- [ ] Windows Firewall allows port 5173
- [ ] Phone and computer on same Wi-Fi network
- [ ] Can access from computer: `http://192.168.1.161:5173/`
- [ ] Phone's browser allows local network access

---

## Expected Results

After firewall fix:
- Phone can access: `http://192.168.1.161:5173/crime-map`
- Page loads (may show "No data available" - that's OK for layout testing)
- Can test responsive design

---

## Note About Backend API

**If page loads but shows "No data available":**
- This is expected - backend API calls won't work from phone
- You can still test:
  - ✅ Layout and responsiveness
  - ✅ Mobile interactions
  - ✅ Text readability
  - ✅ No horizontal scrolling

**To test API calls:**
- Need to configure backend separately
- For now, focus on frontend responsiveness testing

