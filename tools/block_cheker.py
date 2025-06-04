import json
from datetime import datetime, timedelta

def load_codes():
    with open("codes.json", "r") as file:
        return json.load(file)

def save_codes(data):
    with open("codes.json", "w") as file:
        json.dump(data, file, indent=4)

def block_expired_codes():
    codes = load_codes()
    now = datetime.now()

    for code, data in codes.items():
        if data["used"]:
            # Vérifier la durée
            start_time = datetime.fromisoformat(data["start_time"])
            duration_minutes = data.get("duration_minutes", 0)
            end_time = start_time + timedelta(minutes=duration_minutes)
            if now > end_time:
                data["blocked"] = True
                continue

            # Vérifier la consommation de données (simulation)
            # TODO: remplacer data["data_used"] par une vraie mesure si possible
            if data.get("data_used", 0) >= data.get("data_limit_gb", 0):
                data["blocked"] = True

    save_codes(codes)
    print("Blocage des codes expirés ou dépassés effectué.")

if __name__ == "__main__":
    block_expired_codes()
