"""Пакет для управления базой данных SQLite."""
from .database import get_connection, DB_PATH

__all__ = ["get_connection", "DB_PATH"]
