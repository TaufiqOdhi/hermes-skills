---
name: nextjs-tailwind-styling
description: Tailwind CSS patterns, utilities, and best practices for Next.js applications
tags: [nextjs, tailwind, styling, css]
---

# Next.js Tailwind Styling

## Overview
This skill covers Tailwind CSS patterns and best practices for styling Next.js applications, including utility classes, custom configurations, and integration with Next.js features.

## Core Concepts

### Basic Setup

#### Tailwind Configuration
```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
      },
    },
  },
  plugins: [],
}
export default config
```

#### PostCSS Configuration
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Utility Classes

#### Spacing
```tsx
<div className="p-4 m-2 gap-4 space-y-4">
  <div className="mt-8 mb-4">
    <div className="px-4 py-2">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex-1">
```

#### Typography
```tsx
<h1 className="text-3xl font-bold tracking-tight">
  Title
</h1>
<p className="text-slate-400 mt-2">
  Description
</p>
<p className="text-sm text-slate-500">
  Small text
</p>
```

#### Flexbox
```tsx
<div className="flex items-center justify-between">
  <div>Left content</div>
  <div>Right content</div>
</div>

<div className="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div className="flex flex-row items-center justify-center gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

#### Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
</div>

<div className="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div className="lg:col-span-2">Wide item</div>
  <div>Narrow item</div>
</div>
```

#### Borders and Shadows
```tsx
<div className="border border-slate-800 rounded-lg">
  <div className="border-b border-slate-800">
    Header
  </div>
  <div className="p-4">
    Content
  </div>
</div>

<div className="shadow-lg">
  <div className="shadow-md">
    <div className="shadow-sm">
      <div className="shadow-none">
```

#### Colors
```tsx
<div className="bg-slate-950 text-slate-50">
  Dark theme
</div>

<div className="bg-indigo-600 text-white">
  Primary color
</div>

<div className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
  Success state
</div>

<div className="bg-amber-500/20 text-amber-400 border border-amber-500/30">
  Warning state
</div>
```

### Dark Mode

#### Tailwind Config with Dark Mode
```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class', // or 'media'
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
      },
    },
  },
  plugins: [],
}
export default config
```

#### Usage in Components
```tsx
'use client'

import { useEffect } from 'react'

export function ThemeToggle() {
  useEffect(() => {
    const root = document.documentElement
    root.classList.toggle('dark')
  }, [])

  return (
    <button className="px-4 py-2 bg-slate-800 text-white rounded">
      Toggle Theme
    </button>
  )
}
```

### Responsive Design

#### Responsive Classes
```tsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

<div className="p-2 md:p-4 lg:p-6">
  Responsive padding
</div>

<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  Responsive grid
</div>

<div className="hidden md:block lg:hidden">
  Responsive visibility
</div>
```

### Next.js Integration

#### Global Styles
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

#### Next.js Font
```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

### Component Patterns

#### Card Component
```tsx
// components/Card.tsx
export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      {children}
    </div>
  )
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="border-b border-slate-800 pb-4 mb-4">{children}</div>
}

export function CardContent({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

#### Button Component
```tsx
// components/Button.tsx
export function Button({
  children,
  variant = 'primary',
  size = 'md',
}: {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}) {
  const baseClasses = "px-4 py-2 rounded font-medium transition"
  const variants = {
    primary: "bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700",
    secondary: "bg-slate-800 hover:bg-slate-700 active:bg-slate-900",
    ghost: "bg-transparent hover:bg-slate-800",
  }
  const sizes = {
    sm: "text-sm px-3 py-1",
    md: "text-base px-4 py-2",
    lg: "text-lg px-6 py-3",
  }

  return (
    <button className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}>
      {children}
    </button>
  )
}
```

#### Form Component
```tsx
// components/Form.tsx
export function Form({ children }: { children: React.ReactNode }) {
  return (
    <form className="space-y-4">
      {children}
    </form>
  )
}

export function Input({
  placeholder,
  value,
  onChange,
}: {
  placeholder: string
  value: string
  onChange: (value: string) => void
}) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="flex-1 bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
    />
  )
}
```

### Advanced Patterns

#### Custom Utilities
```css
/* app/globals.css */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}
```

#### Animations
```css
/* app/globals.css */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-in-out;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
```

#### Usage in Components
```tsx
<div className="animate-fade-in">
  <div className="animate-slide-up">
    <div className="transition-all duration-300 hover:scale-105">
```

## Best Practices

1. **Use semantic HTML** - Combine Tailwind with semantic elements
2. **Keep classes organized** - Group related utilities
3. **Use responsive prefixes** - Optimize for different screen sizes
4. **Avoid arbitrary values** - Use theme extensions when possible
5. **Use dark mode** - Support both light and dark themes
6. **Keep components focused** - Single responsibility per component
7. **Use composition** - Build complex UI from simple components
8. **Optimize bundle size** - Remove unused Tailwind classes

## Common Patterns

#### Loading State
```tsx
<div className="flex items-center justify-center min-h-screen">
  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
</div>
```

#### Empty State
```tsx
<div className="flex flex-col items-center justify-center min-h-screen text-center">
  <div className="text-6xl mb-4">📭</div>
  <h2 className="text-xl font-semibold text-slate-200">No tasks</h2>
  <p className="text-slate-400 mt-2">Add a task to get started</p>
</div>
```

#### Error State
```tsx
<div className="flex flex-col items-center justify-center min-h-screen text-center">
  <div className="text-6xl mb-4">⚠️</div>
  <h2 className="text-xl font-semibold text-red-400">Something went wrong</h2>
  <p className="text-slate-400 mt-2">Please try again later</p>
</div>
```

## Pitfalls

1. **Don't overuse arbitrary values** - Use theme extensions when possible
2. **Don't forget to configure Tailwind** - Ensure content paths are correct
3. **Don't ignore dark mode** - Support both themes
4. **Don't use too many utility classes** - Keep classes readable
5. **Don't forget to include PostCSS** - Tailwind requires PostCSS

## Related Skills
- `nextjs-app-router-patterns` - Next.js routing patterns
- `nextjs-zustand-state-management` - State management patterns
- `nextjs-swr-data-fetching` - Data fetching patterns