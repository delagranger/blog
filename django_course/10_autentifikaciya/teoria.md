# Урок 10. Аутентификация (вход и пользователи)

## Что такое аутентификация?

**Аутентификация** — это определение того, кто именно обращается к сайту.
Проще говоря — «вход»: пользователь вводит логин и пароль, а сайт
«узнаёт» его.

В Django для этого всё уже готово:

- модель пользователя `User`;
- формы входа и регистрации;
- система прав и разрешений.

## Модель User

Django из коробки даёт модель `User` с полями:

- `username` — логин;
- `password` — пароль (хранится в зашифрованном виде, не как текст!);
- `email` — почта;
- `first_name`, `last_name` — имя и фамилия.

Хранит пользователей Django в таблице `auth_user` (создаётся автоматически).

## Как создать пользователя

В терминале (например, для админа):

```
python manage.py createsuperuser
```

Это уже знакомо из урока 5 — так мы создавали суперпользователя.

## Вход: используем готовый View

Django даёт готовое представление `LoginView`. Подключим его в `urls.py`:

```python
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("vhod/", LoginView.as_view(template_name="registration/vhod.html"),
         name="vhod"),
]
```

В `settings.py` укажи, куда отправлять после входа:

```python
LOGIN_URL = "vhod"
LOGIN_REDIRECT_URL = "glavnaya"
```

Разберём:

- `LOGIN_URL` — адрес страницы входа (если нужно перенаправить
  неавторизованного пользователя).
- `LOGIN_REDIRECT_URL` — куда идти после успешного входа.

## Шаблон входа

`registration/vhod.html`:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Войти</button>
</form>
```

Форма входа — форма `AuthenticationForm`, которую Django создаёт
автоматически для `LoginView`. Нам её писать не нужно.

## Выход

Выход ещё проще — используем `LogoutView`:

```python
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("vyhod/", LogoutView.as_view(), name="vyhod"),
]
```

По умолчанию после выхода Django покажет служебную страницу, но можно
указать, куда перенаправлять:

```python
path("vyhod/", LogoutView.as_view(next_page="glavnaya"), name="vyhod"),
```

`next_page` — куда идти после выхода.

## Проверяем, вошёл ли пользователь

В шаблоне:

```html
{% if user.is_authenticated %}
    <p>Привет, {{ user.username }}!</p>
    <a href="{% url 'vyhod' %}">Выйти</a>
{% else %}
    <a href="{% url 'vhod' %}">Войти</a>
{% endif %}
```

- `user` всегда доступен в шаблоне, Django подставляет его сам.
- `is_authenticated` — свойство: True, если пользователь вошёл.

## Ограничение доступа (защита страниц)

Хочешь, чтобы страницу видели только вошедшие пользователи? Используй
декоратор `login_required`:

```python
from django.contrib.auth.decorators import login_required


@login_required
def sekretnaya_stranica(request):
    return render(request, "blog/sekret.html")
```

Если неавторизованный пользователь зайдёт на эту страницу, Django
перенаправит его на `LOGIN_URL`.

Для классов есть аналог — миксин `LoginRequiredMixin`.

## Регистрация

Готовой регистрации из коробки нет (вход и выход есть, а регистрацию
пишут сами). Простейший вариант:

```python
from django.contrib.auth.forms import UserCreationForm


def registraciya(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vhod")
    else:
        form = UserCreationForm()
    return render(request, "registration/registraciya.html", {"form": form})
```

`UserCreationForm` — готовая форма создания пользователя с проверкой
пароля на надёжность и совпадение двух полей.

## Хеширование паролей

Важно понимать: Django **никогда не хранит пароль в открытом виде**.
Он сохраняет **хеш** — необратимое «преобразование» пароля. При входе
Django проверяет, что введённый пароль даёт тот же хеш. Поэтому даже
если база утечёт, злоумышленник не узнает сами пароли.

## Словарик терминов

- **Аутентификация** — определение личности пользователя (вход).
- **Хеш** — необратимое преобразование пароля.
- **login_required** — декоратор, защищающий View.

## Задание к уроку

1. Создай страницу входа через `LoginView`.
2. Добавь выход через `LogoutView`.
3. В шаблоне-основе покажи приветствие, если пользователь вошёл.
4. Защити одну страницу декоратором `login_required`.
5. Посмотри демо `primery/demo_vhod.py` — принцип проверки пользователя.