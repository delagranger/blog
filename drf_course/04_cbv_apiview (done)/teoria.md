# Урок 4. Class-Based Views: APIView

## Зачем переходить на классы?

В прошлом уроке мы использовали функции с `@api_view`. Они простые и
понятные. Но когда API растёт, в одной функции скапливается много `if`-ов
на разные HTTP-методы. Код становится трудно читать.

**Классы решают эту проблему**: каждый HTTP-метод — отдельный метод класса.
Логика GET не смешивается с логикой POST. И бонус: классы можно наследовать,
добавляя поведение миксинами (как в уроке 12 курса по Django).

## APIView — базовый класс DRF

`APIView` — это самый простой класс для API в DRF. Аналог `@api_view`,
но в виде класса. Вот как выглядит тот же список постов:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from blog.models import Post
from blog.serializers import PostSerializer


class PostListAPIView(APIView):
    """Список постов и создание нового."""

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    """Конкретный пост: просмотр, изменение, удаление."""

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=204)
```

Ключевые отличия от функций:

- Нет декоратора `@api_view` — APIView уже знает, как обрабатывать запросы
- Нет `if request.method == "..."` — каждый метод (GET/POST/...) — свой
  метод класса
- В URL нужно указать `.as_view()` (как с CBV в Django):

```python
# blog/api_urls.py
from blog.api_views import PostListAPIView, PostDetailAPIView

urlpatterns = [
    path("posts/", PostListAPIView.as_view()),
    path("posts/<int:pk>/", PostDetailAPIView.as_view()),
]
```

## Что APIView делает автоматически

APIView (и все классы DRF) не просто вызывают твой метод. Он ещё:

- сам парсит содержимое запроса в `request.data`;
- сам превращает ответ в JSON;
- сам обрабатывает Browsable API (для GET — веб-страница, для остального —
  чистый JSON);
- даёт доступ к `request.user` (даже без отдельной настройки);
- даёт единую систему обработки исключений.

## Повторяющийся код? Выносим в базовый класс

В `PostDetailAPIView` первые две строчки каждого метода одинаковые:
`post = get_object_or_404(Post, pk=pk)`. Можно вынести это в отдельный метод:

```python
class PostDetailAPIView(APIView):

    def get_object(self, pk):
        """Общий метод получения поста. Наследники могут переопределить."""
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        # ...
```

Этот принцип — «общая логика в отдельном методе» — ключевой для DRF.
Все Generic Views (следующий урок) построены именно так.

## Сравнение: функции vs классы

| Критерий | @api_view | APIView |
|----------|-----------|---------|
| Простота начала | Очень просто | Чуть сложнее |
| Ветвление методов | if'ы в одной функции | Методы класса |
| Повторное использование | Сложно | Легко (наследование) |
| Добавление поведения | Через декораторы | Через миксины |
| Когда использовать | Маленький API (1-2 эндпоинта) | Средний/большой API |

## Словарик терминов

- **APIView** — базовый класс для API-views в DRF
- **.as_view()** — метод класса, превращающий его в view-функцию для Django
- **Миксин** — класс-«добавка» с готовой функциональностью

## Задание к уроку

1. Перепиши `post_list` и `post_detail` с функций на классы (APIView).
2. Обнови `api_urls.py`, добавив `.as_view()`.
3. Вынеси поиск поста в метод `get_object(self, pk)`.
4. Запусти `primery/demo_apiview.py` — демонстрация класса-обработчика.