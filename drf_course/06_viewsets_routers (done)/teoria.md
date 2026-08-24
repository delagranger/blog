# Урок 6. ViewSets и Routers

## Проблема: два класса на одну модель

С дженериками код стал короче, но для каждой модели всё равно нужно
два класса: один для списка (ListCreate), второй для деталей
(RetrieveUpdateDestroy). И для каждого свой URL-путь в `urls.py`.

**ViewSet решает эту проблему**: ОДИН класс содержит ВСЕ действия для
ресурса. А **Router** автоматически генерирует URL-пути для этого класса.

## Что такое ViewSet?

ViewSet — это как APIView, но он работает не с HTTP-методами напрямую,
а с **действиями** (actions): `list`, `create`, `retrieve`, `update`,
`partial_update`, `destroy`.

Вот ViewSet для постов:

```python
from rest_framework.viewsets import ModelViewSet
from blog.models import Post
from blog.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

Эти ЧЕТЫРЕ строки заменяют ДВА класса дженериков и ДВА URL-пути.
`ModelViewSet` уже содержит все 6 действий:

| Действие | HTTP-метод | URL |
|----------|-----------|-----|
| `list` | GET | `/posts/` |
| `create` | POST | `/posts/` |
| `retrieve` | GET | `/posts/{pk}/` |
| `update` | PUT | `/posts/{pk}/` |
| `partial_update` | PATCH | `/posts/{pk}/` |
| `destroy` | DELETE | `/posts/{pk}/` |

## Router: автоматические URL

Вместо ручного перечисления путей в `api_urls.py`:

```python
from rest_framework.routers import DefaultRouter
from blog.api_views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = router.urls
```

`router.register("posts", PostViewSet)` автоматически создаст:

- `GET` `/posts/` → `list`
- `POST` `/posts/` → `create`
- `GET` `/posts/{pk}/` → `retrieve`
- `PUT` `/posts/{pk}/` → `update`
- `PATCH` `/posts/{pk}/` → `partial_update`
- `DELETE` `/posts/{pk}/` → `destroy`

А `DefaultRouter` дополнительно даст корневую страницу API со списком всех
эндпоинтов (по адресу `/api/`).

## Кастомные действия (@action)

Иногда нужно действие, которое не вписывается в стандартный CRUD. Например,
«опубликовать пост» или «поставить лайк». Для этого есть декоратор `@action`:

```python
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        """POST /posts/{pk}/publish/ — опубликовать пост."""
        post = self.get_object()
        post.is_published = True
        post.save()
        return Response({"status": "published"})

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """GET /posts/recent/ — последние 5 постов."""
        recent_posts = Post.objects.order_by("-creation_date")[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)
```

- `detail=True` — действие для ОДНОГО объекта, URL: `/posts/{pk}/publish/`
- `detail=False` — действие для всего списка, URL: `/posts/recent/`
- `methods` — список разрешённых HTTP-методов

## Когда использовать ViewSets, а когда дженерики?

| Ситуация | Что выбрать |
|----------|-------------|
| Полный CRUD для модели | `ModelViewSet` + Router |
| Только чтение (ReadOnly) | `ReadOnlyModelViewSet` |
| Список и создание, но без деталей | `GenericViewSet` + миксины |
| Нестандартная логика (не CRUD) | `GenericAPIView` или `APIView` |
| Несколько разных сущностей в одной вьюхе | `APIView` |

## Как это выглядит в твоём проекте

После ViewSet + Router файл `api_urls.py` станет очень компактным:

```python
from rest_framework.routers import DefaultRouter
from blog.api_views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = router.urls
```

И в главном `config/urls.py`:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("api/", include("blog.api_urls")),
]
```

## Словарик терминов

- **ViewSet** — один класс для всех CRUD-операций над ресурсом
- **ModelViewSet** — ViewSet с полным набором действий (list, create, ...)
- **Router** — автоматически генерирует URL для ViewSet'ов
- **@action** — декоратор для кастомных действий в ViewSet
- **DefaultRouter** — Router + корневая страница API со списком эндпоинтов

## Задание к уроку

1. Замени `PostListCreateView` и `PostDetailView` на один `PostViewSet`.
2. Перепиши API для комментариев на ViewSet (`CommentViewSet`).
3. Подключи Router вместо ручных URL-путей.
4. Добавь кастомное действие `@action(detail=True, methods=["post"])`
   для «архивации» поста (меняет статус).
5. Запусти `primery/demo_viewset.py` — принцип ViewSet+Routers наглядно.