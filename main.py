from datetime import date

# Входные данные о документе и версии
document_title = "Трудовой_договор_Иванов.pdf"
category_name = "Кадровые документы"
author_name = "Алексей Смирнов"
version_number = 1.2
file_size_mb = 4.8
max_allowed_size_mb = 10.0
is_signed = True
upload_date = date(2026, 9, 20)


def check_document_status(size: float, max_size: float, signed: bool) -> str:
    """Определяет статус документа на основе его параметров."""
    if size > max_size:
        return "Отклонен: превышен максимальный размер файла"
    elif not signed:
        return "Черновик: ожидает подписания"
    else:
        return "Утвержден: документ готов к регистрации в системе"


# Проверка статуса
status = check_document_status(file_size_mb, max_allowed_size_mb, is_signed)

# Вывод информации о документе
print("=" * 45)
print("КАРТОЧКА ДОКУМЕНТА")
print("=" * 45)
print(f"Название документа: {document_title}")
print(f"Категория:          {category_name}")
print(f"Автор:              {author_name}")
print(f"Версия:             v{version_number}")
print(f"Дата загрузки:      {upload_date.strftime('%d.%m.%Y')}")
print(f"Размер файла:       {file_size_mb} МБ (макс. {max_allowed_size_mb} МБ)")
print(f"ЭЦП:                {'Присутствует' if is_signed else 'Отсутствует'}")
print("-" * 45)
print(f"Текущий статус:     {status}")
print("=" * 45)