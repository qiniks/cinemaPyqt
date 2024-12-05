class User:
    users = {}

    @classmethod
    def add_user(cls, username, phone, password):
        """Добавляет пользователя в базу."""
        cls.users[username] = {"phone": phone, "password": password}

    @classmethod
    def validate_user(cls, username, password):
        """Проверяет данные пользователя."""
        return username in cls.users and cls.users[username]["password"] == password
