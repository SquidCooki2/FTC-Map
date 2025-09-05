# Step 2: Clean nameFull from the output of fetch.py to what is most likely the teams location
import json
import re
from langdetect import detect
from deep_translator import GoogleTranslator as gt

INPUT_FILE = "public/raw_teams.json"
OUTPUT_FILE = "public/raw_teams_adjusted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    teams = json.load(f)

location_keywords = [
    # full words
    "school", "academ", "colleg", "universi", "instit",
    "high", "prep", "elementary", "middle", "primary", "secondary",
    "mosque", "church", "temple", "synagogue", "center",
    "charter", "lyceum", "seminary", "headquarters"
    "jamaat", "islamic", "education", "escola", "escuela",
    "community", "hall", "instituto", "campus", "scool",
    "library", "gymnasium", "colegiul", "colégio", "centras",
    "early", "sekolah",

    # abbreviations
    " sch", " hs", " ms", " ps", " isd", " dist", " jr", " sr", " h s", " m s", " acad", " clg", " ctr"
]

remove_keywords = [
    "family/community", "home school", "foundation", "systems",
    "corp", "corporation", "inc", "inc.", 
    "llc", "company", "technologies", "automation", "industries", 
    "labs", "laboratories", "bank", "research", "development"
]

def clean_full(text: str) -> str:
    """Remove unwanted substrings and extra spaces."""
    if not text:
        return None
    # Remove keywords
    cleaned = re.sub(
        "|".join(re.escape(kw) for kw in remove_keywords),
        "",
        text,
        flags=re.IGNORECASE
    )
    return cleaned.strip()

def safe_detect(text: str, default="en"):
    text = text.strip()
    if not text or text.isnumeric():
        return default
    try:
        return detect(text)
    except:
        return default

def find_location(name_full: str) -> str:
    """Split on & or / and return the first location-like part."""
    name_full = clean_full(name_full)
    if not name_full:
        return None

    # Split into individual sponsors
    parts = re.split(r"[&/]", name_full)
    
    for part in parts:
        # Accurate locations for all my Romanian brothers out there
        # Translate to English
        cleaned = (gt(source='auto', target='en').translate(part) if safe_detect(part) != 'en' else part).strip()
        
        if any(kw in cleaned.lower() for kw in location_keywords):
            print("Accepted:" + cleaned)
            return cleaned 
        else: print("-----:" + cleaned)

    return None

for team in teams:
    print(team["teamNumber"])
    team["nameFull"] = find_location(team.get("nameFull", ""))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(teams, f, indent=2, ensure_ascii=False)