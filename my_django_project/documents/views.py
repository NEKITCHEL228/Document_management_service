from django.shortcuts import render
from db.database import get_connection


def document_list(request):
    """Отображает список всех электронных документов из SQLite."""
    conn = get_connection(row_factory=True)
    doc_rows = conn.execute("""
        SELECT id, title, content
        FROM documents
        ORDER BY id ASC;
    """).fetchall()

    documents = []
    for row in doc_rows:
        doc_dict = dict(row)
        cat_rows = conn.execute("""
            SELECT c.id, c.name, c.description
            FROM categories c
            JOIN document_categories dc ON c.id = dc.category_id
            WHERE dc.document_id = ?
            ORDER BY c.name ASC;
        """, (row["id"],)).fetchall()
        doc_dict["categories"] = cat_rows
        documents.append(doc_dict)
    conn.close()

    context = {
        "documents": documents,
    }
    return render(request, "documents/document_list.html", context)


def document_detail(request, doc_id: int):
    """Отображает детальную карточку конкретного документа из SQLite."""
    conn = get_connection(row_factory=True)
    row = conn.execute("""
        SELECT id, title, content
        FROM documents
        WHERE id = ?;
    """, (doc_id,)).fetchone()

    if row is not None:
        doc_dict = dict(row)
        cat_rows = conn.execute("""
            SELECT c.id, c.name, c.description
            FROM categories c
            JOIN document_categories dc ON c.id = dc.category_id
            WHERE dc.document_id = ?
            ORDER BY c.name ASC;
        """, (doc_id,)).fetchall()
        doc_dict["categories"] = cat_rows
        document = doc_dict
    else:
        document = None
    conn.close()

    context = {
        "document": document,
    }
    return render(
        request,
        "documents/document_detail.html",
        context,
        status=404 if document is None else 200,
    )


def document_search(request):
    """Поиск документов по ключевому слову в названии/содержимом."""
    q = request.GET.get("q", "").strip()
    documents = []
    if q:
        conn = get_connection(row_factory=True)
        search_pattern = f"%{q}%"
        doc_rows = conn.execute("""
            SELECT id, title, content
            FROM documents
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id ASC;
        """, (search_pattern, search_pattern)).fetchall()

        for row in doc_rows:
            doc_dict = dict(row)
            cat_rows = conn.execute("""
                SELECT c.id, c.name, c.description
                FROM categories c
                JOIN document_categories dc ON c.id = dc.category_id
                WHERE dc.document_id = ?
                ORDER BY c.name ASC;
            """, (row["id"],)).fetchall()
            doc_dict["categories"] = cat_rows
            documents.append(doc_dict)
        conn.close()

    context = {
        "query": q,
        "documents": documents,
    }
    return render(request, "documents/document_search.html", context)


def statistics(request):
    """Страница аналитики и сводной статистики документооборота DocFlow."""
    conn = get_connection(row_factory=True)
    summary = conn.execute("""
        SELECT
            COUNT(*) AS total_versions,
            SUM(file_size_mb) AS total_size_mb,
            ROUND(AVG(file_size_mb), 2) AS avg_size_mb,
            MIN(file_size_mb) AS min_size_mb,
            MAX(file_size_mb) AS max_size_mb
        FROM versions;
    """).fetchone()

    total_docs = conn.execute("SELECT COUNT(*) FROM documents;").fetchone()[0]
    signed_count = conn.execute("""
        SELECT COUNT(*) FROM versions WHERE is_signed = 1;
    """).fetchone()[0]

    category_stats = conn.execute("""
        SELECT
            c.id,
            c.name,
            COUNT(dc.document_id) AS doc_count
        FROM categories c
        LEFT JOIN document_categories dc ON c.id = dc.category_id
        GROUP BY c.id, c.name
        ORDER BY doc_count DESC, c.name ASC;
    """).fetchall()

    multi_version_docs = conn.execute("""
        SELECT
            d.id,
            d.title,
            COUNT(v.id) AS version_count
        FROM documents d
        JOIN versions v ON d.id = v.document_id
        GROUP BY d.id, d.title
        HAVING COUNT(v.id) > 1
        ORDER BY version_count DESC;
    """).fetchall()
    conn.close()

    context = {
        "summary": summary,
        "total_docs": total_docs,
        "signed_count": signed_count,
        "category_stats": category_stats,
        "multi_version_docs": multi_version_docs,
    }
    return render(request, "documents/statistics.html", context)
