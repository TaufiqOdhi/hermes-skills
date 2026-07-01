---
name: nextjs-swr-data-fetching
description: SWR data fetching patterns, hooks, and best practices for Next.js applications
tags: [nextjs, swr, data-fetching, hooks, api]
---

# Next.js SWR Data Fetching

## Overview
This skill covers SWR (Stale-While-Revalidate) patterns for data fetching in Next.js applications, including custom hooks, error handling, and integration with Next.js features.

## Core Concepts

### Basic SWR Usage

#### Fetcher Function
```typescript
// hooks/useData.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function useData(url: string) {
  const { data, error, isLoading, mutate } = useSWR(url, fetcher)
  return { data, error, isLoading, mutate }
}
```

#### Usage in Component
```typescript
// components/UserList.tsx
import { useData } from '@/hooks/useData'

export function UserList() {
  const { data, error, isLoading, mutate } = useData('/api/users')

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### Custom Hooks

#### Generic Data Hook
```typescript
// hooks/useApi.ts
import useSWR from 'swr'

interface UseApiOptions<T> {
  revalidateOnFocus?: boolean
  revalidateOnReconnect?: boolean
  shouldRetryOnError?: boolean
}

export function useApi<T>(
  url: string | null,
  options?: UseApiOptions<T>
) {
  const fetcher = (url: string) => fetch(url).then((res) => res.json())

  const { data, error, isLoading, mutate, isValidating } = useSWR<T>(
    url,
    fetcher,
    {
      revalidateOnFocus: options?.revalidateOnFocus ?? true,
      revalidateOnReconnect: options?.revalidateOnReconnect ?? true,
      shouldRetryOnError: options?.shouldRetryOnError ?? true,
    }
  )

  return {
    data,
    error,
    isLoading,
    isValidating,
    mutate,
  }
}
```

#### Usage
```typescript
// components/Users.tsx
import { useApi } from '@/hooks/useApi'

export function Users() {
  const { data, error, isLoading, mutate } = useApi<User[]>('/api/users')

  if (isLoading) return <div>Loading users...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <button onClick={() => mutate()}>Refresh</button>
      <ul>
        {data?.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### SWR with Mutations

#### Optimistic Updates
```typescript
// hooks/useTodo.ts
import useSWR from 'swr'
import useSWRMutation from 'swr/mutation'

const fetcher = async (url: string, { arg }: { arg: { method: string; body?: any } }) => {
  const res = await fetch(url, {
    method: arg.method,
    body: arg.body ? JSON.stringify(arg.body) : undefined,
  })
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export function useTodo() {
  const { data, error, isLoading, mutate } = useSWR('/api/todos', fetcher)

  const { trigger, isMutating } = useSWRMutation('/api/todos', fetcher, {
    onSuccess: () => mutate(),
  })

  return {
    todos: data,
    error,
    isLoading,
    isMutating,
    trigger,
  }
}
```

### Server-Side Data Fetching

#### Next.js Server Components
```typescript
// app/page.tsx
import { useSWR } from 'swr'

async function getData() {
  const res = await fetch('https://api.example.com/data')
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export default async function Page() {
  const data = await getData()

  return (
    <div>
      <h1>Data</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
```

#### Client-Side Data Fetching
```typescript
// components/DataDisplay.tsx
'use client'

import { useSWR } from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function DataDisplay() {
  const { data, error, isLoading } = useSWR('/api/data', fetcher)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>{JSON.stringify(data, null, 2)}</div>
}
```

### Error Handling

#### Error Boundaries
```typescript
// components/ErrorBoundary.tsx
'use client'

import { useSWR } from 'swr'

export function ErrorBoundary({ children }: { children: React.ReactNode }) {
  const { error } = useSWR('/api/data')

  if (error) {
    return (
      <div>
        <h2>Error</h2>
        <p>{error.message}</p>
      </div>
    )
  }

  return <>{children}</>
}
```

#### Retry Logic
```typescript
// hooks/useApi.ts
import useSWR from 'swr'

export function useApi<T>(
  url: string | null,
  options?: { retry?: number }
) {
  const fetcher = (url: string) => fetch(url).then((res) => {
    if (!res.ok) throw new Error('Failed to fetch')
    return res.json()
  })

  const { data, error, isLoading, mutate } = useSWR<T>(
    url,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      shouldRetryOnError: true,
      errorRetryCount: options?.retry ?? 3,
      errorRetryInterval: 5000,
    }
  )

  return {
    data,
    error,
    isLoading,
    mutate,
  }
}
```

### Caching and Revalidation

#### Cache Configuration
```typescript
// hooks/useApi.ts
import useSWR from 'swr'

export function useApi<T>(
  url: string | null,
  options?: { cache?: boolean }
) {
  const fetcher = (url: string) => fetch(url).then((res) => res.json())

  const { data, error, isLoading, mutate } = useSWR<T>(
    url,
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      dedupingInterval: 5000, // 5 seconds
      ...options?.cache ? { keepPreviousData: true } : {},
    }
  )

  return {
    data,
    error,
    isLoading,
    mutate,
  }
}
```

#### Manual Revalidation
```typescript
// components/UserList.tsx
'use client'

import { useSWR } from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function UserList() {
  const { data, error, isLoading, mutate } = useSWR('/api/users', fetcher)

  const refresh = () => mutate()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <button onClick={refresh}>Refresh</button>
      <ul>
        {data?.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Advanced Patterns

#### Conditional Fetching
```typescript
// hooks/useConditionalData.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function useConditionalData(
  condition: boolean,
  url: string
) {
  const { data, error, isLoading } = useSWR(
    condition ? url : null,
    fetcher
  )

  return {
    data,
    error,
    isLoading,
  }
}
```

#### Pagination
```typescript
// hooks/usePagination.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function usePagination<T>(
  url: string,
  page: number,
  pageSize: number
) {
  const { data, error, isLoading, mutate } = useSWR<T[]>(
    `${url}?page=${page}&pageSize=${pageSize}`,
    fetcher
  )

  return {
    data,
    error,
    isLoading,
    mutate,
  }
}
```

#### Infinite Scroll
```typescript
// hooks/useInfiniteScroll.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function useInfiniteScroll<T>(
  url: string,
  page: number
) {
  const { data, error, isLoading, mutate } = useSWR<T[]>(
    `${url}?page=${page}`,
    fetcher
  )

  return {
    data,
    error,
    isLoading,
    mutate,
  }
}
```

## Best Practices

1. **Use typed fetchers** - Ensure fetcher returns correct type
2. **Handle loading states** - Show loading indicators
3. **Handle errors gracefully** - Display error messages
4. **Use dedupingInterval** - Avoid duplicate requests
5. **Optimize revalidation** - Control when to revalidate
6. **Use keepPreviousData** - Maintain previous data during loading
7. **Cache strategically** - Balance between freshness and performance
8. **Use server components** - For initial data fetching

## Common Patterns

### SWR with Next.js API Routes
```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await fetch('https://api.example.com/users')
    .then((res) => res.json())
    .catch(() => [])

  return NextResponse.json(users)
}
```

### SWR with Local Data
```typescript
// hooks/useLocalData.ts
import useSWR from 'swr'

const fetcher = () => Promise.resolve({ name: 'Local Data' })

export function useLocalData() {
  const { data, error, isLoading, mutate } = useSWR('/local-data', fetcher)

  return {
    data,
    error,
    isLoading,
    mutate,
  }
}
```

## Pitfalls

1. **Don't use SWR in server components** - Only for client components
2. **Don't forget to handle null URLs** - SWR requires a string or null
3. **Don't mutate data directly** - Use mutate() for updates
4. **Don't ignore errors** - Always handle error states
5. **Don't use SWR for static data** - Use server components instead

## Related Skills
- `nextjs-app-router-patterns` - Next.js routing patterns
- `nextjs-zustand-state-management` - State management patterns
- `nextjs-tailwind-styling` - Styling patterns