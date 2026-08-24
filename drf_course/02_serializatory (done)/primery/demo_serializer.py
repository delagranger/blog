"""
Демонстрация принципа работы сериализатора на чистом Python
(без Django, чтобы понять суть).

Сериализатор — это «переводчик» между объектом и JSON.
"""

import json
from dataclasses import dataclass


# -------- 1. Модель (как она выглядит в Django) --------

@dataclass
class Post:
    """Упрощённая версия Django-модели Post."""
    id: int
    title: str
    body: str
    creation_date: str


# -------- 2. Сериализатор (вручную, для понимания) --------

class RuchnoySerializer:
    """
    Ручной сериализатор — чтобы показать, что делает DRF «под капотом».

    В реальном коде ты НЕ будешь писать это вручную — DRF делает это сам
    через ModelSerializer. Здесь это просто для понимания.
    """

    def __init__(self, instance=None, data=None, many=False):
        self.instance = instance
        self.data_input = data
        self.many = many
        self._errors = {}

    def to_dict(self, post):
        """Сериализация: объект → словарь (JSON)."""
        return {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "creation_date": post.creation_date,
        }

    @property
    def data(self):
        """Имитация serializer.data из DRF."""
        if self.many:
            return [self.to_dict(p) for p in self.instance]
        return self.to_dict(self.instance)

    def is_valid(self):
        """Валидация: проверка входящих данных."""
        self._errors = {}
        if not self.data_input:
            self._errors["non_field"] = "Нет данных"
            return False
        if not self.data_input.get("title"):
            self._errors["title"] = "Заголовок обязателен"
            return False
        if not self.data_input.get("body"):
            self._errors["body"] = "Текст обязателен"
            return False
        return True

    @property
    def errors(self):
        return self._errors


# -------- 3. Демонстрация --------

def demo_serializaciya():
    """Показываем, как объект превращается в JSON."""
    print("=" * 50)
    print("СЕРИАЛИЗАЦИЯ: объект → JSON")
    print("=" * 50)

    post = Post(
        id=1,
        title="Привет, мир!",
        body="Это мой первый пост в блоге.",
        creation_date="2025-01-15",
    )

    serializer = RuchnoySerializer(post)
    json_str = json.dumps(serializer.data, indent=4, ensure_ascii=False)

    print(f"Объект Python: {post}")
    print()
    print("Словарь (serializer.data):")
    print(serializer.data)
    print()
    print("JSON-строка (отправляется клиенту):")
    print(json_str)
    print()


def demo_deserializaciya():
    """Показываем, как JSON превращается в объект."""
    print("=" * 50)
    print("ДЕСЕРИАЛИЗАЦИЯ: JSON → объект")
    print("=" * 50)

    json_from_client = '{"title": "Новый пост", "body": "Текст нового поста"}'
    data = json.loads(json_from_client)

    serializer = RuchnoySerializer(data=data)

    if serializer.is_valid():
        print("✅ Данные корректны, можно сохранять в БД")
        print(f"   title: {data['title']}")
        print(f"   body: {data['body']}")
    else:
        print("❌ Ошибки валидации:")
        for field, error in serializer.errors.items():
            print(f"   {field}: {error}")


def demo_spisok():
    """Сериализация списка объектов (many=True)."""
    print("=" * 50)
    print("СЕРИАЛИЗАЦИЯ СПИСКА (many=True)")
    print("=" * 50)

    posts = [
        Post(1, "Первый", "Текст 1", "2025-01-15"),
        Post(2, "Второй", "Текст 2", "2025-01-16"),
        Post(3, "Третий", "Текст 3", "2025-01-17"),
    ]

    serializer = RuchnoySerializer(posts, many=True)
    json_str = json.dumps(serializer.data, indent=4, ensure_ascii=False)

    print(f"Список из {len(posts)} объектов → массив JSON:")
    print(json_str)


if __name__ == "__main__":
    demo_serializaciya()
    demo_deserializaciya()
    demo_spisok()

    print("Вывод:")
    print("  Сериализатор — это мост между объектами Python и JSON.")
    print("  DRF автоматизирует это через ModelSerializer.")
    print("  Ты описываешь поля в Meta — остальное делает DRF.")