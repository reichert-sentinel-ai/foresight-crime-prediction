# Step-by-Step Dark Theme Fix for `/crime-map`

## Step 1: Open Browser DevTools

1. Go to `http://localhost:5173/crime-map` in your browser
2. Press **F12** to open DevTools
3. Click on the **Console** tab

## Step 2: Check if Dark Class is Applied

In the console, type this and press Enter:

```javascript
document.documentElement.classList.contains('dark')
```

**What to look for:**
- If it returns `true` → Dark class IS applied (skip to Step 4)
- If it returns `false` → Dark class is NOT applied (go to Step 3)

## Step 3: Check Theme Toggle

1. Click the **moon/sun icon** in the navigation bar (top right)
2. After clicking, check the console again:
   ```javascript
   document.documentElement.classList.contains('dark')
   ```
3. Did it change from `false` to `true`?
   - **Yes** → Theme toggle works, but CSS might not be applying (go to Step 4)
   - **No** → Theme toggle might not be working (go to Step 5)

## Step 4: Check CSS is Applying

In the console, run:

```javascript
window.getComputedStyle(document.body).backgroundColor
```

**Expected results:**
- Dark mode: `rgb(15, 15, 15)` or `#0f0f0f`
- Light mode: `rgb(249, 250, 251)` or `#f9fafb`

**If it shows the wrong color:**
- Dark class is applied but CSS isn't working → Go to Step 6

## Step 5: Test Manual Theme Toggle

Run this in the console to manually apply dark theme:

```javascript
document.documentElement.classList.add('dark')
document.body.style.backgroundColor = '#0f0f0f'
document.body.style.color = '#e5e5e5'
```

**What happens:**
- Page becomes dark → CSS works, but toggle button isn't working (go to Step 7)
- Page stays light → CSS isn't working (go to Step 6)

## Step 6: Fix CSS Issues

If CSS isn't applying, try:

1. **Hard refresh the browser:**
   - Press `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Or `Ctrl+F5`

2. **Clear browser cache:**
   - Press `Ctrl+Shift+Delete` (Windows)
   - Select "Cached images and files"
   - Click "Clear data"

3. **Check if Vite is running:**
   - Make sure the frontend dev server is running
   - Look for "VITE v..." in terminal

## Step 7: Verify Theme Context is Working

In the console, check:

```javascript
localStorage.getItem('theme')
```

**Expected:**
- Should return `'dark'` if dark mode is active
- Should return `'light'` if light mode is active

**If it returns `null`:**
- Theme preference isn't being saved
- Try clicking the toggle button again

## Step 8: Visual Checks

After clicking the theme toggle, check:

1. **Navigation bar** - Should be dark gray (`#1a1a1a`) in dark mode
2. **Page background** - Should be very dark (`#0f0f0f`) in dark mode
3. **Text** - Should be light (`#e5e5e5`) in dark mode
4. **Cards** - Should be dark gray (`#1f1f1f`) in dark mode
5. **Map** - Should have dark background in dark mode

## Step 9: If Still Not Working

1. **Check for JavaScript errors:**
   - Look in the Console tab for red error messages
   - Report any errors you see

2. **Check React DevTools:**
   - Install React DevTools extension if you haven't
   - Check if ThemeProvider is rendering correctly

3. **Restart the dev server:**
   - Stop the frontend server (Ctrl+C)
   - Run `npm run dev` again
   - Hard refresh browser (Ctrl+Shift+R)

## Step 10: Report Back

After going through these steps, tell me:
1. What does Step 2 return? (`true` or `false`)
2. Does Step 3 work? (Does clicking toggle change the value?)
3. What does Step 4 return? (What background color?)
4. Does Step 5 make the page dark?
5. Are there any red errors in the console?

This will help me identify exactly what's wrong!

