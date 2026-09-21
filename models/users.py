import hashlib


class User:
    """Класс, описывающий пользователя системы (сотрудника / автора документа)."""

    def __init__(self, id: int, email: str, password_hash: str) -> None:
        """
        Инициализация пользователя.
        Пароль хранится только в зашифрованном (хэшированном) виде.
        """
        self.id = id
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Статический метод для детерминированного хэширования пароля через SHA-256.
        Не зависит от перезапусков программы.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        """
        Проверяет, совпадает ли введенный пользователем пароль
        с хэшем, хранящимся в объекте.
        """
        return self.password_hash == self.hash_password(password)

    def __str__(self) -> str:
        """Удобное строковое отображение пользователя."""
        return f"Пользователь #{self.id} ({self.email})"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """
        Фабричный метод: восстанавливает объект User из данных JSON.
        """
        return cls(
            id=data["id"],
            email=data["email"],
            password_hash=data["password_hash"]
        )