import { Link } from 'react-router-dom'
export default function NotFoundPage() { return <main className="page-container not-found"><p className="eyebrow">404</p><h1>Page not found</h1><p>The page you requested does not exist or has moved.</p><Link className="text-link" to="/">Go home</Link></main> }
