# app.py

class AppData:
    def __init__(self):
        self.users = {}  # Данные пользователей: {user_id: {"username": str, "email": str, "bookings": []}}
        self.movies = {}  # Данные фильмов: {movie_id: {"title": str, "schedule": [], "seats": {time: [list_of_seats]}}}

    def add_user(self, user_id, username, number):
        if user_id not in self.users:
            self.users[user_id] = {"username": username, "number": number, "bookings": []}

    def add_movie(self, movie_id, title, schedule):
        if movie_id not in self.movies:
            self.movies[movie_id] = {"title": title, "schedule": schedule, "seats": {time: [] for time in schedule}}

    def book_seat(self, user_id, movie_id, time, seat):
        if movie_id in self.movies and time in self.movies[movie_id]["seats"]:
            if seat not in self.movies[movie_id]["seats"][time]:
                self.movies[movie_id]["seats"][time].append(seat)
                self.users[user_id]["bookings"].append({"movie_id": movie_id, "time": time, "seat": seat})
                return True  # Бронирование успешно
        return False  # Место уже занято

    def is_seat_taken(self, movie_id, time, seat):
        return movie_id in self.movies and time in self.movies[movie_id]["seats"] and seat in self.movies[movie_id]["seats"][time]


# Создаем глобальный объект для данных
app_data = AppData()
