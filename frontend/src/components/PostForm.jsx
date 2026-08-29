import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function PostForm({ postId, onDone }) {
  const isEdit = Boolean(postId)
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [image, setImage] = useState(null)
  const [tags, setTags] = useState([])
  const [allTags, setAllTags] = useState([])
  const [newTag, setNewTag] = useState('')
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getTags()
      .then((res) => setAllTags(Array.isArray(res) ? res : res.results || []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!isEdit) return
    api.getPost(postId)
      .then((post) => {
        setTitle(post.title)
        setBody(post.body)
        setTags(post.tags || [])
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [postId, isEdit])

  function toggleTag(id) {
    setTags((prev) => (prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]))
  }

  async function handleAddTag() {
    const name = newTag.trim()
    if (!name) return
    try {
      const created = await api.createTag(name)
      setAllTags((prev) => [...prev, created])
      setTags((prev) => [...prev, created.id])
      setNewTag('')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      const payload = { title, body, image, tags }
      if (isEdit) await api.updatePost(postId, payload)
      else await api.createPost(payload)
      onDone()
    } catch (err) {
      setError(err.message)
      setSaving(false)
    }
  }

  if (loading) return <p>Загрузка…</p>

  return (
    <div className="card form-card">
      <h2>{isEdit ? 'Редактировать пост' : 'Новый пост'}</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Заголовок
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
          />
        </label>
        <label>
          Текст
          <textarea value={body} onChange={(e) => setBody(e.target.value)} required rows={8} />
        </label>
        <label>
          Изображение
          <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files[0] || null)} />
        </label>

        <fieldset className="tags-field">
          <legend>Теги</legend>
          {allTags.length === 0 && <p className="muted">Тегов пока нет.</p>}
          <div className="tags-select">
            {allTags.map((t) => (
              <label key={t.id} className="tag-check">
                <input
                  type="checkbox"
                  checked={tags.includes(t.id)}
                  onChange={() => toggleTag(t.id)}
                />
                {t.name}
              </label>
            ))}
          </div>
          <div className="add-tag">
            <input
              placeholder="Новый тег…"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              maxLength={10}
            />
            <button type="button" className="btn btn-outline" onClick={handleAddTag}>+ Тег</button>
          </div>
        </fieldset>

        {error && <p className="error">{error}</p>}
        <div className="actions">
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Сохранение…' : isEdit ? 'Сохранить' : 'Опубликовать'}
          </button>
          <button type="button" className="btn" onClick={onDone}>Отмена</button>
        </div>
      </form>
    </div>
  )
}
