from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox


class RemoveMovieDialog(QDialog):
    def __init__(self, movies, remove_movie_callback):
        super().__init__()
        self.movies = movies
        self.remove_movie_callback = remove_movie_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Remove Movie")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.movie_selector = QComboBox()
        self.movie_selector.addItems([movie["title"] for movie in self.movies])

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_movie)

        layout.addWidget(QLabel("Select a movie to remove"))
        layout.addWidget(self.movie_selector)
        layout.addWidget(remove_button)

        self.setLayout(layout)

    def remove_movie(self):
        selected_title = self.movie_selector.currentText()

        if selected_title:
            self.remove_movie_callback(selected_title)
            QMessageBox.information(self, "Success", f"Movie '{selected_title}' removed successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No movie selected.")
