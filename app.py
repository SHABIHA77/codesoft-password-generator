from flask import Flask, render_template, request, jsonify
import string
import secrets
import sqlite3

app = Flask(__name__, static_folder="static", template_folder="templates")


# ---------------- DATABASE ----------------

def init_db():

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------- PASSWORD GENERATOR ----------------

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    length = int(data.get("length", 16))

    uppercase = data.get("uppercase", True)
    lowercase = data.get("lowercase", True)
    numbers = data.get("numbers", True)
    symbols = data.get("symbols", True)

    characters = ""

    if uppercase:
        characters += string.ascii_uppercase

    if lowercase:
        characters += string.ascii_lowercase

    if numbers:
        characters += string.digits

    if symbols:
        characters += string.punctuation

    if not characters:

        return jsonify({
            "error": "Please select at least one character type."
        }), 400

    if length < 4 or length > 100:

        return jsonify({
            "error": "Password length must be between 4 and 100."
        }), 400

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return jsonify({
        "password": password
    })


# ---------------- SUBMIT FEEDBACK ----------------

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():

    data = request.get_json()

    rating = data.get("rating")
    message = data.get("message")

    if not rating or not message:

        return jsonify({
            "success": False,
            "message": "Rating and feedback are required."
        }), 400

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback (rating, message) VALUES (?, ?)",
        (int(rating), message)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })


# ---------------- START DATABASE ----------------

init_db()


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app.run(debug=True)