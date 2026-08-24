"""
Урок 7. Пример: демонстрация валидации формы на чистом Python.

В Django форма (forms.Form / forms.ModelForm) умеет проверять данные
методом is_valid(). Если данные некорректны, форма «запоминает» ошибки,
и пользователь видит их рядом с полями.

Этот скрипт имитирует простейшую валидацию: форма контактов с полями
"имя" и "email". Показываем, как один и тот же объект формы ведёт себя
с корректными и некорректными данными.

Как запустить:
    > python demo_forma.py
"""

# --- Мини-форма с проверкой (аналог forms.Form в Django) -------------------
class ContactForm:
    """
    Простая форма. Хранит введённые данные и список ошибок,
    как это делает Django-форма.
    """

    def __init__(self, imya: str = "", email: str = ""):
        self.imya = imya
        self.email = email
        self.oshibki: dict[str, str] = {}

    def is_valid(self) -> bool:
        """Проверяет данные. Возвращает True, если ошибок нет."""
        self.oshibki = {}

        if not self.imya.strip():
            self.oshibki["imya"] = "Имя не может быть пустым."

        if "@" not in self.email:
            self.oshibki["email"] = "Введите корректный e-mail."

        return not self.oshibki


def pokazat_rezultat(form: ContactForm):
    """Имитирует то, как View обрабатывает форму."""
    if form.is_valid():
        print("   ✓ Данные корректны — сохраняем в базу.")
    else:
        print("   ✗ Данные некорректны — показываем ошибки:")
        for pole, oshibka in form.oshibki.items():
            print(f"      {pole}: {oshibka}")


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: валидация формы (как работает is_valid)")
    print("=" * 55)

    print("\n1. Корректные данные:")
    forma1 = ContactForm(imya="Аня", email="anna@example.com")
    pokazat_rezultat(forma1)

    print("\n2. Пустое имя и кривой e-mail:")
    forma2 = ContactForm(imya="  ", email="ne-email")
    pokazat_rezultat(forma2)

    print("\n3. Имя есть, но e-mail без @:")
    forma3 = ContactForm(imya="Иван", email="ivan.example.com")
    pokazat_rezultat(forma3)

    print("\n" + "=" * 55)
    print("Вывод: is_valid() проверяет данные по правилам.")
    print("Если есть ошибки — форма их запоминает, и мы")
    print("показываем их пользователю вместо сохранения.")
    print("=" * 55)