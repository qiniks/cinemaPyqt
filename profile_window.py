from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt


class ProfileWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Profile")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # Приветственное сообщение
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Кнопка выхода из аккаунта
        logout_button = QPushButton("Log Out")
        logout_button.setStyleSheet("background-color: red; color: white; border-radius: 10px; padding: 10px;")
        logout_button.clicked.connect(self.logout)

        layout.addWidget(welcome_label)
        layout.addWidget(logout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()
