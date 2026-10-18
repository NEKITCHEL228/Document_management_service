from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="list"),
    path("search/", views.document_search, name="search"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:doc_id>/", views.document_detail, name="detail"),
]
