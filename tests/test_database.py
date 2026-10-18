from pathlib import Path
from db.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent


def test_db_connection():
    """Проверка подключения к SQLite и проверки внешних ключей."""
    conn = get_connection()
    try:
        fk_status = conn.execute("PRAGMA foreign_keys;").fetchone()[0]
        assert fk_status == 1, "PRAGMA foreign_keys должна быть включена (1)"
    finally:
        conn.close()


def test_schema_and_tables_exist():
    """Проверка наличия всех реляционных таблиц в схеме DocFlow."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables = {row[0] for row in cursor.fetchall()}
        expected_tables = {
            "categories",
            "users",
            "documents",
            "document_categories",
            "versions",
        }
        assert expected_tables.issubset(tables)
    finally:
        conn.close()


def test_import_json_data():
    """Проверка корректности импорта данных из JSON в SQLite."""
    conn = get_connection()
    try:
        cat_count = conn.execute(
            "SELECT COUNT(*) FROM categories;"
        ).fetchone()[0]
        user_count = conn.execute("SELECT COUNT(*) FROM users;").fetchone()[0]
        doc_count = conn.execute(
            "SELECT COUNT(*) FROM documents;"
        ).fetchone()[0]
        ver_count = conn.execute(
            "SELECT COUNT(*) FROM versions;"
        ).fetchone()[0]
        dc_count = conn.execute(
            "SELECT COUNT(*) FROM document_categories;"
        ).fetchone()[0]

        assert cat_count >= 3
        assert user_count >= 2
        assert doc_count >= 3
        assert ver_count >= 3
        assert dc_count >= 3
    finally:
        conn.close()


def test_queries_file_execution():
    """Проверка выполнения всех SQL-запросов из sql/queries.sql."""
    queries_file = BASE_DIR / "sql" / "queries.sql"
    assert queries_file.exists(), "Файл sql/queries.sql должен существовать"

    with open(queries_file, "r", encoding="utf-8") as file:
        content = file.read()

    queries = [q.strip() for q in content.split(";") if q.strip()]
    msg = "Должно быть разработано не менее 10 SQL-запросов"
    assert len(queries) >= 10, msg

    conn = get_connection()
    try:
        for idx, query in enumerate(queries, 1):
            cursor = conn.execute(query)
            results = cursor.fetchall()
            err_msg = f"Запрос {idx} вернул некорректный результат"
            assert isinstance(results, list), err_msg
    finally:
        conn.close()


def test_web_routes_search_and_statistics(client):
    """Проверка маршрутов поиска и аналитической статистики."""
    res_search_empty = client.get("/documents/search/")
    assert res_search_empty.status_code == 200

    res_search_query = client.get("/documents/search/?q=договор")
    assert res_search_query.status_code == 200
    assert "Трудовой_договор" in res_search_query.content.decode("utf-8")

    res_stats = client.get("/documents/statistics/")
    assert res_stats.status_code == 200
    content = res_stats.content.decode("utf-8")
    assert "Статистика и аналитика" in content
    assert "Всего документов" in content
