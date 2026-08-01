import client from '../api/client'

export function uploadFile(file: File) {
  const data = new FormData()
  data.append('file', file)
  return client.post('/uploads', data, { headers: { 'Content-Type': 'multipart/form-data' } })
}
