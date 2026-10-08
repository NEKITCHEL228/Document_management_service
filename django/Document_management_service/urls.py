"""
URL configuration for Document_management_service project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('documents/', include('documents.urls')),
    path('categories/', include('categories.urls')),
    path('versions/', include('versions.urls')),
]

handler404 = 'homepage.views.page_not_found'
