
import os
from datetime import datetime
from urllib.parse import quote_plus

from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Initialize Flask application
app = Flask(__name__)

# MongoDB configuration from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
MONGO_HOST = os.getenv(
    "MONGO_HOST",
    "mongodb.faralpha.svc.cluster.local"
)

# Construct authenticated MongoDB connection URI
MONGODB_URI = (
    f"mongodb://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}"
    f"@{MONGO_HOST}:27017/flask_db?authSource=admin"
)

# Connect to MongoDB
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

# Select database and collection
db = client["flask_db"]
collection = db["data"]


# Root endpoint: Welcome message with current time
@app.route("/", methods=["GET"])
def home():
    current_time = datetime.now().astimezone()
    return (
        f"Welcome to the Flask app! "
        f"The current time is: {current_time}"
    ), 200


# Health endpoint for Kubernetes probes
@app.route("/health", methods=["GET"])
def health():
    try:
        client.admin.command("ping")
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except PyMongoError:
        app.logger.exception("MongoDB health check failed")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


# Data endpoint: Insert and retrieve MongoDB records
@app.route("/data", methods=["GET", "POST"])
def data():

    if request.method == "POST":
        record = request.get_json(silent=True)

        if not isinstance(record, dict) or not record:
            return jsonify({
                "error": "Please provide a non-empty JSON object."
            }), 400

        try:
            collection.insert_one(record)
            return jsonify({
                "status": "Data inserted"
            }), 201

        except PyMongoError:
            app.logger.exception("MongoDB insert failed")
            return jsonify({
                "error": "Database operation failed"
            }), 500

    elif request.method == "GET":
        try:
            records = list(
                collection.find({}, {"_id": 0})
            )
            return jsonify(records), 200

        except PyMongoError:
            app.logger.exception("MongoDB read failed")
            return jsonify({
                "error": "Database operation failed"
            }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
