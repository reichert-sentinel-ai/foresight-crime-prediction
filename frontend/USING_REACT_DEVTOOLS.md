# Using React DevTools to Debug Dark Theme

## Step 1: Open React DevTools

1. Go to `http://localhost:5173/crime-map` in Chrome
2. Press **F12** to open DevTools
3. You should now see a **"⚛️ Components"** tab (next to Console, Elements, etc.)
4. Click on the **"⚛️ Components"** tab

## Step 2: Find ThemeProvider

1. In the Components tab, you'll see the React component tree
2. Look for **`ThemeProvider`** in the tree
3. Click on it to select it

## Step 3: Check Theme State

1. With `ThemeProvider` selected, look at the right panel
2. You should see **hooks** listed, including `useState`
3. Look for the theme state value:
   - Should show `"dark"` or `"light"`
   - This is the current theme state

## Step 4: Check ThemeToggle Component

1. In the component tree, find **`ThemeToggle`**
2. Click on it
3. Check the right panel for:
   - **Props**: Should show `theme` and `toggleTheme` from context
   - **Hooks**: Should show the theme value

## Step 5: Verify Theme Context

1. Select `ThemeProvider` again
2. In the right panel, look for **Context** section
3. You should see `ThemeContext` with:
   - `theme`: current theme value
   - `toggleTheme`: function
   - `setTheme`: function

## Step 6: Test Theme Toggle with DevTools

1. Select `ThemeToggle` component
2. In the right panel, find the **hooks** section
3. Look for the `theme` value
4. Click the toggle button in the browser
5. Watch if the `theme` value changes in DevTools

## What to Look For:

### If ThemeProvider shows theme = "dark":
- ✅ Theme state is correct
- Check if CSS is applying (go to Step 7)

### If ThemeProvider shows theme = "light" when you expect dark:
- ❌ Theme toggle might not be working
- Or localStorage might have "light" saved

### If ThemeProvider doesn't exist:
- ❌ ThemeProvider might not be wrapping the app
- Check `App.jsx` to ensure `<ThemeProvider>` wraps everything

## Step 7: Check DOM Element

1. Switch to **Elements** tab (or click the Elements tab)
2. Find the `<html>` element in the tree
3. Check if it has `class="dark"` when theme is dark
4. Find the `<body>` element
5. Check its `style` attribute - should have `background-color: #0f0f0f` in dark mode

## Step 8: Console Commands with React DevTools

With React DevTools open, you can also run these in Console:

```javascript
// Check theme state (if you can access React internals)
// Or use localStorage:
localStorage.getItem('theme')

// Check DOM:
document.documentElement.classList.contains('dark')

// Check body styles:
window.getComputedStyle(document.body).backgroundColor
```

## Troubleshooting:

### Issue: ThemeProvider shows "dark" but page is light
**Solution:** CSS isn't applying - try hard refresh (Ctrl+Shift+R)

### Issue: ThemeProvider shows "light" when you want dark
**Solution:** Click the toggle button and watch if it changes in DevTools

### Issue: ThemeProvider doesn't exist in tree
**Solution:** Check that `ThemeProvider` wraps the app in `App.jsx`

### Issue: ThemeToggle doesn't have access to context
**Solution:** Check that `ThemeToggle` is inside `ThemeProvider` in the component tree

## Next Steps:

After checking React DevTools, report back:
1. What theme value does `ThemeProvider` show?
2. When you click the toggle, does the theme value change in DevTools?
3. Does the `<html>` element have `class="dark"`?
4. What color is the body background?

