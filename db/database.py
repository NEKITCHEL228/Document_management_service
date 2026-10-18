import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "data" / "docflow.sqlite")


def get_connection(
    db_path: Optional[str] = None,
    row_factory: bool = False
) -> sqlite3.Connection:
    """
    Создает и возвращает подключение к базе данных SQLite.
    Включает проверку внешних ключей PRAGMA foreign_keys = ON.
    """
    path = db_path if db_path is not None else DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    if row_factory:
        conn.row_factory = sqlite3.Row
    return conn
