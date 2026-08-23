"""
Урок 3. Пример: демонстрация маршрутизации (URL -> View).

В Django маршрутизация работает через файлы urls.py: каждый адрес
связывается с функцией-представлением (view). Этот скрипт МОДЕЛИРУЕТ
тот же принцип на чистом Python, чтобы ты понял идею без запуска сервера.

Как работает Django (напомним):
    адрес /post/7/  -->  path("post/<int:nomer>/", view)  -->  view(request, nomer=7)

Запусти скрипт и посмотри, как адреса разбираются на части и находят
нужную «функцию-представление».

Как запустить:
    > python demo_marshruty.py
"""

import re


# --- 1. Определяем «представления» (views) ---------------------------------
# В Django это функции в blog/views.py. Здесь просто печатаем ответ.

def glavnaya():
    return "Привет, это мой блог!"


def o_sayte():
    return "Это страница «О сайте»."


def post_po_nomeru(nomer):
    return f"Ты открыл пост номер {nomer}."


# --- 2. Строим таблицу маршрутов (аналог urlpatterns) ----------------------
# Каждый маршрут: текстовый шаблон адреса -> функция-представление.
# Символы вроде <int:nomer> означают «поймать число из адреса».

MARSHUTY = [
    ("", glavnaya),                    # корень сайта
    ("o-sayte/", o_sayte),             # страница о сайте
    ("post/<int:nomer>/", post_po_nomeru),  # пост с номером
]


# --- 3. Пишем упрощённый «диспетчер» (то, что делает Django) ---------------
def razobrat_adres(adres: str):
    """
    Получает "хвост" адреса (например, "post/7/") и ищет подходящий маршрут.
    Возвращает кортеж (функция, словарь_параметров), либо None, если не нашёл.
    """
    for shablon, view in MARSHUTY:
        # Превращаем <int:имя> в регулярное выражение, ловящее число.
        regex = "^" + re.sub(r"<int:(\w+)>", r"(?P<\1>\\d+)", shablon) + "$"
        sovpadenie = re.match(regex, adres)
        if sovpadenie:
            # groupdict() вернёт {"nomer": "7"} — параметры из адреса.
            parametry = {
                k: int(v) for k, v in sovpadenie.groupdict().items()
            }
            return view, parametry
    return None


def zaprosit(adres: str):
    """Имитация «запроса браузера» по адресу."""
    print(f"\nЗапрос к адресу: /{adres}")
    rezultat = razobrat_adres(adres)

    if rezultat is None:
        print("  404: страница не найдена")
        return

    view, parametry = rezultat
    otvet = view(**parametry)  # вызываем view с параметрами из адреса
    print(f"  Ответ: {otvet}")


# --- 4. Проверяем работу ----------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО МАРШРУТИЗАЦИИ (как urlpatterns ищет view)")
    print("=" * 55)

    zaprosit("")             # главная
    zaprosit("o-sayte/")    # о сайте
    zaprosit("post/7/")     # пост с параметром
    zaprosit("post/42/")    # тот же маршрут, другой номер
    zaprosit("ne-sushestvuet/")  # такого адреса нет

    print("\n" + "=" * 55)
    print("Вывод: один и тот же маршрут 'post/<int:nomer>/'")
    print("обрабатывает и /post/7/, и /post/42/. Именно так")
    print("работает path() с параметрами в Django.")
    print("=" * 55)