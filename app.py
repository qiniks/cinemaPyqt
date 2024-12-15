class AppData:
    def __init__(self):
        self.users = {
            "admin": {"username": "admin", "number": "0700162010", "password": "123", "bookings": [], "is_admin": True},
        }
        self.movies = [
            {"title": "Movie 1", "image_path": r"res\moana.jpeg", "schedule": ["10:00", "14:00", "18:00"],
             "seats": {  # Обязательное поле
                 "10:00": {"A1": "User1", "A2": "User2"},
                 "14:00": {},
                 "18:00": {}
             }},
            {"title": "Movie 2", "image_path": r"res\moana.jpeg", "schedule": ["16:00", "20:00"],
             "seats": {  # Обязательное поле
                 "16:00": {},
                 "20:00": {}
             }},
            {"title": "Movie 3", "image_path": r"res\moana.jpeg", "schedule": ["15:00", "19:00"],
             "seats": {  # Обязательное поле
                 "15:00": {},
                 "19:00": {}
             }}
        ]  # Данные фильмов: {"title": str, "schedule": [], "seats": {time: [list_of_seats]}}

    def register_user(self, username, number, password):
        if username not in self.users:
            self.users[username] = {"username": username, "number": number, "password": password, "bookings": [],
                                    "is_admin": False}
            print("User {} added".format(username))

    def validate_user(self, username, password):
        if username in self.users:
            if password == self.users[username]["password"]:
                return True

    def is_admin(self, username):
        if username in self.users:
            return self.users[username]["is_admin"]
        return False

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

    def book_seat(self, username, movie_title, time, seat):
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        if movie is None:
            return False

        # Проверяем, существует ли указанное время в расписании
        if time not in movie["seats"]:
            return False  # Сеанс с таким временем не найден

        # Проверяем, не занято ли место
        if seat in movie["seats"][time]:
            return False  # Место уже занято

        movie["seats"][time][seat] = username
        self.users[username]["bookings"].append({
            "movie_title": movie_title,
            "time": time,
            "seat": seat
        })

        return True

    def is_seat_taken(self, movie_title, time, seat):
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        if movie is None:
            return False  # Фильм не найден

        return time in movie["seats"] and seat in movie["seats"][time]


# Создаем глобальный объект для данных
app_data = AppData()
