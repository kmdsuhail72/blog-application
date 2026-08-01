import { FiArrowUpRight, FiClock } from 'react-icons/fi'
import Card from '../ui/Card'
import Badge from '../ui/Badge'

export interface FeaturedPost { id: number; title: string; content?: string; cover_image?: string; created_at?: string; reading_time?: string }

export default function FeaturedPostCard({ post }: { post: FeaturedPost }) { return <Card className="featured-card">{post.cover_image ? <img src={post.cover_image} alt="" /> : <div className="post-cover" />}<div className="featured-card__body"><Badge>Article</Badge><h2>{post.title}</h2><p>{post.content?.slice(0, 140) || 'Thoughtful ideas for developers, makers, and lifelong learners.'}</p><div><span><FiClock /> {post.reading_time || '3 min read'}</span><a href={`#post-${post.id}`}>Read article <FiArrowUpRight /></a></div></div></Card> }
