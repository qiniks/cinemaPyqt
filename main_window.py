import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout
from add_movie_dialog import AddMovieDialog
from movie_card import MovieCard
from profile_window import ProfileWindow
from remove_movie_dialog import RemoveMovieDialog


class MainWindow(QWidget):
    SERVER_URL = "http://127.0.0.1:5000"  # URL сервера Flask

    def __init__(self):
        super().__init__()
        self.username = None
        self.is_admin = False  # По умолчанию пользователь не является администратором
        self.movies = []  # Список фильмов (будет загружен с сервера)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MOVAI")
        self.setFixedSize(1280, 832)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Верхняя панель
        self.header = QHBoxLayout()

        title_label = QLabel("MOVAI")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Кнопка входа
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.open_login)

        # Кнопка регистрации
        self.register_button = QPushButton("Sign Up")
        self.register_button.clicked.connect(self.open_register)

        # Кнопка профиля
        self.profile_button = QPushButton("Профиль")
        self.profile_button.clicked.connect(self.open_profile)
        self.profile_button.hide()  # Скрываем кнопку профиля до входа в аккаунт

        # Кнопки "Add" и "Remove" для администратора
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("background-color: green; color: white;")
        self.add_button.clicked.connect(self.open_add_movie_dialog)
        self.add_button.hide()  # Скрываем кнопку, пока пользователь не админ

        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet("background-color: red; color: white;")
        self.remove_button.clicked.connect(self.open_remove_movie_dialog)
        self.remove_button.hide()  # Скрываем кнопку, пока пользователь не админ

        self.header.addWidget(title_label)
        self.header.addStretch()
        self.header.addWidget(self.login_button)
        self.header.addWidget(self.register_button)
        self.header.addWidget(self.profile_button)
        self.header.addWidget(self.add_button)
        self.header.addWidget(self.remove_button)

        # Карточки фильмов
        self.movie_layout = QGridLayout()
        self.update_movies()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.movie_layout)
        scroll_area.setWidget(container)

        layout.addLayout(self.header)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Загружаем фильмы с сервера
        self.fetch_movies()

    def open_login(self):
        from login_dialog import LoginDialog
        dialog = LoginDialog(self.update_user_state)
        dialog.exec_()

    def open_register(self):
        from register_dialog import RegisterDialog
        dialog = RegisterDialog(self.update_user_state)
        dialog.exec_()

    def update_user_state(self, username):
        """Обновляет состояние интерфейса при входе в аккаунт"""
        self.username = username
        self.is_admin = self.check_if_admin(username)
        self.login_button.hide()
        self.register_button.hide()
        self.profile_button.show()
        self.add_button.setVisible(self.is_admin)
        self.remove_button.setVisible(self.is_admin)

    def open_profile(self):
        """Открывает окно профиля"""
        self.profile_window = ProfileWindow(self.username, self.logout)
        self.profile_window.show()

    def logout(self):
        """Обновляет состояние интерфейса после выхода из аккаунта"""
        self.username = None
        self.is_admin = False
        self.login_button.show()
        self.register_button.show()
        self.profile_button.hide()
        self.add_button.hide()
        self.remove_button.hide()

    def open_add_movie_dialog(self):
        """Открывает диалоговое окно для добавления фильма"""
        dialog = AddMovieDialog(self.add_movie)
        dialog.exec_()

    def open_remove_movie_dialog(self):
        """Открывает диалоговое окно для удаления фильма"""
        dialog = RemoveMovieDialog(self.movies, self.remove_movie)
        dialog.exec_()

    def add_movie(self, title, image_path):
        """Добавление фильма через сервер"""
        response = requests.post(f"{self.SERVER_URL}/movies", json={
            "title": title,
            "image_path": image_path
        })
        if response.status_code == 201:
            self.fetch_movies()  # Обновляем список фильмов

    def remove_movie(self, title):
        """Удаление фильма через сервер"""
        movie = next((movie for movie in self.movies if movie["title"] == title), None)
        if movie:
            response = requests.delete(f"{self.SERVER_URL}/movies/{movie['id']}")
            if response.status_code == 200:
                self.fetch_movies()  # Обновляем список фильмов

    def fetch_movies(self):
        """Получение списка фильмов с сервера"""
        response = requests.get(f"{self.SERVER_URL}/movies")
        if response.status_code == 200:
            self.movies = response.json()
            self.update_movies()

    def check_if_admin(self, username):
        """Проверяет, является ли пользователь администратором"""
        response = requests.get(f"{self.SERVER_URL}/users")
        if response.status_code == 200:
            users = response.json()
            user = next((u for u in users if u["username"] == username), None)
            return user and user.get("is_admin", False)
        return False

    def update_movies(self):
        """Обновляет отображение фильмов"""
        for i in reversed(range(self.movie_layout.count())):  # Удаляем старые виджеты
            widget = self.movie_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, movie in enumerate(self.movies):  # Добавляем обновленные фильмы
            card = MovieCard(movie["title"], movie["image_path"])
            self.movie_layout.addWidget(card, i // 4, i % 4)
