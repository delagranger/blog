import { useEffect, useState } from 'react'
import { api, mediaUrl } from '../api.js'
import CommentList from './CommentList.jsx'

export default function PostDetail({ postId, token, onBack, onEdit, onDeleted }) {
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    api.getPost(postId)
      .then((res) => { if (active) setPost(res) })
      .catch((err) => { if (active) setError(err.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [postId])

  async function handleDelete() {
    if (!window.confirm('Удалить этот пост?')) return
    setDeleting(true)
    try {
      await api.deletePost(postId)
      onDeleted()
    } catch (err) {
      setError(err.message)
      setDeleting(false)
    }
  }

  if (loading) return <p>Загрузка…</p>
  if (error && !post) return <p className="error">{error}</p>
  if (!post) return null

  const image = mediaUrl(post.image)

  return (
    <article>
      <button className="link back" onClick={onBack}>← К постам</button>
      <div className="card detail-card">
        <h1>{post.title}</h1>
        <div className="post-meta">
          <span>👤 {post.author_username || `#${post.author}`}</span>
          <span>🕒 {new Date(post.creation_date).toLocaleString()}</span>
          <span>📏 {post.char_count} симв.</span>
        </div>
        {image && <img className="post-image" src={image} alt={post.title} />}
        {post.tag_names && post.tag_names.length > 0 && (
          <div className="tags">
            {post.tag_names.map((t) => <span key={t} className="tag">#{t}</span>)}
          </div>
        )}
        <p className="post-body">{post.body}</p>

        {token && (
          <div className="actions">
            <button className="btn btn-outline" onClick={() => onEdit(post.id)}>Редактировать</button>
            <button className="btn btn-danger" onClick={handleDelete} disabled={deleting}>
              {deleting ? 'Удаление…' : 'Удалить'}
            </button>
          </div>
        )}
        {error && <p className="error">{error}</p>}
      </div>

      <CommentList postId={postId} token={token} />
    </article>
  )
}
