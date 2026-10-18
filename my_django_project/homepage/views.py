from django.shortcuts import render


def index(request):
    """Главная страница сервиса DocFlow."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception=None):
    """Обработчик ошибки 404 с единым стилизованным шаблоном."""
    return render(request, "homepage/404.html", status=404)
