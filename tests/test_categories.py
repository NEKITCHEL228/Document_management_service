from models import Category


def test_category_creation():
    """Проверка корректности создания объекта Category и установки атрибутов."""
    category = Category(id=1, name="Договоры", description="Договорная документация")

    assert category.id == 1
    assert category.name == "Договоры"
    assert category.description == "Договорная документация"


def test_category_str():
    """Проверка строкового представления категории (__str__)."""
    category = Category(id=2, name="Приказы", description="Кадровые приказы")

    expected_str = "Категория #2: Приказы"
    assert str(category) == expected_str


def test_category_from_data():
    """Проверка создания категории через фабричный метод from_data (из словаря JSON)."""
    raw_data = {
        "id": 10,
        "name": "Бухгалтерия",
        "description": "Счета и акты"
    }
    category = Category.from_data(raw_data)

    assert category.id == 10
    assert category.name == "Бухгалтерия"
    assert category.description == "Счета и акты"