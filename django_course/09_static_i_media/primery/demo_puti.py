"""
Урок 9. Пример: объяснение MEDIA_ROOT, MEDIA_URL и путей.

Django разделяет адрес (URL) и реальное место на диске (путь).
Одно и то же изображение имеет:
  - URL, который видит браузер (/media/posty/kartinka.jpg);
  - путь на диске, куда Django сохранил файл (C:\...\media\posty\kartinka.jpg).

Этот скрипт наглядно показывает разницу между URL и путём на диске,
не требуя запущенного проекта.

Как запустить:
    > python demo_puti.py
"""

import os


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: MEDIA_URL и MEDIA_ROOT (URL vs путь на диске)")
    print("=" * 55)

    # --- Настройки, как в settings.py --------------------------------------
    # BASE_DIR — корень проекта (в реальном проекте Django вычисляет сам).
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MEDIA_URL = "media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    print("\n1. Настройки:")
    print(f"   BASE_DIR   = {BASE_DIR}")
    print(f"   MEDIA_URL  = {MEDIA_URL}")
    print(f"   MEDIA_ROOT = {MEDIA_ROOT}")

    # --- Картинка, загруженная через ImageField(upload_to='posty/') --------
    imya_fayla = "kartinka.jpg"
    otnositelnyy_put = os.path.join("posty", imya_fayla)  # upload_to + имя

    print("\n2. Файл плюс настройки:")
    print(f"   Относительный путь (upload_to + имя): {otnositelnyy_put}")

    # URL — то, что видит браузер
    polnyy_url = MEDIA_URL + "posty/" + imya_fayla
    print(f"   URL в браузере:  /{polnyy_url}")

    # Путь — то, куда файл реально сохранился на диске
    polnyy_put = os.path.join(MEDIA_ROOT, otnositelnyy_put)
    print(f"   Путь на диске:   {polnyy_put}")

    print("\n" + "=" * 55)
    print("Вывод: MEDIA_ROOT — папка на диске, MEDIA_URL — адрес.")
    print("ImageField хранит относительный путь (upload_to + имя).")
    print("Объект .url отдаёт URL, а не путь на диске.")
    print("=" * 55)