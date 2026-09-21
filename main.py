from datetime import date
from typing import List
from models import Category, User, Document, Version
import storage
from utils import get_next_id, input_int, input_float


# =====================================================================
# 1. ПОДМЕНЮ: УПРАВЛЕНИЕ КАТЕГОРИЯМИ
# =====================================================================

def show_categories(categories: List[Category]) -> None:
    """Отображает список всех категорий."""
    print("\n--- СПИСОК КАТЕГОРИЙ ---")
    if not categories:
        print("Категорий пока нет.")
        return
    for cat in categories:
        print(cat)


def add_category_flow(categories: List[Category]) -> None:
    """Сценарий создания новой категории."""
    print("\n--- СОЗДАНИЕ КАТЕГОРИИ ---")
    name = input("Введите название категории: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return

    desc = input("Введите описание категории: ").strip()
    new_id = get_next_id(categories)

    # Исправлено: точное совпадение с параметром id
    new_cat = Category(id=new_id, name=name, description=desc)
    categories.append(new_cat)
    print(f"Категория '{name}' успешно добавлена (ID: {new_id})!")


def categories_menu(categories: List[Category]) -> None:
    """Меню раздела категорий."""
    while True:
        print("\n[УПРАВЛЕНИЕ КАТЕГОРИЯМИ]")
        print("1. Показать список категорий")
        print("2. Добавить категорию")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_categories(categories)
        elif choice == "2":
            add_category_flow(categories)
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")


# =====================================================================
# 2. ПОДМЕНЮ: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
# =====================================================================

def show_users(users: List[User]) -> None:
    """Отображает список пользователей."""
    print("\n--- СПИСОК ПОЛЬЗОВАТЕЛЕЙ ---")
    if not users:
        print("Пользователей нет.")
        return
    for u in users:
        print(u)


def add_user_flow(users: List[User]) -> None:
    """Сценарий регистрации пользователя."""
    print("\n--- РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ ---")
    email = input("Введите email: ").strip()
    if not email:
        print("Email не может быть пустым.")
        return

    password = input("Введите пароль: ").strip()
    if not password:
        print("Пароль не может быть пустым.")
        return

    new_id = get_next_id(users)
    hashed_pwd = User.hash_password(password)

    # Исправлено: параметр id
    new_user = User(id=new_id, email=email, password_hash=hashed_pwd)
    users.append(new_user)
    print(f"Пользователь '{email}' успешно создан (ID: {new_id})!")


def users_menu(users: List[User]) -> None:
    """Меню раздела пользователей."""
    while True:
        print("\n[УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ]")
        print("1. Показать список пользователей")
        print("2. Добавить пользователя")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_users(users)
        elif choice == "2":
            add_user_flow(users)
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")


# =====================================================================
# 3. ПОДМЕНЮ: УПРАВЛЕНИЕ ДОКУМЕНТАМИ
# =====================================================================

def show_documents(documents: List[Document]) -> None:
    """Отображает список документов."""
    print("\n--- СПИСОК ДОКУМЕНТОВ ---")
    if not documents:
        print("Документов пока нет.")
        return
    for doc in documents:
        print(doc)


def create_document_flow(
    documents: List[Document],
    categories: List[Category]
) -> None:
    """Сценарий создания документа с привязкой к категории."""
    print("\n--- СОЗДАНИЕ ДОКУМЕНТА ---")
    title = input("Введите название документа: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return

    content = input("Введите краткое описание / содержание: ").strip()

    chosen_categories: List[Category] = []
    if categories:
        show_categories(categories)
        cat_id = input_int("Введите ID категории для привязки (или 0 для пропуска): ")
        if cat_id != 0:
            matched = next((c for c in categories if c.id == cat_id), None)
            if matched:
                chosen_categories.append(matched)
            else:
                print("Категория с таким ID не найдена. Документ создан без категории.")

    new_id = get_next_id(documents)
    # Исправлено: параметр id
    new_doc = Document(
        id=new_id,
        title=title,
        content=content,
        categories=chosen_categories
    )
    documents.append(new_doc)
    print(f"Документ '{title}' успешно создан (ID: {new_id})!")


def search_documents(documents: List[Document]) -> None:
    """Поиск документов по ключевому слову в названии."""
    query = input("Введите строку для поиска: ").strip().lower()
    matched = [d for d in documents if query in d.title.lower()]
    print(f"\nНайдено документов: {len(matched)}")
    for d in matched:
        print(d)


def documents_menu(
    documents: List[Document],
    categories: List[Category]
) -> None:
    """Меню раздела документов."""
    while True:
        print("\n[УПРАВЛЕНИЕ ДОКУМЕНТАМИ]")
        print("1. Показать список документов")
        print("2. Создать новый документ")
        print("3. Найти документ по названию")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_documents(documents)
        elif choice == "2":
            create_document_flow(documents, categories)
        elif choice == "3":
            search_documents(documents)
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")


# =====================================================================
# 4. ПОДМЕНЮ: УПРАВЛЕНИЕ ВЕРСИЯМИ
# =====================================================================

def show_document_history(
    documents: List[Document],
    versions: List[Version]
) -> None:
    """Показывает хронологию всех версий конкретного документа."""
    if not documents:
        print("Документов нет.")
        return

    show_documents(documents)
    doc_id = input_int("Введите ID документа для просмотра истории версий: ")
    doc = next((d for d in documents if d.id == doc_id), None)
    if not doc:
        print("Документ не найден.")
        return

    history = [v for v in versions if v.document.id == doc.id]
    print(f"\n--- ИСТОРИЯ ВЕРСИЙ ДЛЯ '{doc.title}' ---")
    if not history:
        print("Версий для этого документа еще не создано.")
        return

    for v in history:
        print(v)


def add_version_flow(
    documents: List[Document],
    users: List[User],
    versions: List[Version]
) -> None:
    """Сценарий создания новой версии документа."""
    print("\n--- ДОБАВЛЕНИЕ НОВОЙ ВЕРСИИ ---")
    if not documents or not users:
        print("Для добавления версии необходим хотя бы один документ и один пользователь!")
        return

    show_documents(documents)
    doc_id = input_int("Введите ID документа: ")
    doc = next((d for d in documents if d.id == doc_id), None)
    if not doc:
        print("Документ не найден.")
        return

    show_users(users)
    author_id = input_int("Введите ID пользователя (автора редакции): ")
    author = next((u for u in users if u.id == author_id), None)
    if not author:
        print("Пользователь не найден.")
        return

    ver_num = input("Введите номер версии (например, 1.0, 1.1): ").strip()
    size_mb = input_float("Введите размер файла в МБ: ")

    new_id = get_next_id(versions)
    new_version = Version(
        version_id=new_id,
        version_num=ver_num,
        file_size_mb=size_mb,
        release_date=date.today(),
        is_signed=False,
        author=author,
        document=doc
    )

    if not new_version.is_valid_size(max_size_mb=15.0):
        print("Внимание: размер файла превышает лимит (15 МБ). Версия отклонена.")
        return

    versions.append(new_version)
    print(f"Версия v{ver_num} успешно добавлена к документу '{doc.title}'!")


def sign_version_flow(versions: List[Version]) -> None:
    """Сценарий подписания версии документа электронной подписью."""
    print("\n--- ПОДПИСАНИЕ ВЕРСИИ ---")
    unsigned = [v for v in versions if not v.is_signed]
    if not unsigned:
        print("Все версии уже подписаны.")
        return

    print("Неподписанные версии:")
    for v in unsigned:
        print(v)

    ver_id = input_int("Введите ID версии для подписания: ")
    version = next((v for v in unsigned if v.id == ver_id), None)
    if not version:
        print("Версия с таким ID не найдена или уже подписана.")
        return

    version.sign()
    print(f"Версия ID #{version.id} успешно подписана ЭЦП!")


def versions_menu(
    documents: List[Document],
    users: List[User],
    versions: List[Version]
) -> None:
    """Меню раздела версий."""
    while True:
        print("\n[УПРАВЛЕНИЕ ВЕРСИЯМИ]")
        print("1. Показать историю версий документа")
        print("2. Добавить новую версию к документу")
        print("3. Подписать версию")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_document_history(documents, versions)
        elif choice == "2":
            add_version_flow(documents, users, versions)
        elif choice == "3":
            sign_version_flow(versions)
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")


# =====================================================================
# ГЛАВНЫЙ ЦИКЛ ПРИЛОЖЕНИЯ
# =====================================================================

def main() -> None:
    """Точка запуска приложения."""
    print("Инициализация данных...")
    categories = storage.load_categories()
    users = storage.load_users()
    documents = storage.load_documents(categories)
    versions = storage.load_versions(documents, users)

    print("Данные успешно загружены из JSON-файлов.")

    while True:
        print("\n" + "=" * 45)
        print(" СЕРВИС УПРАВЛЕНИЯ ДОКУМЕНТАМИ (DOCFLOW)")
        print("=" * 45)
        print("1. Управление категориями")
        print("2. Управление пользователями")
        print("3. Управление документами")
        print("4. Управление версиями документов")
        print("0. Выход и сохранение данных")
        print("=" * 45)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            categories_menu(categories)
        elif choice == "2":
            users_menu(users)
        elif choice == "3":
            documents_menu(documents, categories)
        elif choice == "4":
            versions_menu(documents, users, versions)
        elif choice == "0":
            print("\nСохранение изменений в JSON...")
            storage.save_categories(categories)
            storage.save_users(users)
            storage.save_documents(documents)
            storage.save_versions(versions)
            print("Все данные сохранены. Работа завершена!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите цифру от 0 до 4.")


if __name__ == "__main__":
    main()