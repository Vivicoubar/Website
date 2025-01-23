from flask import Flask, jsonify, request
import jwt
from flask_cors import CORS
from time import gmtime
import mysql.connector
import os
import hashlib

db_config = {
    "host": "192.168.0.5",  # L'adresse IP de votre serveur MySQL
    "user": "backend-user",  # Le nom d'utilisateur
    "password": "backend-password",  # Le mot de passe
    "database": "hour_api_db",  # Le nom de la base de données
}

app = Flask(__name__)
CORS(app)


SECRET_KEY = "super_secret"


def generate_jwt(user_id):
    expiration_date = str(gmtime().tm_hour + 1)
    payload = {"user_id": user_id, "exp": expiration_date}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/hour", methods=["GET"])
def get_hour():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]  # Extract token (remove "Bearer" part)
        payload = verify_jwt(token)
        if payload:
            return jsonify({"hour": gmtime().tm_hour, "min": gmtime().tm_min})
    return jsonify({"message": "Unauthorized"}), 401


@app.route("/api/verifyjwt", methods=["GET"])
def verify_jwt_route():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        payload = verify_jwt(token)
        if payload:
            return {"authenticated": True}
    return {"authenticated": False}


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if username == "admin" and password == "admin":
            return jsonify(
                {
                    "message": "Login successful!",
                    "result": True,
                    "token": generate_jwt(username),
                }
            )
        else:
            return jsonify({"message": "Login failed!", "result": False})
    else:
        return jsonify({"message": "Method not allowed!"})


def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


def generate_salt(length=10):
    """Génère un sel aléatoire de longueur spécifiée (max 10)."""
    salt = os.urandom(length)  # Génère un sel aléatoire
    return salt.hex()[
        :length
    ]  # Convertit le sel en hex et le tronque à la longueur voulue


def verify_password():
    try:
        # Se connecter à MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Effectuer une requête SELECT
        cursor.execute("SELECT * FROM ma_table;")
        result = cursor.fetchall()

        # Fermer la connexion
        cursor.close()
        conn.close()

        # Afficher les résultats dans la page
        return f"Résultats de la requête : {result}"

    except mysql.connector.Error as err:
        return f"Erreur : {err}"


def hash_password(plain_password):
    """Hache le mot de passe en utilisant SHA-256 après avoir ajouté un sel."""
    # Génère un sel aléatoire
    salt = generate_salt()

    # Ajoute le sel au mot de passe en clair
    salted_password = plain_password + salt

    # Hache le mot de passe salé avec SHA-256
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    return salt, hashed_password


if __name__ == "__main__":
    app.run(debug=True)
