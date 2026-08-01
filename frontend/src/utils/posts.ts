import dayjs from 'dayjs'
import type { Post } from '../api/posts'

export function readingTime(content = '') { return `${Math.max(1, Math.ceil(content.trim().split(/\s+/).filter(Boolean).length / 200))} min read` }
export function publishedDate(date?: string | null) { return date ? dayjs(date).format('MMM D, YYYY') : 'Recently published' }
export function postExcerpt(post: Post, max = 155) { return post.content.replace(/[#*_`>[\]]/g, '').replace(/\s+/g, ' ').trim().slice(0, max) }
