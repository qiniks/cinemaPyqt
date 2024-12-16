from flask import Flask, jsonify, request
from app_data import app_data  # Импортируйте ваш класс AppData

app = Flask(__name__)


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


# Маршрут для удаления фильма (только для админа)
@app.route('/movies/<title>', methods=['DELETE'])
def remove_movie(title):
    if app_data.remove_movie(title):
        return jsonify({"message": f"Movie '{title}' removed successfully"}), 200
    return jsonify({"error": "Movie not found"}), 404


# Маршрут для регистрации пользователя
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


# Маршрут для авторизации пользователя
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
