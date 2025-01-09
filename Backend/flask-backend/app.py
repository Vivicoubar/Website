from flask import Flask, jsonify
from flask_cors import CORS
from time import gmtime

app = Flask(__name__)
CORS(app)


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello from Flask!"})


@app.route("/api/hour", methods=["GET"])
def get_hour():
    return jsonify({"hour": gmtime().tm_hour})


if __name__ == "__main__":
    app.run(debug=True)
