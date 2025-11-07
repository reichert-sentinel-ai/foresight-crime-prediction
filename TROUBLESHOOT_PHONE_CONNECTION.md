# Troubleshooting Phone Connection Issues

## Issue: Phone Can't Connect to Dev Server

### Step 1: Verify Server is Running on Network

**Check Vite Output:**
- Should show: `Network: http://192.168.1.161:5173/`
- If it shows "use --host to expose", the config didn't apply

**Current Status:**
- ✅ Vite config updated with `host: true`
- ✅ Server restarted
- ✅ Network URL shown: `http://192.168.1.161:5173/`

---

### Step 2: Check Windows Firewall

Windows Firewall might be blocking port 5173.

**Quick Fix - Allow Port 5173:**

1. Open Windows Firewall:
   - Press `Win + R`
   - Type: `wf.msc`
   - Press Enter

2. Click "Inbound Rules" → "New Rule"

3. Select "Port" → Next

4. Select "TCP" and enter "5173" in "Specific local ports" → Next

5. Select "Allow the connection" → Next

6. Check all profiles (Domain, Private, Public) → Next

7. Name: "Vite Dev Server" → Finish

**Alternative - PowerShell (Run as Administrator):**
```powershell
New-NetFirewallRule -DisplayName "Vite Dev Server" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

---

### Step 3: Verify Network Connection

**Check Both Devices Are on Same Network:**

1. **On Computer:**
   ```powershell
   ipconfig
   ```
   - Note your IP: `192.168.1.161`
   - Note your network: `192.168.1.x`

2. **On Phone:**
   - Go to Wi-Fi settings
   - Check connected network
   - Should match computer's network (192.168.1.x)

**If Different Networks:**
- Connect phone to same Wi-Fi network as computer

---

### Step 4: Test Connection from Computer

**Test from Computer First:**

1. Open browser on computer
2. Try: `http://192.168.1.161:5173/crime-map`
3. Should load correctly

**If this doesn't work:**
- Vite config issue
- Check vite.config.js has `host: true`

---

### Step 5: Test from Phone

**On Your Android Phone:**

1. Open Chrome browser
2. Go to: `http://192.168.1.161:5173/crime-map`
3. Should load

**If Still Not Working:**

**Option A: Try Network IP Directly**
- Try: `http://192.168.1.161:5173/` (without /crime-map)
- Should show Vite default page

**Option B: Check Phone's Browser**
- Try different browser (Firefox, Edge)
- Some browsers block local network access

**Option C: Check Phone's Network Settings**
- Make sure phone isn't on "Mobile Data Only" mode
- Ensure Wi-Fi is actually connected (not just showing icon)

---

### Step 6: Backend API Issue (If Page Loads But No Data)

If the page loads but shows "No data available":

**The Problem:**
- Backend is on `localhost:8000`
- Phone can't reach `localhost` (that's the phone's localhost, not your computer)

**Solutions:**

**Option A: Use Computer's IP for Backend**
- Update Vite proxy to use computer's IP instead of localhost
- Or update backend CORS to allow phone's IP

**Option B: Test Frontend Only**
- Test layout and responsiveness
- API calls won't work, but you can test:
  - Layout adapts to mobile
  - Filters stack vertically
  - Map is visible
  - No horizontal scrolling
  - Text readability

---

### Step 7: Alternative Testing Method

If phone connection still doesn't work:

**Use Chrome DevTools Mobile Emulation:**

1. Open Chrome on computer
2. Press F12 (DevTools)
3. Click "Toggle device toolbar" (Ctrl+Shift+M)
4. Select device:
   - "Pixel 5" (Android)
   - "Galaxy S20" (Android)
   - Or custom size: 375px width
5. Test all mobile features

**This is a good alternative for:**
- Testing responsive layout
- Testing touch interactions (simulated)
- Testing text readability
- Testing no horizontal scrolling

---

## Quick Diagnostic Checklist

- [ ] Vite shows Network URL: `http://192.168.1.161:5173/`
- [ ] Windows Firewall allows port 5173
- [ ] Phone and computer on same Wi-Fi network
- [ ] Can access from computer: `http://192.168.1.161:5173/`
- [ ] Phone's browser allows local network access
- [ ] Phone's Wi-Fi is actually connected (not just icon)

---

## Most Common Issues

1. **Firewall blocking port 5173** ← Most likely
2. **Different networks** (phone on mobile data, computer on Wi-Fi)
3. **Backend API won't work** (expected - need to configure separately)

---

## Next Steps

1. Check Windows Firewall first
2. Verify both devices on same network
3. Test from computer's browser first
4. If still not working, use Chrome DevTools mobile emulation

