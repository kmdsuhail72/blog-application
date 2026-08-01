import { lazy, Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'
import ProtectedRoute from './ProtectedRoute'

const HomePage = lazy(() => import('../pages/posts/HomePage'))
const PostListPage = lazy(() => import('../pages/posts/PostListPage'))
const PostDetailsPage = lazy(() => import('../pages/posts/PostDetailsPage'))
const SearchPage = lazy(() => import('../pages/search/SearchPage'))
const LoginPage = lazy(() => import('../pages/auth/LoginPage'))
const RegisterPage = lazy(() => import('../pages/auth/RegisterPage'))
const DashboardPage = lazy(() => import('../pages/dashboard/DashboardPage'))
const ProfilePage = lazy(() => import('../pages/profile/ProfilePage'))
const SettingsPage = lazy(() => import('../pages/profile/SettingsPage'))
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'))

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <MainLayout><Suspense fallback={<main className="page-container">Loading…</main>}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/posts" element={<PostListPage />} />
          <Route path="/posts/:postId" element={<PostDetailsPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense></MainLayout>
    </BrowserRouter>
  )
}
