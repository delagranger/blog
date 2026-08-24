"""
Урок 10. Пример: принцип входа и хеширования пароля.

Django не хранит пароли открытым текстом. Вместо этого он хранит хеш —
«отпечаток» пароля, из которого нельзя восстановить исходный пароль.
При входе Django хеширует введённый пароль и сравнивает отпечатки.

Этот скрипт демонстрирует:
  1) как работает проверка логина и пароля;
  2) что пароль хранится как хеш, а не как текст.

Для наглядности используем встроенный в Python модуль hashlib.

Как запустить:
    > python demo_vhod.py
"""

import hashlib


def zaxheshirovat(parol: str) -> str:
    """
    Превращает пароль в хеш (упрощённо).

    Реальный Django использует PBKDF2 с «солью» — случайной добавкой,
    делающей хеш более стойким. Здесь показан сам принцип.
    """
    return hashlib.sha256(parol.encode("utf-8")).hexdigest()


# --- «Пользователь» с сохранённым хешем пароля -----------------------------
class Polzovatel:
    """Игрушечный пользователь. Хранит не пароль, а его хеш."""

    def __init__(self, username: str, parol: str):
        self.username = username
        self.khesh_parolya = zaxheshirovat(parol)  # сохранили отпечаток

    def proverit_parol(self, vvedennyy: str) -> bool:
        """Сравнивает хеш введённого пароля с сохранённым."""
        return zaxheshirovat(vvedennyy) == self.khesh_parolya


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: вход и хеширование пароля (принцип)")
    print("=" * 55)

    anna = Polzovatel("anna", "sverhsekretnyy123")

    print("\n1. Смотрим, что хранится у пользователя:")
    print(f"   Логин: {anna.username}")
    print(f"   Сохранённый хеш: {anna.khesh_parolya[:20]}...")
    print("   (сам пароль в открытом виде НЕ хранится!)")

    print("\n2. Попытка входа с правильным паролем:")
    ok = anna.proverit_parol("sverhsekretnyy123")
    print(f"   Результат: {'✓ вход разрешён' if ok else '✗ доступ запрещён'}")

    print("\n3. Попытка входа с неверным паролем:")
    ok = anna.proverit_parol("nepravilnyy")
    print(f"   Результат: {'✓ вход разрешён' if ok else '✗ доступ запрещён'}")

    print("\n" + "=" * 55)
    print("Вывод: Django сравнивает хеши, а не пароли напрямую.")
    print("Пользователь вошёл — если хеши совпали.")
    print("=" * 55)