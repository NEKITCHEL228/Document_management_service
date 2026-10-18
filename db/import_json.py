import json
import sqlite3
from pathlib import Path
from db.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"

CATEGORIES_FILE = DATA_DIR / "categories.json"
USERS_FILE = DATA_DIR / "users.json"
DOCUMENTS_FILE = DATA_DIR / "documents.json"
VERSIONS_FILE = DATA_DIR / "versions.json"


def load_json(filepath: Path):
    """Загрузить JSON-данные из файла."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def init_database(conn: sqlite3.Connection):
    """Применить DDL-схему к базе данных."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema_sql = file.read()
    conn.executescript(schema_sql)


def import_categories(conn: sqlite3.Connection):
    """Импортировать категории в таблицу categories."""
    categories = load_json(CATEGORIES_FILE)
    records = [
        (cat["id"], cat["name"], cat.get("description", ""))
        for cat in categories
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO categories (id, name, description)
        VALUES (?, ?, ?)
        """,
        records,
    )


def import_users(conn: sqlite3.Connection):
    """Импортировать пользователей в таблицу users."""
    users = load_json(USERS_FILE)
    records = [
        (user["id"], user["email"], user["password_hash"])
        for user in users
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO users (id, email, password_hash)
        VALUES (?, ?, ?)
        """,
        records,
    )


def import_documents(conn: sqlite3.Connection):
    """Импортировать документы и их связи с категориями."""
    documents = load_json(DOCUMENTS_FILE)
    doc_records = [
        (doc["id"], doc["title"], doc.get("content", ""))
        for doc in documents
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO documents (id, title, content)
        VALUES (?, ?, ?)
        """,
        doc_records,
    )

    doc_cat_records = []
    for doc in documents:
        for cat_id in doc.get("category_ids", []):
            doc_cat_records.append((doc["id"], cat_id))

    if doc_cat_records:
        conn.executemany(
            """
            INSERT OR IGNORE INTO document_categories (
                document_id, category_id
            )
            VALUES (?, ?)
            """,
            doc_cat_records,
        )


def import_versions(conn: sqlite3.Connection):
    """Импортировать редакции документов в таблицу versions."""
    versions = load_json(VERSIONS_FILE)
    records = [
        (
            ver["id"],
            ver["version_num"],
            float(ver["file_size_mb"]),
            ver["release_date"],
            int(bool(ver.get("is_signed", False))),
            ver["author_id"],
            ver["document_id"],
        )
        for ver in versions
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO versions (
            id, version_num, file_size_mb, release_date,
            is_signed, author_id, document_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        records,
    )


def run_import(db_path: str = None):
    """Запустить полный цикл миграции данных из JSON в SQLite."""
    conn = get_connection(db_path)
    try:
        init_database(conn)
        import_categories(conn)
        import_users(conn)
        import_documents(conn)
        import_versions(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_import()
    print("Импорт данных из JSON в SQLite успешно завершен.")
