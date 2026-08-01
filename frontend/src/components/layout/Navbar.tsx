import { useState } from 'react'
import { FiMenu, FiX } from 'react-icons/fi'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import Avatar from '../ui/Avatar'
import Button from '../ui/Button'
import Logo from '../common/Logo'
import ThemeToggle from '../common/ThemeToggle'
import SearchBar from '../common/SearchBar'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const close = () => setOpen(false)
  const handleLogout = () => { logout(); close(); navigate('/login') }
  return <header className="site-header"><div className="nav-shell"><Logo /><button className="nav-menu" type="button" onClick={() => setOpen(!open)} aria-label="Toggle navigation">{open ? <FiX /> : <FiMenu />}</button><nav className={open ? 'nav-links nav-links--open' : 'nav-links'}><NavLink to="/" onClick={close}>Home</NavLink><NavLink to="/posts" onClick={close}>Articles</NavLink><SearchBar />{user ? <><NavLink to="/dashboard" onClick={close}>Dashboard</NavLink><Link className="nav-user" to="/profile" onClick={close}><Avatar name={user.name} /><span>{user.name}</span></Link><Button variant="ghost" onClick={handleLogout}>Logout</Button></> : <><Link to="/login" onClick={close}>Log in</Link><Link to="/register" onClick={close}><Button>Start writing</Button></Link></>}<ThemeToggle /></nav></div></header>
}
