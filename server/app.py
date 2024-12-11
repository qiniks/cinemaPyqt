from flask import Flask, jsonify, request

app = Flask(__name__)

# Данные
users = [
    {"username": "admin", "phone": "123456789", "password": "admin123", "is_admin": True, "tickets": []},
    {"username": "1", "phone": "123456789", "password": "1", "is_admin": True, "tickets": []},
    {"username": "user1", "phone": "987654321", "password": "user123", "is_admin": False, "tickets": []}
]

movies = [
    {"title": "Movie 1", "image_path": "res/moana.jpeg"},
    {"title": "Movie 2", "image_path": "res/moana.jpeg"},
    {"title": "Movie 3", "image_path": "res/moana.jpeg"},
    {"title": "Movie 4", "image_path": "res/moana.jpeg"},
    {"title": "Movie 5", "image_path": "res/moana.jpeg"}
]


# Маршруты

# Главная страница
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Cinema API"})


# Получить список фильмов
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)


# Добавить фильм (только для админа)
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.json
    if not data or 'title' not in data or 'image_path' not in data:
        return jsonify({"error": "Invalid data"}), 400

    movies.append({"title": data['title'], "image_path": data['image_path']})
    return jsonify({"message": "Movie added successfully"}), 201


# Удалить фильм (только для админа)
@app.route('/movies/<title>', methods=['DELETE'])
def remove_movie(title):
    global movies
    movies = [movie for movie in movies if movie['title'] != title]
    return jsonify({"message": "Movie deleted successfully"})


# Авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid data"}), 400

    user = next((u for u in users if u['username'] == data['username'] and u['password'] == data['password']), None)
    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'phone' not in data or 'password' not in data:
        return jsonify({"error": "Invalid data"}), 400

    if any(u['username'] == data['username'] for u in users):
        return jsonify({"error": "Username already exists"}), 400

    new_user = {
        "username": data['username'],
        "phone": data['phone'],
        "password": data['password'],
        "is_admin": False,
        "tickets": []
    }
    users.append(new_user)
    return jsonify({"message": "User registered successfully"}), 201


# Покупка билета
@app.route('/buy_ticket', methods=['POST'])
def buy_ticket():
    data = request.json
    if not data or 'username' not in data or 'movie_title' not in data:
        return jsonify({"error": "Invalid data"}), 400

    user = next((u for u in users if u['username'] == data['username']), None)
    movie = next((m for m in movies if m['title'] == data['movie_title']), None)
    if user and movie:
        user['tickets'].append(movie['title'])
        return jsonify({"message": "Ticket purchased successfully"}), 200
    else:
        return jsonify({"error": "User or movie not found"}), 404


if __name__ == '__main__':
    app.run()
