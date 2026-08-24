# Урок 3. Function-Based Views + @api_view

## Что такое View в DRF?

Во втором уроке мы написали сериализатор — теперь он умеет превращать
посты в JSON. Но как отдать этот JSON клиенту, который зашёл по адресу
`/api/posts/`? Для этого нужен **View** — обработчик запроса.

DRF даёт два основных способа создавать views:

1. **@api_view** — декоратор для обычных функций (разбираем сейчас)
2. **APIView** — классы (разберём в уроке 4)

Начнём с `@api_view` — он проще и ближе к тому, что ты уже знаешь.

## Декоратор @api_view

В обычном Django ты писал:

```python
def main_page(request):
    posts = Post.objects.all()
    return render(request, "blog/main_page.html", {"posts": posts})
```

В DRF аналог выглядит так:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Post
from blog.serializers import PostSerializer


@api_view(["GET"])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
```

Разберём:

- `@api_view(["GET"])` — декоратор: «эта функция обрабатывает только GET».
  Можно указать несколько методов: `@api_view(["GET", "POST"])`.
- `PostSerializer(posts, many=True)` — сериализуем список постов.
- `Response(serializer.data)` — DRF-ответ, сам превратит словарь в JSON
  и выставит правильный заголовок `Content-Type`.

## Подключение к URL

Создай файл `blog/api_urls.py` (отдельно от обычных `urls.py`):

```python
from django.urls import path
from blog.api_views import post_list, post_detail

urlpatterns = [
    path("posts/", post_list),
    path("posts/<int:pk>/", post_detail),
]
```

И подключи его в главном `config/urls.py`:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),          # старые HTML-вьюхи
    path("api/", include("blog.api_urls")),  # новые API-вьюхи
]
```

Теперь у тебя одновременно: `http://127.0.0.1:8000/` (HTML) и
`http://127.0.0.1:8000/api/posts/` (JSON API).

## Обработка нескольких методов в одной функции

```python
@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

- `request.data` — в DRF аналог `request.POST`, но умнее: понимает
  и формы, и JSON из тела запроса.
- `status=201` — HTTP-статус «Created».
- `status=400` — «Bad Request», данные не прошли валидацию.
## Отдельный пост: GET, PUT, PATCH, DELETE

Вторая вьюха — для конкретного поста по его `id`:

```python
from django.shortcuts import get_object_or_404


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=204)
```

Отличие PUT от PATCH:
- **PUT** — клиент передаёт ВСЕ поля. Непереданные поля сбросятся.
- **PATCH** — клиент передаёт ТОЛЬКО изменяемые поля. `partial=True`
  это и включает.

## Browsable API — тестируем в браузере

DRF автоматически даёт **Browsable API** — веб-страницу для каждого
эндпоинта. Открой `http://127.0.0.1:8000/api/posts/` в браузере:

- увидишь список постов в JSON (красиво отформатированный);
- увидишь форму для создания нового поста (POST);
- увидишь кнопки для PUT, PATCH, DELETE.

Это очень удобно: тестируешь API без Postman или curl.

## request.data vs request.POST

В обычном Django: `request.POST` — только для форм, `request.body` —
для JSON (надо парсить вручную). В DRF: `request.data` — единый способ
получить данные из любого формата (форма, JSON, файлы).

## Словарик терминов

- **@api_view** — декоратор, делающий функцию DRF-view
- **Response()** — DRF-ответ, аналог JsonResponse, но умнее
- **request.data** — разобранные данные запроса (замена request.POST)
- **Browsable API** — веб-интерфейс тестирования API (автоматически!)
- **partial=True** — разрешить частичное обновление для PATCH

## Задание к уроку

1. Создай файл `blog/api_views.py` с функциями `post_list` и `post_detail`.
2. Создай `blog/api_urls.py` и подключи его в `config/urls.py`.
3. Открой `http://127.0.0.1:8000/api/posts/` — посмотри Browsable API.
4. Создай, измени и удали пост через веб-интерфейс DRF.
5. Запусти `primery/demo_api_view.py` — упрощённая демонстрация view.