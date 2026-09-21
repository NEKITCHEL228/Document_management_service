from datetime import date
from models import User, Document, Version


def test_version_creation_and_relations():
    """Проверка композиции: связь Version с объектами User и Document."""
    user = User(id=1, email="author@test.ru", password_hash="hash")
    doc = Document(id=10, title="Регламент.docx", content="")

    version = Version(
        version_id=1,
        version_num="1.0",
        file_size_mb=2.4,
        release_date=date(2026, 9, 20),
        is_signed=False,
        author=user,
        document=doc
    )

    assert version.id == 1
    assert version.version_num == "1.0"
    assert version.document is doc  # Ссылка на объект Document
    assert version.author is user    # Ссылка на объект User
    assert version.is_signed is False


def test_version_sign_method():
    """Проверка метода изменения состояния (подписание версии ЭЦП)."""
    user = User(id=1, email="user@test.ru", password_hash="h")
    doc = Document(id=1, title="Договор", content="")
    version = Version(1, "1.0", 3.0, date.today(), False, user, doc)

    assert version.is_signed is False
    assert "Черновик" in str(version)

    # Вызываем метод объекта
    version.sign()

    assert version.is_signed is True
    assert "Подписан" in str(version)


def test_version_file_size_validation():
    """Проверка бизнес-правила допустимого размера файла."""
    user = User(id=1, email="user@test.ru", password_hash="h")
    doc = Document(id=1, title="Файл", content="")

    valid_version = Version(1, "1.0", 4.5, date.today(), True, user, doc)
    oversized_version = Version(2, "2.0", 25.0, date.today(), True, user, doc)

    assert valid_version.is_valid_size(max_size_mb=10.0) is True
    assert oversized_version.is_valid_size(max_size_mb=10.0) is False