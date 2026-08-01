import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useAuth } from '../../context/AuthContext'
import Button from '../ui/Button'

const loginSchema = z.object({
  email: z.string().email('Enter a valid email address'),
  password: z.string().min(1, 'Enter your password'),
})
type LoginValues = z.infer<typeof loginSchema>

function errorMessage(error: unknown) {
  const detail = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail
  return detail || 'Unable to sign in. Check your connection and try again.'
}

export default function LoginForm() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginValues>({ resolver: zodResolver(loginSchema) })

  const submit = async (values: LoginValues) => {
    try {
      await login(values)
      toast.success('Welcome back!')
      navigate('/dashboard', { replace: true })
    } catch (error) {
      toast.error(errorMessage(error))
    }
  }

  return <form className="auth-form" onSubmit={handleSubmit(submit)} noValidate>
    <div><p className="eyebrow">Welcome back</p><h1>Sign in to your account</h1><p>Continue reading, writing, and sharing your ideas.</p></div>
    <label className="ui-input">Email<input type="email" autoComplete="email" {...register('email')} />{errors.email && <small>{errors.email.message}</small>}</label>
    <label className="ui-input">Password<input type="password" autoComplete="current-password" {...register('password')} />{errors.password && <small>{errors.password.message}</small>}</label>
    <Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Signing in…' : 'Sign in'}</Button>
    <p className="auth-form__footer">New here? <Link to="/register">Create an account</Link></p>
  </form>
}
