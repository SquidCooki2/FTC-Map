# Step 1: Fetch raw team data from the FIRST v2.0 API
import requests
import base64
import os
import json

# ---- CONFIG ----
FIRST_USER = "[redacted]"
FIRST_PASS = "[redacted]"
SEASON = 2025
OUTPUT_FILE = "public/raw_teams.json"

# ---- AUTH HEADER ----
auth_str = f"{FIRST_USER}:{FIRST_PASS}"
b64_auth = base64.b64encode(auth_str.encode()).decode("utf-8")
headers = {"Authorization": f"Basic {b64_auth}"}

# ---- GET TEAM DATA ----
url = f"https://ftc-api.firstinspires.org/v2.0/{SEASON}/teams"
params = {"page": 1}
teams = []

while True:
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    teams.extend(data.get("teams", []))
    
    if not data.get("teams") or not data.get("pageTotal"):
        break
    if params["page"] >= data["pageTotal"]:
        break
    params["page"] += 1

print(f"Fetched {len(teams)} teams")

# ---- SAVE RAW DATA ----
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(teams, f, indent=2)

print("Saved to:", os.path.abspath(OUTPUT_FILE))
