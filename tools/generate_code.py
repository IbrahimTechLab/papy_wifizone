import json
import random
import string

# Générer un code aléatoire
def generate_random_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Ajouter des codes
def add_codes(n=5, duration=60, data_limit=1, speed=10):
    try:
        with open("codes.json", "r") as f:
            codes = json.load(f)
    except FileNotFoundError:
        codes = {}

    for _ in range(n):
        code = generate_random_code()
        codes[code] = {
            "used": False,
            "duration": duration,         # en minutes
            "data_limit": data_limit,     # en Go
            "speed": speed                # en Mbps
        }

    with open("codes.json", "w") as f:
        json.dump(codes, f, indent=4)

    print(f"{n} code(s) généré(s) avec succès.")

# Exemple : Génère 5 codes de 1h avec 1 Go et 10 Mbps
if __name__ == "__main__":
    add_codes(n=5, duration=60, data_limit=1, speed=10)
