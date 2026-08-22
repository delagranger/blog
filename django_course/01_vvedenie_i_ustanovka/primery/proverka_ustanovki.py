"""
Урок 1. Пример 2: проверка установки Django.

Этот скрипт проверяет, что Python и Django установлены правильно,
и показывает их версии. Он не требует работающего проекта — только
установленной библиотеки Django в активном виртуальном окружении.

Как запустить (предварительно активировав окружение):
    > python proverka_ustanovki.py

Если Django не установлен, скрипт сообщит об этом и подскажет команду.
"""

import sys

print("=" * 50)
print("ПРОВЕРКА УСТАНОВКИ")
print("=" * 50)

# --- Проверяем версию Python ----------------------------------------------
print(f"\nВерсия Python: {sys.version.split()[0]}")
print(f"Полный путь к Python: {sys.executable}")

# Проверяем, что Python достаточно новый (Django 5 требует Python 3.10+).
# sys.version_info — кортеж вида (major, minor, micro).
major, minor = sys.version_info[0], sys.version_info[1]

if (major, minor) < (3, 10):
    print("\nВНИМАНИЕ: у тебя слишком старый Python.")
    print("Django 5 требует Python 3.10 или новее. Обнови Python.")
else:
    print("Версия Python подходит для Django 5.")

# --- Проверяем Django ------------------------------------------------------
try:
    import django  # пробуем импортировать Django

except ImportError:
    # ImportError возникает, если библиотека не установлена.
    print("\nDjango НЕ установлен.")
    print("Установи его командой: pip install django")
    print("Не забудь сначала активировать виртуальное окружение!")

else:
    # Если импорт удался, выводим версию Django.
    print(f"\nВерсия Django: {django.get_version()}")
    print("Django установлен корректно. Можно переходить к уроку 2!")

print("\n" + "=" * 50)