"""
Демонстрация принципа Generic Views: класс, который сам знает,
что делать для списка / создания / деталей.

В реальном DRF дженерики работают так же, но используют
queryset и сериализаторы из Django.
"""


class FakeQuerySet:
    """Имитация Django QuerySet: хранит записи и умеет их фильтровать."""

    def __init__(self, items=None):
        self._items = items or []

    def all(self):
        return list(self._items)

    def filter(self, **kwargs):
        """Очень упрощённый filter()."""
        result = self._items
        for key, value in kwargs.items():
            result = [item for item in result if item.get(key) == value]
        return FakeQuerySet(result)

    def __iter__(self):
        return iter(self._items)


class FakeSerializer:
    """Имитация DRF сериализатора."""

    def __init__(self, data=None):
        self.data_input = data

    def is_valid(self):
        return bool(self.data_input and self.data_input.get("title"))

    def save(self):
        return {"id": 99, **self.data_input}


# -------- Упрощённый дженерик --------

class ListCreateAPIView:
    """
    Имитация DRF ListCreateAPIView.

    Ты указываешь queryset и serializer_class — а класс сам
    знает, как обработать GET и POST.
    """
    queryset = None          # какой QuerySet использовать
    serializer_class = None  # какой сериализатор использовать

    def get(self, request):
        """Вернуть список всех записей (GET /api/posts/)."""
        items = self.queryset.all()
        # В реальном DRF здесь был бы serializer = self.serializer_class(items, many=True)
        return {"status": 200, "data": items, "count": len(items)}

    def post(self, request):
        """Создать новую запись (POST /api/posts/)."""
        serializer = self.serializer_class(data=request.get("data"))
        if serializer.is_valid():
            item = serializer.save()
            return {"status": 201, "data": item}
        return {"status": 400, "data": {"error": "Валидация не пройдена"}}

    def dispatch(self, method, request):
        if method == "GET":
            return self.get(request)
        elif method == "POST":
            return self.post(request)
        return {"status": 405, "data": {"error": f"Метод {method} не разрешён"}}


# -------- Конкретный API (как твой PostListCreateView) --------

class PostAPI(ListCreateAPIView):
    """
    Минимальная конфигурация: только queryset и serializer_class.
    Вся логика GET/POST уже в родителе.
    """
    queryset = FakeQuerySet([
        {"id": 1, "title": "Первый пост", "body": "Текст 1"},
        {"id": 2, "title": "Второй пост", "body": "Текст 2"},
    ])
    serializer_class = FakeSerializer


# -------- Демонстрация --------

if __name__ == "__main__":
    api = PostAPI()

    # GET — список
    print("=" * 50)
    print("GET /api/posts/")
    print("=" * 50)
    resp = api.dispatch("GET", {})
    print(f"  {resp}")
    print()

    # POST — создание
    print("=" * 50)
    print("POST /api/posts/")
    print("=" * 50)
    resp = api.dispatch("POST", {"data": {"title": "Новый пост", "body": "Текст"}})
    print(f"  {resp}")
    print()

    print("Вывод:")
    print("  Ты указываешь queryset и serializer_class — дженерик делает всё сам.")
    print("  Никаких get() и post() писать не нужно, они уже есть в родителе.")
    print("  Код сокращается с 80 строк до 8.")