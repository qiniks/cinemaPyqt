from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

from res.styles import AUTH_STYLE, WELCOME_STYLE
from user import User


class LoginDialog(QDialog):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet(AUTH_STYLE)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Log in")
        self.login_button.clicked.connect(self.login)

        self.welcome_label = QLabel("WELCOME TO MOVAI")
        self.welcome_label.setStyleSheet(WELCOME_STYLE)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if User.validate_user(username, password):
            QMessageBox.information(self, "Login", "Welcome back!")
            self.on_success(username)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
