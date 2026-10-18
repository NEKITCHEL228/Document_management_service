from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path("", views.category_list, name="list"),
    path("<int:cat_id>/", views.category_detail, name="detail"),
    path("", views.category_list, name="category_list"),
    path("<int:cat_id>/", views.category_detail, name="category_detail"),
]
