import api from './api'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  name: string
  email: string
  password: string
}

export async function login(payload: LoginPayload) {
  const response = await api.post(
    '/auth/login',
    new URLSearchParams({ username: payload.email, password: payload.password }),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } },
  )
  return response.data
}

export async function register(payload: RegisterPayload) {
  const response = await api.post('/users/', payload)
  return response.data
}

export async function getCurrentUser() {
  const response = await api.get('/auth/me')
  return response.data
}
