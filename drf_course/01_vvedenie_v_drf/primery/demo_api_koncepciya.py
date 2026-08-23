"""
Демонстрация концепции REST API на примере «ресторана».

Представь: ты — клиент, сервер — кухня, API — меню.
"""

def pokazat_menu():
    """Меню — это и есть API. Оно говорит, ЧТО можно заказать и КАК."""
    print("=" * 50)
    print("МЕНЮ РЕСТОРАНА (API блога)")
    print("=" * 50)
    print()

    # Каждый пункт меню — это эндпоинт (endpoint)
    menu = {
        "GET    /api/posts/": "Получить список всех постов",
        "POST   /api/posts/": "Создать новый пост",
        "GET    /api/posts/5/": "Получить пост с id=5",
        "PUT    /api/posts/5/": "Полностью обновить пост",
        "PATCH  /api/posts/5/": "Частично обновить пост",
        "DELETE /api/posts/5/": "Удалить пост",
    }

    for endpoint, opisanie in menu.items():
        print(f"  {endpoint}")
        print(f"       → {opisanie}")
        print()

    print("Обрати внимание:")
    print("  - Адрес один и тот же (/api/posts/5/)")
    print("  - Действие зависит от HTTP-метода (GET, PUT, DELETE)")
    print()


def sdelat_zakaz():
    """Имитация: клиент отправляет запрос, сервер отвечает в JSON."""

    import json

    # Запрос клиента (имитация GET-запроса)
    zapros = {
        "method": "GET",
        "url": "/api/posts/1/",
    }

    print("=" * 50)
    print("КЛИЕНТ → СЕРВЕР")
    print("=" * 50)
    print(f"Запрос: {zapros['method']} {zapros['url']}")
    print()

    # Ответ сервера в JSON
    otvet = {
        "id": 1,
        "title": "Первый пост",
        "body": "Текст моего первого поста в блоге",
        "creation_date": "2025-01-15T12:00:00Z",
    }

    print("=" * 50)
    print("СЕРВЕР → КЛИЕНТ (JSON)")
    print("=" * 50)
    print(f"HTTP 200 OK")
    print(f"Content-Type: application/json")
    print()
    print(json.dumps(otvet, indent=4, ensure_ascii=False))
    print()


def pokazat_http_kody():
    """Основные HTTP-коды ответа и их смысл."""

    kody = {
        200: "OK — запрос выполнен успешно",
        201: "Created — ресурс создан (после POST)",
        204: "No Content — успешно, но ответа нет (после DELETE)",
        400: "Bad Request — ошибка в данных запроса",
        401: "Unauthorized — нужно войти",
        403: "Forbidden — нет прав",
        404: "Not Found — ресурс не найден",
        405: "Method Not Allowed — неверный HTTP-метод",
        500: "Internal Server Error — ошибка на сервере",
    }

    print("=" * 50)
    print("HTTP-КОДЫ ОТВЕТА")
    print("=" * 50)
    print()
    print("Код  │ Значение")
    print("─────┼──────────────────────────────────")
    for kod, znachenie in kody.items():
        print(f" {kod}  │ {znachenie}")
    print()


if __name__ == "__main__":
    pokazat_menu()
    sdelat_zakaz()
    pokazat_http_kody()

    print("Вывод:")
    print("  REST API — это способ общения клиента и сервера через HTTP.")
    print("  URL указывает НА ЧТО (ресурс), метод — ЧТО ДЕЛАТЬ (действие).")
    print("  Ответ приходит в JSON, статус — в HTTP-коде.")