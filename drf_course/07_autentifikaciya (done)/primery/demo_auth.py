"""
Демонстрация принципа аутентификации и прав доступа.
Показывает, как API различает «своих» и «чужих».
"""


# -------- Имитация базы пользователей --------

USERS = {
    "admin": {"password": "1234", "is_admin": True},
    "user1": {"password": "abcd", "is_admin": False},
}

# -------- Имитация «базы» токенов --------

TOKENS = {}  # token → username


def authenticate(username, password):
    """Проверить логин/пароль и выдать токен."""
    user = USERS.get(username)
    if user and user["password"] == password:
        import hashlib
        token = hashlib.md5(username.encode()).hexdigest()[:8]
        TOKENS[token] = username
        return token
    return None


def get_user_from_token(token):
    """Узнать пользователя по токену."""
    username = TOKENS.get(token)
    return USERS.get(username)


# -------- Права (Permissions) --------

class Permissions:
    """Имитация DRF permissions."""

    @staticmethod
    def is_authenticated(user):
        """Вообще вошёл?"""
        return user is not None

    @staticmethod
    def is_admin(user):
        """Админ?"""
        return user and user.get("is_admin", False)

    @staticmethod
    def can_write(user):
        """Может писать = вошёл (IsAuthenticatedOrReadOnly)."""
        return user is not None


# -------- Демонстрация --------

if __name__ == "__main__":
    print("=" * 50)
    print("ПОЛУЧЕНИЕ ТОКЕНА")
    print("=" * 50)

    # Правильный логин → токен
    token = authenticate("admin", "1234")
    print(f"admin:1234       → token = {token}  ✅")

    # Неправильный логин → None
    token = authenticate("admin", "неверный")
    print(f"admin:неверный   → token = {token}  ❌")
    print()

    # -------- Проверка прав --------

    print("=" * 50)
    print("ПРОВЕРКА ПРАВ (имитация запроса)")
    print("=" * 50)

    def simulate_request(token, action):
        user = get_user_from_token(token)
        username = TOKENS.get(token, "аноним")

        print(f"Пользователь: {username} ({'вошёл' if user else 'не вошёл'})")
        print(f"  Действие: {action}")

        if action in ("GET", "HEAD", "OPTIONS"):
            # Чтение — всем
            print(f"  → 200 OK (чтение разрешено всем) ✅")
        elif action in ("POST", "PUT", "PATCH", "DELETE"):
            if Permissions.can_write(user):
                print(f"  → 200 OK (запись разрешена) ✅")
            else:
                print(f"  → 401 Unauthorized (нужно войти) ❌")
        print()

    # Админ читает
    admin_token = authenticate("admin", "1234")
    simulate_request(admin_token, "GET")

    # Админ пишет
    simulate_request(admin_token, "POST")

    # Аноним читает
    simulate_request(None, "GET")

    # Аноним пытается писать
    simulate_request(None, "POST")

    print("Вывод:")
    print("  Аутентификация = «кто ты?» (токен → пользователь).")
    print("  Permissions = «что тебе можно?» (IsAuthenticated ↔ AllowAny).")
    print("  В DRF это настраивается парой строчек в settings.py и вьюхах.")