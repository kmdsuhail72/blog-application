import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()
  const location = useLocation()
  if (loading) return <main className="page-container">Loading your account…</main>
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location }} />
  return children
}
