"""
Демонстрация вложенных сериализаторов (Nested Serializers):
как показать связанные данные внутри основного объекта.
"""

import json


# -------- Данные --------

COMMENTS = {
    1: [{"id": 1, "text": "Отлично!"}, {"id": 2, "text": "Интересно"}],
    2: [{"id": 3, "text": "Полезная статья"}],
}

POSTS = {
    1: {"id": 1, "title": "Django REST", "body": "Текст..."},
    2: {"id": 2, "title": "Python tips", "body": "Советы..."},
}


# -------- Имитация сериализаторов --------

def serialize_comment(comment):
    """Простой комментарий — только id и text."""
    return {"id": comment["id"], "text": comment["text"]}


def serialize_post_flat(post):
    """Пост БЕЗ комментариев."""
    return {
        "id": post["id"],
        "title": post["title"],
        "body": post["body"],
    }


def serialize_post_with_comments(post):
    """
    Пост С вложенными комментариями — как PostSerializer с полем comments.
    """
    data = serialize_post_flat(post)
    # «Подтягиваем» комментарии (имитация prefetch_related)
    post_comments = COMMENTS.get(post["id"], [])
    data["comments"] = [serialize_comment(c) for c in post_comments]
    return data


# -------- Демонстрация --------

if __name__ == "__main__":
    print("=" * 50)
    print("БЕЗ вложений (просто пост)")
    print("=" * 50)
    post = POSTS[1]
    print(json.dumps(serialize_post_flat(post), indent=4, ensure_ascii=False))
    print()

    print("=" * 50)
    print("С вложенными комментариями (Nested Serializer)")
    print("=" * 50)
    post = POSTS[1]
    print(json.dumps(serialize_post_with_comments(post), indent=4, ensure_ascii=False))
    print()

    print("Вывод:")
    print("  Поле comments внутри поста — это и есть nested serializer.")
    print("  Клиенту не нужно делать отдельный запрос за комментариями.")
    print("  prefetch_related() оптимизирует SQL-запросы (N+1 problem).")
    print()

    # Показываем проблему N+1
    print("=" * 50)
    print("N+1 PROBLEM (почему нужен prefetch_related)")
    print("=" * 50)
    print("  Без оптимизации для 10 постов:")
    print("    1 запрос: SELECT * FROM posts")
    print("    10 запросов: SELECT * FROM comments WHERE post_id = ...")
    print("    Итого: 11 запросов!")
    print()
    print("  С prefetch_related('comments'):")
    print("    1 запрос: SELECT * FROM posts")
    print("    1 запрос: SELECT * FROM comments WHERE post_id IN (1,2,...)")
    print("    Итого: 2 запроса!")