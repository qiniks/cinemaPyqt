from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from user import User


class LoginDialog(QDialog):
    def __init__(self, on_success, open_register):
        super().__init__()
        self.on_success = on_success
        self.open_register = open_register
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Log in")
        login_button.clicked.connect(self.login)

        register_label = QLabel('Don’t have account?<a href="#">Register</a>')
        register_label.setAlignment(Qt.AlignCenter)
        register_label.linkActivated.connect(self.open_register)

        layout.addWidget(QLabel("WELCOME TO MOVAI", alignment=Qt.AlignCenter))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_label)

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
