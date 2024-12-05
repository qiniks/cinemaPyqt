class User:
    users = {}

    @classmethod
    def add_user(cls, username, phone, password, is_admin=False):
        cls.users[username] = {
            "username": username,
            "phone": phone,
            "password": password,
            "tickets": [],
            "is_admin": is_admin
        }

    @classmethod
    def is_admin(cls, username):
        return cls.users.get(username, {}).get("is_admin", False)

    @classmethod
    def validate_user(cls, username, password):
        return username in cls.users and cls.users[username]["password"] == password

    @classmethod
    def add_ticket(cls, username, ticket_info):
        """Добавляет билет в историю пользователя"""
        if username in cls.users:
            cls.users[username]["tickets"].append(ticket_info)
