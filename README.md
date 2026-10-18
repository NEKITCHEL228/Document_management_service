# DocFlow – сервис управления документами

## 1. Назначение проекта
DocFlow – система для централизованного хранения, тематической классификации, контроля версий и отслеживания статуса обработки электронных документов.
Проект развивается поэтапно: консольная версия приложения (ПР3) была дополнена веб-интерфейсом на Django (ПР5), переведена на полноценную систему шаблонов DTL и статических файлов (ПР6), а в рамках ПР7 получила собственный слой реляционной базы данных SQLite и набор SQL-запросов с прямой интеграцией в веб-представления.

Приложение позволяет:
* просматривать главную страницу сервиса в браузере;
* просматривать реестр электронных документов, загружаемый напрямую из базы данных SQLite;
* искать документы по ключевым словам через параметризованные SQL-запросы (`LIKE ?`);
* просматривать детальные карточки документов и связанных категорий;
* просматривать список категорий с подсчетом входящих документов (`GROUP BY`);
* отслеживать журнал версий документов и проверять статус наличия электронной подписи (ЭЦП);
* анализировать сводную статистику документооборота (агрегатные функции `COUNT`, `SUM`, `AVG`, `HAVING`);
* сохранять данные в реляционной базе данных `data/docflow.sqlite` при сохранении обратной совместимости с JSON.

## 2. Используемые технологии
* Python 3.11+;
* SQLite 3 – встраиваемая реляционная СУБД;
* SQL (DDL, DML, JOIN, GROUP BY, HAVING, агрегатные функции);
* Django 5.2 – веб-фреймворк;
* Django Template Language (DTL) – шаблонизация веб-страниц;
* HTML5 и CSS3 / Bootstrap 5.3 – адаптивная верстка и кастомное оформление;
* JavaScript – клиентская динамика (автоматическое определение текущего года);
* pytest – автоматизированное модульное тестирование;
* flake8 – контроль качества и соответствия стандарту PEP 8;
* Git – контроль версий.

## 3. Слой реляционной базы данных (ПР7)
В рамках ПР7 проект получил независимый слой реляционной базы данных на базе СУБД SQLite без использования Django ORM (переход к ORM запланирован на последующие практические работы).

### 3.1. Структура таблиц базы данных (`data/docflow.sqlite`)

1. **`categories`** – тематические категории:
   * `id INTEGER PRIMARY KEY` – уникальный идентификатор;
   * `name TEXT NOT NULL` – название категории;
   * `description TEXT` – текстовое описание.
2. **`users`** – пользователи сервиса:
   * `id INTEGER PRIMARY KEY` – уникальный идентификатор;
   * `email TEXT NOT NULL UNIQUE` – адрес электронной почты;
   * `password_hash TEXT NOT NULL` – хэш пароля.
3. **`documents`** – электронные документы:
   * `id INTEGER PRIMARY KEY` – уникальный идентификатор;
   * `title TEXT NOT NULL` – заголовок документа;
   * `content TEXT` – текстовое содержание.
4. **`document_categories`** – связующая таблица «многие-ко-многим»:
   * `document_id INTEGER NOT NULL` – внешний ключ к `documents(id)`;
   * `category_id INTEGER NOT NULL` – внешний ключ к `categories(id)`;
   * `PRIMARY KEY (document_id, category_id)`.
5. **`versions`** – редакции файлов документов:
   * `id INTEGER PRIMARY KEY` – уникальный идентификатор версии;
   * `version_num TEXT NOT NULL` – номер версии (например, `1.0`);
   * `file_size_mb REAL NOT NULL` – размер файла в мегабайтах;
   * `release_date TEXT NOT NULL` – дата создания в формате `YYYY-MM-DD`;
   * `is_signed INTEGER NOT NULL DEFAULT 0` – статус ЭЦП (0 — черновик, 1 — подписан);
   * `author_id INTEGER NOT NULL` – внешний ключ к `users(id)`;
   * `document_id INTEGER NOT NULL` – внешний ключ к `documents(id)`.

### 3.2. Файлы и модули базы данных
* `sql/schema.sql` – DDL-скрипт создания всех таблиц и связей с ограничениями `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `DEFAULT`.
* `sql/queries.sql` – комплект из 12 структурированных SQL-запросов предметной области (выборка, фильтрация `WHERE`, объединение `JOIN`, агрегация `COUNT`/`SUM`/`AVG`, группировка `GROUP BY` и фильтрация групп `HAVING`).
* `db/database.py` – модуль подключения к SQLite с обязательным включением проверки внешних ключей `PRAGMA foreign_keys = ON` и поддержкой фабрики строк `sqlite3.Row`.
* `db/import_json.py` – скрипт миграции существующих данных из JSON-файлов в таблицы SQLite с использованием пакетной вставки `executemany()` и транзакционного контроля (`commit`/`rollback`).

## 4. Веб-интерфейс и страницы
Веб-представления в `my_django_project` получают данные из SQLite с помощью `sqlite3.Row` (доступ к полям по именам колонок):

* `/` – главная страница сервиса и навигация (view-функция `index`);
* `/documents/` – реестр документов из SQLite (view-функция `document_list`);
* `/documents/<int:doc_id>/` – карточка документа со связанными категориями через SQL JOIN (view-функция `document_detail`);
* `/documents/search/?q=...` – параметризованный SQL-поиск по названию или содержанию (view-функция `document_search`);
* `/documents/statistics/` – сводная статистика и аналитика хранилища на базе SQL-агрегатов и `GROUP BY`/`HAVING` (view-функция `statistics`);
* `/categories/` – список категорий с подсчетом количества документов (view-функция `category_list`);
* `/categories/<int:cat_id>/` – карточка категории и перечень входящих документов (view-функция `category_detail`);
* `/versions/` – журнал версий с авторами и документами через SQL JOIN (view-функция `version_list`);
* `/versions/<int:ver_id>/` – карточка редакции и статус ЭЦП (view-функция `version_detail`).

Если объект по указанному ID не найден, возвращается кастомная страница со статусом 404.

## 5. Django Template Language (DTL) и статика
* Базовый шаблон: `my_django_project/templates/base.html`;
* Включаемые шаблоны: `navigation.html`, `footer.html`, `document_card.html`, `category_card.html`, `version_status.html`;
* Статические файлы: `my_django_project/static/css/style.css` и `my_django_project/static/js/main.js` (автоматический вывод текущего года);
* Пространства имён: `homepage`, `documents`, `categories`, `versions`.

## 6. Структура проекта
```text
Document_management_service/
├── db/                                # Модули работы с базой данных (ПР7)
│   ├── __init__.py
│   ├── database.py                    # get_connection() с PRAGMA foreign_keys = ON
│   └── import_json.py                 # Скрипт переноса данных JSON -> SQLite
├── sql/                               # SQL-файлы проекта (ПР7)
│   ├── schema.sql                     # DDL-схема таблиц
│   └── queries.sql                    # Набор SQL-запросов (12 запросов)
├── data/                              # Файлы данных
│   ├── docflow.sqlite                 # База данных SQLite (ПР7)
│   ├── categories.json
│   ├── documents.json
│   ├── users.json
│   └── versions.json
├── my_django_project/                 # Веб-приложение Django
│   ├── Document_management_service/   # Конфигурация проекта (settings.py, urls.py)
│   ├── homepage/                      # Главная страница
│   ├── documents/                     # Документы, поиск, статистика
│   ├── categories/                    # Категории
│   ├── versions/                      # Журнал версий
│   ├── templates/                     # Шаблоны (base.html, includes)
│   ├── static/                        # Статические файлы (CSS, JS)
│   └── manage.py
├── models/                            # Классы предметной области (ПР3)
├── tests/                             # Автотесты (pytest)
├── main.py                            # Консольный интерфейс (сохранен с ПР3)
├── storage.py                         # Сериализация / десериализация JSON
├── utils.py                           # Вспомогательные функции
├── requirements.txt
└── README.md
```

## 7. Запуск приложения

### Миграция данных в SQLite:
```bash
python -m db.import_json
```

### Веб-версия (Django):
```bash
cd my_django_project
python manage.py runserver
```
Веб-интерфейс доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Консольная версия:
Из корневой папки проекта:
```bash
python main.py
```

## 8. Тестирование и контроль качества
Запуск полного набора автотестов:
```bash
pytest -v
```

Проверка соответствия стандарту PEP 8:
```bash
flake8 . --extend-exclude=.venv,my_django_project,.agents
```

Проверка конфигурации Django:
```bash
python my_django_project/manage.py check
```

## 9. Текущее состояние и план развития
**Реализовано (ПР7):**
* Спроектирована реляционная схема базы данных с первичными и внешними ключами;
* Создан файл схемы `sql/schema.sql` и база данных `data/docflow.sqlite`;
* Разработан модуль `db/database.py` с контролем внешних ключей (`PRAGMA foreign_keys = ON`);
* Реализован скрипт `db/import_json.py` для безопасного транзакционного импорта данных из JSON в SQLite;
* Составлен комплект из 12 проверенных SQL-запросов (`sql/queries.sql`) всех требуемых видов (`WHERE`, `JOIN`, `COUNT`/`SUM`/`AVG`, `GROUP BY`, `HAVING`);
* Веб-представления переведены на получение данных из SQLite через `sqlite3.Row`;
* Реализованы сценарии параметризованного поиска документов (`/documents/search/`) и страницы статистики (`/documents/statistics/`);
* Обновлена навигация сайта;
* Добавлены автотесты базы данных и запросов в `tests/test_database.py` (всего 42 теста проходят);
* Документация полностью обновлена.

**Планируется (ПР8–ПР10):**
* Перенос моделей данных на Django ORM (`models.Model`);
* Замена прямого выполнения SQL-запросов на Django QuerySet API;
* Использование механизма миграций Django (`makemigrations`, `migrate`);
* Настройка административной панели Django (`admin.py`);
* Внедрение Django Forms для создания и редактирования документов.