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
    "auth_plugin": "mysql_native_password",
}

app = Flask(__name__)
CORS(app)
conn = mysql.connector.connect(**db_config)

SECRET_KEY = "super_secret"


def generate_jwt(user_id):
    expiration_date = str(gmtime().tm_hour + 1)
    payload = {"user_id": user_id, "exp": expiration_date}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/hour", methods=["POST"])
def get_hour():
    data = request.get_json()
    token = data["authToken"]
    if token:
        payload = verify_jwt(token)
        if payload:
            return jsonify({"hour": gmtime().tm_hour, "min": gmtime().tm_min})
    return jsonify({"message": "Unauthorized"}), 401


@app.route("/api/verifyjwt", methods=["POST"])
def verify_jwt_route():
    data = request.get_json()
    token = data["authToken"]
    if token:
        payload = verify_jwt(token)
        if payload:
            return {"authenticated": True}
    return {"authenticated": False}


@app.route("/api/register", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        print("Try to find username")
        if not exists_username(username):
            print("Username not found")
            return {"registered": register_user(username, password)}
        print("Username found")
        return {"registered": False}
    return {"registered": False}


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if verify_password(username, password):
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
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


def register_user(username: str, password: str):
    cursor = conn.cursor()
    try:
        salt = generate_salt(10)
        print("Lets")
        cursor.execute(
            """INSERT
                    INTO
                    user (username, salt, password)
                    VALUES(%(username)s, %(salt)s, %(password)s);
                """,
            {
                "username": username,
                "salt": salt,
                "password": hash_password(password, salt),
            },
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False
    finally:
        cursor.close()


def generate_salt(length=10):
    """Génère un sel aléatoire de longueur spécifiée (max 10)."""
    salt = os.urandom(length)  # Génère un sel aléatoire
    return salt.hex()[
        :length
    ]  # Convertit le sel en hex et le tronque à la longueur voulue


def verify_password(username: str, password: str) -> bool:
    cursor = conn.cursor(dictionary=True)
    try:
        print("fetching username", username)
        # Effectuer une requête SELECT
        cursor.execute(
            """
            SELECT
                salt,password
            FROM
                user
            WHERE
                username = %(username)s
        """,
            {"username": username},
        )
        result = cursor.fetchone()
        hashed_password = hash_password(password, result.get("salt"))  # type: ignore
        if hashed_password == result.get("password"):  # type: ignore
            print("OKAY")
            return True
        else:
            print("Pas Okay")
            return False
    except mysql.connector.Error:
        return False
    finally:
        cursor.close()


def exists_username(username: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                admin
            FROM
                user
            WHERE
                username = %(username)s
        """,
            {"username": username},
        )
        result = cursor.fetchone()
        print(result)
        if result:
            print(result)
            return False
        # Afficher les résultats dans la page
        return True

    except mysql.connector.Error:
        return False
    finally:
        cursor.close()


def hash_password(plain_password, salt):
    """Hache le mot de passe en utilisant SHA-256 après avoir ajouté un sel."""

    # Ajoute le sel au mot de passe en clair
    salted_password = plain_password + salt

    # Hache le mot de passe salé avec SHA-256
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    return hashed_password


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.4", port=5000)
