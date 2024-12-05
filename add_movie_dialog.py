from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox


class AddMovieDialog(QDialog):
    def __init__(self, add_movie_callback):
        super().__init__()
        self.add_movie_callback = add_movie_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Movie")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Movie Title")

        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("Image Path")

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_movie)

        layout.addWidget(QLabel("Add a new movie"))
        layout.addWidget(self.title_input)
        layout.addWidget(self.image_path_input)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_movie(self):
        title = self.title_input.text()
        image_path = self.image_path_input.text()

        if title and image_path:
            self.add_movie_callback(title, image_path)
            QMessageBox.information(self, "Success", "Movie added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "All fields are required.")
