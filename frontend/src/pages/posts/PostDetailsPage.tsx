import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { FiArrowLeft, FiClock, FiTag } from 'react-icons/fi'
import { fetchPost } from '../../api/posts'
import Alert from '../../components/ui/Alert'
import Badge from '../../components/ui/Badge'
import MarkdownContent from '../../components/posts/MarkdownContent'
import { publishedDate, readingTime } from '../../utils/posts'

export default function PostDetailsPage() {
  const { postId } = useParams(); const id = Number(postId)
  const { data: post, isLoading, isError } = useQuery({ queryKey: ['post', id], queryFn: () => fetchPost(id), enabled: Number.isInteger(id) && id > 0 })
  if (isLoading) return <main className="page-container">Loading article…</main>
  if (isError || !post) return <main className="page-container"><Alert>We could not find that article.</Alert><Link className="text-link" to="/posts"><FiArrowLeft /> Back to articles</Link></main>
  return <article className="article-page"><Link className="text-link" to="/posts"><FiArrowLeft /> All articles</Link>{post.cover_image ? <img className="article-page__cover" src={post.cover_image} alt="" /> : null}<header><div className="article-page__tags">{post.tags.map((tag) => <Badge key={tag.id}>{tag.name}</Badge>)}</div><h1>{post.title}</h1><div className="article-page__meta"><span>{publishedDate(post.created_at)}</span><span><FiClock /> {readingTime(post.content)}</span><span>By author #{post.author_id}</span></div></header><MarkdownContent content={post.content} /><footer className="article-page__footer"><FiTag /> {post.tags.length ? post.tags.map((tag) => tag.name).join(', ') : 'No tags'}</footer></article>
}
