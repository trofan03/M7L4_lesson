import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."


def test_add_existing_user():
    add_user("maks", "maks@mail.com", "12345")

    result = add_user("maks", "new@mail.com", "54321")

    assert result is False



def test_successful_authentication():
    add_user("maks", "maks@mail.com", "12345")

    result = authenticate_user("maks", "12345")

    assert result is True



def test_authentication_nonexistent_user():
    result = authenticate_user("unknown", "12345")

    assert result is False



def test_authentication_wrong_password():
    add_user("maks", "maks@mail.com", "12345")

    result = authenticate_user("maks", "wrongpassword")

    assert result is False



def test_display_users(capsys):
    add_user("maks", "maks@mail.com", "12345")
    add_user("alex", "alex@mail.com", "67890")

    display_users()

    captured = capsys.readouterr()

    assert "maks@mail.com" in captured.out
    assert "alex@mail.com" in captured.out

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""