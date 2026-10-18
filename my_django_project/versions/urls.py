from django.urls import path
from . import views

app_name = "versions"

urlpatterns = [
    path("", views.version_list, name="list"),
    path("<int:ver_id>/", views.version_detail, name="detail"),
]
