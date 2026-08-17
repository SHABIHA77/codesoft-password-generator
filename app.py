from flask import Flask, render_template, request, jsonify
import secrets
import string

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_password():

    data = request.get_json()

    length = int(data.get("length", 12))

    if length < 4 or length > 100:
        return jsonify({
            "error": "Password length must be between 4 and 100."
        }), 400

    characters = ""

    if data.get("uppercase"):
        characters += string.ascii_uppercase

    if data.get("lowercase"):
        characters += string.ascii_lowercase

    if data.get("numbers"):
        characters += string.digits

    if data.get("symbols"):
        characters += string.punctuation

    if not characters:
        return jsonify({
            "error": "Please select at least one character type."
        }), 400

    password = ""

    for i in range(length):
        password += secrets.choice(characters)

    return jsonify({
        "password": password
    })


if __name__ == "__main__":
    app.run(debug=True)