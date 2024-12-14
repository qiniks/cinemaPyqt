from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from seat_selection import SeatSelectionWindow


class MovieDetailsWindow(QWidget):
    def __init__(self, movie, username, main_window):
        super().__init__()
        self.movie = movie
        self.username = username
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.movie["title"])
        self.setFixedSize(1280, 832)

        layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel(self.movie["title"])
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addLayout(header_layout)

        # Schedule buttons
        schedule_layout = QHBoxLayout()
        times = self.movie.get("schedule", [])
        if not times:  # Если расписание пустое, показываем сообщение
            no_schedule_label = QLabel("No schedule available for this movie.")
            no_schedule_label.setStyleSheet("font-size: 16px; color: gray;")
            schedule_layout.addWidget(no_schedule_label, alignment=Qt.AlignCenter)
        else:
            for time in times:
                button = QPushButton(time)
                button.setStyleSheet("padding: 10px; font-size: 16px;")
                button.clicked.connect(lambda _, t=time: self.open_seat_selection(t))
                schedule_layout.addWidget(button, alignment=Qt.AlignCenter)

        layout.addLayout(schedule_layout)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("padding: 10px; font-size: 16px; margin-top: 20px;")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def go_back(self):
        """Возвращение к основному окну"""
        self.main_window.show()  # Показываем основное окно
        self.close()  # Закрываем окно с расписанием

    def open_seat_selection(self, time):
        try:
            print(f"Opening seat selection for movie: {self.movie['title']}, time: {time}")
            seat_selection_dialog = SeatSelectionWindow(self.username, self.movie["title"], time)
            seat_selection_dialog.exec()
        except Exception as e:
            print(f"Error in open_seat_selection: {e}")



