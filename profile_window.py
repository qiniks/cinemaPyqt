from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QFormLayout, QGroupBox, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt

from app import app_data


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

        self.username_input = QLineEdit(app_data.users[self.username]["username"])
        self.phone_input = QLineEdit(app_data.users[self.username]["number"])
        self.password_input = QLineEdit(app_data.users[self.username]["password"])
        self.password_input.setEchoMode(QLineEdit.Password)

        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("background-color: green; color: white; border-radius: 10px; padding: 5px;")
        save_button.clicked.connect(self.save_changes)

        edit_layout.addRow("Username:", self.username_input)
        edit_layout.addRow("Number:", self.phone_input)
        edit_layout.addRow("Password:", self.password_input)
        edit_layout.addRow(save_button)
        edit_group.setLayout(edit_layout)

        # Секция истории билетов
        history_group = QGroupBox("Purchase History")
        history_layout = QVBoxLayout()

        try:
            self.ticket_list = QListWidget()
            # Заполняем историю билетов (заглушки для примера)
            tickets = app_data.users[self.username].get("bookings", [])
            if tickets:
                for ticket in tickets:
                    ticket_info = f"Movie: {ticket['movie_title']}, Time: {ticket['time']}, Seat: {ticket['seat']}"
                    self.ticket_list.addItem(ticket_info)  # Добавляем строку с информацией
            else:
                self.ticket_list.addItem("No tickets purchased yet.")
        except Exception as e:
            print(f"Error in open_seat_selection: {e}")

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

        if new_username != self.username and new_username in app_data.users:
            QMessageBox.warning(self, "Error", f"Username '{new_username}' is already taken.")
            return

        # Обновляем данные пользователя
        print(app_data.users)
        user_data = app_data.users.pop(self.username)
        user_data["username"] = new_username
        user_data["number"] = new_phone
        user_data["password"] = new_password
        app_data.users[new_username] = user_data
        print(app_data.users)

        self.username = new_username
        QMessageBox.information(self, "Success", "Profile updated successfully.")

    def logout(self):
        """Обрабатывает выход пользователя из аккаунта"""
        confirm = QMessageBox.question(self, "Log Out", "Are you sure you want to log out?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.on_logout()
            self.close()
