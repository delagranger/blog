"""
Урок 2. Пример: изучение структуры проекта Django.

Этот скрипт показывает структуру папок и файлов твоего проекта, чтобы ты
запомнил, где что лежит. Он просто обходит папки и печатает дерево файлов.

Как запустить (из папки, где лежит manage.py):
    > python django_course/02_proekt_i_prilozheniya/primery/struktura_proekta.py

Или, если ты положил курс внутрь проекта, просто запусти скрипт откуда угодно —
он сам найдёт верхнюю папку проекта по файлу manage.py.
"""

from pathlib import Path

# --- Находим корень проекта -------------------------------------------------
# Ищем вверх по папкам файл manage.py — это признак корня Django-проекта.
start_point = Path(__file__).resolve()
project_root = None

for parent in [start_point, *start_point.parents]:
    if (parent / "manage.py").exists():
        project_root = parent
        break

if project_root is None:
    print("Не нашёл manage.py! Запусти скрипт из папки с проектом Django.")
    raise SystemExit(1)

print(f"Корень проекта: {project_root}\n")

# Папки, которые не нужно показывать (внутри много служебных файлов).
IGNORED_DIRS = {".git", "__pycache__", "venv", ".venv", "db.sqlite3"}

# Файлы, которые важны для изучения структуры.
KEY_FILES = {
    "manage.py": "главный помощник разработчика",
    "settings.py": "настройки всего проекта",
    "urls.py": "таблица адресов сайта",
    "models.py": "данные (урок 4)",
    "views.py": "логика страниц (урок 3)",
    "admin.py": "настройка админ-панели (урок 5)",
    "apps.py": "настройки приложения",
    "tests.py": "автотесты",
}


def opisanie_faila(imya: str) -> str:
    """Возвращает пояснение к файлу, если оно есть."""
    return KEY_FILES.get(imya, "")


# --- Печатаем дерево --------------------------------------------------------
def pokazat_derivo(folder: Path, urovni: int = 0):
    """Рекурсивно обходит папку и печатает её содержимое с пояснениями."""
    try:
        entries = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name))
    except PermissionError:
        print("  " * urovni + "└── (нет доступа)")
        return

    for entry in entries:
        otstup = "  " * urovni
        if entry.is_dir():
            if entry.name in IGNORED_DIRS:
                print(f"{otstup}├── {entry.name}/  (служебная папка, пропущена)")
                continue
            print(f"{otstup}├── {entry.name}/")
            pokazat_derivo(entry, urovni + 1)
        else:
            poyasneniye = opisanie_faila(entry.name)
            if poyasneniye:
                print(f"{otstup}├── {entry.name}  ← {poyasneniye}")
            else:
                print(f"{otstup}├── {entry.name}")


print("Структура проекта:\n")
pokazat_derivo(project_root)

print("\n" + "=" * 60)
print("Запомни главное:")
print("  manage.py  — через него запускаются все команды")
print("  config/    — настройки проекта")
print("  blog/      — наше приложение (если уже создано)")
print("=" * 60)