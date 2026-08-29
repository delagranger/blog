const TOKEN_KEY = 'blog_token'
const USERNAME_KEY = 'blog_username'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function getUsername() {
  return localStorage.getItem(USERNAME_KEY)
}

export function setUsername(name) {
  localStorage.setItem(USERNAME_KEY, name)
}

export function clearUsername() {
  localStorage.removeItem(USERNAME_KEY)
}

export function isAuthenticated() {
  return Boolean(getToken())
}

// Превращает абсолютный URL (http://localhost:8000/media/...)
// в относительный, чтобы запросы шли через Vite-прокси.
export function mediaUrl(url) {
  if (!url) return null
  return url.replace(/^https?:\/\/[^/]+/i, '')
}

async function request(path, { method = 'GET', body, isForm = false } = {}) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Token ${token}`
  if (body && !isForm) headers['Content-Type'] = 'application/json'

  const res = await fetch(path, {
    method,
    headers,
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  })

  if (res.status === 204) return null

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    const detail =
      data && (data.detail || data.title || data.body || data.text || data.non_field_errors)
    const message = Array.isArray(detail) ? detail.join(', ') : detail || `Ошибка HTTP ${res.status}`
    const err = new Error(message)
    err.data = data
    throw err
  }

  return data
}

function postForm(url, method, data) {
  const form = new FormData()
  form.append('title', data.title)
  form.append('body', data.body)
  if (data.image) form.append('image', data.image)
  ;(data.tags || []).forEach((id) => form.append('tags', id))
  return request(url, { method, body: form, isForm: true })
}

export const api = {
  login: (username, password) =>
    request('/api/auth/', { method: 'POST', body: { username, password } }),

  getPosts: (params = {}) => {
    const q = new URLSearchParams()
    if (params.page) q.set('page', params.page)
    if (params.search) q.set('search', params.search)
    if (params.ordering) q.set('ordering', params.ordering)
    const qs = q.toString()
    return request(`/api/posts/${qs ? `?${qs}` : ''}`)
  },

  getPost: (id) => request(`/api/posts/${id}/`),
  getRecentPosts: () => request('/api/posts/get_recent_posts/'),

  createPost: (data) => postForm('/api/posts/', 'POST', data),
  updatePost: (id, data) => postForm(`/api/posts/${id}/`, 'PATCH', data),
  deletePost: (id) => request(`/api/posts/${id}/`, { method: 'DELETE' }),

  getTags: () => request('/api/tags/'),
  createTag: (name) => request('/api/tags/', { method: 'POST', body: { name } }),

  getComments: (postId) => request(`/api/comments/?post=${postId}`),
  createComment: (postId, text) =>
    request('/api/comments/', { method: 'POST', body: { post: postId, text } }),
  deleteComment: (id) => request(`/api/comments/${id}/`, { method: 'DELETE' }),
}
