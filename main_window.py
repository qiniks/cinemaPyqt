from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt
from movie_card import MovieCard
from login_dialog import LoginDialog
from register_dialog import RegisterDialog
from profile_window import ProfileWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.username = None  # Состояние пользователя
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MOVAI")
        self.setFixedSize(1280, 832)
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        # Верхняя панель
        self.header = QHBoxLayout()

        title_label = QLabel("MOVAI")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Кнопка входа
        self.login_button = QPushButton("Sign In")
        self.login_button.setStyleSheet("background-color: black; color: white; border-radius: 10px; padding: 10px;")
        self.login_button.clicked.connect(self.open_login)

        # Кнопка регистрации
        self.register_button = QPushButton("Sign Up")
        self.register_button.setStyleSheet("background-color: black; color: white; border-radius: 10px; padding: 10px;")
        self.register_button.clicked.connect(self.open_register)

        # Кнопка профиля
        self.profile_button = QPushButton("Профиль")
        self.profile_button.setStyleSheet("background-color: black; color: white; border-radius: 10px; padding: 10px;")
        self.profile_button.clicked.connect(self.open_profile)
        self.profile_button.hide()  # Скрываем кнопку профиля до входа в аккаунт

        self.header.addWidget(title_label)
        self.header.addStretch()
        self.header.addWidget(self.login_button)
        self.header.addWidget(self.register_button)
        self.header.addWidget(self.profile_button)

        # Карточки фильмов
        movie_layout = QGridLayout()
        for i in range(200):  # Заглушки для фильмов
            card = MovieCard(f"Movie {i + 1}", r"C:\Users\talan\PycharmProjects\PLanguage\pyqt\moana.jpeg")
            movie_layout.addWidget(card, i // 4, i % 4)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(movie_layout)
        scroll_area.setWidget(container)

        layout.addLayout(self.header)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def open_login(self):
        dialog = LoginDialog(self.update_user_state, self.open_register)
        dialog.exec_()

    def open_register(self):
        dialog = RegisterDialog(self.update_user_state)
        dialog.exec_()

    def update_user_state(self, username):
        """Обновляет состояние интерфейса при входе в аккаунт"""
        self.username = username
        self.login_button.hide()
        self.register_button.hide()
        self.profile_button.show()

    def open_profile(self):
        """Открывает окно профиля"""
        self.profile_window = ProfileWindow(self.username)
        self.profile_window.show()
