import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useAuth } from '../../context/AuthContext'
import Button from '../ui/Button'

const registerSchema = z.object({
  name: z.string().trim().min(2, 'Use at least 2 characters').max(100, 'Name is too long'),
  email: z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Use at least 8 characters'),
})
type RegisterValues = z.infer<typeof registerSchema>

function errorMessage(error: unknown) {
  const detail = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail
  return detail || 'Unable to create your account. Please try again.'
}

export default function RegisterForm() {
  const { register: createAccount } = useAuth()
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<RegisterValues>({ resolver: zodResolver(registerSchema) })
  const submit = async (values: RegisterValues) => {
    try {
      await createAccount(values)
      toast.success('Account created. You can sign in now.')
      navigate('/login', { replace: true })
    } catch (error) {
      toast.error(errorMessage(error))
    }
  }
  return <form className="auth-form" onSubmit={handleSubmit(submit)} noValidate>
    <div><p className="eyebrow">Join the community</p><h1>Create your account</h1><p>Start publishing ideas that help other developers.</p></div>
    <label className="ui-input">Name<input autoComplete="name" {...register('name')} />{errors.name && <small>{errors.name.message}</small>}</label>
    <label className="ui-input">Email<input type="email" autoComplete="email" {...register('email')} />{errors.email && <small>{errors.email.message}</small>}</label>
    <label className="ui-input">Password<input type="password" autoComplete="new-password" {...register('password')} />{errors.password && <small>{errors.password.message}</small>}</label>
    <Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Creating account…' : 'Create account'}</Button>
    <p className="auth-form__footer">Already have an account? <Link to="/login">Sign in</Link></p>
  </form>
}
