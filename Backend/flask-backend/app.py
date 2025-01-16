import token
from flask import Flask, jsonify, request
import jwt
from flask_cors import CORS
from time import gmtime

app = Flask(__name__)
CORS(app)


SECRET_KEY = "super_secret"


def generate_jwt(user_id):
    expiration_date = gmtime().tm_hour + 1
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
                    token: generate_jwt(username),
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


if __name__ == "__main__":
    app.run(debug=True)
