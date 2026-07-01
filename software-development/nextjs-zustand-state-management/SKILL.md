---
name: nextjs-zustand-state-management
description: Zustand state management patterns, store patterns, and best practices for Next.js applications
tags: [nextjs, zustand, state-management, store]
---

# Next.js Zustand State Management

## Overview
This skill covers Zustand patterns for managing global state in Next.js applications, including store creation, selectors, middleware, and integration with Next.js features.

## Core Concepts

### Basic Store Creation

#### Simple Store
```typescript
// store/useStore.ts
import { create } from 'zustand'

interface StoreState {
  count: number
  increment: () => void
  decrement: () => void
}

export const useStore = create<StoreState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}))
```

#### Usage in Component
```typescript
// components/Counter.tsx
import { useStore } from '@/store/useStore'

export function Counter() {
  const count = useStore((state) => state.count)
  const increment = useStore((state) => state.increment)
  const decrement = useStore((state) => state.decrement)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  )
}
```

### Store with State and Actions

#### Typed Store
```typescript
// store/useAppStore.ts
import { create } from 'zustand'

interface AppState {
  currentTask: string | null
  setCurrentTask: (task: string | null) => void
  logs: string[]
  addLog: (log: string) => void
}

export const useAppStore = create<AppState>((set) => ({
  currentTask: null,
  setCurrentTask: (task) => set({ currentTask: task }),
  logs: ["Container started", "Next.js initialized"],
  addLog: (log) => set((state) => ({ logs: [...state.logs, log] })),
}))
```

### Selectors

#### Optimized Re-renders
```typescript
// store/useStore.ts
import { create } from 'zustand'

interface StoreState {
  user: { name: string; email: string }
  tasks: Task[]
  updateUser: (user: Partial<StoreState['user']>) => void
  addTask: (task: Task) => void
}

export const useStore = create<StoreState>((set) => ({
  user: { name: '', email: '' },
  tasks: [],
  updateUser: (updates) => set((state) => ({ user: { ...state.user, ...updates } })),
  addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
}))

// Usage - only re-renders when user.name changes
const userName = useStore((state) => state.user.name)
```

### Middleware

#### Persist Middleware
```typescript
// store/useStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface StoreState {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

export const useStore = create<StoreState>()(
  persist(
    (set) => ({
      theme: 'dark',
      toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
    }),
    {
      name: 'theme-storage', // localStorage key
    }
  )
)
```

#### DevTools Middleware
```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface StoreState {
  count: number
  increment: () => void
}

export const useStore = create<StoreState>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    { name: 'CounterStore' }
  )
)
```

### Async Actions

#### Server Actions Integration
```typescript
// store/useStore.ts
import { create } from 'zustand'
import { createServerAction } from 'zsa'

interface StoreState {
  isLoading: boolean
  error: string | null
  fetchData: () => Promise<void>
}

export const useStore = create<StoreState>((set) => ({
  isLoading: false,
  error: null,
  fetchData: async () => {
    set({ isLoading: true, error: null })
    try {
      const res = await fetch('/api/data')
      const data = await res.json()
      // Handle data
    } catch (error) {
      set({ error: 'Failed to fetch' })
    } finally {
      set({ isLoading: false })
    }
  },
}))
```

### Integration with Next.js

#### Server Component Usage
```typescript
// app/page.tsx
import { useStore } from '@/store/useStore'

export default function Page() {
  const logs = useStore((state) => state.logs)
  return (
    <div>
      <h1>Logs</h1>
      <ul>
        {logs.map((log, i) => <li key={i}>{log}</li>)}
      </ul>
    </div>
  )
}
```

#### Client Component Usage
```typescript
// components/Counter.tsx
'use client'

import { useStore } from '@/store/useStore'

export function Counter() {
  const count = useStore((state) => state.count)
  const increment = useStore((state) => state.increment)
  return <button onClick={increment}>Count: {count}</button>
}
```

### Advanced Patterns

#### Derived State
```typescript
// store/useStore.ts
import { create } from 'zustand'

interface StoreState {
  items: Item[]
  addItem: (item: Item) => void
}

interface DerivedState {
  total: number
  itemsByCategory: Record<string, Item[]>
}

export const useStore = create<StoreState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
}))

// Derived selector
export const useDerivedState = () => {
  const items = useStore((state) => state.items)
  return {
    total: items.length,
    itemsByCategory: items.reduce((acc, item) => {
      acc[item.category] = [...(acc[item.category] || []), item]
      return acc
    }, {} as Record<string, Item[]>),
  }
}
```

#### Reset State
```typescript
// store/useStore.ts
import { create } from 'zustand'

interface StoreState {
  data: Data[]
  reset: () => void
}

export const useStore = create<StoreState>((set) => ({
  data: [],
  reset: () => set({ data: [] }),
}))
```

## Best Practices

1. **Type your store** - Use TypeScript interfaces for type safety
2. **Use selectors** - Avoid unnecessary re-renders
3. **Keep stores focused** - One store per domain
4. **Use middleware wisely** - persist for user preferences, devtools for debugging
5. **Handle async actions** - Use loading/error states
6. **Export typed hooks** - Create typed selector functions
7. **Keep actions pure** - Avoid side effects in actions
8. **Use immer middleware** - For complex state mutations

## Common Patterns

### Store with Immer
```typescript
// store/useStore.ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface StoreState {
  todos: Todo[]
  addTodo: (todo: Todo) => void
  toggleTodo: (id: string) => void
}

export const useStore = create<StoreState>()(
  immer((set) => ({
    todos: [],
    addTodo: (todo) => set((state) => {
      state.todos.push(todo)
    }),
    toggleTodo: (id) => set((state) => {
      const todo = state.todos.find(t => t.id === id)
      if (todo) todo.completed = !todo.completed
    }),
  }))
)
```

### Store with Persistence
```typescript
// store/useStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface StoreState {
  user: User | null
  setUser: (user: User | null) => void
}

export const useStore = create<StoreState>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
    }),
    {
      name: 'user-storage',
      partialize: (state) => ({ user: state.user }), // Only persist user
    }
  )
)
```

## Pitfalls

1. **Don't mutate state directly** - Always use set or immer
2. **Don't create infinite loops** - Ensure actions don't trigger themselves
3. **Don't forget to export** - Export typed hooks for reuse
4. **Don't use in server components** - Only for client components
5. **Don't overuse global state** - Prefer local state when possible

## Related Skills
- `nextjs-app-router-patterns` - Next.js routing patterns
- `nextjs-swr-data-fetching` - Data fetching patterns
- `nextjs-tailwind-styling` - Styling patterns