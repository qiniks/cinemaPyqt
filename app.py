from flask import Flask, jsonify, request

# from app_data import app_data

app = Flask(__name__)


class AppData:
    def __init__(self):
        self.users = {
            "admin": {"username": "admin", "number": "0700162010", "password": "123", "bookings": [], "is_admin": True},
            "test": {"username": "test", "number": "test", "password": "1", "bookings": [{
                "movie_title": 'test',
                "time": 'test',
                "seat": 'test'
            }], "is_admin": True},
        }
        self.movies = [
            {"title": "Moana", "image_path": r"res\moana.jpeg", "schedule": ["10:00", "14:00", "18:00"],
             "seats": {
                 "10:00": {"3-A": "User1", "3-B": "User2"},
                 "14:00": {},
                 "18:00": {}
             }},
            {"title": "Spider man", "image_path": r"res\spider_man.png", "schedule": ["16:00", "20:00"],
             "seats": {
                 "16:00": {},
                 "20:00": {}
             }},
            {"title": "Solo leveling", "image_path": r"res\solo.png", "schedule": ["15:00", "19:00"],
             "seats": {
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
                                "seats": {time: {} for time in schedule}})
            print(self.movies[-1])

    def remove_movie(self, title):
        for movie in self.movies:
            if movie["title"] == title:
                self.movies.remove(movie)
                print(title + " removed")
                return True
        return False

    def book_seat(self, username, movie_title, time, seat):
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        if movie is None:
            return False

        if time not in movie["seats"]:
            return False

        if seat in movie["seats"][time]:
            return False

        movie["seats"][time][seat] = username
        self.users[username]["bookings"].append({
            "movie_title": movie_title,
            "time": time,
            "seat": seat
        })

        return True

    def taken_seats(self, movie_title, time):
        movie = next((m for m in self.movies if m["title"] == movie_title), None)
        return movie["seats"][time]


app_data = AppData()


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    """Получение данных пользователя"""
    user = app_data.users.get(username)
    if user:
        return jsonify({
            "username": user["username"],
            "number": user["number"],
            "password": user["password"],
            "bookings": user["bookings"]
        })
    return jsonify({"error": "User not found"}), 404


@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    """Обновление данных пользователя"""
    user = app_data.users.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    new_number = data.get("number")
    new_password = data.get("password")

    if not new_number or not new_password:
        return jsonify({"error": "Missing fields"}), 400

    user["number"] = new_number
    user["password"] = new_password

    return jsonify({"message": "User updated successfully"})


# Маршрут для получения списка фильмов
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(app_data.movies)


# Маршрут для добавления фильма
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.json
    title = data.get('title')
    image_path = data.get('image_path')
    schedule = data.get('schedule')

    if title in [movie["title"] for movie in app_data.movies]:
        return jsonify({"error": "Movie already exists"}), 409

    app_data.add_movie(title, image_path, schedule)
    return jsonify({'message': 'Movie added'}), 201


@app.route('/movies/<title>', methods=['DELETE'])
def remove_movie(title):
    if app_data.remove_movie(title):
        return jsonify({"message": f"Movie '{title}' removed successfully"}), 200
    return jsonify({"error": "Movie not found"}), 404


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    number = data.get('number')
    password = data.get('password')

    if username in app_data.users:
        return jsonify({'error': 'User already exists'}), 400

    app_data.register_user(username, number, password)
    return jsonify({'message': f'User {username} registered'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if app_data.validate_user(username, password):
        return jsonify({'message': 'Login successful', 'is_admin': app_data.is_admin(username)})
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/update_movie', methods=['POST'])
def update_movie():
    data = request.json
    title = data.get('title')
    new_image_path = data.get('image_path')
    new_schedule = data.get('schedule')

    # Валидация
    if not title or not new_image_path or not new_schedule:
        return jsonify({"error": "Missing fields"}), 400

    # Найти фильм
    movie = next((m for m in app_data.movies if m["title"] == title), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Обновление данных
    movie["image_path"] = new_image_path
    movie["schedule"] = new_schedule
    movie["seats"] = {time: movie["seats"].get(time, {}) for time in new_schedule}

    return jsonify({"message": "Movie updated successfully", "movie": movie})


@app.route('/get_taken_seats', methods=['GET'])
def is_seats_taken():
    movie_id = request.args.get("movie_id")
    time = request.args.get("time")

    if not movie_id or not time:
        return jsonify({"error": "Missing parameters"}), 400

    return app_data.taken_seats(movie_id, time)


@app.route('/book_seat', methods=['POST'])
def book_seat():
    data = request.json
    username = data.get("username")
    movie_id = data.get("movie_id")
    time = data.get("time")
    seat = data.get("seat")

    if not all([username, movie_id, time, seat]):
        return jsonify({"error": "Missing fields"}), 400

    success = app_data.book_seat(username, movie_id, time, seat)
    if success:
        return jsonify({"message": "Seat booked successfully!"})
    else:
        return jsonify({"error": "Seat already taken"}), 409


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
