# Урок 10. Документация и продвинутые техники

## Автоматическая документация API

DRF даёт Browsable API — это удобно, но для внешних разработчиков нужно
что-то более формальное. Золотой стандарт — **OpenAPI / Swagger**.

### drf-spectacular (Swagger для DRF)

Установка:

```
> pip install drf-spectacular
```

В `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'REST API для блога',
    'VERSION': '1.0.0',
}
```

В `config/urls.py`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    ...
]
```

Теперь `http://127.0.0.1:8000/api/docs/` покажет **интерактивную
Swagger-документацию**: все эндпоинты, модели запросов/ответов, кнопка
«Try it out». Swagger сам читает твои сериализаторы и генерит схему.

## Throttling (ограничение запросов)

Чтобы один клиент не «заддосил» API сотнями запросов в секунду:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',   # для анонимов
        'rest_framework.throttling.UserRateThrottle',   # для авторизованных
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',   # 100 запросов в день для анонимов
        'user': '1000/day',  # 1000 запросов в день для пользователей
    },
}
```

Можно настроить и для конкретной вьюхи:

```python
from rest_framework.throttling import ScopedRateThrottle


class PostViewSet(ModelViewSet):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "posts"  # в settings: 'posts': '50/minute'
```

## Версионирование API

Когда API меняется, старые клиенты могут сломаться. Версионирование
позволяет поддерживать несколько версий одновременно:

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

```python
# config/urls.py
urlpatterns = [
    path("api/<version>/", include("blog.api_urls")),
]
```

Теперь: `GET /api/v1/posts/` и `GET /api/v2/posts/` — разные версии.

## Обработка ошибок (кастомный exception handler)

DRF автоматически превращает исключения в HTTP-ответы. Можно настроить
свой обработчик:

```python
# blog/exceptions.py
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # Добавим поле 'code' с HTTP-статусом
        response.data['code'] = response.status_code
    return response
```

В `settings.py`:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'blog.exceptions.custom_exception_handler',
}
```

## Что ты теперь умеешь после всего курса

Ты прошёл путь от простого блога на HTML до полноценного REST API:

| Урок | Что добавили |
|------|-------------|
| 1 | Понимание REST и установка DRF |
| 2 | Сериализаторы (модель → JSON) |
| 3 | Function-Based Views (@api_view) |
| 4 | Class-Based Views (APIView) |
| 5 | Generic Views (короткий CRUD) |
| 6 | ViewSets + Routers (ещё короче) |
| 7 | Аутентификация и права доступа |
| 8 | Пагинация, поиск, фильтрация |
| 9 | Вложенные сериализаторы |
| 10 | Документация, throttling, версионирование |

И всё это — в дополнение к существующему HTML-сайту. API и сайт работают
одновременно, используя одни и те же модели.

## Словарик терминов

- **Swagger / OpenAPI** — стандарт описания REST API (машиночитаемый
  и человекочитаемый)
- **Throttling** — ограничение частоты запросов
- **Версионирование API** — поддержка разных версий API одновременно
- **Exception Handler** — функция, превращающая Python-исключения
  в HTTP-ответы

## Задание к уроку

1. Установи `drf-spectacular` и добавь `/api/docs/` с Swagger.
2. Настрой throttling: 5 запросов в минуту для анонимов на создание поста.
3. Добавь свой `EXCEPTION_HANDLER`, который добавляет поле `status` к ответу.
4. Запусти `primery/demo_itog.py` — итоговая картина: что мы построили
   за весь курс.

## Что дальше?

- **Django + DRF + React** — раздели фронт и бек (SPA)
- **Тесты для API** — `APITestCase` в DRF позволяет тестировать API
- **WebSockets** — реальное время (DRF не поддерживает, нужен Django Channels)
- **Деплой** — Docker + Gunicorn + Nginx
- **Кеширование** — Redis для частых запросов

Поздравляю с завершением курса!