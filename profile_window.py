from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QFormLayout, QGroupBox, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt

from res.styles import APP_STYLE
from user import User


class ProfileWindow(QMainWindow):
    def __init__(self, username, on_logout):
        super().__init__()
        self.username = username
        self.on_logout = on_logout  # Метод для обновления главного окна при выходе
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Profile")
        self.setFixedSize(600, 600)

        layout = QVBoxLayout()

        # Приветственное сообщение
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Секция редактирования данных
        edit_group = QGroupBox("Edit Profile")
        edit_layout = QFormLayout()

        self.username_input = QLineEdit(User.users[self.username]["username"])
        self.phone_input = QLineEdit(User.users[self.username]["phone"])
        self.password_input = QLineEdit(User.users[self.username]["password"])
        self.password_input.setEchoMode(QLineEdit.Password)

        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("background-color: green; color: white; border-radius: 10px; padding: 5px;")
        save_button.clicked.connect(self.save_changes)

        edit_layout.addRow("Username:", self.username_input)
        edit_layout.addRow("Phone:", self.phone_input)
        edit_layout.addRow("Password:", self.password_input)
        edit_layout.addRow(save_button)
        edit_group.setLayout(edit_layout)

        # Секция истории билетов
        history_group = QGroupBox("Purchase History")
        history_layout = QVBoxLayout()

        self.ticket_list = QListWidget()
        # Заполняем историю билетов (заглушки для примера)
        tickets = User.users[self.username].get("tickets", [])
        if tickets:
            for ticket in tickets:
                self.ticket_list.addItem(ticket)
        else:
            self.ticket_list.addItem("No tickets purchased yet.")

        history_layout.addWidget(self.ticket_list)
        history_group.setLayout(history_layout)

        # Кнопка выхода
        logout_button = QPushButton("Log Out")
        logout_button.setStyleSheet("background-color: red; color: white; border-radius: 10px; padding: 10px;")
        logout_button.clicked.connect(self.logout)

        # Добавляем все элементы на главный layout
        layout.addWidget(welcome_label)
        layout.addWidget(edit_group)
        layout.addWidget(history_group)
        layout.addWidget(logout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_changes(self):
        """Сохраняет изменения профиля пользователя"""
        new_username = self.username_input.text().strip()
        new_phone = self.phone_input.text().strip()
        new_password = self.password_input.text().strip()

        if not new_username or not new_phone or not new_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_username != self.username and new_username in User.users:
            QMessageBox.warning(self, "Error", f"Username '{new_username}' is already taken.")
            return

        # Обновляем данные пользователя
        user_data = User.users.pop(self.username)
        user_data["username"] = new_username
        user_data["phone"] = new_phone
        user_data["password"] = new_password
        User.users[new_username] = user_data

        self.username = new_username
        QMessageBox.information(self, "Success", "Profile updated successfully.")

    def logout(self):
        """Обрабатывает выход пользователя из аккаунта"""
        confirm = QMessageBox.question(self, "Log Out", "Are you sure you want to log out?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.on_logout()
            self.close()
