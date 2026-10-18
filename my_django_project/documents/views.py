from django.shortcuts import render
from models.documents import find_document_by_id
from storage import load_categories, load_documents


def document_list(request):
    """Отображает список всех электронных документов."""
    categories = load_categories()
    documents = load_documents(categories)
    context = {
        "documents": documents,
    }
    return render(request, "documents/document_list.html", context)


def document_detail(request, doc_id: int):
    """Отображает детальную карточку конкретного документа."""
    categories = load_categories()
    documents = load_documents(categories)
    document = find_document_by_id(documents, doc_id)

    context = {
        "document": document,
    }
    return render(
        request,
        "documents/document_detail.html",
        context,
        status=404 if document is None else 200,
    )
