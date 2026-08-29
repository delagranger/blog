import { useEffect, useState } from 'react'
import { api } from '../api.js'
import PostCard from './PostCard.jsx'
import Pagination from './Pagination.jsx'

const PAGE_SIZE = 5

export default function PostList({ onOpen }) {
  const [data, setData] = useState({ results: [], count: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [query, setQuery] = useState('')
  const [ordering, setOrdering] = useState('-creation_date')
  const [recent, setRecent] = useState([])

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    api.getPosts({ page, search: query, ordering })
      .then((res) => { if (active) setData(res) })
      .catch((err) => { if (active) setError(err.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [page, query, ordering])

  useEffect(() => {
    api.getRecentPosts().then(setRecent).catch(() => {})
  }, [])

  const totalPages = Math.max(1, Math.ceil(data.count / PAGE_SIZE))

  function handleSearch(e) {
    e.preventDefault()
    setPage(1)
    setQuery(search)
  }

  return (
    <div className="posts-layout">
      <div className="posts-main">
        <h1>Посты</h1>

        <form className="toolbar" onSubmit={handleSearch}>
          <input
            className="search-input"
            placeholder="Поиск по заголовку и тексту…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            value={ordering}
            onChange={(e) => { setOrdering(e.target.value); setPage(1) }}
          >
            <option value="-creation_date">Сначала новые</option>
            <option value="creation_date">Сначала старые</option>
            <option value="title">Название: А → Я</option>
            <option value="-title">Название: Я → А</option>
          </select>
          <button className="btn btn-primary" type="submit">Найти</button>
        </form>

        {error && <p className="error">{error}</p>}
        {loading ? (
          <p>Загрузка…</p>
        ) : data.results.length === 0 ? (
          <p className="empty">Постов не найдено.</p>
        ) : (
          <>
            <div className="post-list">
              {data.results.map((post) => (
                <PostCard key={post.id} post={post} onOpen={() => onOpen(post.id)} />
              ))}
            </div>
            <Pagination page={page} totalPages={totalPages} onChange={setPage} />
          </>
        )}
      </div>

      {recent.length > 0 && (
        <aside className="sidebar">
          <h2>Недавние</h2>
          <ul className="recent-list">
            {recent.map((post) => (
              <li key={post.id}>
                <button className="link" onClick={() => onOpen(post.id)}>{post.title}</button>
              </li>
            ))}
          </ul>
        </aside>
      )}
    </div>
  )
}
