from django.shortcuts import render
from django.template.loader import render_to_string


def page(title: str, content: str) -> str:
    """
    Вспомогательная функция-каркас HTML из требований методички ПР5.
    Использует единый макет base.html.
    """
    return render_to_string("base.html", {"title": title, "content": content})


def index(request):
    """Главная страница сервиса DocFlow."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception=None):
    """Обработчик ошибки 404 с единым стилизованным шаблоном."""
    return render(request, "homepage/404.html", status=404)
