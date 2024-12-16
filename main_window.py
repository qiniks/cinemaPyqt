import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, \
    QApplication, QCheckBox, QMessageBox, QDialog, QLineEdit, QTextEdit
from pyqtcaptcha import Captcha, CaptchaDifficulty

from add_movie_dialog import AddMovieDialog
from app_data import app_data
from movie_card import MovieCard
from movie_edit import MovieEditDialog
from profile_window import ProfileWindow
from remove_movie_dialog import RemoveMovieDialog
from seat_selection import SeatSelectionWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.api_url = "http://127.0.0.1:5000"
        self.api_url = "https://qiniks.pythonanywhere.com"
        self.username = None
        self.is_admin = False
        self.edit_mode = False
        self.movies = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MOVAI")
        self.setFixedSize(1280, 832)
        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        self.header = QHBoxLayout()
        self.header.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("MOVAI")
        title_label.setStyleSheet("font-size: 52px; font-weight: bold; font-family: Agency FB")

        self.login_button = QPushButton("Sign In")
        self.login_button.setStyleSheet("color: #373737; border: 1px solid #373737; background-color: white;")
        self.login_button.clicked.connect(self.open_login)

        self.register_button = QPushButton("Sign Up")
        self.register_button.clicked.connect(self.open_register)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_movies)

        self.profile_button = QPushButton("Profile")
        self.profile_button.clicked.connect(self.open_profile)
        self.profile_button.hide()

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("background-color: green; color: white;")
        self.add_button.clicked.connect(self.open_add_movie_dialog)
        self.add_button.hide()

        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet("background-color: red; color: white;")
        self.remove_button.clicked.connect(self.open_remove_movie_dialog)
        self.remove_button.hide()

        self.edit_mode_checkbox = QPushButton("Edit Mode")
        self.edit_mode_checkbox.setCheckable(True)
        self.edit_mode_checkbox.toggled.connect(self.toggle_edit_mode)
        self.edit_mode_checkbox.hide()

        self.header.addWidget(title_label)
        self.header.addStretch()
        self.header.addWidget(self.refresh_button)
        self.header.addWidget(self.login_button)
        self.header.addWidget(self.register_button)
        self.header.addWidget(self.profile_button)
        self.header.addWidget(self.add_button)
        self.header.addWidget(self.remove_button)
        self.header.addWidget(self.edit_mode_checkbox)

        self.captcha = Captcha()
        self.captcha.setDifficulty(CaptchaDifficulty.EASY)
        self.captcha.passed.connect(self.show_header)

        # Карточки фильмов
        self.movie_layout = QGridLayout()
        self.update_movies()

        # фильмы
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_container = QWidget()
        self.scroll_area.setStyleSheet('border: 0px')
        self.scroll_container.setLayout(self.movie_layout)
        self.scroll_area.setWidget(self.scroll_container)

        # расписание
        self.schedule_widget = QWidget()
        self.schedule_widget_layout = QVBoxLayout()
        self.schedule_widget.setLayout(self.schedule_widget_layout)
        self.schedule_widget.hide()
        layout.addLayout(self.header)
        layout.addWidget(self.captcha)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.schedule_widget)

        self.setLayout(layout)

    def show_header(self):
        self.captcha.hide()

    def open_login(self):
        if self.captcha.isPassed():
            from login_dialog import LoginDialog
            dialog = LoginDialog(self.api_url, self.update_user_state)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Captha", "Solve captcha first!.")

    def open_register(self):
        if self.captcha.isPassed():
            from register_dialog import RegisterDialog
            dialog = RegisterDialog(self.api_url, self.update_user_state)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Captha", "Solve captcha first!.")

    def update_user_state(self, username):
        """Обновляет состояние интерфейса при входе в аккаунт"""
        self.username = username
        self.is_admin = app_data.is_admin(self.username)
        self.login_button.hide()
        self.register_button.hide()
        self.profile_button.show()
        self.add_button.setVisible(self.is_admin)
        self.remove_button.setVisible(self.is_admin)
        self.edit_mode_checkbox.setVisible(self.is_admin)

    def open_profile(self):
        """Открывает окно профиля"""
        self.profile_window = ProfileWindow(self.username, self.logout, self.api_url)
        self.profile_window.show()

    def logout(self):
        """Обновляет состояние интерфейса после выхода из аккаунта"""
        self.username = None
        self.login_button.show()
        self.register_button.show()
        self.profile_button.hide()
        self.add_button.hide()
        self.remove_button.hide()
        self.edit_mode_checkbox.hide()
        self.edit_mode = False

    def open_add_movie_dialog(self):
        dialog = AddMovieDialog(self.api_url)
        if dialog.exec_():
            self.update_movies()

    def open_remove_movie_dialog(self):
        dialog = RemoveMovieDialog(self.movies, self.api_url)
        if dialog.exec_():
            self.update_movies()

    def update_movies(self):
        try:
            response = requests.get(f"{self.api_url}/movies")
            print(response, response.text)
            if response.status_code == 200:
                self.movies = response.json()
            else:
                QMessageBox.warning(self, "Error", "Unable to fetch movies from the server.")
        except requests.RequestException:
            QMessageBox.critical(self, "Error", f"Server connection failed")

        # Очищаем старые виджеты
        for i in reversed(range(self.movie_layout.count())):
            widget = self.movie_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Добавляем обновленные карточки фильмов
        for i, movie in enumerate(self.movies):
            card = MovieCard(movie["title"], movie["image_path"], self.show_schedule, movie)
            self.movie_layout.addWidget(card, i // 4, i % 4)

    def show_schedule(self, movie):
        if self.edit_mode:
            self.open_movie_edit_dialog(movie)
        else:
            # удаление содержимого слоя
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

            """Показывает расписание выбранного фильма"""
            self.scroll_area.hide()
            self.schedule_widget_layout.setContentsMargins(0, 0, 0, 0)
            self.schedule_widget_layout.setSpacing(10)

            title_label = QLabel(movie["title"])
            title_label.setStyleSheet("font-size: 48px; font-weight: bold; font-family: Agency FB")
            self.schedule_widget_layout.addWidget(title_label, alignment=Qt.AlignCenter)

            schedule_layout = QHBoxLayout()
            schedule_layout.setSpacing(10)

            times = movie.get("schedule", [])
            if not times:
                no_schedule_label = QLabel("No schedule available.")
                no_schedule_label.setStyleSheet("font-size: 16px; color: gray;")
                self.schedule_widget_layout.addWidget(no_schedule_label, alignment=Qt.AlignCenter)
            else:
                for time in times:
                    button = QPushButton(time)
                    button.setFixedSize(100, 50)
                    button.setStyleSheet(
                        "color: black; border: 3px solid #373737; background-color: white;")
                    button.clicked.connect(lambda _, t=time: self.open_seat_selection(movie, t))
                    schedule_layout.addWidget(button)

            self.schedule_widget_layout.addLayout(schedule_layout)

            back_button = QPushButton("Back")
            back_button.setStyleSheet("font-size: 24px; margin-top: 20px;padding: 10px")
            back_button.clicked.connect(self.show_movie_list)
            self.schedule_widget_layout.addWidget(back_button, alignment=Qt.AlignCenter)

            self.schedule_widget.show()

    def open_seat_selection(self, movie, time):
        try:
            print(f"Opening seat selection for movie: {movie['title']} time: {time}")
            seat_selection_dialog = SeatSelectionWindow(self.username, movie["title"], time, self.api_url)
            seat_selection_dialog.exec()
        except Exception as e:
            print(e)

    def show_movie_list(self):
        self.schedule_widget.hide()
        self.scroll_area.show()

    def toggle_edit_mode(self, checked):
        self.edit_mode = checked
        if checked:
            self.edit_mode_checkbox.setStyleSheet("background-color: green;")
        else:
            self.edit_mode_checkbox.setStyleSheet("background-color: #373737;")

    def open_movie_edit_dialog(self, movie):
        dialog = MovieEditDialog(movie, self.api_url, self)
        if dialog.exec_():
            self.update_movies()
