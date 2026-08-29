import { mediaUrl } from '../api.js'

export default function PostCard({ post, onOpen }) {
  const image = mediaUrl(post.image)
  return (
    <article className="card post-card" onClick={onOpen}>
      <h3 className="post-title">{post.title}</h3>
      <div className="post-meta">
        <span>👤 {post.author_username || `#${post.author}`}</span>
        <span>🕒 {new Date(post.creation_date).toLocaleString()}</span>
        <span>📏 {post.char_count} симв.</span>
      </div>
      {image && <img className="post-thumb" src={image} alt={post.title} />}
      {post.tag_names && post.tag_names.length > 0 && (
        <div className="tags">
          {post.tag_names.map((t) => <span key={t} className="tag">#{t}</span>)}
        </div>
      )}
      <p className="post-excerpt">
        {post.body.slice(0, 180)}{post.body.length > 180 ? '…' : ''}
      </p>
    </article>
  )
}
