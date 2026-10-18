import os
import sys
from pathlib import Path
import pytest
import django

# Добавляем каталог my_django_project в sys.path
DJANGO_DIR = Path(__file__).resolve().parent.parent / "my_django_project"
if str(DJANGO_DIR) not in sys.path:
    sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Document_management_service.settings"
)
django.setup()

from django.test import Client  # noqa: E402


@pytest.fixture
def client():
    """Тестовый HTTP-клиент Django."""
    return Client()
