# Step 3: Geocode each teams location with the given information
import json
import os
import re
import requests
from geopy.geocoders import Nominatim as nom
from geopy.geocoders import GoogleV3 as goog

GOOGLE_MAPS_API_KEY = "[redacted]"
OUTPUT_FILE = "public/teams.json"
INPUT_FILE = "public/raw_teams_adjusted.json"

# ---- FETCH AVATAR CSS ----
avatar_url = "https://ftc-scoring.firstinspires.org/avatars/composed/2025.css"
css_text = requests.get(avatar_url).text

# Regex to extract team-specific avatars
pattern = re.compile(r"\.team-(\d+)\s*{\s*background-image:\s*url\(([^)]+)\)")
team_avatars = {m[0]: m[1] for m in pattern.findall(css_text)}

# Regex to extract default avatar (class .team-avatar)
default_match = re.search(r"\.team-avatar\s*{\s*background-image:\s*url\(([^)]+)\)", css_text)
default_avatar = default_match.group(1) if default_match else ""

# ---- LOAD TEAMS ----
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    teams = json.load(f)

nom_g = nom(user_agent="ftc_team_locator")
goog_g = goog(GOOGLE_MAPS_API_KEY)

data = []
for t in teams:
    # ---- BUILD LOCATION STRING ----
    name_full = t.get("nameFull")
    has_sponsor = name_full is not None
    query = f"{(name_full + ', ') if has_sponsor else ''}{t.get('displayLocation')}"

    print("Geocoding:", query)

    # ---- GEOCODE ----
    location = None
    for geocoder, label, arg in [
        (goog_g, "GoogleV3", query),
        (nom_g, "Nominatim", t.get("displayLocation")),
    ]:
        try:
            location = geocoder.geocode(arg)
        except Exception as e:
            print(f"Error with {label}: {e}")
            continue
        if location:
            break
        print(f"Could not geocode with {label}: {arg}")

    if not location:
        print(f"Could not geocode at all: {query}")
        continue


    # ---- SAVE TO JSON ----
    lat, lon = location.latitude, location.longitude
    team_number = str(t.get("teamNumber"))
    icon_url = team_avatars.get(team_number, default_avatar)

    print(f"{team_number}: {lat}, {lon}")
    team_entry = {
        "teamNumber": team_number,
        "name": t.get("nameShort"),
        "lat": lat,
        "lng": lon,
        "iconUrl": icon_url,
        "place": query,
        "website": t.get("website")
    }

    data.append(team_entry)

# ---- WRITE OUTPUT ----
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saving to: ", os.path.abspath(OUTPUT_FILE))