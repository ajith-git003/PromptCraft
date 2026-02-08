# Theme Toggle Feature

## Overview
Added a light/dark theme toggle to the PromptCraft application with smooth transitions and persistent theme selection.

## Implementation Details

### 1. Theme Context (`src/context/ThemeContext.js`)
- Created a React Context for managing theme state globally
- Stores theme preference in localStorage for persistence
- Provides `theme` (current theme) and `toggleTheme` (function to switch themes)

### 2. Tailwind Configuration (`tailwind.config.js`)
- Enabled `darkMode: 'class'` for class-based dark mode
- Added new color palette:
  - **Beige colors** (for light theme): beige-50 through beige-500
  - **Warm colors** (for light theme accents): warm-blue, warm-purple, warm-pink

### 3. Theme Toggle Button
- Location: Top-right corner of the Home page
- Shows sun icon ☀️ in dark mode
- Shows moon icon 🌙 in light mode
- Smooth hover effects with backdrop blur

### 4. Theme Variants

#### Dark Theme (Default)
- Background: Midnight navy (`midnight-900`)
- Text: White/light gray
- Accents: Neon blue, purple, pink
- Glow effects: Vibrant neon glows

#### Light Theme
- Background: Beige/cream (`beige-50`)
- Text: Dark gray/black
- Accents: Warm blue, purple, pink (softer tones)
- Glow effects: Subtle, less intense

### 5. Updated Components

All components now support theme-aware styling:

**Home.js**
- Background transitions between midnight-900 and beige-50
- Hero text gradients adapt to theme
- Feature cards with beige tones in light mode
- Animated blobs with softer opacity in light mode

**PromptInput.js**
- Input field backgrounds adapt (dark overlay vs light beige)
- Button gradients switch between neon and warm colors
- All cards and sections support both themes
- STOK framework sections have colored backgrounds in light mode

**Navbar.js**
- Background switches between gray-900 and beige-200
- Text and hover states adapt to theme

## Usage

The theme automatically loads from localStorage on page load. Users can toggle between themes by clicking the sun/moon icon in the top-right corner.

## Technical Notes

- All theme transitions use `duration-300` for smooth animations
- Dark mode is set as the default theme
- Pattern: `className="dark:dark-value light-value"`
- Example: `className="bg-midnight-900 dark:bg-midnight-900 bg-beige-50"`

## Color Palette

### Dark Theme Colors
```
midnight-900: #0f172a (main background)
midnight-800: #1e293b (cards)
midnight-700: #334155 (borders)
neon-blue: #3b82f6
neon-purple: #8b5cf6
neon-pink: #ec4899
```

### Light Theme Colors
```
beige-50: #fdfcfb (main background)
beige-100: #f5f1e8 (cards)
beige-200: #ebe3d5 (navbar, accents)
beige-300: #dfd2bb (borders)
warm-blue: #2563eb
warm-purple: #7c3aed
warm-pink: #db2777
```

## Future Enhancements
- Add more theme options (e.g., high contrast, sepia)
- Add system theme detection (prefer-color-scheme)
- Add theme transition animations
- Add theme customization options
