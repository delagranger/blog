# Урок 7. Аутентификация и permissions

## Зачем защищать API?

Сейчас твой API открыт: кто угодно может создавать, изменять и удалять
посты. Для учебного проекта это нормально, но в реальном мире это проблема.

DRF даёт два уровня защиты:

1. **Аутентификация** — «кто ты?» (узнать пользователя)
2. **Permissions** — «что тебе можно?» (проверить права)

## Встроенные способы аутентификации

DRF поддерживает несколько способов «узнать пользователя»:

| Класс | Как работает |
|-------|-------------|
| `BasicAuthentication` | Логин/пароль в каждом запросе (HTTP Basic Auth) |
| `SessionAuthentication` | Сессии Django (для Browsable API) |
| `TokenAuthentication` | Токен в заголовке `Authorization: Token ...` |
| `JWTAuthentication` | JWT-токен (через стороннюю библиотеку) |

Для API чаще всего используют **TokenAuthentication** (простой токен) или
**JWT** (более безопасный, с ограниченным сроком жизни).

## Настройка TokenAuthentication

### Шаг 1. Добавь в настройки

В `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',  # ← приложение для токенов
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Browsable API
    ],
}
```

### Шаг 2. Создай миграции и примени их

```
> python manage.py makemigrations
> python manage.py migrate
```

### Шаг 3. Создай View для получения токена

Готового View нет, но можно использовать встроенный `obtain_auth_token`:

```python
# config/urls.py
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("api/auth/", obtain_auth_token),  # POST: {"username":"...", "password":"..."}
    path("api/", include("blog.api_urls")),
    ...
]
```

### Шаг 4. Как получить токен

Клиент отправляет POST-запрос с логином и паролем:

```
POST /api/auth/
Content-Type: application/json

{"username": "admin", "password": "..."}
```

Ответ:

```json
{"token": "9944b09199c62bcf9418ad84..."}
```

### Шаг 5. Использовать токен

Теперь клиент добавляет заголовок к каждому запросу:

```
GET /api/posts/
Authorization: Token 9944b09199c62bcf9418ad84...
```

В Browsable API токен вбивать не нужно — если вошёл в админку Django,
сессия работает автоматически (через SessionAuthentication).

## Права доступа (Permissions)

После аутентификации DRF проверяет **права**. Основные классы:

| Класс | Разрешает |
|-------|----------|
| `AllowAny` | Всем (по умолчанию) |
| `IsAuthenticated` | Только вошедшим пользователям |
| `IsAdminUser` | Только админам |
| `IsAuthenticatedOrReadOnly` | Чтение всем, запись — вошедшим |

### Глобальная настройка (для всего API)

В `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    ...
}
```

Это значит: читать посты могут все, а создавать/менять/удалять — только
авторизованные.

### Настройка на уровне View

Можно переопределить для конкретного ViewSet:

```python
from rest_framework.permissions import IsAuthenticated, AllowAny


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        """Для разных действий — разные права."""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]  # читать могут все
        else:
            permission_classes = [IsAuthenticated]  # писать — только свои
        return [permission() for permission in permission_classes]
```

## Кастомные права

Иногда стандартных недостаточно. Например: «только автор может менять пост»:

```python
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Читать могут все, изменять — только автор."""

    def has_object_permission(self, request, view, obj):
        # obj — это экземпляр модели (Post), который пытаются изменить
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True  # чтение разрешено всем
        return obj.author == request.user  # запись — только автору
```

- `has_permission` — проверяется ДО доступа к данным
- `has_object_permission` — проверяется на конкретном объекте (например,
  при PUT /posts/5/)

Использование:

```python
class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    ...
```

## Словарик терминов

- **Аутентификация** — определение пользователя (кто ты?)
- **Permission** — проверка прав (что тебе можно?)
- **Token** — ключ, который клиент передаёт вместо пароля при каждом запросе
- **IsAuthenticatedOrReadOnly** — гостям можно читать, писать — после входа

## Задание к уроку

1. Добавь `rest_framework.authtoken` в `INSTALLED_APPS` и сделай миграции.
2. Настрой `DEFAULT_AUTHENTICATION_CLASSES` (Token + Session).
3. Добавь URL для получения токена.
4. Установи `DEFAULT_PERMISSION_CLASSES = IsAuthenticatedOrReadOnly`.
5. Проверь через Browsable API: без входа можно читать, нельзя писать.
6. Запусти `primery/demo_auth.py` — принцип токенов и прав.