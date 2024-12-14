class AppData:
    def __init__(self):
        self.users = {}  # Данные пользователей: {user_id: {"username": str, "email": str, "bookings": []}}
        self.movies = [
            {"title": "Movie 1", "image_path": r"res\moana.jpeg", "schedule": ["10:00", "14:00", "18:00"],
             "seats": {  # Обязательное поле
                 "10:00": ["1-A", "1-B"],  # Уже занятые места
                 "14:00": [],
                 "18:00": []
             }},
            {"title": "Movie 2", "image_path": r"res\moana.jpeg", "schedule": ["12:00", "16:00", "20:00"],
             "seats": {  # Обязательное поле
                 "12:00": ["3-B", "1-C"],  # Уже занятые места
                 "16:00": [],
                 "20:00": []
             }},
            {"title": "Movie 3", "image_path": r"res\moana.jpeg", "schedule": ["11:00", "15:00", "19:00"],
             "seats": {  # Обязательное поле
                 "11:00": ["4-A", "1-D"],  # Уже занятые места
                 "15:00": [],
                 "19:00": []
             }}
        ]  # Данные фильмов: {"title": str, "schedule": [], "seats": {time: [list_of_seats]}}

    def add_user(self, username, number, password):
        if username not in self.users:
            self.users[username] = {"username": username, "number": number, "password": password, "bookings": []}
            print("User {} added".format(username))

    def add_movie(self, title, image_path, schedule):
        if title not in self.movies:
            self.movies.append({"title": title, "image_path": image_path, "schedule": schedule,
                                "seats": {time: [] for time in schedule}})
            print(self.movies[-1])

    def remove_movie(self, title):
        for movie in self.movies:
            if movie["title"] == title:
                self.movies.remove(movie)
                print(title + " removed")

    def book_seat(self, user_id, movie_title, time, seat):
        # Поиск фильма по title
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        if movie is None:
            return False  # Фильм не найден

        # Проверяем, существует ли указанное время и не занято ли место
        if time in movie["seats"] and seat not in movie["seats"][time]:
            movie["seats"][time].append(seat)  # Добавляем место как занятое

            # Добавляем информацию о бронировании для пользователя
            self.users[user_id]["bookings"].append({
                "movie_title": movie_title,
                "time": time,
                "seat": seat
            })
            return True  # Бронирование успешно

        return False  # Место уже занято или время отсутствует

    def is_seat_taken(self, movie_title, time, seat):
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        if movie is None:
            return False  # Фильм не найден

        return time in movie["seats"] and seat in movie["seats"][time]

    def validate_user(self, username, password):
        if username in self.users:
            if password == self.users[username]["password"]:
                return True


# Создаем глобальный объект для данных
app_data = AppData()
