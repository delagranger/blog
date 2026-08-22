"""
Урок 6. Пример: демонстрация подстановки значений в шаблон.

Django-шаблоны используют конструкции {{ переменная }} для вывода данных
и {% for %} / {% if %} для логики. Этот скрипт имитирует подстановку
значений на чистом Python, чтобы показать, что происходит «под капотом».

Важно: это УПРОЩЁННАЯ иллюстрация идеи. Реальный Django-шаблонизатор
гораздо мощнее и безопаснее (он экранирует HTML-спецсимволы).

Как запустить:
    > python demo_shablon.py
"""

# --- 1. Данные (аналог контекста из views.py) ------------------------------
# View передаёт в шаблон словарь с данными. Здесь список постов.
posts = [
    {"zagolovok": "Первый пост", "tekst": "Привет, мир!"},
    {"zagolovok": "Про Django", "tekst": "Шаблоны — это легко."},
]

# --- 2. Шаблон (аналог glavnaya.html) --------------------------------------
# Вместо файла — строка с конструкциями, похожими на Django-шаблон.
shablon = """
{% for post in posts %}
    <h2>{{ post.zagolovok }}</h2>
    <p>{{ post.tekst }}</p>
{% endfor %}
"""


def podstavit(shablon_str: str, kontekst: dict) -> str:
    """
    Имитация работы шаблонизатора: заменяет конструкции в строке на значения.

    В реальном Django это делает движок шаблонов, а не обычный str.replace.
    Здесь мы упрощаем, чтобы показать лишь принцип подстановки.
    """
    rezultat = shablon_str

    # Подставляем значения {{ post.zagolovok }} и {{ post.tekst }}
    for post in kontekst["posts"]:
        rezultat = rezultat.replace(
            "{{ post.zagolovok }}", post["zagolovok"], 1
        )
        rezultat = rezultat.replace(
            "{{ post.tekst }}", post["tekst"], 1
        )

    return rezultat


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: подстановка значений в шаблон (принцип)")
    print("=" * 55)

    print("\nИсходный шаблон:")
    print(shablon)

    print("\nПосле подстановки (что видит браузер):")
    kontekst = {"posts": posts}
    itog = podstavit(shablon, kontekst)

    # Просто показываем итог с HTML-тегами вокруг, как на странице
    print("<html><body>")
    print(itog)
    print("</body></html>")

    print("\n" + "=" * 55)
    print("Вывод: {{ ... }} — это «место под значение», а не сам текст.")
    print("Шаблонизатор заменяет их данными из контекста.")
    print("=" * 55)