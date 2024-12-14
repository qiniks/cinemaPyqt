from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout

from add_movie_dialog import AddMovieDialog
from movie_card import MovieCard
from profile_window import ProfileWindow
from remove_movie_dialog import RemoveMovieDialog
from movie_schedule import MovieDetailsWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.username = None
        self.is_admin = True  # Флаг для проверки администратора
        self.movies = [
            {"title": "Movie 1", "image_path": r"res\moana.jpeg", "schedule": ["10:00", "14:00", "18:00"]},
            {"title": "Movie 2", "image_path": r"res\moana.jpeg", "schedule": ["12:00", "16:00", "20:00"]},
            {"title": "Movie 3", "image_path": r"res\moana.jpeg", "schedule": ["11:00", "15:00", "19:00"]}
        ]
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
        self.login_button.setStyleSheet("color: black; border: 1px solid #ccc; background-color: transparent;")
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
        # for i in range(200):  # Заглушки для фильмов
        #     card = MovieCard(f"Movie {i + 1}", r"res/moana.jpeg")
        #     self.movie_layout.addWidget(card, i // 4, i % 4)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.movie_layout)
        scroll_area.setWidget(container)

        layout.addLayout(self.header)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

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
        self.login_button.hide()
        self.register_button.hide()
        self.profile_button.show()
        self.add_button.setVisible(self.is_admin)
        self.remove_button.setVisible(self.is_admin)

    def open_profile(self):
        """Открывает окно профиля"""
        self.profile_window = ProfileWindow(self.username)
        self.profile_window.show()

    def open_profile(self):
        """Открывает окно профиля"""
        self.profile_window = ProfileWindow(self.username, self.logout)
        self.profile_window.show()

    def logout(self):
        """Обновляет состояние интерфейса после выхода из аккаунта"""
        self.username = None
        self.login_button.show()
        self.register_button.show()
        self.profile_button.hide()
        self.add_button.hide()
        self.remove_button.hide()

    def open_add_movie_dialog(self):
        dialog = AddMovieDialog(self.add_movie)
        dialog.exec_()

    def open_remove_movie_dialog(self):
        dialog = RemoveMovieDialog(self.movies, self.remove_movie)
        dialog.exec_()

    def remove_movie(self, title):
        self.movies = [movie for movie in self.movies if movie["title"] != title]
        self.update_movies()

    def add_movie(self, title, image_path, showtimes):
        self.movies.append({"title": title, "image_path": image_path, "schedule": showtimes})
        self.update_movies()

    def update_movies(self):
        for i in reversed(range(self.movie_layout.count())):  # Удаляем старые виджеты
            widget = self.movie_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, movie in enumerate(self.movies):  # Добавляем обновленные фильмы
            card = MovieCard(movie["title"], movie["image_path"], self.open_movie_details, movie)
            self.movie_layout.addWidget(card, i // 4, i % 4)

    def open_movie_details(self, movie):
        if movie:
            self.movie_details_window = MovieDetailsWindow(movie, self)
            self.movie_details_window.show()
            self.hide()
        else:
            print("Invalid movie data!")
