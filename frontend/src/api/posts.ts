import api from './api'

export interface PostTag { id: number; name: string }
export interface Post {
  id: number
  title: string
  slug: string
  content: string
  published: boolean
  cover_image?: string | null
  author_id: number
  category_id: number
  tags: PostTag[]
  created_at?: string | null
  updated_at?: string | null
}
export interface PostListResponse { page: number; limit: number; total: number; items: Post[] }

export async function fetchPosts(params?: Record<string, string | number | boolean>): Promise<PostListResponse> {
  const response = await api.get('/posts/', { params })
  return response.data
}

export async function fetchPost(postId: number): Promise<Post> {
  const response = await api.get(`/posts/${postId}`)
  return response.data
}

export async function createPost(payload: FormData) {
  const response = await api.post('/posts/', payload, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}
