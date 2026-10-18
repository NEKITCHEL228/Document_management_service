from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="list"),
    path("<int:doc_id>/", views.document_detail, name="detail"),
    path("", views.document_list, name="document_list"),
    path("<int:doc_id>/", views.document_detail, name="document_detail"),
]
