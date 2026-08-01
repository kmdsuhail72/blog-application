import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { FiArrowRight, FiBookOpen, FiEdit3, FiUsers } from 'react-icons/fi'
import { fetchPosts } from '../../api/posts'
import Button from '../../components/ui/Button'
import Alert from '../../components/ui/Alert'
import EmptyState from '../../components/ui/EmptyState'
import PostCard from '../../components/posts/PostCard'
import SkeletonCard from '../../components/posts/SkeletonCard'

export default function HomePage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['posts', 'home'], queryFn: () => fetchPosts({ page: 1, limit: 6 }) })
  return <><section className="hero"><div className="hero__copy"><p className="eyebrow">The developer writing space</p><h1>Write.<br />Share.<br />Inspire.</h1><p>A modern blogging platform built with React, FastAPI and PostgreSQL. Find fresh perspectives, then publish your own.</p><div className="hero__actions"><Link to="/register"><Button>Start writing <FiArrowRight /></Button></Link><Link className="text-link" to="/posts">Explore articles</Link></div><div className="hero__proof"><span><FiEdit3 /> Write freely</span><span><FiUsers /> Learn together</span><span><FiBookOpen /> Read deeply</span></div></div><div className="hero__art"><div className="hero__card hero__card--top"><span>Featured thought</span><strong>Make room for better questions.</strong></div><div className="hero__card hero__card--bottom"><span>Made for makers</span><strong>Your next useful idea starts here.</strong></div></div></section><section className="articles-section"><div className="section-heading"><div><p className="eyebrow">Fresh perspectives</p><h2>Latest articles</h2></div><Link className="text-link" to="/posts">View all <FiArrowRight /></Link></div>{isError ? <Alert>We could not load articles right now. Please try again shortly.</Alert> : null}{isLoading ? <div className="post-grid">{[1, 2, 3].map((item) => <SkeletonCard key={item} />)}</div> : data?.items.length ? <div className="post-grid">{data.items.map((post) => <PostCard key={post.id} post={post} />)}</div> : <EmptyState title="No articles yet" description="The first great idea is waiting to be published." />}</section></>
}
