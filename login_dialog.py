from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from res.styles import AUTH_STYLE, WELCOME_STYLE
import requests


class LoginDialog(QDialog):
    def __init__(self, api_url, on_success):
        super().__init__()
        self.on_success = on_success
        self.api_url = api_url
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
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Both fields are required.")
            return

        try:
            response = requests.post(
                f"{self.api_url}/login",
                json={"username": username, "password": password},
            )

            if response.status_code == 200:
                QMessageBox.information(self, "Login", "Welcome back!")
                self.on_success(username)
                self.accept()
            elif response.status_code == 401:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
            else:
                QMessageBox.warning(self, "Error", f"Unexpected error: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to the server: {str(e)}")
