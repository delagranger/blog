# Урок 9. Static и Media файлы

## Что такое статические и медиа-файлы?

Настоящий сайт — это не только HTML, но и картинки, стили (CSS), скрипты
(JavaScript). Все эти файлы в Django делятся на две большие группы:

- **Static (статические)** — файлы, которые являются частью самого сайта:
  стили (`style.css`), скрипты (`script.js`), логотипы, фоновые картинки.
  Их создаёт разработчик, они одни и те же для всех посетителей.
- **Media (медиа)** — файлы, которые загружают пользователи или админ:
  фотографии в постах, аватары. Они меняются во время работы сайта.

## Какая разница простыми словами

- Static — это «оформление сайта». Меняется редко, создаётся при разработке.
- Media — это «контент пользователей». Загружается в процессе жизни сайта.

## Настраиваем static

### Шаг 1. Папка

Создадим папку `static/` внутри приложения (или общую в корне проекта):

```
blog/
└── static/
    └── blog/
        └── style.css
```

Так же как с шаблонами, внутри `static/` создаём вложенную папку `blog/`,
чтобы файлы разных приложений не перепутались.

### Шаг 2. Подключаем в шаблоне

В начале шаблона добавь:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'blog/style.css' %}">
```

- `{% load static %}` — подключает тег static.
- `{% static 'blog/style.css' %}` — вернёт правильный адрес к файлу.

## Параметр STATIC_URL

В `config/settings.py` уже есть строка:

```python
STATIC_URL = "static/"
```

`STATIC_URL` — это адрес-префикс, по которому Django отдаёт статические
файлы. Менять его не нужно — оно уже настроено.

## Настраиваем media

Media-файлы требуют чуть больше настроек.

### Шаг 1. Укажем, куда их класть

В `config/settings.py` добавь:

```python
import os

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
```

Разберём:

- `MEDIA_URL` — адрес-префикс для медиа-файлов (аналог STATIC_URL).
- `MEDIA_ROOT` — реальная папка на диске, куда будут сохраняться файлы.
- `BASE_DIR` — корень проекта (путь к папке, где лежит manage.py).
- `os.path.join` — склеивает путь правильно под конкретную систему.

### Шаг 2. Поле с картинкой в модели

Добавим в модель `Post` поле для изображения:

```python
class Post(models.Model):
    zagolovok = models.CharField(max_length=200)
    tekst = models.TextField()
    izobrazhenie = models.ImageField(upload_to="posty/", blank=True)
```

- `ImageField` — поле для хранения картинки.
- `upload_to="posty/"` — подпапка внутри MEDIA_ROOT, куда грузить файлы.
- `blank=True` — поле необязательное.

> Для работы `ImageField` нужна библиотека **Pillow**. Установи её:
> `pip install Pillow`.

После изменения модели не забудь выполнить `makemigrations` и `migrate`.

### Шаг 3. Обслуживание media при разработке

В `config/urls.py` добавь (только для режима разработки):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... твои маршруты ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`DEBUG` — режим отладки (включён, пока ты разрабатываешь). В этом режиме
Django сам отдаёт медиа-файлы по адресу `MEDIA_URL`.

## Вывод картинки в шаблоне

```html
{% if post.izobrazhenie %}
    <img src="{{ post.izobrazhenie.url }}" alt="{{ post.zagolovok }}">
{% endif %}
```

`post.izobrazhenie.url` — полный адрес картинки.

## Словарик терминов

- **CSS** — язык описания внешнего вида страницы.
- **JavaScript** — язык интерактивности в браузере.
- **Pillow** — библиотека Python для работы с изображениями.

## Задание к уроку

1. Создай папку `static/blog/style.css`, добавь простой стиль и подключи
   его через `{% static %}`.
2. Добавь в модель `Post` поле `izobrazhenie` и сделай миграции.
3. Через админку добавь пост с картинкой.
4. Выведи картинку в шаблоне `detal.html`.
5. Посмотри демо `primery/demo_puti.py` — объяснение MEDIA_ROOT и путей.