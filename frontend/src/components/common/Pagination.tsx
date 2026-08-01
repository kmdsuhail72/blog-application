export default function Pagination({ page, total, limit, onPageChange }: { page: number; total: number; limit: number; onPageChange: (page: number) => void }) {
  const pages = Math.max(1, Math.ceil(total / limit))
  if (pages === 1) return null
  return <nav className="pagination" aria-label="Pagination"><button type="button" disabled={page === 1} onClick={() => onPageChange(page - 1)}>Previous</button><span>Page {page} of {pages}</span><button type="button" disabled={page === pages} onClick={() => onPageChange(page + 1)}>Next</button></nav>
}
