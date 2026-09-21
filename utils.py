from datetime import date

def get_next_id(items: list) -> int:
    """Генерирует следующий порядковый ID (1, 2, 3...)."""
    if not items:
        return 1
    return max(item.id for item in items) + 1

def input_int(prompt: str) -> int:
    """Проверка ввода целого числа."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")

def input_float(prompt: str) -> float:
    """Проверка ввода числа с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число (например, 3.14).")

def input_date(prompt: str) -> "date":
    """Проверка ввода даты в формате ДД.ММ.ГГГГ."""
    from datetime import datetime
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")
