# Урок 8. Class-Based Views (CBV)

## Что такое Class-Based Views?

До сих пор мы писали View как функции. Django предлагает и другой способ —
**представления-классы** (Class-Based Views, сокращённо CBV).

**Class-Based View** — это класс, который обрабатывает запросы. Вместо того
чтобы писать логику для каждого метода (GET, POST) вручную, ты наследуешься
от готового класса, и Django многое делает за тебя.

Функции (их называют FBV — Function-Based Views) хорошо подходят для
нестандартных задач, а классы отлично экономят время на типовых: показать
список объектов, показать один объект, создать, изменить, удалить.

## Пример: та же страница двумя способами

Функцией (FBV):

```python
def glavnaya(request):
    posts = Post.objects.all()
    return render(request, "blog/spisok.html", {"posts": posts})
```

Классом (CBV):

```python
from django.views.generic import ListView


class SpisokPostov(ListView):
    model = Post
    template_name = "blog/spisok.html"
    context_object_name = "posts"
```

Что здесь написано:

- `model = Post` — «с какой моделью работаем».
- `template_name` — какой шаблон показать.
- `context_object_name = "posts"` — под каким именем список попадёт
  в шаблон. По умолчанию это `object_list`, но лучше задать своё.

Django сам достанет все записи (`Post.objects.all()`) и передаст их
в шаблон под именем `posts`.

## Основные готовые классы

| Класс | Назначение |
|-------|-----------|
| `ListView` | показать список объектов |
| `DetailView` | показать один объект |
| `CreateView` | создать объект (форма) |
| `UpdateView` | изменить объект |
| `DeleteView` | удалить объект |

Это «универсальные» представления (generic views). Разберём часто
используемое — `ListView` и `DetailView`.

## DetailView: показать один пост

Для страницы одного поста обычно нужен адрес с параметром, например
`/post/3/`. Класс `DetailView` сам находит объект по этому параметру.

В `urls.py` пишем:

```python
from django.urls import path
from .views import SpisokPostov, DetalPosta

urlpatterns = [
    path("", SpisokPostov.as_view(), name="spisok"),
    path("post/<int:pk>/", DetalPosta.as_view(), name="post"),
]
```

Разберём новое:

- `.as_view()` — превращает класс в обычное представление, которое
  понимает Django. Без него класс подключить к адресу нельзя.
- `<int:pk>` — параметр с именем `pk` (primary key). Именно по нему
  `DetailView` ищет запись.

В `views.py`:

```python
from django.views.generic import DetailView
from .models import Post


class DetalPosta(DetailView):
    model = Post
    template_name = "blog/detal.html"
    context_object_name = "post"
```

Всё. Django сам выполнит `Post.objects.get(pk=3)` и положит результат
в шаблон под именем `post`.

## Что такое pk

**pk (primary key)** — «первичный ключ», уникальный номер каждой записи
в таблице. Django создаёт его автоматически для каждой модели — это поле
`id`. То есть `pk` и `id` — практически одно и то же.

## Шаблон DetailView

Файл `detal.html`:

```html
{% extends "blog/osnova.html" %}

{% block soderzhimoye %}
    <h1>{{ post.zagolovok }}</h1>
    <p>{{ post.tekst }}</p>
    <p>{{ post.data_sozdaniya }}</p>
{% endblock %}
```

## Когда что использовать

- **FBV (функции)** — когда логика нестандартная, и нужно полностью
  контролировать процесс. Легче понять новичку.
- **CBV (классы)** — для типовых операций (список, детали, создание,
  изменение, удаление). Меньше кода, но требуется понимание наследования.

Хорошая новость: и то, и другое — полноценный Django. Выбирай по задаче.

## Словарик терминов

- **Primary key (pk)** — уникальный идентификатор записи.
- **Generic views** — готовые универсальные представления.
- **as_view()** — метод, превращающий класс в представление.

## Задание к уроку

1. Замени функцию `glavnaya` на `ListView`.
2. Добавь `DetailView` и страницу `/post/<int:pk>/`.
3. Создай шаблон `detal.html` и выведи пост.
4. Посмотри демо `primery/demo_cbv.py`, объясняющее принцип работы
   классов-представлений и `pk`.