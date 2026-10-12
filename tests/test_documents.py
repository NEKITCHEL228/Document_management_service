from models import Document, Category


def test_document_creation_empty_categories():
    """Проверка создания документа без указания категорий."""
    doc = Document(id=1, title="Устав.pdf", content="Текст устава компании")

    assert doc.id == 1
    assert doc.title == "Устав.pdf"
    assert doc.content == "Текст устава компании"
    assert doc.categories == []


def test_document_add_and_remove_category():
    """Проверка добавления и удаления категорий документа."""
    cat1 = Category(id=1, name="Юриспруденция", description="")
    cat2 = Category(id=2, name="Архив", description="")
    doc = Document(id=1, title="Договор.pdf", content="", categories=[cat1])

    # Добавление категории
    doc.add_category(cat2)
    assert len(doc.categories) == 2
    assert cat2 in doc.categories

    # Защита от дубликатов
    doc.add_category(cat2)
    assert len(doc.categories) == 2

    # Удаление категории
    doc.remove_category(cat1)
    assert len(doc.categories) == 1
    assert cat1 not in doc.categories


def test_document_from_data_linking():
    """Проверка связывания документа с объектами категорий при чтении из JSON."""
    cat_hr = Category(id=1, name="Кадры", description="")
    cat_legal = Category(id=2, name="Юристы", description="")
    all_categories = [cat_hr, cat_legal]

    raw_data = {
        "id": 1,
        "title": "Приказ о приеме",
        "content": "Содержание",
        "category_ids": [1]
    }

    doc = Document.from_data(raw_data, all_categories)
    assert len(doc.categories) == 1
    assert doc.categories[0] is cat_hr


def test_document_change_categories_and_str():
    """Проверка смены категорий и строкового представления документа."""
    cat1 = Category(id=1, name="Бухгалтерия", description="")
    doc = Document(id=10, title="Накладная.pdf", content="", categories=[cat1])

    assert "Бухгалтерия" in str(doc)

    cat2 = Category(id=2, name="Архив", description="")
    doc.change_categories([cat2])
    assert doc.categories == [cat2]
    assert "Архив" in str(doc)

    doc_empty = Document(id=11, title="Пустой.txt", content="")
    assert "нет категорий" in str(doc_empty)