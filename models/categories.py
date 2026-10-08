from typing import List, Optional


class Category:
    """Класс, представляющий категорию документов."""

    def __init__(self, id: int, name: str, description: str) -> None:
        """
        Инициализация объекта категории.
        :param id: Уникальный идентификатор категории.
        :param name: Название категории.
        :param description: Краткое описание назначения категории.
        """
        self.id = id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """
        Строковое представление категории.
        Вызывается автоматически при print(category) или str(category).
        """
        return f"Категория #{self.id}: {self.name}"

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """
        Фабричный метод: создает экземпляр класса Category из словаря,
        полученного при чтении JSON-файла.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", "")
        )


def find_category_by_id(
    categories: List[Category],
    cat_id: int,
) -> Optional[Category]:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category.id == cat_id:
            return category
    return None