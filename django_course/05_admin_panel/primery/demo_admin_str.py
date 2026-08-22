"""
Урок 5. Пример: зачем нужен метод __str__ в модели.

Когда модель регистрируют в админке, Django показывает её записи списком.
Без метода __str__ запись выглядит так: "Post object (1)" — непонятно.
С методом __str__ — так: "Первый пост" — сразу видно, что это.

Этот скрипт наглядно показывает разницу.

Как запустить:
    > python demo_admin_str.py
"""


# --- Модель БЕЗ метода __str__ (как было сначала) --------------------------
class PostBezMetoda:
    """Модель поста без магического метода __str__."""

    def __init__(self, zagolovok, tekst):
        self.zagolovok = zagolovok
        self.tekst = tekst


# --- Модель С методом __str__ (как надо) -----------------------------------
class PostSMetodom:
    """Модель поста с методом __str__."""

    def __init__(self, zagolovok, tekst):
        self.zagolovok = zagolovok
        self.tekst = tekst

    def __str__(self):
        # Возвращаем человекочитаемое название записи.
        return self.zagolovok


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: как __str__ влияет на отображение в админке")
    print("=" * 55)

    # Одинаковые данные
    bez = PostBezMetoda("Первый пост", "Привет!")
    s = PostSMetodom("Первый пост", "Привет!")

    print("\nКак запись видна БЕЗ __str__ (Django пишет 'Post object'):")
    print(f"   {bez}")

    print("\nКак запись видна С методом __str__ (сразу виден заголовок):")
    print(f"   {s}")

    print("\n" + "=" * 55)
    print("Вывод: добавь в модели метод __str__, и админка")
    print("покажет читаемое название вместо 'Post object (1)'.")
    print("=" * 55)