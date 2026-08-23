# Урок 9. Вложенные сериализаторы и связи

## Проблема: связанные данные

У тебя есть пост и комментарии к нему. Сейчас API для постов возвращает
только поля самой модели: `id`, `title`, `body`, `creation_date`.
Но клиенту (React-приложению, мобилке) часто нужны сразу и комментарии
к посту — чтобы не делать лишних запросов.

Как в DRF отдать комментарии ВНУТРИ ответа о посте? Через **вложенные
сериализаторы** (nested serializers).

## Чтение: показываем комментарии внутри поста

Создадим сериализатор для комментариев:

```python
# blog/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "creation_date"]
```

Теперь вложим его в `PostSerializer`:

```python
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date", "comments"]
```

- `comments = CommentSerializer(many=True, ...)` — поле `comments`
  будет содержать список сериализованных комментариев.
- `read_only=True` — через это поле нельзя создать комментарий
  при создании/редактировании поста (для этого есть отдельный эндпоинт).
- Связь работает благодаря `related_name`: Django по умолчанию даёт
  обратную связь `post.comment_set.all()`, но если в модели
  `Comment.post` указать `related_name="comments"`, то будет
  `post.comments.all()` — и DRF найдёт поле автоматически.

Теперь `GET /api/posts/1/` вернёт:

```json
{
    "id": 1,
    "title": "Первый пост",
    "body": "Текст...",
    "creation_date": "2025-01-15",
    "comments": [
        {"id": 1, "text": "Классный пост!", "creation_date": "..."},
        {"id": 2, "text": "Согласен", "creation_date": "..."}
    ]
}
```

## Оптимизация запросов (N+1 problem)

Когда ты добавил `comments` в сериализатор, DRF для каждого поста
делает ОТДЕЛЬНЫЙ запрос за комментариями. 10 постов = 1 запрос за
постами + 10 запросов за комментариями = 11 запросов.

Это называется **N+1 problem**. Решается через `prefetch_related`:

```python
class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related("comments").all()
    ...
```

Теперь DRF сделает ВСЕГО 2 запроса: один за постами, один за
комментариями (и сам «склеит» их в памяти).

## Запись: создание комментария через пост

Хочешь создать комментарий вместе с постом? Нужно переопределить
`create()` в сериализаторе:

```python
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date", "comments"]

    def create(self, validated_data):
        """Если клиент передал comments, создадим их вместе с постом."""
        comments_data = self.context.get("comments_data", [])
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        return post
```

Но обычно комментарии создают через ОТДЕЛЬНЫЙ эндпоинт
`POST /api/posts/{pk}/comments/` — это логичнее.

## SlugRelatedField — показать связанный объект кратко

Иногда полный вложенный объект не нужен, достаточно ID или названия:

```python
class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.ReadOnlyField(source="post.title")

    class Meta:
        model = Comment
        fields = ["id", "text", "post", "post_title", "creation_date"]
```

- `source="post.title"` — идём по цепочке связей: от комментария
  к посту, от поста — к его заголовку.

## Вложенные сериализаторы для записи (Writable Nested)

Чтобы клиент МОГ создать комментарий через поле `comments` внутри
запроса на создание поста:

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)  # без read_only!

    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date", "comments"]

    def create(self, validated_data):
        comments_data = validated_data.pop("comments", [])
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        return post
```

Теперь можно создать пост с комментариями одним запросом:

```json
{
    "title": "Новый пост",
    "body": "Текст",
    "comments": [
        {"text": "Комментарий 1"},
        {"text": "Комментарий 2"}
    ]
}
```

## Словарик терминов

- **Nested Serializer** — сериализатор, вложенный в другой
- **N+1 problem** — лишние запросы к БД из-за ленивой загрузки
- **prefetch_related** — загрузка связанных данных одним запросом
- **Writable Nested** — вложенный сериализатор, через который можно писать
- **SlugRelatedField** — показывает связанный объект в сокращённом виде

## Задание к уроку

1. Создай `CommentSerializer` с полями `id`, `text`, `creation_date`.
2. Добавь поле `comments` в `PostSerializer` (read_only, many=True).
3. В `PostViewSet` добавь `prefetch_related("comments")` в queryset.
4. Проверь через Browsable API: комментарии отображаются внутри поста.
5. Запусти `primery/demo_nested.py` — демонстрация вложенных объектов.