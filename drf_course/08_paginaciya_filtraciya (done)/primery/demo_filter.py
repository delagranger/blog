"""
Демонстрация пагинации, поиска и фильтрации на упрощённой модели.
"""


# -------- «База» с постами --------

POSTS = [
    {"id": 1, "title": "Python для начинающих", "date": "2025-01-10"},
    {"id": 2, "title": "Django REST Framework",  "date": "2025-02-15"},
    {"id": 3, "title": "SQL для бекенда",        "date": "2025-03-01"},
    {"id": 4, "title": "Python декораторы",       "date": "2025-01-20"},
    {"id": 5, "title": "DRF сериализаторы",       "date": "2025-02-28"},
    {"id": 6, "title": "Docker основы",           "date": "2025-03-10"},
    {"id": 7, "title": "Тестирование в Python",   "date": "2025-04-01"},
    {"id": 8, "title": "DRF ViewSets",            "date": "2025-04-15"},
]


# -------- Поиск (как SearchFilter) --------

def search_posts(posts, query):
    """Имитация search_fields = ['title', 'body']."""
    if not query:
        return posts
    query = query.lower()
    return [
        p for p in posts
        if query in p["title"].lower()
    ]


# -------- Фильтрация (как DjangoFilterBackend) --------

def filter_posts(posts, **filters):
    """Имитация filterset_fields."""
    result = posts
    for field, value in filters.items():
        if value:
            result = [p for p in result if p.get(field) == value]
    return result


# -------- Пагинация (как PageNumberPagination) --------

def paginate(posts, page=1, page_size=3):
    """Имитация PageNumberPagination."""
    total = len(posts)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = posts[start:end]

    return {
        "count": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "has_next": end < total,
        "has_previous": page > 1,
        "results": page_items,
    }


# -------- Демонстрация --------

if __name__ == "__main__":
    # 1. Поиск
    print("=" * 50)
    print("ПОИСК: ?search=python")
    print("=" * 50)
    result = search_posts(POSTS, query="python")
    for p in result:
        print(f"  {p}")
    print()

    # 2. Фильтрация по дате
    print("=" * 50)
    print("ФИЛЬТРАЦИЯ: ?date=2025-01-10")
    print("=" * 50)
    result = filter_posts(POSTS, date="2025-01-10")
    for p in result:
        print(f"  {p}")
    print()

    # 3. Поиск + пагинация (как в реальном API)
    print("=" * 50)
    print("ПОИСК + ПАГИНАЦИЯ: ?search=drf&page=1")
    print("=" * 50)
    result = search_posts(POSTS, query="drf")
    paginated = paginate(result, page=1, page_size=2)
    print(f"  Найдено: {paginated['count']}")
    print(f"  Страница: {paginated['page']}/{paginated['total_pages']}")
    print(f"  Есть ещё: {paginated['has_next']}")
    print(f"  Результаты:")
    for p in paginated["results"]:
        print(f"    {p}")
    print()

    # 4. Все три вместе (имитация GET /api/posts/?search=python&page=2)
    print("=" * 50)
    print("ВСЁ ВМЕСТЕ: ?search=python&page=2")
    print("=" * 50)
    result = search_posts(POSTS, query="python")
    paginated = paginate(result, page=2, page_size=2)
    print(f"  Страница 2:")
    for p in paginated["results"]:
        print(f"    {p}")

    print()
    print("Вывод:")
    print("  search — текстовый поиск (LIKE %слово%).")
    print("  filter — точное совпадение по полю (=).")
    print("  pagination — разбивка на страницы (page=2).")
    print("  В DRF всё это подключается парой строк в filter_backends.")