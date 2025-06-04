from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

CODES_FILE = "data/codes.json"

# -------- Fonctions Utilitaires --------
def load_codes():
    if os.path.exists(CODES_FILE):
        with open(CODES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_codes(codes):
    with open(CODES_FILE, "w") as f:
        json.dump(codes, f, indent=4)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# -------- Route Page de Connexion --------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/connect", methods=["POST"])
def connect():
    code = request.form["code"].strip().upper()
    codes = load_codes()

    if code not in codes:
        return render_template("expired.html", message="Code invalide.")

    code_data = codes[code]

    now = datetime.now()

    # Initialisation
    if not code_data.get("used"):
        code_data["used"] = True
        code_data["start_time"] = now.isoformat()
        code_data["used_gb"] = 0  # Si non déjà présent
        if not code_data.get("speed_mbps"):
            code_data["speed_mbps"] = 10  # Valeur par défaut
        codes[code] = code_data
        save_codes(codes)

    # Calcul du temps
    start_time = datetime.fromisoformat(code_data["start_time"])
    duration_minutes = code_data.get("duration", 60)
    end_time = start_time + timedelta(minutes=duration_minutes)
    remaining_time = int((end_time - now).total_seconds() / 60)

    if remaining_time <= 0:
        return render_template("expired.html", message="Votre session a expiré.")

    # Calcul des données restantes
    data_limit = code_data.get("data_limit", 1)
    used_gb = code_data.get("used_gb", 0)
    data_remaining = round(max(data_limit - used_gb, 0), 2)

    if data_remaining <= 0:
        return render_template("expired.html", message="Quota de données atteint.")

    return render_template("success.html",
        code=code,
        remaining_time=remaining_time,
        data_limit=data_limit,
        used_gb=round(used_gb, 2),
        data_remaining=data_remaining,
        speed_mbps=code_data.get("speed_mbps", 10)
    )

# -------- Page Admin pour générer des codes --------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    codes = load_codes()

    if request.method == "POST":
        n = int(request.form["n"])
        duration = int(request.form["duration"])
        data_limit = float(request.form["data_limit"])

        for _ in range(n):
            code = generate_code()
            codes[code] = {
                "used": False,
                "duration": duration,
                "data_limit": data_limit,
                "speed_mbps": 10,
                "used_gb": 0
            }

        save_codes(codes)
        return redirect(url_for("admin"))

    return render_template("admin.html", codes=codes)

if __name__ == "__main__":
    app.run(debug=True)
