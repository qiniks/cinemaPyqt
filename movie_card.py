from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MovieCard(QFrame):
    def __init__(self, title, image_path):
        super().__init__()
        self.title = title
        self.image_path = image_path
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(220, 320)

        layout = QVBoxLayout()
        pixmap = QPixmap(self.image_path).scaled(220, 320, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        text_container = QLabel(self.title)
        text_container.setFixedSize(220, 50)
        text_container.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(text_container)
        self.setLayout(layout)

        self.mousePressEvent = self.on_click

    def on_click(self, event):
        QMessageBox.information(self, "Movie Info", f"Title: {self.title}")
