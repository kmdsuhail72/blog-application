import { memo } from 'react'
import { Link } from 'react-router-dom'
import { FiArrowUpRight, FiClock } from 'react-icons/fi'
import type { Post } from '../../api/posts'
import Badge from '../ui/Badge'
import { postExcerpt, publishedDate, readingTime } from '../../utils/posts'

function PostCard({ post }: { post: Post }) {
  return <article className="post-card">
    <Link to={`/posts/${post.id}`} aria-label={`Read ${post.title}`}>{post.cover_image ? <img src={post.cover_image} alt="" loading="lazy" /> : <div className="post-cover" />}</Link>
    <div className="post-card__body"><div className="post-card__meta"><Badge>{post.tags[0]?.name || `Category ${post.category_id}`}</Badge><span><FiClock /> {readingTime(post.content)}</span></div><h2><Link to={`/posts/${post.id}`}>{post.title}</Link></h2><p>{postExcerpt(post)}</p><footer><span>{publishedDate(post.created_at)}</span><Link to={`/posts/${post.id}`}>Read more <FiArrowUpRight /></Link></footer></div>
  </article>
}
export default memo(PostCard)
