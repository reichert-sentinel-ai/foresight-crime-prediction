# Dark Theme Troubleshooting for `/crime-map` Route

## If dark theme isn't showing on `/crime-map`:

### Quick Fixes:

1. **Clear Browser Cache**
   - Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
   - Select "Cached images and files"
   - Click "Clear data"
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

2. **Check if Dark Class is Applied**
   - Open DevTools (F12)
   - Go to Elements/Inspector tab
   - Look at the `<html>` element
   - Should have `class="dark"` when dark mode is active

3. **Verify Theme Toggle**
   - Click the moon/sun icon in the navigation bar
   - Check browser console (F12 → Console tab)
   - Should see theme changes applied

4. **Manual Theme Check**
   - Open browser console (F12)
   - Run: `document.documentElement.classList.contains('dark')`
   - Should return `true` if dark mode is active
   - Run: `localStorage.getItem('theme')`
   - Should return `'dark'` if dark mode is saved

### CSS Verification:

The dark theme should apply to:
- ✅ Background: `#0f0f0f` (dark) or `#f9fafb` (light)
- ✅ Text: `#e5e5e5` (dark) or `#111827` (light)
- ✅ Navigation bar: `#1a1a1a` (dark) or white (light)
- ✅ Cards: `#1f1f1f` (dark) or white (light)
- ✅ Map: `#1a1a1a` (dark) or `#f5f5f5` (light)

### If Still Not Working:

1. **Check Tailwind Config**
   - Verify `darkMode: 'class'` is set in `tailwind.config.js`

2. **Check CSS Variables**
   - Open DevTools → Elements tab
   - Select `<html>` element
   - Check Computed styles
   - `--bg-color` should be `#0f0f0f` in dark mode

3. **Force Refresh**
   - Stop the Vite dev server (Ctrl+C)
   - Delete `node_modules/.vite` folder
   - Restart: `npm run dev`
   - Hard refresh browser (Ctrl+Shift+R)

4. **Check Component Rendering**
   - Verify all components have `dark:` classes
   - Check if `CardContent` has dark theme text colors
   - Verify `CrimeHeatmap` component wrapper has dark theme support

### Expected Behavior:

When dark theme is active:
- Page background should be very dark (`#0f0f0f`)
- All text should be light (`#e5e5e5` or `#a0a0a0`)
- Cards should have dark background (`#1f1f1f`)
- Navigation should be dark (`#1a1a1a`)
- Map should have dark background (`#1a1a1a`)

### Files Updated:

- ✅ `App.jsx` - Added dark theme text colors to main element
- ✅ `CrimeHeatmap.jsx` - Already has dark theme classes
- ✅ `card.jsx` - Added dark theme text colors to CardContent
- ✅ `ThemeContext.jsx` - Directly sets body styles for reliability

