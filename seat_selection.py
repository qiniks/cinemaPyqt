from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from app import app_data


class SeatSelectionWindow(QDialog):
    def __init__(self, username, movie_id, time, parent=None):
        super().__init__(parent)
        self.username = username
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

        for row in range(5):  # 5 рядов
            for col in range(5):  # 5 мест в ряду
                seat = f"{row + 1}-{chr(65 + col)}"
                button = QPushButton(seat)
                button.setCheckable(True)
                if app_data.is_seat_taken(self.movie_id, self.time, seat):
                    button.setStyleSheet("background-color: red; color: white;")  # Место занято
                    button.setEnabled(False)  # Отключаем нажатие
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
        if self.username == None:
            QMessageBox.warning(self, "Ошибка", "Для брони места вы должны авторизоваться.")
            self.close()
            return False

        if not self.selected_seats:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одно место!")
            return

        success = True
        for seat in self.selected_seats:
            if not app_data.book_seat(self.username, self.movie_id, self.time, seat):
                success = False
                QMessageBox.warning(self, "Ошибка", f"Место {seat} уже занято!")

        if success:
            QMessageBox.information(self, "Успех", "Билеты успешно куплены!")
            self.close()
        else:
            self.init_ui()  # Обновляем интерфейс, чтобы отразить актуальный статус мест
