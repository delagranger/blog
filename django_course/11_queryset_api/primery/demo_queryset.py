"""
Урок 11. Пример: принцип QuerySet API на обычных списках Python.

Django-QuerySet умеет фильтровать, сортировать, нарезать и проверять
наличие данных при помощи методов filter(), order_by(), exclude()
и т.д. Эти методы складываются в цепочки.

Этот скрипт имитирует ключевые операции QuerySet на обычном списке
словарей, чтобы ты понял саму идею, не запуская Django.

Как запустить:
    > python demo_queryset.py
"""


# --- «База данных»: список постов ------------------------------------------
POSTY = [
    {"pk": 1, "zagolovok": "Первый пост", "published": True,  "data": "2026-01-10"},
    {"pk": 2, "zagolovok": "Изучаем Django", "published": True,  "data": "2026-03-15"},
    {"pk": 3, "zagolovok": "Черновик", "published": False, "data": "2026-05-20"},
    {"pk": 4, "zagolovok": "Django и формы", "published": True,  "data": "2026-07-01"},
]


def filter_(spisok: list, **usloviya) -> list:
    """Аналог filter(): оставить записи, подходящие под все условия."""
    rezultat = spisok
    for klyuch, znachenie in usloviya.items():
        rezultat = [x for x in rezultat if x.get(klyuch) == znachenie]
    return rezultat


def exclude_(spisok: list, **usloviya) -> list:
    """Аналог exclude(): убрать записи, подходящие под условия."""
    otbros = filter_(spisok, **usloviya)
    return [x for x in spisok if x not in otbros]


def order_by(spisok: list, pole: str, ubivanie=False) -> list:
    """Аналог order_by(): отсортировать по полю."""
    return sorted(spisok, key=lambda x: x[pole], reverse=ubivanie)


def contains(spisok: list, pole: str, podstroka: str) -> list:
    """Аналог lookup contains: поле содержит подстроку."""
    return [x for x in spisok if podstroka in x[pole]]


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: принцип QuerySet API (filter, exclude, order_by)")
    print("=" * 55)

    print("\n1. filter(published=True) — только опубликованные:")
    for p in filter_(POSTY, published=True):
        print(f"   {p['pk']}: {p['zagolovok']}")

    print("\n2. exclude(published=False) — убрать черновики:")
    for p in exclude_(POSTY, published=False):
        print(f"   {p['pk']}: {p['zagolovok']}")

    print("\n3. order_by('-data') — по дате по убыванию:")
    for p in order_by(POSTY, "data", ubivanie=True):
        print(f"   {p['data']}: {p['zagolovok']}")

    print("\n4. contains(zagolovok, 'Django') — поиск по подстроке:")
    for p in contains(POSTY, "zagolovok", "Django"):
        print(f"   {p['pk']}: {p['zagolovok']}")

    print("\n5. Цепочка: filter(published=True) + order_by('-data'):")
    otobrannye = filter_(POSTY, published=True)
    otobrannye = order_by(otobrannye, "data", ubivanie=True)
    for p in otobrannye:
        print(f"   {p['data']}: {p['zagolovok']}")

    print("\n" + "=" * 55)
    print("Вывод: методы QuerySet складываются в цепочки,")
    print("каждый следующий уточняет результат предыдущего.")
    print("=" * 55)