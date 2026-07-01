---
name: nextjs-app-router-patterns
description: Next.js App Router patterns, conventions, and best practices for building modern Next.js applications
tags: [nextjs, app-router, routing, conventions]
---

# Next.js App Router Patterns

## Overview
This skill covers established patterns and conventions for using Next.js App Router (Next.js 13+), including file organization, routing, layouts, and server/client components.

## Core Concepts

### File Organization
```
app/
├── layout.tsx          # Root layout (metadata, providers)
├── page.tsx            # Home page
├── globals.css         # Global styles
├── [slug]/
│   ├── page.tsx        # Dynamic route
│   └── layout.tsx      # Route-specific layout
├── api/
│   └── [endpoint]/
│       └── route.ts    # API route
├── (group)/
│   ├── page.tsx        # Grouped routes (no URL segment)
│   └── layout.tsx
└── _private/
    └── page.tsx        # Private routes (no URL segment)
```

### Component Types

#### Server Components (Default)
```typescript
// app/page.tsx - Server component by default
export default function Page() {
  return <div>Server rendered content</div>
}
```

#### Client Components
```typescript
// app/components/Button.tsx
'use client'

import { useState } from 'react'

export function Button() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

#### Server Actions
```typescript
// app/actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  // Server-side logic
}
```

### Layouts

#### Root Layout
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

#### Route Layouts
```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard-layout">
      <nav>Navigation</nav>
      <main>{children}</main>
    </div>
  )
}
```

### Dynamic Routes

#### Simple Dynamic Route
```typescript
// app/blog/[slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <div>Post: {params.slug}</div>
}
```

#### Catch-all Routes
```typescript
// app/blog/[...slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string[] } }) {
  return <div>Post: {params.slug.join('/')}</div>
}
```

### Data Fetching

#### Server-Side Data Fetching
```typescript
// app/page.tsx
async function getData() {
  const res = await fetch('https://api.example.com/data')
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export default async function Page() {
  const data = await getData()
  return <div>{data.title}</div>
}
```

#### Client-Side Data Fetching (SWR)
```typescript
// hooks/useData.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function useData(url: string) {
  const { data, error, isLoading, mutate } = useSWR(url, fetcher)
  return { data, error, isLoading, mutate }
}
```

### Error Handling

#### Error Boundary
```typescript
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

#### Loading State
```typescript
// app/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}
```

## Best Practices

1. **Use Server Components by default** - Reduce client bundle size
2. **Keep client components small** - Only use 'use client' where needed
3. **Use metadata API** - SEO-friendly metadata management
4. **Organize routes logically** - Group related routes in folders
5. **Use route groups** - For organization without affecting URL
6. **Handle errors gracefully** - Use error.tsx and loading.tsx
7. **Use dynamic imports** - For code splitting
8. **Follow TypeScript conventions** - Strict typing throughout

## Common Patterns

### Navigation
```typescript
import Link from 'next/link'

<Link href="/dashboard">Dashboard</Link>
```

### Image Optimization
```typescript
import Image from 'next/image'

<Image
  src="/hero.png"
  alt="Hero"
  width={800}
  height={600}
  priority
/>
```

### Metadata
```typescript
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
  },
}
```

## Pitfalls

1. **Don't use 'use client' in server components** - Will cause errors
2. **Avoid client-side state in server components** - Use props or server actions
3. **Don't use Next.js features outside App Router** - Pages router still exists
4. **Don't forget to export metadata** - For SEO
5. **Don't use 'use client' in layout.tsx** - Only in components

## Related Skills
- `nextjs-zustand-state-management` - State management patterns
- `nextjs-swr-data-fetching` - Data fetching patterns
- `nextjs-tailwind-styling` - Styling patterns
- `nextjs-shadcn-ui-components` - UI component patterns