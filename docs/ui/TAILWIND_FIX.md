# Tailwind Dark Mode Class Order Fix

## Issue
The theme toggle wasn't working because Tailwind classes were in the wrong order.

## Tailwind Dark Mode Rules
When using `darkMode: 'class'` in Tailwind, the class order matters:

**❌ Wrong:**
```jsx
className="dark:bg-midnight-900 bg-beige-50"
```

**✅ Correct:**
```jsx
className="bg-beige-50 dark:bg-midnight-900"
```

## How It Works
1. **Default (Light) comes first**: `bg-beige-50`
2. **Dark variant second**: `dark:bg-midnight-900`
3. When the `dark` class is added to `<html>`, dark variants activate

## Fixed Files
- `frontend/src/pages/Home.js` - All background, text, and color classes
- `frontend/src/components/PromptInput.js` - All component styles
- `frontend/src/components/Navbar.js` - Navigation styles

## Testing
After refresh, the app should:
1. Start in **light beige theme** by default
2. Switch to **dark midnight theme** when clicking the sun icon
3. Switch back to **light theme** when clicking the moon icon
4. Remember your choice in localStorage

## Theme States
- **Light Mode**: Beige backgrounds, dark text, warm accent colors
- **Dark Mode**: Midnight backgrounds, light text, neon accent colors
