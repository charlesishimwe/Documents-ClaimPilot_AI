
import json
from pathlib import Path

STORAGE_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "storage"
    / "submitted_claims.json"
)


def load_saved_claims():
    if not STORAGE_FILE.exists():
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_claim(claim):
    claims = load_saved_claims()
    claims.append(claim)

    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(claims, file, indent=2)

    return claim
