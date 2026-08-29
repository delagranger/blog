export default function NavBar({ isAuth, username, onHome, onCreate, onLogin, onLogout }) {
  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <button className="brand" onClick={onHome}>📝 Мой блог</button>
        <nav>
          <button className="link" onClick={onHome}>Посты</button>
          {isAuth && <button className="link" onClick={onCreate}>+ Новый пост</button>}
          {isAuth ? (
            <>
              <span className="username">👤 {username}</span>
              <button className="btn btn-outline" onClick={onLogout}>Выйти</button>
            </>
          ) : (
            <button className="btn btn-primary" onClick={onLogin}>Войти</button>
          )}
        </nav>
      </div>
    </header>
  )
}
