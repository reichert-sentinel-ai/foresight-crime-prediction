# Quick Theme Check - Run in Browser Console (F12)

## Step 1: Check if Dark Class is Applied

Open browser console (F12) and run:

```javascript
// Check if dark class exists on HTML element
document.documentElement.classList.contains('dark')
```

**Expected:**
- Returns `true` if dark mode is active
- Returns `false` if light mode is active

## Step 2: Check Theme in localStorage

```javascript
// Check saved theme preference
localStorage.getItem('theme')
```

**Expected:**
- Returns `'dark'` if dark mode is saved
- Returns `'light'` if light mode is saved
- Returns `null` if no preference saved

## Step 3: Check Body Background Color

```javascript
// Check body background color
window.getComputedStyle(document.body).backgroundColor
```

**Expected:**
- Dark mode: `rgb(15, 15, 15)` or `#0f0f0f`
- Light mode: `rgb(249, 250, 251)` or `#f9fafb`

## Step 4: Manually Toggle Dark Class

```javascript
// Manually add dark class (for testing)
document.documentElement.classList.add('dark')
document.body.style.backgroundColor = '#0f0f0f'
document.body.style.color = '#e5e5e5'
```

If this makes the page dark, then the theme toggle button isn't working properly.

## Step 5: Remove Dark Class (reset to light)

```javascript
// Manually remove dark class (for testing)
document.documentElement.classList.remove('dark')
document.body.style.backgroundColor = '#f9fafb'
document.body.style.color = '#111827'
```

## What to Report Back:

1. Does `document.documentElement.classList.contains('dark')` return `true` or `false`?
2. What does `localStorage.getItem('theme')` return?
3. What is the body background color?
4. When you click the theme toggle button, do these values change?

