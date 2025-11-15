# Skraper Web App - Design Style Guide

## Design Philosophy

### Visual Language
- **Professional Tech Aesthetic**: Clean, modern interface conveying reliability and efficiency
- **Data-Driven Design**: Emphasis on clarity, readability, and information hierarchy
- **Minimalist Approach**: Reduce visual noise while maintaining functionality
- **Trust & Security**: Visual cues that emphasize data privacy and professional service

### Color Palette
- **Primary**: Deep Navy (#1a365d) - Professional, trustworthy
- **Secondary**: Bright Cyan (#00d4ff) - Tech-forward, energetic
- **Accent**: Warm Orange (#ff6b35) - Highlighting important actions
- **Neutral**: Light Gray (#f7fafc) - Background, subtle elements
- **Text**: Charcoal (#2d3748) - High contrast, readable
- **Success**: Emerald (#10b981) - Positive feedback
- **Error**: Red (#ef4444) - Error states, warnings

### Typography
- **Display Font**: "Inter" - Modern, geometric sans-serif for headings
- **Body Font**: "Inter" - Consistent, highly readable for all text
- **Code Font**: "JetBrains Mono" - Monospace for JSON/code display
- **Font Weights**: Light (300), Regular (400), Medium (500), Bold (700)

## Visual Effects & Styling

### Background Effects
- **Animated Gradient Flow**: Subtle animated gradient using CSS animations
- **Particle System**: Light particle effects using p5.js for tech atmosphere
- **Grid Pattern**: Subtle grid overlay suggesting data networks

### Interactive Elements
- **Button Hover**: 3D lift effect with shadow expansion
- **Input Focus**: Glowing border with color transition
- **Card Hover**: Subtle scale and shadow effects
- **Loading States**: Smooth progress bars with gradient fills

### Animation Library Usage
- **Anime.js**: Smooth transitions, button interactions, progress animations
- **p5.js**: Background particle effects, data visualization
- **ECharts.js**: Interactive charts for engagement metrics
- **Splitting.js**: Text reveal animations for headings

### Header Effects
- **Typewriter Animation**: Using Typed.js for dynamic text display
- **Gradient Text**: Animated gradient colors on main headings
- **Floating Elements**: Subtle floating animation on platform icons

### Data Display
- **JSON Tree**: Syntax-highlighted, collapsible tree structure
- **Progress Visualization**: Animated progress bars with percentage display
- **Platform Icons**: Animated brand icons with hover effects
- **Status Indicators**: Color-coded status badges with pulse animations

## Layout & Structure

### Grid System
- **Container**: Max-width 1200px, centered
- **Columns**: CSS Grid with responsive breakpoints
- **Spacing**: 8px base unit system (8, 16, 24, 32, 48, 64px)
- **Responsive**: Mobile-first approach with fluid scaling

### Component Hierarchy
1. **Navigation Bar**: Fixed top navigation with logo and menu
2. **Hero Section**: URL input interface with background effects
3. **Configuration Panel**: Scraping options and settings
4. **Results Display**: JSON viewer and data visualization
5. **Footer**: Minimal footer with copyright and links

### Visual Hierarchy
- **Primary Actions**: Bright orange buttons with strong contrast
- **Secondary Actions**: Cyan buttons for less critical actions
- **Information Display**: Clean white cards with subtle shadows
- **Error States**: Red accents with clear messaging

## Interactive Design Patterns

### Form Elements
- **URL Input**: Large, prominent input with platform detection
- **Sliders**: Custom-styled range inputs for limits and filters
- **Toggles**: Smooth toggle switches for boolean options
- **Dropdowns**: Custom dropdown menus with search functionality

### Feedback Systems
- **Real-time Validation**: Instant feedback on URL format
- **Progress Indicators**: Multi-step progress with visual feedback
- **Status Messages**: Toast notifications for actions and errors
- **Loading States**: Skeleton screens and spinner animations

### Data Visualization
- **Engagement Charts**: Line charts showing post engagement over time
- **Platform Comparison**: Bar charts comparing different platforms
- **Word Clouds**: Tag clouds for hashtag analysis
- **Timeline Views**: Chronological display of scraped posts

This design system creates a professional, trustworthy interface that emphasizes functionality while maintaining visual appeal through subtle animations and modern styling.