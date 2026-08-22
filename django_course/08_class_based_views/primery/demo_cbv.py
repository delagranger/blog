"""
Урок 8. Пример: принцип Class-Based Views и первичный ключ (pk).

В Django представления-классы (ListView, DetailView и др.) берут на себя
типовую работу: достать список/один объект и передать в шаблон. Ключевая
идея DetailView — найти запись по первичному ключу (pk).

Этот скрипт имитирует:
  1) как ListView отдаёт список объектов;
  2) как DetailView находит ОДИН объект по pk.

Как запустить:
    > python demo_cbv.py
"""


# --- «Модель» с pk (в Django pk создаётся автоматически как id) -----------
class Post:
    """Игрушечная модель поста с первичным ключом."""

    def __init__(self, pk: int, zagolovok: str, tekst: str):
        self.pk = pk                 # первичный ключ (как id в Django)
        self.zagolovok = zagolovok
        self.tekst = tekst

    def __repr__(self):
        return f"<Post pk={self.pk}: {self.zagolovok}>"


# --- «База данных» ---------------------------------------------------------
BAZA = [
    Post(1, "Первый пост", "Привет, мир!"),
    Post(2, "Про Django", "CBV — это удобно."),
    Post(3, "Планы", "Изучить статику и медиа."),
]


# --- Имитация ListView ------------------------------------------------------
class SpisokPostov:
    """Аналог ListView: возвращает ВСЕ объекты."""

    model = Post  # с какой моделью работаем

    @classmethod
    def poluchit_spisok(cls):
        return list(BAZA)


# --- Имитация DetailView ----------------------------------------------------
class DetalPosta:
    """Аналог DetailView: находит ОДИН объект по pk."""

    model = Post

    @classmethod
    def nayti_po_pk(cls, pk: int):
        for post in BAZA:
            if post.pk == pk:
                return post
        # В Django здесь будет исключение DoesNotExist.
        raise ValueError(f"Пост с pk={pk} не найден")


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: принцип ListView и DetailView (поиск по pk)")
    print("=" * 55)

    print("\n1. ListView — показать список (все объекты):")
    for post in SpisokPostov.poluchit_spisok():
        print(f"   {post}")

    print("\n2. DetailView — показать один объект по pk:")
    print("   Запрос: /post/2/  →  pk = 2")
    post = DetalPosta.nayti_po_pk(2)
    print(f"   Найден: {post}")
    print(f"   Заголовок: {post.zagolovok}")
    print(f"   Текст: {post.tekst}")

    print("\n3. Попытка найти несуществующий pk:")
    try:
        DetalPosta.nayti_po_pk(99)
    except ValueError as e:
        print(f"   Ошибка: {e}")
        print("   (В Django — 404 страница не найдена)")

    print("\n" + "=" * 55)
    print("Вывод: DetailView сам ищет запись по pk, который")
    print("пришёл из адреса. Отсюда шаблон адреса <int:pk>.")
    print("=" * 55)