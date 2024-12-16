import re
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox


class AddMovieDialog(QDialog):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url  # Базовый URL для API
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Movie")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Movie Title")

        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("Image Path")

        self.schedule_input = QLineEdit()
        self.schedule_input.setPlaceholderText("Showtimes (e.g., 10:00, 14:00, 18:00)")

        add_button = QPushButton("Add Movie")
        add_button.clicked.connect(self.add_movie)

        layout.addWidget(QLabel("Add a new movie"))
        layout.addWidget(self.title_input)
        layout.addWidget(self.image_path_input)
        layout.addWidget(self.schedule_input)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_movie(self):
        title = self.title_input.text().strip()
        image_path = self.image_path_input.text().strip()
        schedule = self.schedule_input.text().strip()

        if not title or not image_path or not schedule:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Проверяем формат времени
        showtimes = [time.strip() for time in schedule.split(",") if time.strip()]
        valid_schedule = []
        invalid_times = []

        time_pattern = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
        for time in showtimes:
            if time_pattern.match(time):
                valid_schedule.append(time)
            else:
                invalid_times.append(time)

        if invalid_times:
            QMessageBox.warning(
                self,
                "Invalid Schedule",
                f"Invalid times: {', '.join(invalid_times)}. Please use HH:MM format."
            )
            return

        # Отправляем данные на сервер
        movie_data = {
            "title": title,
            "image_path": image_path,
            "schedule": valid_schedule
        }

        try:
            response = requests.post(f"{self.api_url}/movies", json=movie_data)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Movie added successfully!")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"Failed to add movie: {response.text}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Server Error", f"Unable to connect to server: {e}")
