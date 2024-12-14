from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QGridLayout, QDialog, QMessageBox
)
from PyQt5.QtCore import Qt


class SeatSelectionWindow(QDialog):
    def __init__(self, movie_title, schedule_time):
        super().__init__()
        self.movie_title = movie_title
        self.schedule_time = schedule_time
        self.selected_seats = set()  # Хранит выбранные места
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Select Seats - {self.movie_title} ({self.schedule_time})")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # Заголовок
        header_label = QLabel(f"Select your seats for '{self.movie_title}' at {self.schedule_time}")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header_label, alignment=Qt.AlignCenter)

        # Сетка мест (5x8 для примера)
        self.seat_grid = QGridLayout()
        for row in range(5):  # 5 рядов
            for col in range(8):  # 8 мест в каждом ряду
                seat_button = QPushButton(f"{row+1}{chr(65+col)}")  # Нумерация: 1A, 1B, ...
                seat_button.setCheckable(True)
                seat_button.setStyleSheet("padding: 10px; font-size: 14px;")
                seat_button.clicked.connect(self.toggle_seat)
                self.seat_grid.addWidget(seat_button, row, col)

        layout.addLayout(self.seat_grid)

        # Кнопка "Buy"
        buy_button = QPushButton("Buy")
        buy_button.setStyleSheet("padding: 10px; font-size: 16px; background-color: green; color: white;")
        buy_button.clicked.connect(self.buy_tickets)
        layout.addWidget(buy_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_seat(self):
        """Обработчик выбора/отмены выбора места"""
        button = self.sender()
        seat = button.text()

        if button.isChecked():
            self.selected_seats.add(seat)  # Добавляем место в выбор
            button.setStyleSheet("background-color: lightblue; padding: 10px; font-size: 14px;")
        else:
            self.selected_seats.remove(seat)  # Убираем место из выбора
            button.setStyleSheet("padding: 10px; font-size: 14px;")

    def buy_tickets(self):
        """Обработчик покупки билетов"""
        if not self.selected_seats:
            QMessageBox.warning(self, "No Seats Selected", "Please select at least one seat before buying.")
            return

        seats = ", ".join(sorted(self.selected_seats))
        QMessageBox.information(self, "Purchase Successful", f"Seats purchased: {seats}")
        self.accept()  # Закрыть диалог после покупки