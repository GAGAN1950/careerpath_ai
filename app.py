from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from database import initialize_database, get_connection
from ai_engine import recommend_careers

import json
import os

app = Flask(__name__)

CORS(app)

initialize_database()


# -------------------------
# Home
# -------------------------

@app.route("/")
def home():

    frontend_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "frontend"
    )

    return send_from_directory(
        frontend_path,
        "index.html"
    )


# -------------------------
# Register User
# -------------------------

@app.route("/api/register", methods=["POST"])
def register():

    data = request.json

    name = data.get("name")
    email = data.get("email")

    if not name or not email:

        return jsonify({
            "error": "Name and email are required"
        }), 400

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email)
            VALUES (?, ?)
            """,
            (name, email)
        )

        user_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        })

    except Exception:

        return jsonify({
            "error": "Email already exists"
        }), 400


# -------------------------
# Career Assessment
# -------------------------

@app.route("/api/assessment", methods=["POST"])
def assessment():

    data = request.json

    user_id = data.get("user_id")
    skills = data.get("skills", [])
    interests = data.get("interests", [])
    goal = data.get("goal", "")

    results = recommend_careers(
        skills,
        interests
    )

    # Save assessment

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO assessments
        (user_id, skills, interests, goal)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            json.dumps(skills),
            json.dumps(interests),
            goal
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "goal": goal,
        "recommendations": results
    })


# -------------------------
# Get Careers
# -------------------------

@app.route("/api/careers", methods=["GET"])
def careers():

    careers = [
        "Cybersecurity Engineer",
        "Cloud Engineer",
        "Data Scientist"
        "Web Developer"
    ]

    return jsonify(careers)


# -------------------------
# Run Server
# -------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )