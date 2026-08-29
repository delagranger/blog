# Фронтенд блога (React + Vite)

SPA-фронтенд для Django-API блога.

## Запуск

1. Поднимите Django-сервер (из корня проекта):

   ```bash
   python manage.py runserver
   ```

2. Установите зависимости и запустите Vite:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Откройте http://localhost:5173

## Сборка для production

```bash
npm run build
```

Готовые файлы появятся в `frontend/dist`.

## Как устроено

- Dev-сервер Vite проксирует `/api` и `/media` на `http://localhost:8000`, поэтому CORS не нужен.
- Токен авторизации хранится в `localStorage` и подставляется в заголовок `Authorization: Token <token>`.
- Без токена пользователь может только читать посты/комментарии (`IsAuthenticatedOrReadOnly`).
