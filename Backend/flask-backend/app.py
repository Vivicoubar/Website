from flask import Flask, jsonify, request
from flask_cors import CORS
from time import gmtime

app = Flask(__name__)
CORS(app)


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/hour", methods=["GET"])
def get_hour():
    return jsonify({"hour": gmtime().tm_hour, "min": gmtime().tm_min})


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if username == "admin" and password == "admin":
            return jsonify({"message": "Login successful!", "result": True})
        else:
            return jsonify({"message": "Login failed!", "result": False})
    else:
        return jsonify({"message": "Method not allowed!"})


if __name__ == "__main__":
    app.run(debug=True)
