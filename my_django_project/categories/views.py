from django.shortcuts import render
from models.categories import find_category_by_id
from storage import load_categories


def category_list(request):
    """Отображает список всех тематических категорий документов."""
    categories = load_categories()
    context = {"categories": categories}
    return render(request, "categories/category_list.html", context)


def category_detail(request, cat_id: int):
    """Отображает детальную информацию о выбранной категории."""
    categories = load_categories()
    category = find_category_by_id(categories, cat_id)

    if category is None:
        context = {
            "message": "Категория с указанным ID не найдена.",
            "back_url": "/categories/",
            "back_label": "← к списку категорий",
        }
        return render(request, "homepage/404.html", context, status=404)

    context = {"category": category}
    return render(request, "categories/category_detail.html", context)
