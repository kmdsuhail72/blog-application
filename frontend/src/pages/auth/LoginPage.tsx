import { Navigate } from 'react-router-dom'
import LoginForm from '../../components/forms/LoginForm'
import { useAuth } from '../../context/AuthContext'

export default function LoginPage() {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return null
  if (isAuthenticated) return <Navigate to="/dashboard" replace />
  return <main className="auth-page"><LoginForm /></main>
}
