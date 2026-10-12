import os
from datetime import date
from models import Category, User, Document, Version
import storage


def test_storage_categories(tmp_path):
    cat_file = str(tmp_path / "categories.json")
    cats = [
        Category(id=1, name="Категория 1", description="Описание 1"),
        Category(id=2, name="Категория 2", description="Описание 2"),
    ]
    storage.save_categories(cats, filepath=cat_file)
    assert os.path.exists(cat_file)

    loaded = storage.load_categories(filepath=cat_file)
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].name == "Категория 1"
    assert loaded[1].id == 2


def test_storage_categories_nonexistent():
    res = storage.load_categories(filepath="nonexistent_categories.json")
    assert res == []


def test_storage_categories_corrupted(tmp_path):
    bad_file = tmp_path / "bad_categories.json"
    bad_file.write_text("{invalid json", encoding="utf-8")
    res = storage.load_categories(filepath=str(bad_file))
    assert res == []


def test_storage_users(tmp_path):
    user_file = str(tmp_path / "users.json")
    users = [
        User(id=1, email="test1@test.ru", password_hash="hash1"),
        User(id=2, email="test2@test.ru", password_hash="hash2"),
    ]
    storage.save_users(users, filepath=user_file)
    assert os.path.exists(user_file)

    loaded = storage.load_users(filepath=user_file)
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].email == "test1@test.ru"


def test_storage_users_nonexistent():
    res = storage.load_users(filepath="nonexistent_users.json")
    assert res == []


def test_storage_users_corrupted(tmp_path):
    bad_file = tmp_path / "bad_users.json"
    bad_file.write_text("{invalid json", encoding="utf-8")
    res = storage.load_users(filepath=str(bad_file))
    assert res == []


def test_storage_documents(tmp_path):
    doc_file = str(tmp_path / "documents.json")
    cat1 = Category(id=1, name="Отчеты", description="")
    docs = [
        Document(id=1, title="Отчет 2026", content="Текст", categories=[cat1]),
    ]
    storage.save_documents(docs, filepath=doc_file)
    assert os.path.exists(doc_file)

    loaded = storage.load_documents([cat1], filepath=doc_file)
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].title == "Отчет 2026"
    assert loaded[0].categories == [cat1]


def test_storage_documents_nonexistent():
    res = storage.load_documents([], filepath="nonexistent_docs.json")
    assert res == []


def test_storage_documents_corrupted(tmp_path):
    bad_file = tmp_path / "bad_docs.json"
    bad_file.write_text("{invalid json", encoding="utf-8")
    res = storage.load_documents([], filepath=str(bad_file))
    assert res == []


def test_storage_versions(tmp_path):
    ver_file = str(tmp_path / "versions.json")
    cat = Category(id=1, name="Кат", description="")
    doc = Document(id=10, title="Док", content="Контент", categories=[cat])
    user = User(id=5, email="user@test.ru", password_hash="h")
    vers = [
        Version(
            version_id=1,
            version_num="1.0",
            file_size_mb=1.5,
            release_date=date(2026, 1, 1),
            is_signed=True,
            author=user,
            document=doc,
        )
    ]
    storage.save_versions(vers, filepath=ver_file)
    assert os.path.exists(ver_file)

    loaded = storage.load_versions([doc], [user], filepath=ver_file)
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].version_num == "1.0"
    assert loaded[0].author == user
    assert loaded[0].document == doc


def test_storage_versions_nonexistent():
    res = storage.load_versions([], [], filepath="nonexistent_vers.json")
    assert res == []


def test_storage_versions_corrupted(tmp_path):
    bad_file = tmp_path / "bad_vers.json"
    bad_file.write_text("{invalid json", encoding="utf-8")
    res = storage.load_versions([], [], filepath=str(bad_file))
    assert res == []


def test_storage_load_data_from_all_files():
    cats, users, docs, vers = storage.load_data_from_all_files()
    assert isinstance(cats, list)
    assert isinstance(users, list)
    assert isinstance(docs, list)
    assert isinstance(vers, list)
