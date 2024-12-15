from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, \
    QApplication

from add_movie_dialog import AddMovieDialog
from app import app_data
from movie_card import MovieCard
from profile_window import ProfileWindow
from remove_movie_dialog import RemoveMovieDialog
from seat_selection import SeatSelectionWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.username = None
        self.is_admin = True  # Флаг для проверки администратора
        self.movies = app_data.movies
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_container = QWidget()
        self.scroll_container.setLayout(self.movie_layout)
        self.scroll_area.setWidget(self.scroll_container)

        # Виджет расписания фильмов
        self.schedule_widget = QWidget()
        self.schedule_widget_layout = QVBoxLayout()
        self.schedule_widget.setLayout(self.schedule_widget_layout)
        self.schedule_widget.hide()  # Прячем расписание при старте

        layout.addLayout(self.header)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.schedule_widget)

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
        app_data.remove_movie(title)
        self.update_movies()

    def add_movie(self, title, image_path, showtimes):
        app_data.add_movie(title, image_path, showtimes)
        self.update_movies()

    def update_movies(self):
        print('update_movies')
        for i in reversed(range(self.movie_layout.count())):  # Удаляем старые виджеты
            widget = self.movie_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, movie in enumerate(self.movies):  # Добавляем обновленные фильмы
            card = MovieCard(movie["title"], movie["image_path"], self.show_schedule, movie)
            self.movie_layout.addWidget(card, i // 4, i % 4)

    def show_schedule(self, movie):
        """Показывает расписание выбранного фильма"""
        self.scroll_area.hide()
        self.schedule_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.schedule_widget_layout.setSpacing(10)

        # Заголовок фильма
        title_label = QLabel(movie["title"])
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.schedule_widget_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Горизонтальный Layout для кнопок времени
        schedule_layout = QHBoxLayout()
        schedule_layout.setSpacing(10)  # Задаём расстояние между кнопками

        times = movie.get("schedule", [])
        if not times:
            no_schedule_label = QLabel("No schedule available.")
            no_schedule_label.setStyleSheet("font-size: 16px; color: gray;")
            self.schedule_widget_layout.addWidget(no_schedule_label, alignment=Qt.AlignCenter)
        else:
            for time in times:
                button = QPushButton(time)
                button.setFixedSize(100, 50)
                # button.setStyleSheet("color: black; border: 3px solid #FFFFFF; background-color: transparent;")
                # button.setStyleSheet("padding: 10px; font-size: 16px;")
                button.clicked.connect(lambda _, t=time: self.open_seat_selection(movie, t))
                schedule_layout.addWidget(button)  # Добавляем кнопку в горизонтальный Layout

        self.schedule_widget_layout.addLayout(schedule_layout)  # Добавляем горизонтальный Layout в общий Layout

        # Кнопка "Back"
        back_button = QPushButton("Back")
        back_button.setStyleSheet("padding: 10px; font-size: 16px; margin-top: 20px;")
        back_button.clicked.connect(self.show_movie_list)
        self.schedule_widget_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.schedule_widget.show()

    def open_seat_selection(self, movie, time):
        try:
            print(f"Opening seat selection for movie: {movie['title']} time: {time}")
            seat_selection_dialog = SeatSelectionWindow(self.username, movie["title"], time)
            seat_selection_dialog.exec()
        except Exception as e:
            print(f"Error in open_seat_selection: {e}")

    def show_movie_list(self):
        """Показывает список фильмов"""
        # Удаляем все виджеты из schedule_widget_layout
        for i in reversed(range(self.schedule_widget_layout.count())):
            item = self.schedule_widget_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    layout = item.layout()
                    if layout:
                        while layout.count():
                            child = layout.takeAt(0)
                            if child.widget():
                                child.widget().deleteLater()
                        layout.deleteLater()

        self.schedule_widget.hide()
        self.scroll_area.show()
