from models import User


def test_user_creation():
    """Проверка создания пользователя и сохранения атрибутов."""
    pwd_hash = User.hash_password("secret123")
    user = User(id=1, email="test@docflow.ru", password_hash=pwd_hash)

    assert user.id == 1
    assert user.email == "test@docflow.ru"
    assert user.password_hash == pwd_hash


def test_user_password_checking():
    """Проверка корректности валидации пароля методом check_password."""
    raw_password = "my_strong_password"
    pwd_hash = User.hash_password(raw_password)
    user = User(id=1, email="user@test.ru", password_hash=pwd_hash)

    assert user.check_password("my_strong_password") is True
    assert user.check_password("wrong_password") is False


def test_user_str():
    """Проверка строкового представления пользователя."""
    user = User(id=5, email="ivanov@docflow.ru", password_hash="dummy_hash")

    assert str(user) == "Пользователь #5 (ivanov@docflow.ru)"


def test_user_from_data():
    """Проверка десериализации пользователя из данных словаря."""
    raw_data = {
        "id": 2,
        "email": "admin@docflow.ru",
        "password_hash": "hash12345"
    }
    user = User.from_data(raw_data)

    assert user.id == 2
    assert user.email == "admin@docflow.ru"
    assert user.password_hash == "hash12345"