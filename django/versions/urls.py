from django.urls import path
from . import views

urlpatterns = [
    path("", views.version_list, name="version_list"),
    path("<int:ver_id>/", views.version_detail, name="version_detail"),
]
