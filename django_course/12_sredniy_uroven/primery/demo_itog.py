"""
Урок 12. Пример: итоговая картина курса Django.

Этот скрипт подводит итог: показывает, как связаны основные части
Django — модель, представление, шаблон и маршрут. В реальном Django
это отдельные файлы, но здесь мы собрали их в одном месте, чтобы
увидеть общий поток запроса:

  браузер → urls (маршрут) → view (обработчик) → model (данные)
                                                → template (HTML-ответ)

Как запустить:
    > python demo_itog.py
"""


# --- 1. Модель (аналог models.py) ------------------------------------------
class Post:
    """Пост блога — как модель Django."""

    obekty = []  # аналог Post.objects (менеджер)

    def __init__(self, pk: int, zagolovok: str, tekst: str):
        self.pk = pk
        self.zagolovok = zagolovok
        self.tekst = tekst

    @classmethod
    def sozdat(cls, zagolovok, tekst):
        post = cls(len(cls.obekty) + 1, zagolovok, tekst)
        cls.obekty.append(post)
        return post

    @classmethod
    def vse(cls):
        return list(cls.obekty)


# --- 2. Представление (аналог views.py) ------------------------------------
def glavnaya(request):
    """View: берёт данные из модели и готовит контекст для шаблона."""
    posty = Post.vse()
    kontekst = {"posty": posty}
    return shablon_otvet("glavnaya.html", kontekst)


# --- 3. Шаблон (упрощённый аналог template) --------------------------------
def shablon_otvet(imya_shablona: str, kontekst: dict) -> str:
    """Имитация рендера шаблона: подставляет данные из контекста."""
    if imya_shablona == "glavnaya.html":
        stroki = []
        for post in kontekst["posty"]:
            stroki.append(f"   <h2>{post.zagolovok}</h2><p>{post.tekst}</p>")
        return "\n".join(stroki) or "   (постов пока нет)"
    return ""


# --- 4. Маршруты (упрощённый аналог urls.py) -------------------------------
MARSHUTY = {
    "/": glavnaya,  # path("", glavnaya, name="glavnaya")
}


def obrabotat_zapros(url: str):
    """Имитация диспетчера URL: находит view по адресу и вызывает его."""
    view = MARSHUTY.get(url)
    if view is None:
        return "Ошибка 404: страница не найдена"
    return view(request=f"Запрос по адресу {url}")


if __name__ == "__main__":
    print("=" * 55)
    print("ДЕМО: итоговая картина Django (сквозной поток запроса)")
    print("=" * 55)

    # Наполняем «базу» через модель
    Post.sozdat("Первый пост", "Привет, мир!")
    Post.sozdat("Изучаем Django", "Это итоговый обзор.")
    Post.sozdat("Планы", "Дальше — практика и REST.")

    print("\nЗапрос браузера: GET /")
    print("-" * 55)
    otvet = obrabotat_zapros("/")
    print(otvet)

    print("\n" + "=" * 55)
    print("Поток запроса в Django:")
    print("  urls.py (маршрут) -> views.py (обработчик)")
    print("  -> models.py (данные) -> templates (HTML-ответ)")
    print("=" * 55)