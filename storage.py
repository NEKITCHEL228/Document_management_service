import json
import os
from datetime import date
from typing import List, Optional
from models import Category, User, Document, Version

# Пути к файлам данных по умолчанию
DATA_DIR = "data"
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
VERSIONS_FILE = os.path.join(DATA_DIR, "versions.json")

# Категории

def load_categories(filepath: str = CATEGORIES_FILE) -> List[Category]:
    """Загружает категории из JSON-файла и возвращает список объектов Category."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return [Category.from_data(item) for item in raw_data]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка при чтении категорий: {e}")
        return []


def save_categories(categories: List[Category], filepath: str = CATEGORIES_FILE) -> None:
    """Преобразует объекты Category в словари и сохраняет их в JSON."""
    data = [
        {"id": c.id, "name": c.name, "description": c.description}
        for c in categories
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Пользователи

def load_users(filepath: str = USERS_FILE) -> List[User]:
    """Загружает пользователей из JSON и возвращает список объектов User."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return [User.from_data(item) for item in raw_data]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка при чтении пользователей: {e}")
        return []


def save_users(users: List[User], filepath: str = USERS_FILE) -> None:
    """Преобразует объекты User в словари и сохраняет в JSON."""
    data = [
        {"id": u.id, "email": u.email, "password_hash": u.password_hash}
        for u in users
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Документы

def load_documents(
    all_categories: List[Category],
    filepath: str = DOCUMENTS_FILE
) -> List[Document]:
    """
    Загружает документы и связывает каждый документ
    с объектами Category из списка all_categories.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return [Document.from_data(item, all_categories) for item in raw_data]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка при чтении документов: {e}")
        return []


def save_documents(documents: List[Document], filepath: str = DOCUMENTS_FILE) -> None:
    """Сохраняет документы, превращая ссылки на Category обратно в category_ids."""
    data = [
        {
            "id": d.id,
            "title": d.title,
            "content": d.content,
            "category_ids": [c.id for c in d.categories]
        }
        for d in documents
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Версии

def load_versions(
    all_documents: List[Document],
    all_users: List[User],
    filepath: str = VERSIONS_FILE
) -> List[Version]:
    """
    Загружает версии и связывает их с соответствующими
    объектами Document и User по их ID.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        versions: List[Version] = []
        for item in raw_data:
            # Находим живой объект Document
            doc = next((d for d in all_documents if d.id == item["document_id"]), None)
            # Находим живой объект User (автора)
            user = next((u for u in all_users if u.id == item["author_id"]), None)

            # Если связанные объекты найдены — создаем Version
            if doc and user:
                versions.append(
                    Version(
                        version_id=item["id"],
                        version_num=item["version_num"],
                        file_size_mb=float(item["file_size_mb"]),
                        release_date=date.fromisoformat(item["release_date"]),
                        is_signed=item["is_signed"],
                        author=user,
                        document=doc
                    )
                )
        return versions
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка при чтении версий: {e}")
        return []


def save_versions(versions: List[Version], filepath: str = VERSIONS_FILE) -> None:
    """Сохраняет версии, заменяя объекты author и document на их ID."""
    data = [
        {
            "id": v.id,
            "version_num": v.version_num,
            "file_size_mb": v.file_size_mb,
            "release_date": v.release_date.isoformat(),
            "is_signed": v.is_signed,
            "author_id": v.author.id,
            "document_id": v.document.id
        }
        for v in versions
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data_from_all_files() -> tuple:
    """
    Загружает все данные из JSON-файлов и возвращает кортеж:
    (список категорий, список пользователей, список документов, список версий).
    """
    categories = load_categories()
    users = load_users()
    documents = load_documents(categories)
    versions = load_versions(documents, users)
    return categories, users, documents, versions