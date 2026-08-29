import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function CommentList({ postId, token }) {
  const [comments, setComments] = useState([])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function loadComments() {
    setLoading(true)
    api.getComments(postId)
      .then((res) => setComments(Array.isArray(res) ? res : res.results || []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadComments()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId])

  async function handleSubmit(e) {
    e.preventDefault()
    if (!text.trim()) return
    setSubmitting(true)
    setError('')
    try {
      await api.createComment(postId, text.trim())
      setText('')
      loadComments()
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(id) {
    try {
      await api.deleteComment(id)
      setComments((c) => c.filter((x) => x.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section className="comments">
      <h2>Комментарии ({comments.length})</h2>

      {token ? (
        <form className="comment-form" onSubmit={handleSubmit}>
          <textarea
            placeholder="Напишите комментарий…"
            value={text}
            onChange={(e) => setText(e.target.value)}
            maxLength={100}
            rows={3}
          />
          <button className="btn btn-primary" disabled={submitting || !text.trim()}>
            {submitting ? 'Отправка…' : 'Отправить'}
          </button>
        </form>
      ) : (
        <p className="empty">Войдите, чтобы оставить комментарий.</p>
      )}

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p>Загрузка…</p>
      ) : comments.length === 0 ? (
        <p className="empty">Комментариев пока нет.</p>
      ) : (
        <ul className="comment-list">
          {comments.map((c) => (
            <li key={c.id} className="card comment">
              <div className="comment-head">
                <strong>{c.author_username || `#${c.author}`}</strong>
                <span className="muted">{new Date(c.creation_date).toLocaleString()}</span>
              </div>
              <p>{c.text}</p>
              {token && (
                <button className="link small" onClick={() => handleDelete(c.id)}>Удалить</button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
