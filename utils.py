def get_next_id(items: list) -> int:
    """Генерирует следующий порядковый ID (1, 2, 3...)."""
    if not items:
        return 1
    return max(item.id for item in items) + 1