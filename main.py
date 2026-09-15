from datetime import date


# 1. Функция: Создание и регистрация нового документа
def create_document(title: str, author: str) -> bool:
    """Проверяет корректность данных при создании нового документа."""
    if len(title.strip()) == 0 or len(author.strip()) == 0:
        return False
    return True


# 2. Функция: Классификация документов по категориям
def classify_document(category_code: int) -> str:
    """Определяет категорию документа по числовому коду."""
    if category_code == 1:
        return "Договорная документация"
    elif category_code == 2:
        return "Кадровые приказы"
    elif category_code == 3:
        return "Финансовые отчеты"
    else:
        return "Общая корреспонденция"


# 3. Функция: Проверка документа на соответствие требованиям (размер и формат)
def validate_file_requirements(
    file_name: str, file_size_mb: float, max_size_mb: float
) -> bool:
    """Проверяет допустимый формат расширения и размер файла."""
    is_valid_format = file_name.endswith(".pdf") or file_name.endswith(".docx")
    is_valid_size = 0.0 < file_size_mb <= max_size_mb
    return is_valid_format and is_valid_size


# 4. Функция: Фиксация новых версий при редактировании
def increment_version(current_version: float, is_major_update: bool) -> float:
    """Вычисляет номер следующей версии документа."""
    if is_major_update:
        # Крупное обновление: 1.2 -> 2.0
        return round(float(int(current_version) + 1), 1)
    else:
        # Минорная правка: 1.2 -> 1.3
        return round(current_version + 0.1, 1)


# 5. Функция: Контроль жизненного цикла и статуса документа
def get_document_status(
    is_archived: bool, is_signed: bool, is_reviewed: bool
) -> str:
    """Определяет статус документа: черновик, на согласовании,
      утвержден, в архиве."""
    if is_archived:
        return "В архиве"
    elif is_signed:
        return "Утвержден"
    elif is_reviewed:
        return "На согласовании"
    else:
        return "Черновик"


# ==============================================================================
# СЦЕНАРИЙ РАБОТЫ ПРОГРАММЫ (ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ)
# ==============================================================================

# Исходные данные документа
doc_title = "Трудовой_договор_Иванов.pdf"
doc_author = "Алексей Смирнов"
cat_code = 2
file_size = 4.5
max_size = 10.0
version = 1.0
reg_date = date(2026, 9, 20)

# Текущее состояние процесса согласования
is_reviewed = True
is_signed = True
is_archived = False

print("=" * 55)
print("     СЕРВИС УПРАВЛЕНИЯ ДОКУМЕНТАМИ (DOCFLOW)")
print("=" * 55)

# Шаг 1: Проверка создания документа
is_created = create_document(doc_title, doc_author)
print(f"1. Регистрация документа:   {'Успешно' if is_created else 'Ошибка'}")

# Шаг 2: Классификация
category = classify_document(cat_code)
print(f"2. Присвоенная категория:    {category}")

# Шаг 3: Проверка требований к файлу
is_valid_file = validate_file_requirements(doc_title, file_size, max_size)
print(
    f"3. Соответствие требованиям: \
    {'Соответствует' if is_valid_file else 'Отклонен'}")

# Шаг 4: Определение статуса
current_status = get_document_status(is_archived, is_signed, is_reviewed)
print(f"4. Текущий статус:          {current_status}")

# Шаг 5: Фиксация новой версии (например, внесли правку)
next_version = increment_version(version, is_major_update=False)
print(f"5. Редактирование версии:   v{version} -> v{next_version}")

print("-" * 55)
print("ИТОГОВАЯ КАРТОЧКА ОБЪЕКТА:")
print(f"Файл:      {doc_title} (v{next_version})")
print(f"Автор:     {doc_author}")
print(f"Категория: {category}")
print(f"Дата:      {reg_date.strftime('%d.%m.%Y')}")
print(f"Статус:    {current_status}")
print("=" * 55)
