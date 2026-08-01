import { useEffect, useState } from 'react'
import { FiSearch } from 'react-icons/fi'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function SearchBar() {
  const [params] = useSearchParams()
  const [term, setTerm] = useState(params.get('q') || '')
  const navigate = useNavigate()
  useEffect(() => {
    const timer = window.setTimeout(() => {
      const query = term.trim()
      if (query) navigate(`/search?q=${encodeURIComponent(query)}`)
    }, 400)
    return () => window.clearTimeout(timer)
  }, [term, navigate])
  return <label className="search-bar"><FiSearch /><input value={term} onChange={(event) => setTerm(event.target.value)} placeholder="Search articles" aria-label="Search articles" /></label>
}
