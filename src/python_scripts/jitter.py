# Optional Step: Jitter stacked coordinates
import json
import random
from math import radians, cos

INPUT_FILE = "public/teams.json"
OUTPUT_FILE = "public/teams.json"
MAX_SHIFT_METERS = 300

# 1 deg latitude ≈ 111,000 meters
METER_TO_DEG = 1 / 111_000  

def jitter(lat, lng, max_meters=500):
    shift_lat = (random.uniform(-1, 1) * max_meters) * METER_TO_DEG
    # Longitude shift depends on latitude
    shift_lng = (random.uniform(-1, 1) * max_meters) * METER_TO_DEG / cos(radians(lat))
    return lat + shift_lat, lng + shift_lng

# Load teams
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    teams = json.load(f)

# Build a dict of coordinates to detect duplicates
coord_map = {}
for team in teams:
    key = (round(team["lat"], 6), round(team["lng"], 6))  # rounding to 1e-6 deg ≈ 0.11 m
    if key not in coord_map:
        coord_map[key] = []
    coord_map[key].append(team)

# Apply jitter for teams at the same coordinates
for same_coord_teams in coord_map.values():
    if len(same_coord_teams) > 1:
        for t in same_coord_teams:
            t["lat"], t["lng"] = jitter(t["lat"], t["lng"], MAX_SHIFT_METERS)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(teams, f, indent=2)

print(f"Jittered {len(teams)} teams and saved to {OUTPUT_FILE}")
