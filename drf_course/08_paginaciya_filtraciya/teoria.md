# Урок 8. Пагинация, фильтрация, поиск

## Зачем это нужно?

Представь: в блоге 1000 постов. Отдавать их все в одном ответе API —
медленно и неудобно. Нужно отдавать по 10–20 штук за раз — это **пагинация**.

Клиент хочет найти посты по ключевому слову — **поиск**. Или показать
только посты за определённую дату — **фильтрация**.

Всё это есть в DRF из коробки.

## Пагинация

DRF даёт три стиля пагинации, настраиваются глобально в `settings.py`:

### 1. PageNumberPagination (как страницы в книге)

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

Запрос: `GET /api/posts/?page=2` → вернёт посты 11–20.
Ответ будет содержать:

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/posts/?page=3",
    "previous": "http://127.0.0.1:8000/api/posts/?page=1",
    "results": [ ... ]  // сами посты
}
```

### 2. LimitOffsetPagination (сколько пропустить, сколько взять)

Запрос: `GET /api/posts/?limit=10&offset=20` → пропустить 20, взять 10.

### 3. CursorPagination (курсорная — для лент, где важен порядок)

Запрос: `GET /api/posts/?cursor=cD0yMDIzLTAxLTAx` — позиция в ленте.

Для блога PageNumberPagination — самый понятный вариант.

## Поиск (SearchFilter)

Добавь `SearchFilter` в настройки или конкретный ViewSet:

```python
from rest_framework.filters import SearchFilter


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "body"]  # по каким полям искать
```

Теперь клиент может искать:

```
GET /api/posts/?search=python
```

DRF выполнит запрос: `WHERE title LIKE '%python%' OR body LIKE '%python%'`.

Можно использовать специальные префиксы для поля:

- `search_fields = ["^title"]` — поиск начинается с... (startswith)
- `search_fields = ["=title"]` — точное совпадение
- `search_fields = ["@title"]` — полнотекстовый поиск (PostgreSQL)

## Фильтрация (DjangoFilterBackend)

Для фильтрации по точным значениям (статус, дата, автор):

```python
# Установи библиотеку: pip install django-filter
INSTALLED_APPS = [
    ...
    'django_filters',
]
```

```python
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["creation_date"]  # поля для точной фильтрации
    search_fields = ["title", "body"]
```

Запрос: `GET /api/posts/?creation_date=2025-01-15` — вернёт посты
только за эту дату.

## Кастомный фильтр (FilterSet)

Для сложной фильтрации (диапазон дат, поиск по нескольким полям):

```python
import django_filters
from blog.models import Post


class PostFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="creation_date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="creation_date", lookup_expr="lte"
    )
    title_contains = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains"
    )

    class Meta:
        model = Post
        fields = ["date_from", "date_to", "title_contains"]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostFilter  # вместо filterset_fields
```

Теперь: `GET /api/posts/?date_from=2025-01-01&date_to=2025-01-31` —
посты за январь.

## Сортировка (OrderingFilter)

Добавляет возможность сортировать по любому полю:

```python
from rest_framework.filters import OrderingFilter


class PostViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["creation_date", "title"]
    ordering = ["-creation_date"]  # сортировка по умолчанию
```

Запрос: `GET /api/posts/?ordering=-creation_date` — от новых к старым.

## Словарик терминов

- **Пагинация** — разбивка результатов на страницы
- **SearchFilter** — поиск по текстовым полям (LIKE)
- **DjangoFilterBackend** — точная фильтрация по полям (=, >, <)
- **FilterSet** — класс, описывающий правила фильтрации (как форма)
- **OrderingFilter** — сортировка результатов

## Задание к уроку

1. Настрой `PageNumberPagination` с `PAGE_SIZE = 5`.
2. Добавь `SearchFilter` для поиска по заголовкам постов.
3. Добавь `OrderingFilter` для сортировки по дате.
4. Установи `django-filter` и добавь `DjangoFilterBackend`.
5. Открой API в браузере — в Browsable API появятся кнопки «Filters»
   и «Search».
6. Запусти `primery/demo_filter.py` — демонстрация фильтрации.