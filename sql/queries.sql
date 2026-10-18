-- ====================================================================
-- DocFlow: Набор SQL-запросов предметной области (Практическая работа № 7)
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. Выборка списков и базовая сортировка (SELECT, ORDER BY)
-- --------------------------------------------------------------------

-- Запрос 1: Получение списка всех документов с сортировкой по названию
SELECT
    id,
    title,
    content
FROM documents
ORDER BY title ASC;

-- Запрос 2: Получение списка всех категорий с сортировкой по названию
SELECT
    id,
    name,
    description
FROM categories
ORDER BY name ASC;


-- --------------------------------------------------------------------
-- 2. Фильтрация данных (WHERE)
-- --------------------------------------------------------------------

-- Запрос 3: Поиск документов по ключевому слову в названии или содержании
SELECT
    id,
    title,
    content
FROM documents
WHERE title LIKE '%договор%' OR content LIKE '%договор%'
ORDER BY id ASC;

-- Запрос 4: Получение списка только утвержденных версий, подписанных ЭЦП
SELECT
    id,
    version_num,
    file_size_mb,
    release_date,
    document_id,
    author_id
FROM versions
WHERE is_signed = 1
ORDER BY release_date DESC;

-- Запрос 5: Фильтрация версий документов по ограничению размера файла (до 3.0 МБ)
SELECT
    id,
    version_num,
    file_size_mb,
    document_id
FROM versions
WHERE file_size_mb <= 3.0
ORDER BY file_size_mb ASC;


-- --------------------------------------------------------------------
-- 3. Соединение связанных таблиц (JOIN)
-- --------------------------------------------------------------------

-- Запрос 6: Документы со связанными категориями (связь многие-ко-многим)
SELECT
    d.id AS document_id,
    d.title AS document_title,
    c.id AS category_id,
    c.name AS category_name
FROM documents d
JOIN document_categories dc ON d.id = dc.document_id
JOIN categories c ON dc.category_id = c.id
ORDER BY d.id, c.name;

-- Запрос 7: Полная информация о версиях документов с автором и названием документа
SELECT
    v.id AS version_id,
    v.version_num,
    v.file_size_mb,
    v.release_date,
    v.is_signed,
    u.email AS author_email,
    d.id AS document_id,
    d.title AS document_title
FROM versions v
JOIN users u ON v.author_id = u.id
JOIN documents d ON v.document_id = d.id
ORDER BY v.release_date DESC;


-- --------------------------------------------------------------------
-- 4. Подзапросы (NOT IN / подзапрос)
-- --------------------------------------------------------------------

-- Запрос 8: Документы, не имеющие неподписанных черновых версий
SELECT
    d.id,
    d.title
FROM documents d
WHERE d.id NOT IN (
    SELECT v.document_id
    FROM versions v
    WHERE v.is_signed = 0
)
ORDER BY d.title;


-- --------------------------------------------------------------------
-- 5. Агрегатные функции (COUNT, SUM, AVG, MIN, MAX)
-- --------------------------------------------------------------------

-- Запрос 9: Сводная статистика файлов версий хранилища
SELECT
    COUNT(*) AS total_versions,
    SUM(file_size_mb) AS total_size_mb,
    ROUND(AVG(file_size_mb), 2) AS avg_size_mb,
    MIN(file_size_mb) AS min_size_mb,
    MAX(file_size_mb) AS max_size_mb
FROM versions;

-- Запрос 10: Подсчёт количества версий, утверждённых электронной цифровой подписью
SELECT
    COUNT(*) AS signed_versions_count
FROM versions
WHERE is_signed = 1;


-- --------------------------------------------------------------------
-- 6. Группировка (GROUP BY) и фильтрация групп (HAVING)
-- --------------------------------------------------------------------

-- Запрос 11: Количество документов по каждой категории (включая категории без документов)
SELECT
    c.id AS category_id,
    c.name AS category_name,
    COUNT(dc.document_id) AS documents_count
FROM categories c
LEFT JOIN document_categories dc ON c.id = dc.category_id
GROUP BY c.id, c.name
ORDER BY documents_count DESC, c.name ASC;

-- Запрос 12: Документы, имеющие более одной редакции в журнале версий
SELECT
    d.id AS document_id,
    d.title AS document_title,
    COUNT(v.id) AS versions_count
FROM documents d
JOIN versions v ON d.id = v.document_id
GROUP BY d.id, d.title
HAVING COUNT(v.id) > 1
ORDER BY versions_count DESC;
