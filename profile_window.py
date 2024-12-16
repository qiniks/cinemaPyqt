import requests
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QFormLayout, QGroupBox, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt


class ProfileWindow(QMainWindow):
    def __init__(self, username, on_logout, api_url):
        super().__init__()
        self.username = username
        self.api_url = api_url
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

        self.username_input = QLineEdit(self.username)
        self.username_input.setEnabled(False)
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
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

        self.ticket_list = QListWidget()
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

        # Загружаем данные профиля и историю
        self.load_profile()

    def load_profile(self):
        """Загружает данные профиля с сервера"""
        try:
            response = requests.get(f"{self.api_url}/user/{self.username}")
            if response.status_code == 200:
                user_data = response.json()
                self.phone_input.setText(user_data["number"])
                self.password_input.setText(user_data["password"])
                tickets = user_data["bookings"]
                self.ticket_list.clear()
                if tickets:
                    for ticket in tickets:
                        ticket_info = f"Movie: {ticket['movie_title']}, Time: {ticket['time']}, Seat: {ticket['seat']}"
                        self.ticket_list.addItem(ticket_info)
                else:
                    self.ticket_list.addItem("No tickets purchased yet.")
            else:
                QMessageBox.warning(self, "Error", "Failed to load profile data.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to the server: {str(e)}")

    def save_changes(self):
        """Сохраняет изменения профиля пользователя на сервере"""
        new_phone = self.phone_input.text().strip()
        new_password = self.password_input.text().strip()

        if not new_phone or not new_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            response = requests.put(
                f"{self.api_url}/user/{self.username}",
                json={"number": new_phone, "password": new_password},
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Profile updated successfully.")
            else:
                QMessageBox.warning(self, "Error", "Failed to update profile.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to the server: {str(e)}")

    def logout(self):
        """Обрабатывает выход пользователя из аккаунта"""
        confirm = QMessageBox.question(self, "Log Out", "Are you sure you want to log out?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.on_logout()
            self.close()
