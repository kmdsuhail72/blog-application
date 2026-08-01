import { useSearchParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { fetchPosts } from '../../api/posts'
import SearchBar from '../../components/common/SearchBar'
import EmptyState from '../../components/ui/EmptyState'
import Alert from '../../components/ui/Alert'
import PostCard from '../../components/posts/PostCard'
import SkeletonCard from '../../components/posts/SkeletonCard'

export default function SearchPage() {
  const [params] = useSearchParams(); const query = params.get('q') || ''
  const { data, isLoading, isError } = useQuery({ queryKey: ['posts', 'search', query], queryFn: () => fetchPosts({ search: query, limit: 12 }), enabled: Boolean(query) })
  return <main className="page-container posts-page"><div className="posts-page__heading"><div><p className="eyebrow">Search</p><h1>{query ? `Results for “${query}”` : 'Find an article'}</h1></div><SearchBar /></div>{isError ? <Alert>Search is unavailable right now. Please try again shortly.</Alert> : null}{isLoading ? <div className="post-grid">{[1, 2, 3].map((item) => <SkeletonCard key={item} />)}</div> : data?.items.length ? <div className="post-grid">{data.items.map((post) => <PostCard key={post.id} post={post} />)}</div> : <EmptyState title={query ? 'No matching articles' : 'Start typing to search'} description="Try a title, topic, or keyword." />}</main>
}
