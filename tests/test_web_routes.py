import os
import sys
from pathlib import Path
from datetime import date
import pytest

# Добавляем каталог django в sys.path для импорта Document_management_service
DJANGO_DIR = Path(__file__).resolve().parent.parent / "django"
if str(DJANGO_DIR) not in sys.path:
    sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Document_management_service.settings"
)
import django  # noqa: E402
django.setup()

from django.test import Client  # noqa: E402
from models import (  # noqa: E402
    find_category_by_id,
    find_document_by_id,
    find_version_by_id,
    Category,
    Document,
    Version,
    User
)


@pytest.fixture
def client():
    return Client()


def test_homepage_status(client):
    """Проверка доступности главной страницы."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DocFlow" in response.content.decode("utf-8")


def test_documents_routes(client):
    """Проверка списка документов и детальной страницы."""
    res_list = client.get("/documents/")
    assert res_list.status_code == 200

    res_detail = client.get("/documents/1/")
    assert res_detail.status_code == 200

    res_404 = client.get("/documents/99999/")
    assert res_404.status_code == 404


def test_categories_routes(client):
    """Проверка списка категорий и детальной страницы."""
    res_list = client.get("/categories/")
    assert res_list.status_code == 200

    res_detail = client.get("/categories/1/")
    assert res_detail.status_code == 200

    res_404 = client.get("/categories/99999/")
    assert res_404.status_code == 404


def test_versions_routes(client):
    """Проверка списка версий и детальной страницы."""
    res_list = client.get("/versions/")
    assert res_list.status_code == 200

    res_detail = client.get("/versions/1/")
    assert res_detail.status_code == 200

    res_404 = client.get("/versions/99999/")
    assert res_404.status_code == 404


def test_general_404_handler(client):
    """Проверка кастомного обработчика неизвестных URL."""
    res = client.get("/nonexistent_endpoint_for_test/")
    assert res.status_code == 404


def test_find_by_id_helpers():
    """Тестирование функций поиска по идентификаторам."""
    cat = Category(id=1, name="Test", description="Desc")
    assert find_category_by_id([cat], 1) == cat
    assert find_category_by_id([cat], 2) is None

    doc = Document(id=5, title="Doc", content="Txt")
    assert find_document_by_id([doc], 5) == doc
    assert find_document_by_id([doc], 6) is None

    user = User(id=1, email="test@mail.ru", password_hash="123")
    ver = Version(
        version_id=7,
        version_num="1.0",
        file_size_mb=2.0,
        release_date=date.today(),
        is_signed=True,
        author=user,
        document=doc,
    )
    assert find_version_by_id([ver], 7) == ver
    assert find_version_by_id([ver], 8) is None
