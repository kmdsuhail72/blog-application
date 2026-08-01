import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { fetchPosts } from '../../api/posts'
import Alert from '../../components/ui/Alert'
import EmptyState from '../../components/ui/EmptyState'
import Pagination from '../../components/common/Pagination'
import SearchBar from '../../components/common/SearchBar'
import PostCard from '../../components/posts/PostCard'
import SkeletonCard from '../../components/posts/SkeletonCard'

const categories = ['All', 'React', 'Python', 'FastAPI', 'DevOps', 'Docker']
export default function PostListPage() {
  const [page, setPage] = useState(1)
  const [category, setCategory] = useState('')
  const limit = 9
  const { data, isLoading, isError } = useQuery({ queryKey: ['posts', page, category], queryFn: () => fetchPosts({ page, limit, ...(category ? { category } : {}) }) })
  const changeCategory = (value: string) => { setCategory(value); setPage(1) }
  return <main className="page-container posts-page"><div className="posts-page__heading"><div><p className="eyebrow">Browse articles</p><h1>Ideas worth sharing</h1></div><SearchBar /></div><div className="category-chips">{categories.map((item) => <button className={category === (item === 'All' ? '' : item.toLowerCase()) ? 'active' : ''} key={item} onClick={() => changeCategory(item === 'All' ? '' : item.toLowerCase())}>{item}</button>)}</div>{isError ? <Alert>We could not load articles right now. Please try again shortly.</Alert> : null}{isLoading ? <div className="post-grid">{Array.from({ length: 6 }, (_, index) => <SkeletonCard key={index} />)}</div> : data?.items.length ? <><div className="post-grid">{data.items.map((post) => <PostCard key={post.id} post={post} />)}</div><Pagination page={page} total={data.total} limit={limit} onPageChange={setPage} /></> : <EmptyState title="No articles found" description="Try a different category or search term." />}</main>
}
