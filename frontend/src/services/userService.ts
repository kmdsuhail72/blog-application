import client from '../api/client'

export function getUser(userId: number) {
  return client.get(`/users/${userId}`)
}
