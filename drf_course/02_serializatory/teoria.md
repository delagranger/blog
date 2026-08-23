# Урок 2. Сериализаторы: превращаем модели в JSON

## Что такое сериализатор?

**Сериализатор (Serializer)** в DRF — это «переводчик» между моделями Django
и форматом JSON.

```
Модель Django (Python-объект)
        ↕  сериализатор
JSON (текст для передачи по сети)
```

У него две основные задачи:

1. **Сериализация** — превратить Python-объект (или QuerySet) в JSON
   (понятный словарь/список для отправки клиенту).

2. **Десериализация** — принять JSON от клиента, проверить его и превратить
   обратно в Python-объект для сохранения в БД.

Проще говоря: сериализатор решает, КАКИЕ поля модели показывать в API
и в КАКОМ формате.

## ModelSerializer — самый удобный вариант

Есть два вида сериализаторов в DRF:

- `serializers.Serializer` — ты вручную описываешь каждое поле
  (как `forms.Form`)
- `serializers.ModelSerializer` — автоматически строит поля по модели
  (как `forms.ModelForm`)

Для нашего блога будем использовать `ModelSerializer`. Создай файл
`blog/serializers.py`:

```python
from rest_framework import serializers
from blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date"]
```

Разберём построчно:

- `class PostSerializer(serializers.ModelSerializer)` — наследуемся
  от встроенного `ModelSerializer`. Наследование — это «взять готовое
  и добавить своё».
- Внутренний класс `Meta` — настройки сериализатора (какой модели,
  какие поля).
- `model = Post` — на основе какой модели.
- `fields = [...]` — какие поля включить в JSON. Можно указать
  `fields = "__all__"` для всех полей сразу.

## Проверяем работу сериализатора

Самый простой способ — интерактивная консоль Django. Запусти `python
manage.py shell` и попробуй:

```python
from blog.models import Post
from blog.serializers import PostSerializer

# Возьмём первый пост из базы
post = Post.objects.first()

# Создадим сериализатор и «пропустим» через него пост
serializer = PostSerializer(post)

# Результат — обычный словарь Python
print(serializer.data)
# Вывод: {'id': 1, 'title': 'Первый пост', 'body': 'Текст...', 'creation_date': '...'}

# Сериализатор умеет работать и со списком (many=True)
posts = Post.objects.all()
serializer = PostSerializer(posts, many=True)
print(serializer.data)
# Вывод: [{'id': 1, ...}, {'id': 2, ...}]
```

`serializer.data` — это уже знакомый Python-словарь, который DRF потом
превратит в JSON-строку при отправке ответа.

## Десериализация: из JSON в объект

Обратный процесс: клиент прислал данные, нужно сохранить в базу:

```python
# Данные от клиента (в реальности придут через HTTP)
data = {"title": "Новый пост", "body": "Текст нового поста"}

serializer = PostSerializer(data=data)

if serializer.is_valid():       # проверяем корректность данных
    post = serializer.save()    # сохраняем в базу (аналог Post.objects.create)
    print(f"Создан пост: {post.id}, {post.title}")
else:
    print(serializer.errors)    # ошибки валидации
```

Обрати внимание на сходство с формами Django:
- `serializer = PostSerializer(data=data)` — как `Form(request.POST)`
- `serializer.is_valid()` — как `form.is_valid()`
- `serializer.save()` — как `form.save()`

Это не случайно: DRF спроектирован так, чтобы разработчик, знакомый с
формами Django, сразу понимал сериализаторы.

## Настройка полей: что показывать и как

Сериализатор — не просто копия модели. Ты можешь:

```python
class PostSerializer(serializers.ModelSerializer):
    # Добавить вычисляемое поле (которого нет в модели)
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date", "word_count"]
        # Поля только для чтения (клиент не может их менять)
        read_only_fields = ["id", "creation_date", "word_count"]

    def get_word_count(self, obj):
        """Метод для вычисляемого поля. obj — экземпляр Post."""
        return len(obj.body.split())
```

- `read_only_fields` — клиент получит эти поля, но не сможет изменить
- `SerializerMethodField` — поле, которое вычисляется на лету
- `get_<имя_поля>(self, obj)` — метод-вычислитель для MethodField

## Валидация на уровне сериализатора

Можно добавить свои проверки данных:

```python
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date"]

    def validate_title(self, value):
        """Проверка конкретного поля. Вызывается автоматически."""
        if len(value) < 5:
            raise serializers.ValidationError(
                "Заголовок должен быть не короче 5 символов"
            )
        return value

    def validate(self, data):
        """Общая проверка всех полей."""
        if data.get("title") and data.get("body"):
            if data["title"].lower() == data["body"][:len(data["title"])].lower():
                raise serializers.ValidationError(
                    "Заголовок не должен совпадать с началом текста"
                )
        return data
```

Метод `validate_<имя_поля>` проверяет конкретное поле, а `validate` —
все поля вместе (как `clean` в формах Django).

## Словарик терминов

- **Сериализация** — превращение Python-объекта в словарь/JSON
- **Десериализация** — обратный процесс: JSON → Python-объект → запись в БД
- **ModelSerializer** — сериализатор, построенный по модели Django
- **SerializerMethodField** — поле, значение которого вычисляется функцией
- **Валидация** — проверка корректности входящих данных

## Задание к уроку

1. Установи DRF: `pip install djangorestframework`.
2. Создай файл `blog/serializers.py`.
3. Опиши в нём `PostSerializer` с полями `id`, `title`, `body`, `creation_date`.
4. В `python manage.py shell` создай пару постов и проверь работу
   сериализатора (serializer.data).
5. Добавь поле `word_count`, которое считает количество слов в теле поста.
6. Запусти `primery/demo_serializer.py` — упрощённая демонстрация
   сериализации без Django.