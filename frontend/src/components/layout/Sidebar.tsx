import { NavLink } from 'react-router-dom'

export default function Sidebar() { return <aside className="dashboard-sidebar"><strong>Workspace</strong><NavLink to="/dashboard">Overview</NavLink><a href="#posts">Posts</a><a href="#drafts">Drafts</a><a href="#bookmarks">Bookmarks</a><a href="#settings">Settings</a></aside> }
