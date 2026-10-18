from django.shortcuts import render
from db.database import get_connection


def category_list(request):
    """Отображает список всех тематических категорий документов из SQLite."""
    conn = get_connection(row_factory=True)
    categories = conn.execute("""
        SELECT
            c.id,
            c.name,
            c.description,
            COUNT(dc.document_id) AS documents_count
        FROM categories c
        LEFT JOIN document_categories dc ON c.id = dc.category_id
        GROUP BY c.id, c.name, c.description
        ORDER BY c.id ASC;
    """).fetchall()
    conn.close()

    context = {
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_detail(request, cat_id: int):
    """Детальная информация о выбранной категории и ее документах."""
    conn = get_connection(row_factory=True)
    row = conn.execute("""
        SELECT id, name, description
        FROM categories
        WHERE id = ?;
    """, (cat_id,)).fetchone()

    category = dict(row) if row is not None else None
    documents = []
    if category is not None:
        doc_rows = conn.execute("""
            SELECT d.id, d.title, d.content
            FROM documents d
            JOIN document_categories dc ON d.id = dc.document_id
            WHERE dc.category_id = ?
            ORDER BY d.title ASC;
        """, (cat_id,)).fetchall()
        documents = [dict(d) for d in doc_rows]
        category["documents"] = documents
    conn.close()

    context = {
        "category": category,
        "documents": documents,
    }
    return render(
        request,
        "categories/category_detail.html",
        context,
        status=404 if category is None else 200,
    )
