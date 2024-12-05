from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from user import User  # Убедитесь, что файл user.py существует и корректно импортируется


class RegisterDialog(QDialog):
    def __init__(self, on_success=None):
        super().__init__()
        self.on_success = on_success  # Метод вызывается после успешной регистрации
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Кнопка регистрации
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)

        # Добавляем виджеты в layout
        layout.addWidget(QLabel("REGISTER TO MOVAI", alignment=Qt.AlignCenter))
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
        if username in User.users:
            QMessageBox.warning(self, "Error", f"Username '{username}' is already taken.")
            return

        # Добавляем пользователя
        User.add_user(username, phone, password)
        QMessageBox.information(self, "Register", "Registration successful!")

        # Если передан метод on_success, вызываем его
        if self.on_success:
            self.on_success(username)

        # Закрываем диалог
        self.accept()
