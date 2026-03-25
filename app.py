from __future__ import annotations

from flask import Flask, jsonify


app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        {
            "service": "transparent-api-service",
            "message": "Transparent backend starter is running.",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

