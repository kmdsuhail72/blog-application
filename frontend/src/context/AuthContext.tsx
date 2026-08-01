import { createContext, useContext, useEffect, useState } from 'react'
import type { LoginPayload, RegisterPayload } from '../api/auth'
import { getCurrentUser, login as loginRequest, register as registerRequest } from '../api/auth'

export interface AuthUser { id: number; name: string; email: string }

interface AuthContextValue {
  user: AuthUser | null
  loading: boolean
  isAuthenticated: boolean
  login: (payload: LoginPayload) => Promise<void>
  register: (payload: RegisterPayload) => Promise<void>
  refreshUser: () => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)

  async function refreshUser() {
    if (!localStorage.getItem('access_token')) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const data = await getCurrentUser()
      setUser(data)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  async function login(payload: LoginPayload) {
    const data = await loginRequest(payload)
    localStorage.setItem('access_token', data.access_token)
    await refreshUser()
  }

  async function register(payload: RegisterPayload) {
    await registerRequest(payload)
  }

  useEffect(() => {
    const restoreTimer = window.setTimeout(() => {
      void refreshUser()
    }, 0)

    return () => window.clearTimeout(restoreTimer)
  }, [])

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated: Boolean(user), login, register, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// This module intentionally exports the provider and its consumer hook.
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}
