from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MovieCard(QPushButton):
    def __init__(self, title, image_path, callback, movie):
        super().__init__()
        self.title = title
        self.callback = callback
        self.movie = movie
        self.image_path = image_path
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(220, 320)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Картинка
        pixmap = QPixmap(self.image_path).scaled(
            220, 320, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Текстовое поле
        text_container = QLabel(self.title)
        text_container.setFixedSize(220, 30)
        text_container.setStyleSheet(
            "color: white; font-size: 16px; background-color: rgb(200, 100, 255);"
        )
        text_container.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(text_container)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.clicked.connect(self.on_click)

    def on_click(self):
        self.callback(self.movie)
