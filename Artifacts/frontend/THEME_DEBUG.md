# Theme Toggle Debug Guide

## Issue: Theme Toggle Only Affects Page Slider

### What to Check

1. **Open Browser Console (F12)**
   - Go to Console tab
   - Click the theme toggle button
   - Look for console messages:
     - "Theme toggled: light -> dark" or "Theme toggled: dark -> light"
     - "Applying theme: dark" or "Applying theme: light"
     - "Dark class added to root" or "Dark class removed from root"
     - "Root classes: ..."

2. **Check if Theme is Changing**
   - After clicking, check console for theme toggle messages
   - Look for "Root classes:" - should show "dark" class when dark mode is on

3. **Visual Check**
   - Background should change from light gray to dark black
   - Text should change from dark to light
   - Navigation bar should change color

### If Theme Toggle Messages Don't Appear

**Problem:** Button click not working
- Check console for JavaScript errors
- Verify button is clickable (hover should show pointer cursor)
- Try clicking directly on the icon

### If Theme Toggle Messages Appear But No Visual Change

**Problem:** CSS not applying
- Check if `dark` class is added to `<html>` element
- Inspect element (F12 → Elements tab) → Look at `<html>` tag
- Should see `class="dark"` when dark mode is on

### Quick Test in Console

Open browser console (F12) and run:

```javascript
// Check current theme
console.log('Current theme:', localStorage.getItem('theme'));
console.log('Root has dark class:', document.documentElement.classList.contains('dark'));

// Manually toggle
document.documentElement.classList.toggle('dark');
console.log('Manually toggled dark class');
```

If manual toggle works, the issue is with the button click handler.

### Expected Behavior

When clicking theme toggle:
1. Console shows: "Theme toggled: light -> dark"
2. Console shows: "Applying theme: dark"
3. Console shows: "Dark class added to root"
4. Console shows: "Root classes: dark"
5. Page background changes to dark (#0f0f0f)
6. Text changes to light (#e5e5e5)
7. Navigation bar changes to dark (#1a1a1a)

### If Still Not Working

1. Check browser console for errors
2. Verify button is clickable (not hidden behind something)
3. Try right-clicking button → Inspect Element
4. Check if button has `onclick` handler in Elements tab

