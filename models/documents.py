from typing import List
from .categories import Category


class Document:
    """
    Класс документа.
    Хранит информацию о документе и список привязанных к нему категорий.
    """

    def __init__(
        self,
        id: int,
        title: str,
        content: str,
        categories: List[Category] = None
    ) -> None:
        """
        Инициализация документа.
        categories принимает список живых объектов класса Category.
        """
        self.id = id
        self.title = title
        self.content = content
        # Используем список (List), так как он легко сохраняется в JSON
        self.categories: List[Category] = categories if categories is not None else []

    def add_category(self, category: Category) -> None:
        """Добавляет категорию к документу (с проверкой на дубликаты)."""
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category) -> None:
        """Удаляет категорию из документа, если она там есть."""
        if category in self.categories:
            self.categories.remove(category)

    def change_categories(self, new_categories: List[Category]) -> None:
        """Полностью заменяет текущий список категорий документа на новый."""
        self.categories = new_categories

    def __str__(self) -> str:
        """
        Строковое представление документа со списком названий привязанных категорий.
        """
        cat_names = ", ".join([c.name for c in self.categories]) if self.categories else "нет категорий"
        return f"Документ #{self.id} '{self.title}' (Категории: {cat_names})"

    @classmethod
    def from_data(cls, data: dict, all_categories: List[Category]) -> "Document":
        """
        Восстанавливает документ из JSON, связывая его по ID
        с реальными объектами Category из переданного списка all_categories.
        """
        cat_ids = data.get("category_ids", [])
        matched_categories = [c for c in all_categories if c.id in cat_ids]

        return cls(
            id=data["id"],
            title=data["title"],
            content=data.get("content", ""),
            categories=matched_categories
        )