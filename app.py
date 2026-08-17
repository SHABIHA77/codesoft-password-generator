from flask import Flask, render_template, request, jsonify
import string
import secrets

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def home():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)