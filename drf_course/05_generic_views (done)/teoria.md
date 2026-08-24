# Урок 5. Generic Views: быстрый CRUD

## Проблема: слишком много одинакового кода

Посмотри на свой API. `PostListAPIView` и `PostDetailAPIView` делают
стандартные вещи: достать из базы, сериализовать, вернуть. И так для
каждой модели — посты, комментарии, пользователи...

DRF решает это через **Generic Views** — готовые классы для типовых
сценариев. Вместо того чтобы писать `get()` и `post()` руками, ты
просто говоришь: «хочу список и создание — дай `ListCreateAPIView`».

## Основные Generic Views

DRF даёт набор дженериков под каждую комбинацию методов:

| Класс | HTTP-методы | Для чего |
|-------|-------------|----------|
| `ListAPIView` | GET (список) | Только чтение списка |
| `CreateAPIView` | POST | Только создание |
| `ListCreateAPIView` | GET, POST | Список + создание |
| `RetrieveAPIView` | GET (один) | Детали одного объекта |
| `UpdateAPIView` | PUT, PATCH | Только обновление |
| `DestroyAPIView` | DELETE | Только удаление |
| `RetrieveUpdateAPIView` | GET, PUT, PATCH | Детали + обновление |
| `RetrieveDestroyAPIView` | GET, DELETE | Детали + удаление |
| `RetrieveUpdateDestroyAPIView` | GET, PUT, PATCH, DELETE | Всё для одного объекта |

## Переписываем наш API на дженерики

Вместо 80 строк кода из урока 4 — всего два класса:

```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from blog.models import Post
from blog.serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

И всё! Эти 8 строк полностью заменяют ручные `get()`, `post()`, `put()`,
`patch()`, `delete()` из APIView.

Что здесь происходит:

- `queryset` — откуда брать данные. Дженерик сам вызовет
  `queryset.all()` или `queryset.get(pk=...)`.
- `serializer_class` — каким сериализатором обрабатывать данные.
- Дженерик сам знает, что для GET нужен список, для POST — создание,
  для DELETE — удаление.

В `api_urls.py` ничего не меняется — те же `.as_view()`:

```python
urlpatterns = [
    path("posts/", PostListCreateView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
]
```

## Что дженерики делают «под капотом»

Каждый дженерик — это комбинация **миксинов**. Например, `ListCreateAPIView`
собран из двух миксинов:

```python
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

- `ListModelMixin` содержит метод `list()` — возвращает список.
- `CreateModelMixin` содержит метод `create()` — создаёт запись.
- `GenericAPIView` — базовый класс, предоставляющий `get_queryset()`,
  `get_serializer()` и другие полезные методы.

Ты можешь переопределить любой из этих методов, чтобы добавить свою логику.

## Настройка поведения дженерика

Часто нужно лишь слегка подправить стандартное поведение. DRF даёт
«крючки» (hooks) для этого:

```python
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Вызывается перед сохранением. Здесь можно добавить
        автоматическое заполнение полей."""
        # Например: привязать пост к текущему пользователю
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Фильтрация queryset. Например: только посты текущего
        пользователя."""
        return Post.objects.filter(author=self.request.user)
```

- `perform_create(serializer)` — вызывается внутри `create()`, ДО сохранения.
  Здесь `serializer.save(...)` передаёт дополнительные аргументы в модель.
- `get_queryset()` — переопредели этот метод, чтобы изменить, какие именно
  записи возвращаются.

## Словарик терминов

- **Generic View** — готовый view-класс для типового сценария (список,
  создание, детали...)
- **Миксин** — класс-«кирпичик» с одним конкретным действием (list, create)
- **queryset** — объект QuerySet, из которого дженерик берёт данные
- **serializer_class** — класс сериализатора для обработки данных

## Задание к уроку

1. Замени `PostListAPIView` и `PostDetailAPIView` на дженерики.
2. Добавь дженерики для комментариев: `CommentListCreateView` и
   `CommentDetailView` (понадобится `CommentSerializer` — создай его).
3. Попробуй переопределить `perform_create`, чтобы выводить в консоль
   сообщение о создании поста.
4. Запусти `primery/demo_generic.py` — упрощённая модель дженерика.