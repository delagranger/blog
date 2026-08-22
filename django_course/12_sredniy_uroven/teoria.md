# Урок 12. Средний уровень: связи, пагинация, тесты

Здесь собраны темы, которые переводят тебя с базового уровня на средний.

## Связи между моделями (Foreign Key и ManyToMany)

В реальных проектах модели связаны друг с другом.

### ForeignKey — «многие к одному»

У поста есть автор. Один автор — много постов:

```python
from django.contrib.auth.models import User


class Post(models.Model):
    zagolovok = models.CharField(max_length=200)
    tekst = models.TextField()
    avtor = models.ForeignKey(User, on_delete=models.CASCADE)
```

- `ForeignKey` — связь «многие к одному».
- `on_delete=models.CASCADE` — если пользователя удалят, его посты
  тоже удалятся.

Обратиться к автору поста: `post.avtor`.
Обратиться ко всем постам автора: `user.post_set.all()`.

### ManyToManyField — «многие ко многим»

У поста несколько тегов, и тег относится к нескольким постам:

```python
class Teg(models.Model):
    nazvanie = models.CharField(max_length=50)


class Post(models.Model):
    zagolovok = models.CharField(max_length=200)
    tegi = models.ManyToManyField(Teg)
```

Получить все теги поста: `post.tegi.all()`.

## Пагинация (разбивка на страницы)

Когда записей много, их разбивают на страницы. Django делает это
встроенным классом `Paginator`:

```python
from django.core.paginator import Paginator


def spisok_postov(request):
    posty = Post.objects.all()
    paginator = Paginator(posty, 10)          # по 10 на страницу
    stranica = request.GET.get("stranica")
    posty_na_stranice = paginator.get_page(stranica)
    return render(request, "blog/spisok.html", {"posty": posty_na_stranice})
```

`GET.get("stranica")` — номер страницы из адреса (`?stranica=2`).

## Миксины

**Миксин** — это класс с готовой «добавкой» функциональности. Class-Based
Views собираются из миксинов, как из конструктора. Например, чтобы
пустить на страницу только авторизованных:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class MoiPostyView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/moi.html"
```

`LoginRequiredMixin` — миксин, который требует вход.

## Тесты

Django позволяет писать автоматические проверки кода — тесты.

```python
from django.test import TestCase
from .models import Post


class PostTest(TestCase):
    def test_sozdanie_posta(self):
        post = Post.objects.create(zagolovok="Тест", tekst="Текст")
        self.assertEqual(post.zagolovok, "Тест")
```

Запуск:

```
python manage.py test
```

Тест создаёт временную базу, проверяет код и удаляет базу.

## Настройки для продакшена

При разработке полезен `DEBUG = True`. Для реального сайта его
отключают и включают:

- `ALLOWED_HOSTS` — список разрешённых доменов;
- `STATIC_ROOT` — куда собирать статику (`collectstatic`);
- подключение к настоящей базе (PostgreSQL).

## Словарик терминов

- **ForeignKey** — связь «многие к одному».
- **ManyToMany** — связь «многие ко многим».
- **Пагинация** — разбивка на страницы.
- **Миксин** — готовый «кирпичик» функциональности для классов.
- **TestCase** — класс для написания тестов.

## Задание к уроку

1. Добавь модель `Teg` и свяжи её с `Post` через ManyToMany.
2. Выведи теги поста в шаблоне.
3. Сделай пагинацию списка постов (по 5 на страницу).
4. Напиши один простой тест на создание поста.
5. Посмотри демо `primery/demo_itog.py` — итоговая картина курса.

## Что дальше?

- Изучи **Django REST Framework** (создание API).
- Разберись с **развёртыванием** (деплой на сервер).
- Практикуйся: сделай полноценный блог или магазин.