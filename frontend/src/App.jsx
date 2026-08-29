import { useCallback, useState } from 'react'
import NavBar from './components/NavBar.jsx'
import PostList from './components/PostList.jsx'
import PostDetail from './components/PostDetail.jsx'
import PostForm from './components/PostForm.jsx'
import Login from './components/Login.jsx'
import {
  getToken, setToken, clearToken, getUsername, setUsername, clearUsername,
} from './api.js'

export default function App() {
  const [token, setTokenState] = useState(getToken())
  const [username, setUsernameState] = useState(getUsername())
  const [route, setRoute] = useState({ view: 'list', postId: null })

  const navigate = useCallback((view, postId = null) => {
    setRoute({ view, postId })
    window.scrollTo({ top: 0 })
  }, [])

  const handleLogin = (tokenValue, name) => {
    setToken(tokenValue)
    setUsername(name)
    setTokenState(tokenValue)
    setUsernameState(name)
    navigate('list')
  }

  const handleLogout = () => {
    clearToken()
    clearUsername()
    setTokenState(null)
    setUsernameState(null)
    navigate('list')
  }

  let content
  if (route.view === 'login') {
    content = <Login onLogin={handleLogin} />
  } else if (route.view === 'detail') {
    content = (
      <PostDetail
        postId={route.postId}
        token={token}
        onBack={() => navigate('list')}
        onEdit={(id) => navigate('edit', id)}
        onDeleted={() => navigate('list')}
      />
    )
  } else if (route.view === 'create') {
    content = <PostForm token={token} onDone={() => navigate('list')} />
  } else if (route.view === 'edit') {
    content = (
      <PostForm
        token={token}
        postId={route.postId}
        onDone={() => navigate('detail', route.postId)}
      />
    )
  } else {
    content = <PostList token={token} onOpen={(id) => navigate('detail', id)} />
  }

  return (
    <>
      <NavBar
        isAuth={Boolean(token)}
        username={username}
        onHome={() => navigate('list')}
        onCreate={() => navigate('create')}
        onLogin={() => navigate('login')}
        onLogout={handleLogout}
      />
      <main className="container">{content}</main>
    </>
  )
}
