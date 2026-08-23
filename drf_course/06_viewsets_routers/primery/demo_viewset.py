"""
Демонстрация: ViewSet заменяет два класса, Router генерирует URL.
Упрощённая модель без Django.
"""


class FakeViewSet:
    """
    Имитация ModelViewSet.

    Один класс содержит ВСЕ действия: list, create, retrieve, update, destroy.
    """
    def list(self, request):
        return {"action": "list", "method": "GET", "url": "/posts/"}

    def create(self, request):
        return {"action": "create", "method": "POST", "url": "/posts/"}

    def retrieve(self, request, pk):
        return {"action": "retrieve", "method": "GET", "url": f"/posts/{pk}/"}

    def update(self, request, pk):
        return {"action": "update", "method": "PUT", "url": f"/posts/{pk}/"}

    def partial_update(self, request, pk):
        return {"action": "partial_update", "method": "PATCH", "url": f"/posts/{pk}/"}

    def destroy(self, request, pk):
        return {"action": "destroy", "method": "DELETE", "url": f"/posts/{pk}/"}


class FakeRouter:
    """
    Имитация DefaultRouter.

    router.register('posts', PostViewSet) автоматически генерирует
    все URL-пути и связывает их с методами ViewSet.

    В реальном DRF Router делает то же самое, но с реальными URL-диспетчерами.
    """

    def __init__(self):
        self._routes = []  # (url, method, action_handler)

    def register(self, prefix, viewset):
        """
        Автоматически создаёт URL для стандартных действий.

        В реальном DRF Router работает через Django URL-диспетчер,
        здесь просто показываем, какие пути генерируются.
        """
        # Два пути: список и детали
        patterns = [
            # (URL-шаблон, HTTP-метод, метод ViewSet, нужен ли pk)
            (f"{prefix}/", "GET", viewset.list, False),
            (f"{prefix}/", "POST", viewset.create, False),
            (f"{prefix}/{{pk}}/", "GET", viewset.retrieve, True),
            (f"{prefix}/{{pk}}/", "PUT", viewset.update, True),
            (f"{prefix}/{{pk}}/", "PATCH", viewset.partial_update, True),
            (f"{prefix}/{{pk}}/", "DELETE", viewset.destroy, True),
        ]

        for url, method, handler, needs_pk in patterns:
            self._routes.append({
                "url": url,
                "method": method,
                "handler": handler,
                "needs_pk": needs_pk,
            })

    def show_routes(self):
        """Показать все сгенерированные маршруты."""
        for route in self._routes:
            print(f"  {route['method']:6} /api/{route['url']}")


# -------- Демонстрация --------

if __name__ == "__main__":
    post_viewset = FakeViewSet()
    router = FakeRouter()
    router.register("posts", post_viewset)

    print("=" * 50)
    print("ROUTER АВТОМАТИЧЕСКИ ГЕНЕРИРУЕТ:")
    print("=" * 50)
    router.show_routes()

    print()
    print("=" * 50)
    print("ОБРАЩЕНИЕ К КОНКРЕТНОМУ МЕТОДУ (имитация HTTP-запроса):")
    print("=" * 50)

    # GET /posts/ → list
    resp = post_viewset.list({})
    print(f"  GET /posts/       → {resp}")

    # POST /posts/ → create
    resp = post_viewset.create({})
    print(f"  POST /posts/      → {resp}")

    # GET /posts/5/ → retrieve
    resp = post_viewset.retrieve({}, pk=5)
    print(f"  GET /posts/5/     → {resp}")

    # DELETE /posts/5/ → destroy
    resp = post_viewset.destroy({}, pk=5)
    print(f"  DELETE /posts/5/  → {resp}")

    print()
    print("Вывод:")
    print("  ViewSet = ОДИН класс вместо ШЕСТИ отдельных методов в разных классах.")
    print("  Router = НОЛЬ ручных URL вместо ШЕСТИ вызовов path().")
    print(f"  Код сократился: 2 класса + 2 URL → 1 класс + 1 router.register().")