import { useAuth } from '../../context/AuthContext'
import Avatar from '../../components/ui/Avatar'

export default function ProfilePage() {
  const { user } = useAuth()
  if (!user) return null
  return <main className="page-container account-page"><p className="eyebrow">Your profile</p><section className="account-card"><Avatar name={user.name} /><div><h1>{user.name}</h1><p>{user.email}</p></div></section></main>
}
