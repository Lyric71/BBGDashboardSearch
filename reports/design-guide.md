# Beyond Border Group — Design & Style Guide
Source: beyondbordergroup.com
Use this guide for all reports and the reporting website.

---

## Color Palette

| Role | Name | Hex |
|------|------|-----|
| Background | White | `#ffffff` |
| Text | Black | `#000000` |
| Primary Accent | Red | `#cf2e2e` |
| Secondary Accent | Orange | `#ff6900` |
| Tertiary Accent | Cyan Blue | `#0693e3` |
| Purple | Purple | `#9b51e0` |
| Muted Text | Cyan Bluish Gray | `#abb8c3` |
| Surface / BG Alt | Light Gray | `#f0f0f0` |
| Button BG | Dark Gray | `#32373c` |

---

## Typography

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| H1 | 42px | Bold | Page title |
| H2 | 36px | Bold | Section title |
| Body Large | 20px | Regular | Lead text |
| Body | 16px | Regular | Default |
| Small | 13px | Regular | Labels, captions |

- **Font family**: Sans-serif (system stack)
- **Line height**: 1.5 standard
- **Color**: Inherits black `#000000` by default

---

## Spacing

| Token | Value |
|-------|-------|
| xs | 20px |
| sm | 24px (block gap) |
| md | 67px |
| lg | 100px |
| xl | 150px |
| 2xl | 225px |

- **Max content width**: 800px
- **Max wide width**: 1200px

---

## Components

### Cards
```css
border-radius: 25px;
box-shadow: 10px 5px 10px rgba(0, 0, 0, 0.5);
transition: transform 0.2s ease;
```
Hover: `transform: scale(1.05)`

### Buttons
```css
background: #32373c;
color: #ffffff;
border: none;
padding: 0.667em 1.333em;
border-radius: 4px;
```

### Images
```css
border-radius: 25px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
max-width: 100%;
object-fit: cover;
```

---

## Layout

- Grid: CSS Grid, 1-col mobile → multi-col desktop
- Standard section padding: `100px` top/bottom
- Content blocks gap: `24px`

---

## Visual Identity Notes

- Modern, clean, B2B professional
- Generous white space
- Rounded elements (25px radius) throughout
- Subtle shadows for depth
- Bilingual EN/FR with flag switcher
- Positioning: bridge between Western brands and Chinese market
