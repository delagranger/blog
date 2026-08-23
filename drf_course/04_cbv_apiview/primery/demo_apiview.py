"""
Демонстрация принципа Class-Based View на чистом Python.
Показывает, как класс заменяет набор if'ов на методы.
"""


class FakeBlogAPI:
    """Имитация APIView: методы класса вместо if'ов."""

    def __init__(self):
        self.posts = {}  # «база» в памяти
        self._next_id = 1

    # -------- HTTP-методы (как в DRF) --------

    def get(self, request, pk=None):
        """
        Обработчик GET: список (без pk) или детали (с pk).

        В реальном DRF этот метод вызывается автоматически,
        когда приходит GET-запрос.
        """
        if pk is None:
            return {"status": 200, "data": list(self.posts.values())}
        post = self.posts.get(pk)
        if post:
            return {"status": 200, "data": post}
        return {"status": 404, "data": {"error": f"Пост {pk} не найден"}}

    def post(self, request, pk=None):
        """Обработчик POST: создание поста."""
        new_id = self._next_id
        self._next_id += 1
        self.posts[new_id] = {
            "id": new_id,
            "title": request["data"]["title"],
            "body": request["data"]["body"],
        }
        return {"status": 201, "data": self.posts[new_id]}

    def delete(self, request, pk=None):
        """Обработчик DELETE: удаление поста."""
        if pk in self.posts:
            del self.posts[pk]
            return {"status": 204, "data": None}
        return {"status": 404, "data": {"error": f"Пост {pk} не найден"}}

    # -------- Диспетчер (имитация .as_view()) --------

    def dispatch(self, method, request, pk=None):
        """
        В реальном DRF этот метод вызывается у класса автоматически.
        Он смотрит на HTTP-метод и вызывает соответствующий метод класса.
        """
        if method == "GET":
            return self.get(request, pk)
        elif method == "POST":
            return self.post(request, pk)
        elif method == "DELETE":
            return self.delete(request, pk)
        else:
            return {"status": 405, "data": {"error": f"Метод {method} запрещён"}}


# -------- Демонстрация --------

if __name__ == "__main__":
    api = FakeBlogAPI()

    # Создадим посты
    print("=" * 50)
    print("POST /api/posts/  (создание)")
    print("=" * 50)
    resp = api.dispatch("POST", {"data": {"title": "Первый", "body": "Текст 1"}})
    print(f"  → {resp}")
    resp = api.dispatch("POST", {"data": {"title": "Второй", "body": "Текст 2"}})
    print(f"  → {resp}")
    print()

    # GET списка
    print("=" * 50)
    print("GET /api/posts/  (список)")
    print("=" * 50)
    resp = api.dispatch("GET", {})
    print(f"  → {resp}")
    print()

    # GET одного
    print("=" * 50)
    print("GET /api/posts/1/  (детали)")
    print("=" * 50)
    resp = api.dispatch("GET", {}, pk=1)
    print(f"  → {resp}")
    print()

    # DELETE
    print("=" * 50)
    print("DELETE /api/posts/2/  (удаление)")
    print("=" * 50)
    resp = api.dispatch("DELETE", {}, pk=2)
    print(f"  → {resp}")
    print()

    print("Вывод:")
    print("  Класс упорядочивает логику: get() GET, post() POST, delete() DELETE.")
    print("  Нет лапши из if'ов — код читается линейно.")
    print("  Наследование позволяет переиспользовать общую логику.")