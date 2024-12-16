import requests
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGridLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt


class SeatSelectionWindow(QDialog):
    def __init__(self, username, movie_id, time, api_url, parent=None):
        super().__init__(parent)
        self.username = username
        self.api_url = api_url
        self.movie_id = movie_id
        self.time = time
        self.selected_seats = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Выбор мест")
        self.setFixedSize(600, 600)
        layout = QVBoxLayout()

        # Сетка для мест
        self.grid_layout = QGridLayout()
        self.buttons = {}

        taken_seats = self.get_taken_seats()
        print(taken_seats)

        for row in range(5):
            for col in range(5):
                seat = f"{row + 1}-{chr(65 + col)}"
                button = QPushButton(seat)
                button.setCheckable(True)
                if seat in taken_seats:
                    button.setStyleSheet("background-color: red; color: white;")
                    button.setEnabled(False)
                else:
                    button.setStyleSheet("background-color: lightgray;")
                button.clicked.connect(self.toggle_seat)
                self.buttons[seat] = button
                self.grid_layout.addWidget(button, row, col)

        layout.addLayout(self.grid_layout)

        # Кнопка подтверждения
        confirm_button = QPushButton("Buy")
        confirm_button.setStyleSheet("padding: 10px; font-size: 16px;")
        confirm_button.clicked.connect(self.buy_tickets)
        layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def get_taken_seats(self):
        try:
            response = requests.get(
                f"{self.api_url}/get_taken_seats",
                params={"movie_id": self.movie_id, "time": self.time},
            )
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                # QMessageBox.critical(self, "Ошибка", "Не удалось проверить статус мест.")
                print("Ошибка", "Не удалось проверить статус мест.")
                return True  # Считаем место занятым при ошибке
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", str(e))
            return True

    def toggle_seat(self):
        sender = self.sender()
        seat = sender.text()
        if sender.isChecked():
            sender.setStyleSheet("background-color: green; color: white;")  # Выбрано
            self.selected_seats.append(seat)
        else:
            sender.setStyleSheet("background-color: lightgray;")  # Снято
            self.selected_seats.remove(seat)

    def buy_tickets(self):
        if self.username is None:
            QMessageBox.warning(self, "Ошибка", "Для брони места вы должны авторизоваться.")
            self.close()
            return

        if not self.selected_seats:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одно место!")
            return

        success = True
        for seat in self.selected_seats:
            if not self.book_seat(seat):
                success = False
                QMessageBox.warning(self, "Ошибка", f"Место {seat} уже занято!")

        if success:
            QMessageBox.information(self, "Успех", "Билеты успешно куплены!")
            self.close()
        else:
            self.init_ui()  # Обновляем интерфейс, чтобы отразить актуальный статус мест

    def book_seat(self, seat):
        """Бронирование места через Flask API"""
        try:
            response = requests.post(
                f"{self.api_url}/book_seat",
                json={
                    "username": self.username,
                    "movie_id": self.movie_id,
                    "time": self.time,
                    "seat": seat,
                },
            )
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", str(e))
            return False
