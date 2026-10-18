from datetime import datetime
from django.shortcuts import render
from db.database import get_connection


def version_list(request):
    """Отображает журнал версий электронных документов из SQLite с JOIN."""
    conn = get_connection(row_factory=True)
    rows = conn.execute("""
        SELECT
            v.id,
            v.version_num,
            v.file_size_mb,
            v.release_date,
            v.is_signed,
            v.document_id,
            d.title AS document_title,
            u.email AS author_email
        FROM versions v
        JOIN documents d ON v.document_id = d.id
        JOIN users u ON v.author_id = u.id
        ORDER BY v.release_date DESC;
    """).fetchall()
    conn.close()

    version_items = []
    for row in rows:
        try:
            rel_date = datetime.strptime(
                row["release_date"], "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            rel_date = row["release_date"]

        version_items.append({
            "id": row["id"],
            "version_num": row["version_num"],
            "file_size_mb": row["file_size_mb"],
            "release_date": rel_date,
            "is_signed": bool(row["is_signed"]),
            "author": {"email": row["author_email"]},
            "document": {
                "id": row["document_id"],
                "title": row["document_title"]
            },
            "is_valid_size": row["file_size_mb"] <= 10.0,
        })

    context = {
        "versions": version_items,
    }
    return render(request, "versions/version_list.html", context)


def version_detail(request, ver_id: int):
    """Отображает детальную карточку редакции документа из SQLite."""
    conn = get_connection(row_factory=True)
    row = conn.execute("""
        SELECT
            v.id,
            v.version_num,
            v.file_size_mb,
            v.release_date,
            v.is_signed,
            v.document_id,
            d.title AS document_title,
            u.email AS author_email
        FROM versions v
        JOIN documents d ON v.document_id = d.id
        JOIN users u ON v.author_id = u.id
        WHERE v.id = ?;
    """, (ver_id,)).fetchone()
    conn.close()

    if row is not None:
        try:
            rel_date = datetime.strptime(
                row["release_date"], "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            rel_date = row["release_date"]

        version = {
            "id": row["id"],
            "version_num": row["version_num"],
            "file_size_mb": row["file_size_mb"],
            "release_date": rel_date,
            "is_signed": bool(row["is_signed"]),
            "author": {"email": row["author_email"]},
            "document": {
                "id": row["document_id"],
                "title": row["document_title"]
            },
            "is_valid_size": row["file_size_mb"] <= 10.0,
        }
    else:
        version = None

    context = {
        "version": version,
    }
    return render(
        request,
        "versions/version_detail.html",
        context,
        status=404 if version is None else 200,
    )
