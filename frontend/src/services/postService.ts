import client from '../api/client'

export function getPosts() {
  return client.get('/posts')
}
