"""
Итоговая демонстрация: что мы построили за курс по Django REST Framework.

Этот скрипт показывает полную картину API блога — от модели до ответа клиенту.
"""

import json


# ============================================================
# 1. МОДЕЛИ (как в Django)
# ============================================================

class Post:
    def __init__(self, id, title, body, creation_date, author=None):
        self.id = id
        self.title = title
        self.body = body
        self.creation_date = creation_date
        self.author = author
        self._comments = []

    def add_comment(self, comment):
        comment.post = self
        self._comments.append(comment)

    @property
    def comments(self):
        return self._comments


class Comment:
    def __init__(self, id, text, creation_date):
        self.id = id
        self.text = text
        self.creation_date = creation_date
        self.post = None


# ============================================================
# 2. СЕРИАЛИЗАТОРЫ (урок 2, 9)
# ============================================================

class CommentSerializer:
    def serialize(self, comment):
        return {
            "id": comment.id,
            "text": comment.text,
            "creation_date": comment.creation_date,
        }


class PostSerializer:
    comment_serializer = CommentSerializer()

    def serialize(self, post, include_comments=True):
        data = {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "creation_date": post.creation_date,
        }
        if include_comments:
            data["comments"] = [
                self.comment_serializer.serialize(c) for c in post.comments
            ]
        return data


# ============================================================
# 3. АУТЕНТИФИКАЦИЯ (урок 7)
# ============================================================

class AuthSystem:
    def __init__(self):
        self._tokens = {"abc123": "admin"}

    def authenticate(self, token):
        return self._tokens.get(token)

    def has_permission(self, user, action):
        if action == "read":
            return True  # IsAuthenticatedOrReadOnly
        return user is not None


# ============================================================
# 4. ВЬЮХИ / VIEWSET (уроки 3-6)
# ============================================================

class PostAPI:
    serializer = PostSerializer()
    auth = AuthSystem()

    def __init__(self):
        self.posts = {}

    def list_posts(self):
        return [self.serializer.serialize(p, include_comments=False)
                for p in self.posts.values()]

    def get_post(self, pk):
        post = self.posts.get(pk)
        if post:
            return self.serializer.serialize(post, include_comments=True)
        return None

    def create_post(self, data, token=None):
        user = self.auth.authenticate(token)
        if not self.auth.has_permission(user, "write"):
            return {"error": "Unauthorized", "status": 401}
        new_id = max(self.posts.keys(), default=0) + 1
        post = Post(new_id, data["title"], data["body"], "2025-01-01", author=user)
        self.posts[new_id] = post
        return {"data": self.serializer.serialize(post), "status": 201}

    def delete_post(self, pk, token=None):
        user = self.auth.authenticate(token)
        if not self.auth.has_permission(user, "write"):
            return {"error": "Unauthorized", "status": 401}
        if pk in self.posts:
            del self.posts[pk]
            return {"status": 204}
        return {"error": "Not found", "status": 404}
# ============================================================
# 5. ДЕМОНСТРАЦИЯ
# ============================================================

if __name__ == "__main__":
    api = PostAPI()

    # Создадим тестовые посты и комментарии
    post1 = Post(1, "Django REST", "Текст про DRF", "2025-01-10")
    post2 = Post(2, "Python tips", "Полезные советы", "2025-02-15")
    comment1 = Comment(1, "Отличная статья!", "2025-01-11")
    comment2 = Comment(2, "Очень полезно", "2025-01-12")
    post1.add_comment(comment1)
    post1.add_comment(comment2)
    api.posts[1] = post1
    api.posts[2] = post2

    print("=" * 60)
    print("ИТОГ: ЧТО МЫ ПОСТРОИЛИ ЗА КУРС")
    print("=" * 60)
    print()

    print("API ЭНДПОИНТЫ (REST):")
    print("  GET    /api/posts/       -> список постов")
    print("  POST   /api/posts/       -> создать пост")
    print("  GET    /api/posts/{id}/  -> детали + комментарии")
    print("  PUT    /api/posts/{id}/  -> обновить пост")
    print("  DELETE /api/posts/{id}/  -> удалить пост")
    print()

    # Список
    print("=" * 60)
    print("GET /api/posts/ — СПИСОК")
    print("=" * 60)
    print(json.dumps(api.list_posts(), indent=4, ensure_ascii=False))
    print()

    # Детали + комментарии
    print("=" * 60)
    print("GET /api/posts/1/ — ДЕТАЛИ + ВЛОЖЕННЫЕ КОММЕНТАРИИ")
    print("=" * 60)
    print(json.dumps(api.get_post(1), indent=4, ensure_ascii=False))
    print()

    # Создание без токена / с токеном
    print("=" * 60)
    print("POST /api/posts/ — СОЗДАНИЕ (авторизация)")
    print("=" * 60)
    resp = api.create_post({"title": "Новый пост", "body": "Текст"})
    print(f"  Без токена -> {resp}")
    resp = api.create_post({"title": "Новый пост", "body": "Текст"}, token="abc123")
    print(f"  С токеном  -> {resp}")
    print()

    # Что изучили
    print("=" * 60)
    print("ЧТО МЫ ИЗУЧИЛИ:")
    print("=" * 60)
    for name, desc in [
        ("Сериализаторы", "Модель -> JSON (ModelSerializer)"),
        ("@api_view", "Простые функции-обработчики"),
        ("APIView", "Классы с методами get/post/put/delete"),
        ("Generic Views", "Готовые классы CRUD (8 строк кода)"),
        ("ViewSet + Router", "Один класс + авто-URL (4 строки)"),
        ("Аутентификация", "TokenAuth + Permissions"),
        ("Пагинация/Поиск", "PageNumberPagination, SearchFilter"),
        ("Nested Serializers", "Комментарии внутри поста"),
        ("Swagger", "drf-spectacular -> /api/docs/"),
        ("Throttling", "Ограничение запросов"),
    ]:
        print(f"  V {name:24} - {desc}")

    print()
    print("Курс завершён. Ты превратил Django-блог в REST API!")