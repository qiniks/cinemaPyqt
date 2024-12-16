import requests
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
)


class MovieEditDialog(QDialog):
    def __init__(self, movie, api_url, parent=None):
        super().__init__(parent)
        self.movie = movie
        self.api_url = api_url
        self.setWindowTitle(f"Редактирование фильма: {movie['title']}")
        self.setFixedSize(400, 500)

        # Поле для изменения пути картинки
        image_path_label = QLabel("Путь к картинке:")
        self.image_path_edit = QLineEdit(movie["image_path"])

        # Поле для изменения расписания
        schedule_label = QLabel("Расписание (через запятую):")
        self.schedule_edit = QLineEdit(",".join(movie["schedule"]))

        # Поле для выбора сеанса
        session_label = QLabel("Выберите сеанс для отчета:")
        self.session_combo = QComboBox()
        self.session_combo.addItem("Все сеансы")
        self.session_combo.addItems(movie["schedule"])
        self.session_combo.currentIndexChanged.connect(self.generate_report)

        # Поле с отчетом
        report_label = QLabel("Отчет:")
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.generate_report()  # Инициализация отчета для первого сеанса

        # Кнопка "Сохранить изменения"
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_movie_changes)

        # Расположение виджетов
        layout = QVBoxLayout()
        layout.addWidget(image_path_label)
        layout.addWidget(self.image_path_edit)
        layout.addWidget(schedule_label)
        layout.addWidget(self.schedule_edit)
        layout.addWidget(session_label)
        layout.addWidget(self.session_combo)
        layout.addWidget(report_label)
        layout.addWidget(self.report_text)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def generate_report(self):
        report_lines = []

        session = self.session_combo.currentText()

        if session == "Все сеансы":
            # Общий отчёт по фильму
            total_tickets = sum(len(seats) for seats in self.movie["seats"].values())
            report_lines.append(f"Общее количество проданных билетов: {total_tickets}")

            for time, seats in self.movie["seats"].items():
                report_lines.append(f"\nСеанс: {time}")
                report_lines.append(f"  Забронировано мест: {len(seats)}")

                if seats:
                    for seat, user in seats.items():
                        report_lines.append(f"    Место: {seat} - Пользователь: {user}")
                else:
                    report_lines.append("    Нет забронированных мест.")
        elif session in self.movie["seats"]:
            # Отчёт по конкретному сеансу
            booked_seats = self.movie["seats"][session]
            report_lines.append(f"Сеанс: {session}")
            report_lines.append(f"Количество забронированных мест: {len(booked_seats)}")

            if booked_seats:
                report_lines.append("Забронированные места:")
                for seat, user in booked_seats.items():
                    report_lines.append(f"  Место: {seat} - Пользователь: {user}")
            else:
                report_lines.append("Нет забронированных мест.")
        else:
            report_lines.append(f"Сеанс {session} отсутствует в расписании.")

        self.report_text.setText("\n".join(report_lines))

    def save_movie_changes(self):
        import re
        """Сохраняет изменения фильма с отправкой на Flask сервер"""
        new_image_path = self.image_path_edit.text()
        new_schedule_text = self.schedule_edit.text()

        # Проверка расписания (валидация ввода)
        new_schedule = [time.strip() for time in new_schedule_text.split(",") if time.strip()]
        valid_schedule = []
        invalid_times = []

        time_pattern = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')  # Регулярное выражение для проверки формата HH:MM

        for time in new_schedule:
            if not time_pattern.match(time):
                invalid_times.append(time)
            else:
                valid_schedule.append(time)

        if invalid_times:
            QMessageBox.warning(
                self,
                "Некорректное расписание",
                "Пожалуйста, введите время в формате HH:MM."
            )
            return

        # Обновляем слоты для новых сеансов
        if "seats" not in self.movie:
            self.movie["seats"] = {time: [] for time in valid_schedule}
        else:
            for time in valid_schedule:
                if time not in self.movie["seats"]:
                    self.movie["seats"][time] = []

        # Удаляем слоты для сеансов, которые больше не присутствуют в расписании
        for time in list(self.movie["seats"].keys()):
            if time not in valid_schedule:
                del self.movie["seats"][time]

        # Обновляем список сеансов в комбобоксе
        self.session_combo.clear()
        self.session_combo.addItem("Все сеансы")
        self.session_combo.addItems(valid_schedule)

        # Отправка данных на сервер
        payload = {
            "title": self.movie["title"],
            "image_path": new_image_path,
            "schedule": valid_schedule
        }

        try:
            response = requests.post(f"{self.api_url}/update_movie", json=payload)
            if response.status_code == 200:
                QMessageBox.information(self, "Успешно", "Изменения сохранены!")
                self.accept()
            else:
                error_message = response.json().get("error", "Неизвестная ошибка")
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {error_message}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к серверу: {e}")
