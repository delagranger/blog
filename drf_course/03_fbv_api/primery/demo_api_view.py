"""
Демонстрация того, как @api_view обрабатывает запросы.
Упрощённая модель без Django — чтобы понять принцип.
"""

from dataclasses import dataclass, field
from typing import Any


# -------- Упрощённый «request» (как в Django) --------

@dataclass
class FakeRequest:
    """Имитация HTTP-запроса."""
    method: str
    data: dict


# -------- Упрощённый «Response» (как в DRF) --------

@dataclass
class FakeResponse:
    """Имитация DRF Response."""
    data: Any
    status_code: int = 200

    def __repr__(self):
        return f"Response(status={self.status_code}, data={self.data})"


# -------- Упрощённые «модель» и «сериализатор» --------

class FakePost:
    """«База данных» в памяти (словарь)."""
    _storage = {}
    _next_id = 1

    @classmethod
    def create(cls, title, body):
        post = {"id": cls._next_id, "title": title, "body": body}
        cls._storage[cls._next_id] = post
        cls._next_id += 1
        return post

    @classmethod
    def all(cls):
        return list(cls._storage.values())

    @classmethod
    def get(cls, pk):
        return cls._storage.get(pk)


# -------- «View» функции --------

def post_list(request):
    """
    Имитация @api_view(["GET", "POST"]).

    В реальном коде наверху был бы декоратор @api_view,
    здесь мы просто проверяем request.method вручную.
    """
    if request.method == "GET":
        posts = FakePost.all()
        return FakeResponse(data=posts, status_code=200)

    elif request.method == "POST":
        data = request.data
        if not data.get("title") or not data.get("body"):
            return FakeResponse(
                data={"error": "title и body обязательны"},
                status_code=400,
            )
        post = FakePost.create(data["title"], data["body"])
        return FakeResponse(data=post, status_code=201)

    return FakeResponse(
        data={"error": f"Метод {request.method} не поддерживается"},
        status_code=405,
    )


def post_detail(request, pk):
    """
    Имитация @api_view(["GET", "PUT", "DELETE"]).
    """
    post = FakePost.get(pk)

    if post is None:
        return FakeResponse(
            data={"error": f"Пост {pk} не найден"},
            status_code=404,
        )

    if request.method == "GET":
        return FakeResponse(data=post, status_code=200)

    elif request.method == "PUT":
        post["title"] = request.data.get("title", post["title"])
        post["body"] = request.data.get("body", post["body"])
        return FakeResponse(data=post, status_code=200)

    elif request.method == "DELETE":
        del FakePost._storage[pk]
        return FakeResponse(data=None, status_code=204)

    return FakeResponse(
        data={"error": f"Метод {request.method} не поддерживается"},
        status_code=405,
    )


# -------- Демонстрация --------

if __name__ == "__main__":
    # Создадим пару постов
    FakePost.create("Первый пост", "Текст первого поста")
    FakePost.create("Второй пост", "Текст второго поста")

    # GET /api/posts/ — список
    print("=" * 50)
    print("GET /api/posts/")
    print("=" * 50)
    req = FakeRequest(method="GET", data={})
    resp = post_list(req)
    print(f"Запрос: {req.method} /api/posts/")
    print(f"Ответ:  {resp}")
    print()

    # POST /api/posts/ — создание
    print("=" * 50)
    print("POST /api/posts/")
    print("=" * 50)
    req = FakeRequest(method="POST", data={"title": "Новый пост", "body": "Текст"})
    resp = post_list(req)
    print(f"Запрос: {req.method} /api/posts/")
    print(f"Данные: {req.data}")
    print(f"Ответ:  {resp}")
    print()

    # GET /api/posts/1/ — детали
    print("=" * 50)
    print("GET /api/posts/1/")
    print("=" * 50)
    req = FakeRequest(method="GET", data={})
    resp = post_detail(req, pk=1)
    print(f"Запрос: {req.method} /api/posts/1/")
    print(f"Ответ:  {resp}")
    print()

    # DELETE /api/posts/2/ — удаление
    print("=" * 50)
    print("DELETE /api/posts/2/")
    print("=" * 50)
    req = FakeRequest(method="DELETE", data={})
    resp = post_detail(req, pk=2)
    print(f"Запрос: {req.method} /api/posts/2/")
    print(f"Ответ:  {resp}")
    print()

    # Проверим, что осталось
    print("=" * 50)
    print("GET /api/posts/ (после удаления)")
    print("=" * 50)
    req = FakeRequest(method="GET", data={})
    resp = post_list(req)
    print(f"Ответ:  {resp}")

    print()
    print("Вывод:")
    print("  Одна функция обрабатывает все HTTP-методы.")
    print("  request.method говорит, ЧТО делать (GET/POST/DELETE).")
    print("  Response возвращает данные + HTTP-статус.")