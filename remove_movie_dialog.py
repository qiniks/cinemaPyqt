import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

from res.styles import WELCOME_STYLE


class RemoveMovieDialog(QDialog):
    def __init__(self, movies, api_url):
        super().__init__()
        self.movies = movies
        self.api_url = api_url
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Remove Movie")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Remove Movie")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(WELCOME_STYLE)

        self.movie_selector = QComboBox()
        self.movie_selector.addItems([movie["title"] for movie in self.movies])

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_movie)

        layout.addWidget(self.label)
        layout.addWidget(self.movie_selector)
        layout.addWidget(remove_button)

        self.setLayout(layout)

    def remove_movie(self):
        selected_title = self.movie_selector.currentText()

        if not selected_title:
            QMessageBox.warning(self, "Error", "No movie selected.")
            return

        try:
            response = requests.delete(f"{self.api_url}/movies/{selected_title}")
            if response.status_code == 200:
                QMessageBox.information(self, "Success", f"Movie '{selected_title}' removed successfully!")
                self.accept()
            elif response.status_code == 404:
                QMessageBox.warning(self, "Error", f"Movie '{selected_title}' not found on the server.")
            else:
                QMessageBox.warning(self, "Error", f"Failed to remove movie: {response.text}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Server Error", f"Unable to connect to server: {e}")
