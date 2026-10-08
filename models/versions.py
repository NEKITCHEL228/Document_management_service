from datetime import date
from typing import List, Optional
from .users import User
from .documents import Document


class Version:
    """
    Класс версии документа.
    Связующая сущность (композиция): хранит ссылку на Document и User.
    """

    def __init__(
        self,
        version_id: int,
        version_num: str,
        file_size_mb: float,
        release_date: date,
        is_signed: bool,
        author: User,
        document: Document,
    ) -> None:
        """
        Инициализация версии документа.
        Принимает живые объекты author (User) и document (Document).
        """
        self.id = version_id
        self.version_num = version_num
        self.file_size_mb = file_size_mb
        self.release_date = release_date
        self.is_signed = is_signed
        self.author: User = author
        self.document: Document = document

    def sign(self) -> None:
        """
        Метод изменения состояния: фиксирует факт подписания версии.
        (Переводит флаг is_signed в True).
        """
        self.is_signed = True

    def is_valid_size(self, max_size_mb: float = 10.0) -> bool:
        """
        Проверка бизнес-правила: не превышает ли загруженный файл
        максимально допустимый размер.
        """
        return 0.0 < self.file_size_mb <= max_size_mb

    def __str__(self) -> str:
        """
        Строковое представление версии с выводом названия документа,
        автора и статуса подписания.
        """
        status = "Подписан" if self.is_signed else "Черновик (не подписан)"
        date_str = self.release_date.strftime("%d.%m.%Y")
        doc_title = self.document.title
        return (
            f"Версия v{self.version_num} (ID: {self.id}) к документу "
            f"'{doc_title}' | Автор: {self.author.email} | "
            f"Размер: {self.file_size_mb} МБ | Дата: {date_str} | "
            f"Статус: {status}"
        )


def find_version_by_id(
    versions: List[Version],
    ver_id: int,
) -> Optional[Version]:
    """Найти версию документа по идентификатору."""
    for version in versions:
        if version.id == ver_id:
            return version
    return None