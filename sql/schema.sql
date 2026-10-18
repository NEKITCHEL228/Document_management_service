-- ==========================================
-- DocFlow: структура реляционной базы данных
-- ==========================================

PRAGMA foreign_keys = ON;

-- Таблица тематических категорий документов
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- Таблица пользователей системы
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Таблица электронных документов
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT
);

-- Связующая таблица многие-ко-многим (документы <-> категории)
CREATE TABLE IF NOT EXISTS document_categories (
    document_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (document_id, category_id),
    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);

-- Таблица версий (редакций) документов
CREATE TABLE IF NOT EXISTS versions (
    id INTEGER PRIMARY KEY,
    version_num TEXT NOT NULL,
    file_size_mb REAL NOT NULL,
    release_date TEXT NOT NULL,
    is_signed INTEGER NOT NULL DEFAULT 0,
    author_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
);
