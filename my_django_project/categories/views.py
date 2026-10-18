from django.shortcuts import render
from models.categories import find_category_by_id
from storage import load_categories


def category_list(request):
    """Отображает список всех тематических категорий документов."""
    categories = load_categories()
    context = {
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_detail(request, cat_id: int):
    """Отображает детальную информацию о выбранной категории."""
    categories = load_categories()
    category = find_category_by_id(categories, cat_id)

    context = {
        "category": category,
    }
    return render(
        request,
        "categories/category_detail.html",
        context,
        status=404 if category is None else 200,
    )
