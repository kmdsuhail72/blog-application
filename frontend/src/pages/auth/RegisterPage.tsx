import { Navigate } from 'react-router-dom'
import RegisterForm from '../../components/forms/RegisterForm'
import { useAuth } from '../../context/AuthContext'

export default function RegisterPage() {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return null
  if (isAuthenticated) return <Navigate to="/dashboard" replace />
  return <main className="auth-page"><RegisterForm /></main>
}
