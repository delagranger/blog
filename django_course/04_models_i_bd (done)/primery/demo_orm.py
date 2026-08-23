"""
Урок 4. Пример: демонстрация ORM на чистом Python.

ORM (Object-Relational Mapping) — это прослойка между Python-кодом
и базой данных. В Django эту роль выполняет встроенный ORM, но его
принцип можно показать на простейшем примере без Django.

Этот скрипт создаёт «игрушечную» модель и «игрушечную» базу (список
в памяти), чтобы показать, как работают `objects.create()`, `.all()`,
`.get()`, `.filter()`.

Как запустить:
    > python demo_orm.py
"""

# -----------------------------------------------------------------------
# 1. ИГРУШЕЧНАЯ БАЗА ДАННЫХ (в Django это файл db.sqlite3)
# -----------------------------------------------------------------------
# Вместо настоящей базы данных используем простой список.
# В реальности за каждым Post.objects.create() Django выполняет
# SQL-запрос INSERT, а за .all() — SELECT.

_baza_dannykh: list["Post"] = []


# -----------------------------------------------------------------------
# 2. КЛАСС-МОДЕЛЬ (аналог models.Model в Django)
# -----------------------------------------------------------------------
# В Django ты пишешь: class Post(models.Model).
# Здесь мы эмулируем тот же интерфейс, чтобы показать, как работает ORM.

class Post:
    """
    Модель поста. Каждый объект этого класса — одна запись в «базе».
    """
    # Счётчик для авто-ID (в Django ID создаёт база данных).
    _schedchik = 0

    def __init__(self, zagolovok: str, tekst: str):
        Post._schedchik += 1
        self.id = Post._schedchik               # ID записи
        self.zagolovok = zagolovok
        self.tekst = tekst

    def __repr__(self):
        """Как объект будет выглядеть при печати."""
        return f"Post(id={self.id}, zagolovok='{self.zagolovok}')"


# -----------------------------------------------------------------------
# 3. МЕНЕДЖЕР (аналог objects в Django)
# -----------------------------------------------------------------------
# В Django каждая модель имеет менеджер objects. Он — «посредник»
# между тобой и базой данных. Именно он содержит методы create(),
# all(), get(), filter().

class _PostManager:
    """«Менеджер» модели Post — имитация Django-менеджера."""

    @staticmethod
    def create(zagolovok: str, tekst: str) -> Post:
        """Создаёт запись и сохраняет в «базу»."""
        zapis = Post(zagolovok=zagolovok, tekst=tekst)
        _baza_dannykh.append(zapis)
        return zapis

    @staticmethod
    def all() -> list[Post]:
        """Возвращает все записи."""
        return list(_baza_dannykh)

    @staticmethod
    def get(**kriterii) -> Post:
        """
        Ищет ОДНУ запись, строго соответствующую критериям.
        Если запись не найдена — ошибка (как в Django).
        """
        for zapis in _baza_dannykh:
            if all(
                getattr(zapis, pole) == znachenie
                for pole, znachenie in kriterii.items()
            ):
                return zapis
        raise ValueError(f"Запись с {kriterii} не найдена!")

    @staticmethod
    def filter(**kriterii) -> list[Post]:
        """Ищет ВСЕ записи, подходящие под критерии."""
        rezultat = []
        for zapis in _baza_dannykh:
            if all(
                getattr(zapis, pole) == znachenie
                for pole, znachenie in kriterii.items()
            ):
                rezultat.append(zapis)
        return rezultat


# Присоединяем менеджер к классу (как в Django).
Post.objects = _PostManager()


# -----------------------------------------------------------------------
# 4. ТЕСТИРУЕМ — ТОЧНО ТАК ЖЕ, КАК В DJANGO SHELL
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО ORM: имитация Django ORM на чистом Python")
    print("=" * 55)

    # --- Создаём записи (аналог Post.objects.create(...))
    print("\n1. Создаём записи:")
    p1 = Post.objects.create(zagolovok="Первый пост", tekst="Привет, мир!")
    p2 = Post.objects.create(zagolovok="Про Django", tekst="ORM — это круто!")
    p3 = Post.objects.create(zagolovok="Планы", tekst="Изучить шаблоны")

    print(f"   Создано: {p1}, {p2}, {p3}")

    # --- all() — все записи
    print("\n2. Все записи (Post.objects.all()):")
    for post in Post.objects.all():
        print(f"   {post}  →  {post.tekst}")

    # --- get() — одна запись
    print("\n3. Поиск одной записи (Post.objects.get(zagolovok='Про Django')):")
    naydeno = Post.objects.get(zagolovok="Про Django")
    print(f"   Найдено: {naydeno}, текст: {naydeno.tekst}")

    # --- filter() — несколько записей
    print("\n4. Фильтр (имитация filter()):")
    print("   Показывает, что filter() ВСЕГДА возвращает СПИСОК,")
    print("   даже если подошла одна запись или ни одной.")

    # --- Что будет, если запись не найдена через get()
    print("\n5. Попытка найти несуществующее (get() вызывает ошибку):")
    try:
        Post.objects.get(zagolovok="Такого нет")
    except ValueError as e:
        print(f"   Ошибка: {e}")
        print("   (В Django было бы исключение DoesNotExist)")

    print("\n" + "=" * 55)
    print("ИТОГ:")
    print("  objects.create(...) → создать и сохранить")
    print("  objects.all()       → все записи списком")
    print("  objects.get(...)    → одну запись (строго)")
    print("  objects.filter(...) → несколько по условию")
    print("=" * 55)