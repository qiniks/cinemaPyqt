from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

from res.styles import AUTH_STYLE, WELCOME_STYLE
from app import app_data


class RegisterDialog(QDialog):
    def __init__(self, on_success=None):
        super().__init__()
        self.on_success = on_success  # Метод вызывается после успешной регистрации
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")
        self.setFixedSize(400, 500)
        self.setStyleSheet(AUTH_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.welcome = QLabel("REGISTER TO MOVAI")
        self.welcome.setStyleSheet(WELCOME_STYLE)
        self.welcome.setAlignment(Qt.AlignCenter)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)

        # Добавляем виджеты в layout
        layout.addWidget(self.welcome)
        layout.addWidget(self.username_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()

        # Проверяем, что все поля заполнены
        if not username or not phone or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Проверяем, что пользователь с таким именем не существует
        if username in app_data.users:
            QMessageBox.warning(self, "Error", f"Username '{username}' is already taken.")
            return

        # Добавляем пользователя
        app_data.add_user(username, phone, password)
        QMessageBox.information(self, "Register", "Registration successful!")

        # Если передан метод on_success, вызываем его
        if self.on_success:
            self.on_success(username)

        # Закрываем диалог
        self.accept()
