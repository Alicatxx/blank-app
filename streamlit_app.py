import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote, parse_qs, unquote, urlparse
import urllib.request
import urllib.error
import base64
import random
import json
import re
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Mech Ranking System", page_icon="🤖", layout="wide")

# Styling
st.markdown("""
    <style>
    :root {
        color-scheme: dark;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body, .stApp, .main {
        background: radial-gradient(circle at top left, rgba(0, 255, 255, 0.18), transparent 22%),
                    radial-gradient(circle at bottom right, rgba(142, 0, 255, 0.16), transparent 18%),
                    linear-gradient(180deg, #040a17 0%, #02060f 40%, #020613 100%) !important;
        color: #e7fbff;
    }

    .stApp {
        min-height: 100vh;
        background-attachment: fixed !important;
    }

    .stButton>button, button {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.9), rgba(16, 68, 255, 0.95));
        color: #041826 !important;
        border: 1px solid rgba(0, 255, 255, 0.35) !important;
        border-radius: 14px !important;
        box-shadow: 0 0 24px rgba(0, 255, 255, 0.18) !important;
        transition: transform .16s ease, box-shadow .16s ease;
    }

    .stButton>button:hover, button:hover {
        transform: translateY(-1px);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.24) !important;
    }

    input, textarea, select {
        background: rgba(3, 11, 28, 0.9) !important;
        color: #e9ffff !important;
        border: 1px solid rgba(0, 255, 255, 0.24) !important;
        box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.08);
        border-radius: 12px !important;
    }

    .stTextInput>div>label, .stNumberInput>div>label, .stSelectbox>div>label, .stTextArea>div>label {
        color: #bfeeff !important;
    }

    .css-1d391kg, .css-1v0mbdj, .css-1gk10fy, .css-10trblm, .css-ffhzg2, .css-1v0mbdj, .css-1lcbmhc {
        background: rgba(3, 7, 18, 0.76) !important;
        border: 1px solid rgba(0, 255, 255, 0.16) !important;
        box-shadow: 0 0 45px rgba(0, 255, 255, 0.06) !important;
        backdrop-filter: blur(22px);
        border-radius: 20px !important;
    }

    .stMarkdown, .stDataFrame, .stDataFrameWrapper, .streamlit-expanderContent, .streamlit-expanderHeader {
        color: #d8faff !important;
    }

    .css-1t0vk4w, .css-1gk10fy, .css-1outpf7, .css-1hm5j4d {
        border-radius: 20px !important;
        border: 1px solid rgba(32, 251, 255, 0.12) !important;
        background: rgba(5, 10, 25, 0.74) !important;
    }

    .stTabs [role="tab"] {
        color: #baf2ff !important;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        background: rgba(0, 255, 255, 0.18) !important;
        border: 1px solid rgba(0, 255, 255, 0.32) !important;
        border-radius: 16px !important;
    }

    .rank-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.14), rgba(12, 32, 71, 0.7));
        padding: 20px;
        border-radius: 18px;
        color: #e8fdff;
        margin: 12px 0;
        border: 1px solid rgba(0, 255, 255, 0.18);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
    }

    .rank-title { font-size: 24px; font-weight: bold; }
    .rank-progress { font-size: 14px; margin-top: 10px; }
    .match-win { background-color: #184921; }
    .match-loss { background-color: #5d1313; }

    .css-1v0mbdj, .css-1gk10fy, .css-1outpf7, .css-1t0vk4w {
        background-image: radial-gradient(circle at top left, rgba(0,255,255,0.18), transparent 25%);
    }

    img {
        max-width: 100% !important;
        height: auto !important;
    }

    .stApp .block-container {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    @media (max-width: 980px) {
        .stApp .block-container {
            padding-left: 10px !important;
            padding-right: 10px !important;
        }

        .stButton>button, button {
            width: 100% !important;
            min-width: 0 !important;
        }

        .stDataFrame, .stDataFrameWrapper, .streamlit-expanderContent, .streamlit-expanderHeader,
        .css-1d391kg, .css-1v0mbdj, .css-1gk10fy, .css-10trblm, .css-ffhzg2, .css-1lcbmhc,
        .css-1t0vk4w, .css-1outpf7, .css-1hm5j4d {
            width: 100% !important;
            min-width: 0 !important;
        }

        .stTabs [role="tab"] {
            font-size: 0.95rem !important;
            padding: 0.72rem 0.8rem !important;
        }

        .rank-card {
            padding: 14px !important;
        }

        .stTextInput>div>label, .stNumberInput>div>label, .stSelectbox>div>label,
        .stMarkdown, .stDataFrameWrapper {
            font-size: 0.95rem !important;
        }
    }

    @media (max-width: 640px) {
        .stTabs [role="tab"] {
            font-size: 0.88rem !important;
            padding: 0.65rem 0.65rem !important;
        }

        .stMetric, .stMetricBlock {
            padding: 0.8rem 0.8rem !important;
        }

        .stMarkdown, .stTextInput>div>label, .stNumberInput>div>label, .stSelectbox>div>label {
            font-size: 0.9rem !important;
        }

        .stButton>button, button {
            font-size: 0.95rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sample data
RANKS = {
    "Samyak-Dristi": {"min_rating": 0, "color": "#1403FC", "icon": "🜈"},
    "Samyak-Samkalpa": {"min_rating": 1000, "color": "#00FF4C", "icon": "🜇"},
    "Samyag-Vāc": {"min_rating": 1500, "color": "#FF1E00", "icon": "🜆"},
    "Samyak-Karmānta": {"min_rating": 2000, "color": "#FFFEFC", "icon": "🜅"},
    "Samyag-Ájīva": {"min_rating": 2500, "color": "#07CFFC", "icon": "🜄"},
    "Samyag-Vyāyāma": {"min_rating": 3000, "color": "#E5FF00", "icon": "🜃"},
    "SampaJanna": {"min_rating": 3000, "color": "#AE00FF", "icon": "🜂"},
    "Deva Samyak-Samādhi": {"min_rating": 3000, "color": "#FF6B00", "icon": "🜁"},
}

MECHS = [
    "Atlas", "Behemoth", "Bishop", "Dawneye", "Dominator", "Kestrel", "Maverick", "Oklop",
    "Paladin", "Phantom", "Rampart", "Sabre", "Spectre", "Stalker", "Tempest", "Watcher",
    "Weaver", "Nova", "Rhino", "Kaiju", "Maestro", "Piper", "Purifier", "Titan", "Vortex",
    "Ironclad", "Shadow", "Phoenix", "Aegis", "Astraeus"
]
MAPS = ["Steel Valley", "Crimson Canyon", "Azure Wastes", "Neon City", "Volcanic Core"]
SEASON_PROMOTION_SPOTS = 3

DEFAULT_TEAMS = [
    {
        "id": "team_1",
        "name": "Quantrix",
        "tier": "Deva Samyak-Samādhi",
        "points": 1420,
        "wins": 12,
        "losses": 5,
        "created": datetime.now().isoformat(),
        "players": ["Shiva (Ha-Rin)","Yamajara (Kanae tobik)","Skanda (Arik Madi)","Indra (Ayet)"],
        "player_mechs": {"Astra": "Atlas", "Blaze": "Behemoth", "Cipher": "Bishop", "Dynamo": "Dawneye", "Echo": "Dominator", "Falcon": "Kestrel"}
    },
    {
        "id": "team_2",
        "name": "Shadows Grasp",
        "tier": "Deva Samyak-Samādhi",
        "points": 1675,
        "wins": 14,
        "losses": 7,
        "created": datetime.now().isoformat(),
        "players": ["Nova", "Rogue", "Sable", "Talon", "Viper", "Warden"],
        "player_mechs": {"Nova": "Nova", "Rogue": "Rampart", "Sable": "Sabre", "Talon": "Spectre", "Viper": "Stalker", "Warden": "Tempest"}
    },
    {
        "id": "team_3",
        "name": "Platinum Style",
        "tier": "Deva Samyak-Samādhi",
        "points": 1550,
        "wins": 13,
        "losses": 6,
        "created": datetime.now().isoformat(),
        "players": ["Hex", "Ion", "Jinx", "Kestrel", "Lumina", "Maverick"],
        "player_mechs": {"Hex": "Watcher", "Ion": "Weaver", "Jinx": "Rhino", "Kestrel": "Kestrel", "Lumina": "Maestro", "Maverick": "Maverick"}
    },
    {
        "id": "team_4",
        "name": "The Four Lords",
        "tier": "Deva Samyak-Samādhi",
        "points": 1550,
        "wins": 13,
        "losses": 6,
        "created": datetime.now().isoformat(),
        "players": ["Hex", "Ion", "Jinx", "Kestrel", "Lumina", "Maverick"],
        "player_mechs": {"Hex": "Watcher", "Ion": "Weaver", "Jinx": "Rhino", "Kestrel": "Kestrel", "Lumina": "Maestro", "Maverick": "Maverick"}
    }
]

# Persistent storage for teams and images
TEAMS_FILE = Path("teams.json")
IMAGES_FILE = Path("images.json")
MATCHES_FILE = Path("matches.json")
MAPS_FILE = Path("maps.json")
SECURITY_FILE = Path("security.json")

def load_teams_from_disk():
    if TEAMS_FILE.exists():
        try:
            with TEAMS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                # ensure structure is a list
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []

def save_teams_to_disk(teams):
    try:
        with TEAMS_FILE.open("w", encoding="utf-8") as f:
            json.dump(teams, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def load_images_from_disk():
    if IMAGES_FILE.exists():
        try:
            with IMAGES_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {
                        "teams": data.get("teams", {}),
                        "players": data.get("players", {})
                    }
        except Exception:
            return {"teams": {}, "players": {}}
    return {"teams": {}, "players": {}}


def save_images_to_disk(images):
    try:
        with IMAGES_FILE.open("w", encoding="utf-8") as f:
            json.dump(images, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def load_matches_from_disk():
    if MATCHES_FILE.exists():
        try:
            with MATCHES_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_matches_to_disk(matches):
    try:
        with MATCHES_FILE.open("w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception:
        return False


def load_maps_from_disk():
    if MAPS_FILE.exists():
        try:
            with MAPS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_maps_to_disk(maps):
    try:
        with MAPS_FILE.open("w", encoding="utf-8") as f:
            json.dump(maps, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def load_security_from_disk():
    if SECURITY_FILE.exists():
        try:
            with SECURITY_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_security_to_disk(entries):
    try:
        with SECURITY_FILE.open("w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def normalize_map_name(name):
    return name.strip()


def get_map_by_name(name):
    return next((m for m in st.session_state.maps if m.get("name") == name), None)


def add_map(name, description, objectives, image_url, deployment_image_url, special_reaction, environment):
    if not name or not name.strip():
        return False
    name = normalize_map_name(name)
    if any(m["name"].lower() == name.lower() for m in st.session_state.maps):
        return False
    map_entry = {
        "id": f"map_{len(st.session_state.maps) + 1}",
        "name": name,
        "description": description.strip(),
        "objectives": [obj.strip() for obj in objectives if obj and obj.strip()],
        "image_url": image_url.strip(),
        "deployment_image_url": deployment_image_url.strip(),
        "special_reaction": special_reaction.strip(),
        "environment": environment.strip(),
        "created": datetime.now().isoformat()
    }
    st.session_state.maps.append(map_entry)
    save_maps_to_disk(st.session_state.maps)
    return True


def update_map(map_id, name=None, description=None, objectives=None, image_url=None, deployment_image_url=None, special_reaction=None, environment=None):
    map_entry = next((m for m in st.session_state.maps if m.get("id") == map_id), None)
    if not map_entry:
        return False
    if name and name.strip():
        map_entry["name"] = normalize_map_name(name)
    if description is not None:
        map_entry["description"] = description.strip()
    if objectives is not None:
        map_entry["objectives"] = [obj.strip() for obj in objectives if obj and obj.strip()]
    if image_url is not None:
        map_entry["image_url"] = image_url.strip()
    if deployment_image_url is not None:
        map_entry["deployment_image_url"] = deployment_image_url.strip()
    if special_reaction is not None:
        map_entry["special_reaction"] = special_reaction.strip()
    if environment is not None:
        map_entry["environment"] = environment.strip()
    save_maps_to_disk(st.session_state.maps)
    return True


def delete_map(map_id):
    before = len(st.session_state.maps)
    st.session_state.maps = [m for m in st.session_state.maps if m.get("id") != map_id]
    if len(st.session_state.maps) < before:
        save_maps_to_disk(st.session_state.maps)
        return True
    return False


def parse_map_data(entry):
    if not isinstance(entry, dict):
        return None
    name = entry.get("name") or entry.get("title") or entry.get("map") or entry.get("map_name")
    if not name:
        return None
    description = entry.get("description") or entry.get("desc") or ""
    objectives_raw = entry.get("objectives") or entry.get("mission_objectives") or entry.get("missionObjectives") or entry.get("objectives_list") or []
    if isinstance(objectives_raw, str):
        objectives = [line.strip() for line in objectives_raw.split("\n") if line.strip()]
    elif isinstance(objectives_raw, list):
        objectives = [str(item).strip() for item in objectives_raw if item]
    else:
        objectives = []
    image_url = entry.get("image_url") or entry.get("image") or entry.get("map_image") or entry.get("imageUrl") or ""
    deployment_image_url = entry.get("deployment_image_url") or entry.get("deployment_image") or entry.get("deployment_plan") or entry.get("deploymentImage") or ""
    special_reaction = entry.get("special_reaction") or entry.get("specialReaction") or entry.get("special") or ""
    environment = entry.get("environment") or entry.get("env") or ""
    return {
        "name": normalize_map_name(name),
        "description": description.strip(),
        "objectives": objectives,
        "image_url": image_url.strip(),
        "deployment_image_url": deployment_image_url.strip(),
        "special_reaction": special_reaction.strip(),
        "environment": environment.strip()
    }


def import_maps_from_files(uploaded_files):
    imported = []
    for uploaded_file in uploaded_files:
        if not uploaded_file.name.lower().endswith(".json"):
            continue
        try:
            raw = uploaded_file.read()
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            continue
        if isinstance(data, list):
            for entry in data:
                mapped = parse_map_data(entry)
                if mapped:
                    imported.append(mapped)
        elif isinstance(data, dict):
            if "maps" in data and isinstance(data["maps"], list):
                for entry in data["maps"]:
                    mapped = parse_map_data(entry)
                    if mapped:
                        imported.append(mapped)
            else:
                mapped = parse_map_data(data)
                if mapped:
                    imported.append(mapped)
    return imported


def extract_yaml_frontmatter(text):
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S | re.M)
    if not match:
        return {}
    content = match.group(1)
    result = {}
    for line in content.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                try:
                    result[key] = json.loads(value)
                except Exception:
                    result[key] = [item.strip().strip('"\'') for item in value[1:-1].split(",") if item.strip()]
            else:
                result[key] = value
    return result


def parse_obsidian_markdown(text):
    teams = []
    frontmatter = extract_yaml_frontmatter(text)
    if frontmatter:
        if isinstance(frontmatter.get("teams"), list):
            for team in frontmatter["teams"]:
                if isinstance(team, dict):
                    teams.append({
                        "name": team.get("name", "Imported Team"),
                        "players": [normalize_player_name(p) for p in team.get("players", []) if p],
                        "player_mechs": {normalize_player_name(p): m for p, m in team.get("player_mechs", {}).items() if p},
                        "points": int(team.get("points", 0)) if team.get("points") else 0
                    })
        elif isinstance(frontmatter.get("players"), list):
            teams.append({
                "name": frontmatter.get("name", "Imported Team"),
                "players": [normalize_player_name(p) for p in frontmatter.get("players", []) if p],
                "player_mechs": {},
                "points": int(frontmatter.get("points", 0)) if frontmatter.get("points") else 0
            })
    current = None
    first_line = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if first_line is None:
            first_line = stripped
        heading = re.match(r"^#{1,6}\s+(.+)", line)
        if heading:
            if current and current["players"]:
                teams.append(current)
            current = {"name": heading.group(1).strip(), "players": [], "player_mechs": {}, "points": 0}
            continue
        if current is None:
            # Use bare title line as the team name when no markdown heading is provided
            if not re.match(r"^\[\[.*\]\]", stripped) and not re.match(r"^\d+\s*[:.)\-]*\s*\[\[.*\]\]", stripped, flags=re.I) and "tier" not in stripped.lower():
                current = {"name": first_line, "players": [], "player_mechs": {}, "points": 0}
            else:
                continue
        bullet = re.match(r"^[-*+]\s+(.+)", line)
        if not bullet:
            bullet = re.match(r"^\d+\s*[:.)\-]*\s+(.+)", line)
        if bullet:
            item = bullet.group(1).strip()
            item = re.sub(r"^\d+\s*[:.)\-]*\s*", "", item)
            bracketed = re.search(r"\[\[([^\]]+)\]\]", item)
            if bracketed:
                item = bracketed.group(1).strip()
            mech = None
            if item.endswith(")") and "(" in item:
                name, mech_part = item.rsplit("(", 1)
                mech = mech_part[:-1].strip()
                name = name.strip()
            elif " - " in item:
                name, mech = item.split(" - ", 1)
                name = name.strip()
                mech = mech.strip()
            elif ":" in item:
                name, mech = item.split(":", 1)
                name = name.strip()
                mech = mech.strip()
            else:
                name = item
            if name:
                parsed_name = normalize_player_name(name)
                current["players"].append(parsed_name)
                if mech:
                    current["player_mechs"][parsed_name] = mech
    if current and current["players"]:
        teams.append(current)
    return teams


def parse_team_json_data(data):
    teams = []
    if isinstance(data, dict):
        if "teams" in data and isinstance(data["teams"], list):
            for item in data["teams"]:
                if isinstance(item, dict):
                    teams.append({
                        "name": item.get("name", "Imported Team"),
                        "players": [normalize_player_name(p) for p in item.get("players", []) if p],
                        "player_mechs": {normalize_player_name(p): m for p, m in item.get("player_mechs", {}).items() if p} if isinstance(item.get("player_mechs"), dict) else {},
                        "points": int(item.get("points", 0)) if item.get("points") else 0
                    })
        elif "players" in data and isinstance(data["players"], list):
            teams.append({
                "name": data.get("name", "Imported Team"),
                "players": [normalize_player_name(p) for p in data["players"] if p],
                "player_mechs": {normalize_player_name(p): m for p, m in data.get("player_mechs", {}).items() if p} if isinstance(data.get("player_mechs"), dict) else {},
                "points": int(data.get("points", 0)) if data.get("points") else 0
            })
        elif any(k in data for k in ("name", "pilot", "callsign", "character")):
            name = normalize_player_name(data.get("name") or data.get("pilot") or data.get("callsign") or data.get("character") or "Imported Pilot")
            mech = data.get("mech") or data.get("frame") or data.get("chassis")
            team_name = data.get("team") or data.get("company") or "Imported Team"
            teams.append({
                "name": team_name,
                "players": [name],
                "player_mechs": {name: mech} if mech else {},
                "points": int(data.get("points", 0)) if data.get("points") else 0
            })
    elif isinstance(data, list):
        if all(isinstance(item, dict) and item.get("team") for item in data):
            grouped = {}
            for item in data:
                name = normalize_player_name(item.get("name") or item.get("pilot") or item.get("callsign") or item.get("character") or "Imported Pilot")
                team_name = item.get("team")
                mech = item.get("mech") or item.get("frame") or item.get("chassis")
                if team_name not in grouped:
                    grouped[team_name] = {"name": team_name, "players": [], "player_mechs": {}, "points": 0}
                grouped[team_name]["players"].append(name)
                if mech:
                    grouped[team_name]["player_mechs"][name] = mech
            teams.extend(grouped.values())
        else:
            players = []
            player_mechs = {}
            for item in data:
                if isinstance(item, dict):
                    name = normalize_player_name(item.get("name") or item.get("pilot") or item.get("callsign") or item.get("character") or "Imported Pilot")
                    mech = item.get("mech") or item.get("frame") or item.get("chassis")
                    players.append(name)
                    if mech:
                        player_mechs[name] = mech
            if players:
                teams.append({"name": "Imported Team", "players": players, "player_mechs": player_mechs, "points": 0})
    return teams


def import_teams_from_files(uploaded_files):
    imported = []
    for uploaded_file in uploaded_files:
        content_type = uploaded_file.type
        raw = uploaded_file.read()
        try:
            text = raw.decode("utf-8")
        except Exception:
            continue
        if uploaded_file.name.lower().endswith(".json"):
            try:
                data = json.loads(text)
                imported.extend(parse_team_json_data(data))
            except Exception:
                continue
        else:
            imported.extend(parse_obsidian_markdown(text))
    return imported


def normalize_import_team_name(name, existing_names):
    base = name.strip() or "Imported Team"
    if base not in existing_names:
        return base
    counter = 2
    while f"{base} {counter}" in existing_names:
        counter += 1
    return f"{base} {counter}"


def pad_or_split_team(team):
    players = [p for p in team["players"] if p]
    player_mechs = team.get("player_mechs", {}) or {}
    if len(players) == 0:
        return []
    if len(players) <= 6:
        while len(players) < 6:
            placeholder = f"Vacant {len(players) + 1}"
            players.append(placeholder)
            player_mechs[placeholder] = MECHS[0]
        return [{"name": team["name"], "players": players, "player_mechs": player_mechs, "points": team.get("points", 0) or 0}]
    split_teams = []
    chunk = 1
    for i in range(0, len(players), 6):
        chunk_players = players[i:i+6]
        while len(chunk_players) < 6:
            placeholder = f"Vacant {len(chunk_players) + 1}"
            chunk_players.append(placeholder)
            player_mechs[placeholder] = MECHS[0]
        split_teams.append({
            "name": f"{team['name']} {chunk}",
            "players": chunk_players,
            "player_mechs": player_mechs,
            "points": int(team.get("points", 0) or 0)
        })
        chunk += 1
    return split_teams


def generate_team_id(teams):
    max_id = 0
    for t in teams:
        tid = t.get("id", "")
        if isinstance(tid, str) and tid.startswith("team_"):
            try:
                n = int(tid.split("_")[-1])
                if n > max_id:
                    max_id = n
            except Exception:
                pass
    return f"team_{max_id + 1}"

RANK_ORDER = sorted(RANKS.keys(), key=lambda rank: RANKS[rank]["min_rating"])


def get_rank(rating):
    """Get rank tier based on rating."""
    for rank in reversed(list(RANKS.keys())):
        if rating >= RANKS[rank]["min_rating"]:
            return rank
    return "Bronze"


def get_promotion_pairings(teams, pair_count=3):
    pairings = []
    for i in range(len(RANK_ORDER) - 1):
        lower_rank = RANK_ORDER[i]
        higher_rank = RANK_ORDER[i + 1]
        lower_teams = [t for t in teams if t["tier"] == lower_rank]
        higher_teams = [t for t in teams if t["tier"] == higher_rank]
        lower_teams = sorted(lower_teams, key=lambda t: t.get("points", 0), reverse=True)
        higher_teams = sorted(higher_teams, key=lambda t: t.get("points", 0))
        count = min(pair_count, len(lower_teams), len(higher_teams))
        for j in range(count):
            pairings.append({
                "pair_id": f"{lower_rank}_{higher_rank}_{j}",
                "lower_rank": lower_rank,
                "higher_rank": higher_rank,
                "lower_team": lower_teams[j]["name"],
                "higher_team": higher_teams[j]["name"],
            })
    return pairings


def apply_end_of_season_results(pairings, winners):
    summary = []
    for pair in pairings:
        winner = winners.get(pair["pair_id"])
        if winner not in (pair["lower_team"], pair["higher_team"]):
            continue
        lower_team = get_team_by_name(pair["lower_team"])
        higher_team = get_team_by_name(pair["higher_team"])
        if not lower_team or not higher_team:
            continue
        if winner == pair["lower_team"]:
            lower_team["tier"] = pair["higher_rank"]
            higher_team["tier"] = pair["lower_rank"]
            summary.append(f"{lower_team['name']} promoted to {pair['higher_rank']} and {higher_team['name']} relegated to {pair['lower_rank']}")
        else:
            lower_team["tier"] = pair["lower_rank"]
            higher_team["tier"] = pair["higher_rank"]
            summary.append(f"{higher_team['name']} remains in {pair['higher_rank']} and {lower_team['name']} remains in {pair['lower_rank']}")
    save_teams_to_disk(st.session_state.teams)
    st.session_state.promotion_pairings = []
    return summary


def reset_season():
    for team in st.session_state.teams:
        team["points"] = 0
        team["wins"] = 0
        team["losses"] = 0
    save_teams_to_disk(st.session_state.teams)
    st.session_state.matches = []
    save_matches_to_disk(st.session_state.matches)
    return True


def generate_sample_players(count=10):
    """Generate sample player data."""
    players = []
    for i in range(count):
        rating = random.randint(500, 3500)
        rank = get_rank(rating)
        players.append({
            "Username": f"Pilot_{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma'])}_{i+1}",
            "Rank": rank,
            "Rating": rating,
            "Wins": random.randint(10, 200),
            "Losses": random.randint(5, 100),
            "Winrate": f"{random.randint(45, 75)}%",
            "Main Mech": random.choice(MECHS),
            "Last Played": f"{random.randint(1, 7)} days ago"
        })
    return sorted(players, key=lambda x: x["Rating"], reverse=True)

def generate_match_history(count=10):
    """Generate sample match history."""
    matches = []
    for i in range(count):
        result = random.choice(["Win", "Loss"])
        rating_change = random.randint(15, 35) if result == "Win" else -random.randint(10, 25)
        matches.append({
            "Date": datetime.now() - timedelta(days=random.randint(0, 30)),
            "Result": result,
            "Opponent": f"Pilot_{random.choice(['Omega', 'Zeta', 'Eta', 'Theta'])}_{random.randint(1, 100)}",
            "Map": random.choice(MAPS),
            "Mech Used": random.choice(MECHS),
            "Rating Change": f"{rating_change:+d}",
            "Duration": f"{random.randint(5, 15)} min"
        })
    return sorted(matches, key=lambda x: x["Date"], reverse=True)

def normalize_player_name(name):
    return name.strip()


def generate_player_profile(username, team=None, points=0, mech=None, call_sign=None):
    username = normalize_player_name(username)
    if not username:
        return None

    seed = sum(ord(ch) for ch in username)
    rng = random.Random(seed)
    base_rating = max(400, min(3800, int(points * 1.5 + rng.randint(-150, 250))))
    rating = max(400, min(3800, base_rating + rng.randint(-100, 100)))
    rank = get_rank(rating)
    wins = max(5, int((rating + rng.randint(0, 200)) / 18))
    losses = max(1, int((4200 - rating + rng.randint(0, 150)) / 30))
    winrate_val = min(98, max(40, int(50 + (rating - 1500) / 40 + rng.randint(-5, 5))))
    selected_mech = mech if mech in MECHS else rng.choice(MECHS)

    return {
        "Username": username,
        "Call Sign": call_sign or "",
        "Rank": rank,
        "Rating": rating,
        "Wins": wins,
        "Losses": losses,
        "Winrate": f"{winrate_val}%",
        "Main Mech": selected_mech,
        "Last Played": f"{rng.randint(1, 7)} days ago",
        "Team": team or "Free Agent"
    }


def generate_player_match_history(username, count=8):
    seed = sum(ord(ch) for ch in username) + 1
    rng = random.Random(seed)
    matches = []

    for _ in range(count):
        result = rng.choice(["Win", "Loss"])
        rating_change = rng.randint(15, 35) if result == "Win" else -rng.randint(10, 25)
        matches.append({
            "Date": datetime.now() - timedelta(days=rng.randint(0, 30)),
            "Result": result,
            "Opponent": f"Pilot_{rng.choice(['Omega', 'Zeta', 'Eta', 'Theta'])}_{rng.randint(1, 100)}",
            "Map": rng.choice(MAPS),
            "Mech Used": rng.choice(MECHS),
            "Rating Change": f"{rating_change:+d}",
            "Duration": f"{rng.randint(5, 15)} min"
        })

    return sorted(matches, key=lambda x: x["Date"], reverse=True)


DEFAULT_MIYO_AVATAR = "https://imgup.uk/i/qZxsu8YO.jpg"
DEFAULT_CHAT_AVATAR = "https://imgup.uk/i/qMBLy1lJ.png"


def format_discord_match_result(match):
    return (
        f"**Miyo Match Report**\n"
        f"Result: {match['Result']}\n"
        f"Opponent: {match['Opponent']}\n"
        f"Map: {match['Map']}\n"
        f"Mech: {match['Mech Used']}\n"
        f"Rating Change: {match['Rating Change']}\n"
        f"Duration: {match['Duration']}\n"
        f"Date: {match['Date'].strftime('%Y-%m-%d %H:%M')}"
    )


def format_match_result_message(match):
    participants = ", ".join(match["participants"])
    detail_lines = []
    for team in match["updated_teams"]:
        point_change = match["win_points"] if team["result"] == "Win" else match["loss_points"]
        sign = "+" if point_change >= 0 else ""
        detail_lines.append(
            f"- {team['name']}: {team['result']} ({sign}{point_change} pts), now {team['points']} pts, tier {team['tier']}"
        )

    notes = f"\nNotes: {match['notes']}" if match.get("notes") else ""
    return (
        f"**Miyo Match Result**\n"
        f"Winner: {match['winner']}\n"
        f"Map: {match.get('map', 'Unknown')}\n"
        f"Mission: {match.get('mission', 'Unknown')}\n"
        f"Participants: {participants}\n"
        f"""Details:\n{ '\n'.join(detail_lines) }"""
        f"{notes}"
    )


def format_security_work_message(entry):
    teams = ", ".join(entry.get("teams", [])) if entry.get("teams") else "None"
    pilots = ", ".join(entry.get("pilots", [])) if entry.get("pilots") else "None"

    team_lines = []
    for update in entry.get("team_updates", []):
        sign = "+" if int(update.get("points", 0)) >= 0 else ""
        team_lines.append(f"- Team {update['team']}: {sign}{update['points']} league pts (now {update['new_points']})")

    pilot_lines = []
    for update in entry.get("pilot_updates", []):
        sign = "+" if int(update.get("points", 0)) >= 0 else ""
        pilot_lines.append(
            f"- Pilot {update['pilot']} ({update['team']}): {sign}{update['points']} league pts (team now {update['new_points']})"
        )

    details = []
    if team_lines:
        details.append("Team Point Changes:\n" + "\n".join(team_lines))
    if pilot_lines:
        details.append("Pilot Point Changes:\n" + "\n".join(pilot_lines))

    detail_text = "\n\n".join(details) if details else "No league points awarded."
    return (
        "**Miyo Security Work Report**\n"
        f"Mission: {entry.get('mission', 'Unknown')}\n"
        f"Description: {entry.get('description', '')}\n"
        f"Work: {entry.get('work', '')}\n"
        f"Teams Involved: {teams}\n"
        f"Pilots Involved: {pilots}\n\n"
        f"{detail_text}"
    )


def normalize_discord_webhook_url(raw_url):
    if not raw_url:
        return raw_url

    raw_url = raw_url.strip()
    parsed = urlparse(raw_url)
    if parsed.netloc.endswith("safelinks.protection.outlook.com"):
        qs = parse_qs(parsed.query)
        extracted = qs.get("url") or qs.get("u")
        if extracted:
            return normalize_discord_webhook_url(unquote(extracted[0]))

    if parsed.scheme.lower() in ("http", "https") and parsed.netloc.endswith(("discord.com", "discordapp.com")):
        return raw_url

    safe_match = re.search(r"https://(?:canary\\.|ptb\\.)?(?:discord|discordapp)\\.com/api/webhooks/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", raw_url)
    if safe_match:
        return safe_match.group(0)

    return raw_url


def post_to_discord(webhook_url, content, username="Miyo", avatar_url=None):
    if not webhook_url:
        return False, "Discord webhook URL is required."

    webhook_url = normalize_discord_webhook_url(webhook_url)
    payload = {"username": username, "content": content}
    payload["avatar_url"] = avatar_url or DEFAULT_MIYO_AVATAR
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "MiyoBot/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if 200 <= resp.getcode() < 300:
                return True, "Posted match result to Discord successfully."
            return False, f"Discord returned status {resp.getcode()}."
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return False, "Discord forbidden (403). Check that the webhook URL is correct and still active."
        return False, f"Discord error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"Discord request failed: {e.reason}"
    except Exception as e:
        return False, str(e)


DEFAULT_AVATAR_URL = "https://imgup.uk/i/5Q1amHsg.png"
DEFAULT_MATCH_RESULTS_WEBHOOK = "https://discord.com/api/webhooks/1524804436009160969/8Us7Y-y8CF83FrfWTsaG7810j3SWdVU88nLoYaRSGPoyoYuxkWa_hUMa_TWdoFSqyJYt"

HYPE_SALT_MESSAGES = [
    "What a fight! Next season is heating up!",
    "That was brutal — the arena is still smoking!",
    "Oof, salt levels are off the charts!",
    "Miyo says: ‘That was a spicy one!’",
    "Hype incoming! Winners are climbing!",
    "Next season is going to be legendary after that!",
    "Did you feel that? That was icy competition!",
    "The energy is real — this league is wild!",
    "Somebody’s got to bounce back after that!",
    "Winners be flexing, losers be studying tapes.",
    "This clash was a masterpiece of mayhem and mechanics!",
    "The arena is still buzzing from that last showdown!",
    "Salt is flowing, but so is the glory — what a match!",
    "The fight was fierce; may the best pilots rise!"
]

CONGRATULATION_MESSAGES = [
    "Congrats to the teams who proved they belong in the next rank!",
    "What a season — champions earned every inch of that climb.",
    "Respect to every pilot who brought the heat and held the line.",
    "Promotion and survival both taste sweet tonight — well done!",
    "You showed heart, grit, and the kind of plays that make legends.",
    "This season belonged to those who refused to back down."
]


def format_end_of_season_pairings_message(pairings):
    if not pairings:
        return "No end-of-season promotion pairings are available."

    pair_lines = [f"{p['lower_team']} ({p['lower_rank']}) vs {p['higher_team']} ({p['higher_rank']})" for p in pairings]
    return (
        "**Miyo End of Season Pairings**\n"
        "It's time for the finals, let's see who will climb towards Deva, and who falls towards Naraka. "
        "Top three teams from each rank battle it out with the bottom three of the next to see who deserves to move up and down.\n\n"
        "**Pairings:**\n"
        + "\n".join(pair_lines)
    )


def format_season_final_results_message(summary):
    if not summary:
        result_text = "The season ended with no promotion results applied."
    else:
        result_text = "\n".join([f"- {line}" for line in summary])

    congratulations = random.sample(CONGRATULATION_MESSAGES, min(3, len(CONGRATULATION_MESSAGES)))
    return (
        "**Miyo Season Results**\n"
        "That's it for this season, we've had excitement, death, tears and oodles of promotion, love you all, me our fights and Sutra will see you in a month.\n\n"
        "**Season Summary:**\n"
        + result_text
        + "\n\n"
        + "\n".join(congratulations)
    )


def send_hype_or_salt_messages(webhook_url, avatar_url=None, count=3):
    if not webhook_url:
        return False, "No webhook configured for hype messages."

    chosen = random.sample(HYPE_SALT_MESSAGES, min(count, len(HYPE_SALT_MESSAGES)))
    for msg in chosen:
        success, error = post_to_discord(
            webhook_url,
            msg,
            username="chat",
            avatar_url=DEFAULT_CHAT_AVATAR
        )
        if not success:
            return False, f"Hype/salt send failed: {error}"
    return True, f"Sent {len(chosen)} hype/salt messages as chat."


def get_avatar_url(name):
    custom_url = get_custom_avatar_url(name)
    if custom_url:
        return custom_url
    safe_name = quote(name.replace(' ', '_'))
    return f"https://robohash.org/{safe_name}.png?set=set2&size=180x180"


def get_custom_avatar_url(name):
    if "player_images" in st.session_state and name in st.session_state.player_images:
        return st.session_state.player_images[name]
    return None


def get_avatar_url_for_player(name):
    return get_custom_avatar_url(name) or DEFAULT_AVATAR_URL


def get_avatar_url_for_team(team):
    if isinstance(team, dict):
        custom_url = team.get("avatar_url")
        if custom_url:
            return custom_url
        return DEFAULT_AVATAR_URL
    return DEFAULT_AVATAR_URL


def get_all_pilots():
    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
    pilots = []
    seen = set()
    for team in teams:
        for player in team["players"]:
            if player not in seen:
                seen.add(player)
                pilots.append({
                    "Username": player,
                    "Call Sign": get_player_call_sign(team, player),
                    "Team": team["name"],
                    "Team Points": team["points"],
                    "Team Tier": team["tier"],
                    "Main Mech": get_player_mech(team, player) or "Unknown"
                })
    return pilots


def get_team_summary(team):
    profiles = [generate_player_profile(
        name,
        team=team["name"],
        points=team["points"],
        mech=get_player_mech(team, name)
    ) for name in team["players"]]
    total_wins = sum(p["Wins"] for p in profiles if p)
    total_losses = sum(p["Losses"] for p in profiles if p)
    avg_rating = int(sum(p["Rating"] for p in profiles if p) / len(profiles)) if profiles else 0
    avg_winrate = f"{int(sum(int(p["Winrate"].replace('%', '')) for p in profiles if p) / len(profiles))}%" if profiles else "0%"
    return {
        "profiles": profiles,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "avg_rating": avg_rating,
        "avg_winrate": avg_winrate,
        "roster_table": pd.DataFrame([{
            "Pilot": p["Username"],
            "Rank": p["Rank"],
            "Rating": p["Rating"],
            "Winrate": p["Winrate"],
            "Main Mech": p["Main Mech"]
        } for p in profiles])
    }


def get_team_by_name(name):
    return next((t for t in st.session_state.teams if t["name"] == name), None)


def add_team(name, tier, players, player_mechs, points, player_callsigns=None, npc_mechs=None):
    if not name or not name.strip():
        return False
    name = name.strip()
    if any(t["name"].lower() == name.lower() for t in st.session_state.teams):
        return False

    players = [p.strip() for p in players if p and p.strip()]
    team_mechs = {player: mech for player, mech in zip(players, player_mechs) if player}
    team_callsigns = {}
    if player_callsigns:
        for i, player in enumerate(players):
            if i < len(player_callsigns) and player:
                team_callsigns[player] = player_callsigns[i].strip()

    team = {
        "id": generate_team_id(st.session_state.teams),
        "name": name,
        "tier": tier,
        "points": int(points),
        "wins": 0,
        "losses": 0,
        "created": datetime.now().isoformat(),
        "players": players,
        "player_mechs": team_mechs,
        "player_callsigns": team_callsigns,
        "npc_mechs": npc_mechs or [],
        "avatar_url": ""
    }
    st.session_state.teams.append(team)
    save_teams_to_disk(st.session_state.teams)
    return True


def update_team_points(team_id, delta):
    team = next((t for t in st.session_state.teams if t.get("id") == team_id), None)
    if not team:
        return False
    team["points"] = int(team.get("points", 0)) + int(delta)
    save_teams_to_disk(st.session_state.teams)
    return True


def update_team(team_id, name=None, tier=None, points=None, players=None, player_mechs=None, player_callsigns=None, npc_mechs=None):
    team = next((t for t in st.session_state.teams if t.get("id") == team_id), None)
    if not team:
        return False
    if name is not None:
        team["name"] = name.strip()
    if tier is not None:
        team["tier"] = tier
    if points is not None:
        team["points"] = int(points)
    if players is not None:
        current_mechs = team.get("player_mechs", {})
        current_callsigns = team.get("player_callsigns", {})
        team["players"] = players
        if player_mechs is None:
            team["player_mechs"] = {p: current_mechs.get(p, MECHS[0]) for p in players}
        else:
            team["player_mechs"] = {p: player_mechs.get(p, current_mechs.get(p, MECHS[0])) for p in players}
        if player_callsigns is None:
            team["player_callsigns"] = {p: current_callsigns.get(p, "") for p in players}
        else:
            team["player_callsigns"] = {p: player_callsigns.get(p, current_callsigns.get(p, "")) for p in players}
    else:
        if player_mechs is not None:
            current_mechs = team.get("player_mechs", {})
            team["player_mechs"] = {p: player_mechs.get(p, current_mechs.get(p, MECHS[0])) for p in team.get("players", [])}
        if player_callsigns is not None:
            current_callsigns = team.get("player_callsigns", {})
            team["player_callsigns"] = {p: player_callsigns.get(p, current_callsigns.get(p, "")) for p in team.get("players", [])}
    # update npc mechs if provided
    if npc_mechs is not None:
        team["npc_mechs"] = npc_mechs
    save_teams_to_disk(st.session_state.teams)
    return True


def delete_team(team_id):
    st.session_state.teams = [t for t in st.session_state.teams if t.get("id") != team_id]
    save_teams_to_disk(st.session_state.teams)
    return True


def move_pilot(pilot_name, source_team_name, target_team_name):
    source_team = get_team_by_name(source_team_name)
    target_team = get_team_by_name(target_team_name)
    if not source_team or not target_team:
        return False
    if pilot_name not in source_team["players"]:
        return False
    if len(target_team["players"]) >= 6:
        return False

    source_team["players"].remove(pilot_name)
    target_team["players"].append(pilot_name)
    if "player_mechs" in source_team:
        mech = source_team["player_mechs"].pop(pilot_name, None)
        if mech:
            target_team.setdefault("player_mechs", {})[pilot_name] = mech
    if "player_callsigns" in source_team:
        callsign = source_team["player_callsigns"].pop(pilot_name, None)
        if callsign is not None:
            target_team.setdefault("player_callsigns", {})[pilot_name] = callsign
    save_teams_to_disk(st.session_state.teams)
    return True


def get_promotion_candidates(teams, spots=SEASON_PROMOTION_SPOTS):
    return sorted(teams, key=lambda t: int(t.get("points", 0)), reverse=True)[:spots]


def apply_match_result(participant_names, winner_name, win_points=20, loss_points=-10, notes="", map_name="", mission_name=""):
    if len(participant_names) < 2:
        return False, "Select at least two teams for a match."
    if winner_name not in participant_names:
        return False, "Winning team must be one of the participating teams."

    now = datetime.now()
    updated_teams = []
    for team_name in participant_names:
        team = get_team_by_name(team_name)
        if not team:
            return False, f"Team {team_name} not found."

        if team_name == winner_name:
            team["points"] = int(team.get("points", 0)) + int(win_points)
            team["wins"] = int(team.get("wins", 0)) + 1
            result = "Win"
        else:
            team["points"] = int(team.get("points", 0)) + int(loss_points)
            team["losses"] = int(team.get("losses", 0)) + 1
            result = "Loss"

        updated_teams.append({
            "name": team["name"],
            "points": team["points"],
            "tier": team["tier"],
            "result": result
        })

    save_teams_to_disk(st.session_state.teams)
    match_record = {
        "id": f"match_{len(st.session_state.matches) + 1}",
        "date": now.isoformat(),
        "participants": participant_names,
        "winner": winner_name,
        "map": map_name,
        "mission": mission_name,
        "win_points": int(win_points),
        "loss_points": int(loss_points),
        "notes": notes,
        "updated_teams": updated_teams
    }
    st.session_state.matches.append(match_record)
    save_matches_to_disk(st.session_state.matches)
    return True, "Match result saved and team points updated."


def get_player_mech(team, name):
    return team.get("player_mechs", {}).get(name)


def get_player_call_sign(team, name):
    return team.get("player_callsigns", {}).get(name, "")


def get_team_matches(team_name):
    matches = [m for m in st.session_state.matches if team_name in m.get("participants", [])]
    return sorted(matches, key=lambda x: x.get("date", ""), reverse=True)


def build_match_history_df(matches):
    if not matches:
        return pd.DataFrame([])
    df = pd.DataFrame(matches)
    df["Date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["Participants"] = df["participants"].apply(lambda x: ", ".join(x) if isinstance(x, list) else str(x))
    # Support stored map name on match records
    if "map" in df.columns:
        df["Map"] = df["map"].fillna("")
    else:
        df["Map"] = ""
    # Support stored mission name on match records
    if "mission" in df.columns:
        df["Mission"] = df["mission"].fillna("")
    else:
        df["Mission"] = ""
    df["Win Points"] = df["win_points"]
    df["Loss Points"] = df["loss_points"]
    df["Notes"] = df.get("notes", "")
    return df[["Date", "Winner", "Map", "Mission", "Participants", "Win Points", "Loss Points", "Notes"]]


def get_league_players():
    team_players = []
    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS

    for team in teams:
        for name in team["players"]:
            profile = generate_player_profile(
                name,
                team=team["name"],
                points=team["points"],
                mech=get_player_mech(team, name),
                call_sign=get_player_call_sign(team, name)
            )
            if profile:
                team_players.append(profile)

    return sorted(team_players, key=lambda x: x["Rating"], reverse=True)


def get_rank_progress(rating):
    """Get progress to next rank."""
    current_rank = get_rank(rating)
    rank_list = list(RANKS.keys())
    current_idx = rank_list.index(current_rank)
    
    if current_idx == len(rank_list) - 1:
        return current_rank, 100, "Max rank achieved!"
    
    next_rank = rank_list[current_idx + 1]
    current_min = RANKS[current_rank]["min_rating"]
    next_min = RANKS[next_rank]["min_rating"]
    
    progress = ((rating - current_min) / (next_min - current_min)) * 100
    return next_rank, min(progress, 100), f"To {next_rank}"

# Session state initialization
if "teams" not in st.session_state:
    disk_teams = load_teams_from_disk()
    st.session_state.teams = disk_teams if disk_teams else [dict(t) for t in DEFAULT_TEAMS]

if "player_images" not in st.session_state:
    st.session_state.player_images = load_images_from_disk().get("players", {})

if "matches" not in st.session_state:
    st.session_state.matches = load_matches_from_disk()
if "maps" not in st.session_state:
    st.session_state.maps = load_maps_from_disk()
if "security_work" not in st.session_state:
    st.session_state.security_work = load_security_from_disk()

# Main app
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Leaderboard", "My Profile", "Stats", "Match History", "Match Results", "Rank Info", "Teams", "Maps", "Security Work"])

with tab1:
    st.header("Leaderboard")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        rank_filter = st.selectbox("Filter by Rank:", ["All"] + list(RANKS.keys()), key="rank_filter")
    with col2:
        view_mode = st.selectbox("View:", ["Pilot View", "Team View"], key="leaderboard_view")
    
    if view_mode == "Team View":
        teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
        teams_df = pd.DataFrame([{
            "Team": t["name"],
            "Tier": t["tier"],
            "Points": t["points"],
            "Players": ", ".join(t["players"])
        } for t in teams])
        teams_df = teams_df.sort_values(by="Points", ascending=False)
        st.dataframe(teams_df, use_container_width=True, hide_index=True)
    else:
        players = get_league_players()
        
        if rank_filter != "All":
            players = [p for p in players if p["Rank"] == rank_filter]
        
        df = pd.DataFrame(players)
        df_display = df.copy()
        df_display["Rank"] = df_display["Rank"].apply(lambda x: f"{RANKS[x]['icon']} {x}")
        if "Team" not in df_display.columns:
            df_display["Team"] = "Solo"
        
        df_display["Call Sign"] = df_display.get("Call Sign", "")
        st.dataframe(
            df_display[["Rank", "Username", "Call Sign", "Team", "Rating", "Wins", "Losses", "Winrate", "Main Mech"]],
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.header(" योध Fighter View")

    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
    pilot_entries = get_all_pilots()
    team_names = [team["name"] for team in teams]

    profile_type = st.radio("Profile Type:", ["Pilot", "Team"], horizontal=True, key="profile_type")

    if profile_type == "Pilot":
        selected_pilot = st.selectbox("Select Pilot:", [p["Username"] for p in pilot_entries], key="profile_pilot")
        selected_team = next((p["Team"] for p in pilot_entries if p["Username"] == selected_pilot), "Free Agent")
        selected_team_data = next((t for t in teams if t["name"] == selected_team), None)
        profile = generate_player_profile(selected_pilot, team=selected_team, points=selected_team_data["points"] if selected_team_data else 0)
        history = get_team_matches(selected_team)

        top_col, metrics_col = st.columns([1, 3])
        with top_col:
            st.image(get_avatar_url_for_player(selected_pilot), width=170)
            new_avatar = st.text_input("Pilot image URL", value=st.session_state.player_images.get(selected_pilot, ""), key=f"profile_player_avatar_{selected_pilot}")
            if st.button("Save Pilot Picture", key=f"save_profile_player_avatar_{selected_pilot}"):
                st.session_state.player_images[selected_pilot] = new_avatar.strip()
                save_images_to_disk({"players": st.session_state.player_images, "teams": {}})
                st.success(f"{selected_pilot} picture updated.")
                st.rerun()
        with metrics_col:
            st.subheader(selected_pilot)
            st.write(f"**Team:** {selected_team}")
            st.write(f"**Tier:** {selected_team_data['tier'] if selected_team_data else 'Free Agent'}")
            st.metric("Rating", profile["Rating"], delta="+12")
            st.metric("Rank", f"{RANKS[profile['Rank']]['icon']} {profile['Rank']}")
            st.metric("Win Rate", profile["Winrate"], "±0")

        st.markdown("---")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        with stats_col1:
            st.metric("Wins", profile["Wins"])
        with stats_col2:
            st.metric("Losses", profile["Losses"])
        with stats_col3:
            st.metric("Main Mech", profile["Main Mech"])
        with stats_col4:
            st.metric("Last Played", profile["Last Played"])

        st.markdown("---")
        row1, row2 = st.columns([2, 1])
        with row1:
            st.subheader("Match History")
            history_df = build_match_history_df(history)
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.info("No recorded matches exist for this pilot's team yet.")
        with row2:
            st.subheader("Team Roster")
            if selected_team_data:
                roster_profiles = [generate_player_profile(name, team=selected_team_data["name"], points=selected_team_data["points"]) for name in selected_team_data["players"]]
                roster_df = pd.DataFrame([{
                    "Pilot": p["Username"],
                    "Rank": p["Rank"],
                    "Rating": p["Rating"],
                    "Winrate": p["Winrate"]
                } for p in roster_profiles])
                st.dataframe(roster_df, use_container_width=True, hide_index=True)
            else:
                st.info("Free agent pilots do not currently belong to a roster.")

    else:
        selected_team = st.selectbox("Select Team:", team_names, key="profile_team")
        team_data = next((t for t in teams if t["name"] == selected_team), None)
        team_summary = get_team_summary(team_data)
        history = get_team_matches(selected_team)

        top_col, metrics_col = st.columns([1, 3])
        with top_col:
            st.image(get_avatar_url_for_team(team_data), width=170)
            new_team_avatar = st.text_input("Team image URL", value=team_data.get("avatar_url", ""), key=f"profile_team_avatar_{team_data['id']}")
            if st.button("Save Team Picture", key=f"save_profile_team_avatar_{team_data['id']}"):
                team_data["avatar_url"] = new_team_avatar.strip()
                save_teams_to_disk(st.session_state.teams)
                st.success(f"{selected_team} picture updated.")
                st.rerun()
        with metrics_col:
            st.subheader(selected_team)
            st.write(f"**Tier:** {team_data['tier']}")
            st.metric("Points", team_data["points"], delta="+10")
            st.metric("Wins", team_data["wins"])
            st.metric("Losses", team_data["losses"])
            st.metric("Roster Size", f"{len(team_data['players'])}/6")

        st.markdown("---")
        stat_row1, stat_row2, stat_row3 = st.columns(3)
        with stat_row1:
            st.metric("Avg Rating", team_summary["avg_rating"])
        with stat_row2:
            st.metric("Avg Winrate", team_summary["avg_winrate"])
        with stat_row3:
            st.metric("Total Matches", team_summary["total_wins"] + team_summary["total_losses"])

        st.markdown("---")
        st.subheader("Team Roster")
        st.dataframe(team_summary["roster_table"], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Recent Team Matches")
        history_df = build_match_history_df(history)
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("No recorded matches exist for this team yet.")

with tab3:
    st.header("Statistics & Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mech Performance")
        # Collect mechs assigned to teams (including NPC mechs)
        teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
        mech_map = {}
        for t in teams:
            for mech in t.get("player_mechs", {}).values():
                if mech:
                    mech_map.setdefault(mech, set()).add(t["name"])
            for npc in t.get("npc_mechs", []) or []:
                if isinstance(npc, dict):
                    m = npc.get("mech") or ""
                    if m:
                        mech_map.setdefault(m, set()).add(t["name"])
                elif isinstance(npc, str) and npc:
                    mech_map.setdefault(npc, set()).add(t["name"])

        mech_rows = []
        for mech, teams_using in sorted(mech_map.items()):
            mech_rows.append({
                "Mech": mech,
                "Assigned Count": len(teams_using),
                "Teams": ", ".join(sorted(teams_using))
            })
        if mech_rows:
            mech_stats = pd.DataFrame(mech_rows)
            st.dataframe(mech_stats, use_container_width=True, hide_index=True)
        else:
            st.info("No mechs assigned to teams yet.")
    
    with col2:
        st.subheader("Map Performance")
        maps_list = st.session_state.maps if "maps" in st.session_state else []
        matches = st.session_state.matches if "matches" in st.session_state else []
        map_rows = []
        for m in maps_list:
            name = m.get("name")
            match_count = sum(1 for mm in matches if mm.get("map") == name)
            mission_counts = {}
            for mm in matches:
                if mm.get("map") == name:
                    ms = mm.get("mission") or "Unknown"
                    mission_counts[ms] = mission_counts.get(ms, 0) + 1
            top_missions = ", ".join([f"{k}({v})" for k, v in sorted(mission_counts.items(), key=lambda x: -x[1])]) if mission_counts else ""
            map_rows.append({"Map": name, "Matches": match_count, "Top Missions": top_missions})
        if map_rows:
            map_stats = pd.DataFrame(map_rows)
            st.dataframe(map_stats, use_container_width=True, hide_index=True)
        else:
            st.info("No maps defined or no matches recorded yet.")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rating Over Time")
        rating_data = pd.DataFrame({
            "Days Ago": list(range(30, 0, -1)),
            "Rating": sorted([1800 + random.randint(-100, 400) for _ in range(30)])
        })
        st.line_chart(rating_data.set_index("Days Ago"))
    
    with col2:
        st.subheader("Win/Loss Distribution")
        wl_data = pd.DataFrame({
            "Result": ["Wins", "Losses"],
            "Count": [156, 96]
        })
        st.bar_chart(wl_data.set_index("Result"))

with tab4:
    st.header("Match History")
    
    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
    team_names = [team["name"] for team in teams]

    col1, col2, col3 = st.columns(3)
    with col1:
        result_filter = st.selectbox("Result:", ["All", "Win", "Loss"], key="result_filter")
    with col2:
        team_filter = st.selectbox("Team:", ["All"] + team_names, key="match_history_team_filter")
    with col3:
        limit = st.selectbox("Show:", [5, 10, 20, 50], key="match_limit")

    matches = sorted(st.session_state.matches, key=lambda x: x.get("date", ""), reverse=True)
    if team_filter != "All":
        matches = [m for m in matches if team_filter in m.get("participants", [])]
        if result_filter == "Win":
            matches = [m for m in matches if m.get("winner") == team_filter]
        elif result_filter == "Loss":
            matches = [m for m in matches if team_filter in m.get("participants", []) and m.get("winner") != team_filter]
    elif result_filter != "All":
        st.warning("Select a specific team to filter by Win/Loss results.")
    matches = matches[:limit]

    st.markdown("---")
    if matches:
        match_df = build_match_history_df(matches)
        st.dataframe(match_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recorded matches to display with the current filters.")

with tab5:
    st.header("Match Results Entry")
    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
    team_names = [team["name"] for team in teams]

    with st.expander("Miyo Discord Match Results Settings", expanded=True):
        match_results_webhook = st.text_input(
            "Match Results Channel Webhook URL",
            value=st.session_state.get("match_results_webhook", DEFAULT_MATCH_RESULTS_WEBHOOK),
            placeholder="Webhook created in Discord #match-results channel",
            key="match_results_webhook"
        )
        match_results_avatar = st.text_input(
            "Miyo Avatar URL (optional)",
            value=st.session_state.get("match_results_avatar", ""),
            key="match_results_avatar"
        )
        st.write("Miyo will post to the default match-results webhook unless you override it here.")

    st.markdown("---")
    st.subheader("Season Controls")
    with st.expander("New season and end-of-season flow", expanded=True):
        cs1, cs2 = st.columns(2)
        with cs1:
            if st.button("Start New Season", key="start_new_season"):
                reset_season()
                st.success("New season started: wins/losses reset, ranks preserved.")
                new_season_message = (
                    "Hey there fighters, Watchers, Fan, Investors and support teams. "
                    "The new Mara season is live, support your favorate teams and lets all cheer them to victory"
                )
                webhook_to_use = st.session_state.get("match_results_webhook") or DEFAULT_MATCH_RESULTS_WEBHOOK
                if webhook_to_use:
                    post_to_discord(
                        webhook_to_use,
                        new_season_message,
                        username="Miyo",
                        avatar_url=st.session_state.get("match_results_avatar")
                    )
                st.rerun()
        with cs2:
            if st.button("Prepare End of Season Pairings", key="prepare_end_of_season"):
                st.session_state.promotion_pairings = get_promotion_pairings(st.session_state.teams)
                if st.session_state.promotion_pairings:
                    st.success("End-of-season promotion pairings prepared.")
                    webhook_to_use = st.session_state.get("match_results_webhook") or DEFAULT_MATCH_RESULTS_WEBHOOK
                    if webhook_to_use:
                        pairing_message = format_end_of_season_pairings_message(st.session_state.promotion_pairings)
                        post_to_discord(
                            webhook_to_use,
                            pairing_message,
                            username="Miyo",
                            avatar_url=st.session_state.get("match_results_avatar")
                        )
                else:
                    st.warning("Not enough teams in adjacent ranks to prepare promotion pairings.")
                st.rerun()

    if len(team_names) < 2:
        st.warning("Create at least two teams before recording match results.")
    else:
        participants = st.multiselect("Participating Teams", team_names, key="match_participants")
        if len(participants) >= 2:
            winner = st.selectbox("Winning Team", participants, key="match_winner")
            col1, col2 = st.columns(2)
            with col1:
                win_points = st.number_input("Winner Points Gain", value=20, step=1, key="match_win_points")
            with col2:
                loss_points = st.number_input("Loser Points Loss", value=-10, step=1, key="match_loss_points")
            notes = st.text_area("Match Notes", key="match_notes")
            # Map selection for the match
            available_maps = [m.get("name") for m in st.session_state.maps] if st.session_state.get("maps") else []
            map_choice = st.selectbox("Map", ["None"] + available_maps, key="match_map_select")
            # Mission selection based on chosen map
            if map_choice and map_choice != "None":
                map_obj = get_map_by_name(map_choice)
                objectives = map_obj.get("objectives", []) if map_obj else []
                mission_choice = st.selectbox("Mission Type", ["None"] + objectives, key="match_mission_select")
            else:
                mission_choice = st.selectbox("Mission Type", ["None"], key="match_mission_select")

            if st.button("Record Match Result", key="record_match_result"):
                selected_map = "" if map_choice == "None" else map_choice
                selected_mission = "" if not mission_choice or mission_choice == "None" else mission_choice
                success, message = apply_match_result(participants, winner, win_points, loss_points, notes, map_name=selected_map, mission_name=selected_mission)
                if success:
                    st.success(message)
                    webhook_to_use = match_results_webhook or DEFAULT_MATCH_RESULTS_WEBHOOK
                    if webhook_to_use:
                        match_record = st.session_state.matches[-1]
                        content = format_match_result_message(match_record)
                        discord_success, discord_msg = post_to_discord(
                            webhook_to_use,
                            content,
                            username="Miyo",
                            avatar_url=match_results_avatar
                        )
                        if discord_success:
                            st.success("Miyo posted the match to the Discord #match-results channel.")
                        else:
                            st.error(f"Miyo failed to post to Discord: {discord_msg}")

                        hype_success, hype_msg = send_hype_or_salt_messages(
                            webhook_to_use,
                            avatar_url=match_results_avatar,
                            count=3
                        )
                        if hype_success:
                            st.success(hype_msg)
                        else:
                            st.warning(hype_msg)
                    else:
                        st.info("Match recorded. Add your #match-results channel webhook above to post automatically.")
                else:
                    st.error(message)
        else:
            st.info("Select two or more participating teams to record a match.")

    if st.session_state.get("promotion_pairings"):
        st.markdown("---")
        st.subheader("End of Season Promotion Matches")
        promotion_form = st.form("promotion_results_form")
        winner_choices = {}
        for pair in st.session_state.promotion_pairings:
            promotion_form.write(f"**{pair['lower_team']}** ({pair['lower_rank']}) vs **{pair['higher_team']}** ({pair['higher_rank']})")
            winner_choices[pair["pair_id"]] = promotion_form.radio(
                "Winner", [pair["lower_team"], pair["higher_team"]], key=f"winner_{pair['pair_id']}")
            promotion_form.markdown("---")
        apply_results = promotion_form.form_submit_button("Apply End of Season Results")
        if apply_results:
            summary = apply_end_of_season_results(st.session_state.promotion_pairings, winner_choices)
            if summary:
                for item in summary:
                    st.success(item)
            else:
                st.warning("No promotion results were applied.")
            webhook_to_use = st.session_state.get("match_results_webhook") or DEFAULT_MATCH_RESULTS_WEBHOOK
            if webhook_to_use:
                results_message = format_season_final_results_message(summary)
                post_to_discord(
                    webhook_to_use,
                    results_message,
                    username="Miyo",
                    avatar_url=st.session_state.get("match_results_avatar")
                )
            st.session_state.promotion_pairings = []
            st.rerun()

    st.markdown("---")
    st.subheader("Promotion Candidates")
    promotion_candidates = get_promotion_candidates(teams)
    promo_df = pd.DataFrame([{
        "Team": t["name"],
        "Tier": t["tier"],
        "Points": t["points"],
        "Wins": t.get("wins", 0),
        "Losses": t.get("losses", 0)
    } for t in promotion_candidates])
    st.dataframe(promo_df, use_container_width=True, hide_index=True)
    st.write(f"The top {SEASON_PROMOTION_SPOTS} teams are in line for season promotion or top-tier placement.")

    st.markdown("---")
    st.subheader("Season Match Results")
    if st.session_state.matches:
        matches_df = pd.DataFrame([{
            "Date": m["date"],
            "Winner": m["winner"],
            "Participants": ", ".join(m["participants"]),
            "Win Points": m["win_points"],
            "Loss Points": m["loss_points"],
            "Notes": m.get("notes", "")
        } for m in reversed(st.session_state.matches)])
        st.dataframe(matches_df, use_container_width=True, hide_index=True)
    else:
        st.info("No season match results recorded yet.")

with tab6:
    st.header(" Rank Information")
    
    for rank_name, rank_info in RANKS.items():
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            st.markdown(f"<div style='font-size: 40px; text-align: center;'>{rank_info['icon']}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='font-size: 20px; font-weight: bold; color: {rank_info['color']};'>{rank_name}</div>", unsafe_allow_html=True)
            st.write(f"Rating: **{rank_info['min_rating']}+**")
        
        with col3:
            rank_rewards = {
                "Bronze": ["1 Mech Blueprint", "100 Credits"],
                "Silver": ["2 Mech Blueprints", "250 Credits"],
                "Gold": ["3 Mech Blueprints", "500 Credits", "1 Weapon Skin"],
                "Platinum": ["4 Mech Blueprints", "1000 Credits", "2 Weapon Skins"],
                "Diamond": ["5 Mech Blueprints", "2000 Credits", "3 Weapon Skins", "1 Exclusive Skin"],
                "Legendary": ["Exclusive Mech", "5000 Credits", "All Skins", "Title: Legendary"]
            }
            st.write("**Season Rewards:**")
            for reward in rank_rewards.get(rank_name, []):
                st.write(f"• {reward}")
        
        st.divider()

with tab7:
    st.header("Teams")

    # Initialize session teams storage (load from disk if present)
    if "teams" not in st.session_state:
        disk_teams = load_teams_from_disk()
        if disk_teams:
            st.session_state.teams = disk_teams
        else:
            st.session_state.teams = [dict(t) for t in DEFAULT_TEAMS]
    if "player_images" not in st.session_state:
        st.session_state.player_images = load_images_from_disk().get("players", {})

    st.subheader("Import Lancer / Obsidian Roster Files")
    uploaded_files = st.file_uploader(
        "Upload team/pilot JSON or Obsidian markdown files", 
        type=["json", "md", "markdown", "txt"], 
        accept_multiple_files=True,
        key="import_files"
    )
    if uploaded_files:
        imported_teams = import_teams_from_files(uploaded_files)
        if imported_teams:
            existing_names = [t["name"] for t in st.session_state.teams]
            added = 0
            for imported_team in imported_teams:
                padded_groups = pad_or_split_team(imported_team)
                for group in padded_groups:
                    group_name = normalize_import_team_name(group["name"], existing_names)
                    existing_names.append(group_name)
                    team = {
                        "id": generate_team_id(st.session_state.teams),
                        "name": group_name,
                        "tier": get_rank(group.get("points", 0) or 0),
                        "points": int(group.get("points", 0) or 0),
                        "wins": 0,
                        "losses": 0,
                        "created": datetime.now().isoformat(),
                        "players": group["players"],
                        "player_mechs": group.get("player_mechs", {}),
                        "avatar_url": ""
                    }
                    st.session_state.teams.append(team)
                    added += 1
            save_teams_to_disk(st.session_state.teams)
            st.success(f"Imported {added} team(s) from uploaded files.")
        else:
            st.warning("No valid teams found in the uploaded files.")

    # Team creation form
    with st.expander("Create a new team"):
        with st.form("create_team_form"):
            team_name = st.text_input("Team Name")
            st.caption("Tier is auto-assigned based on starting points; you cannot choose it here.")
            cols = st.columns([2, 1, 1])
            players_inputs = []
            player_callsigns = []
            mech_inputs = []
            for i in range(6):
                with cols[0]:
                    players_inputs.append(st.text_input(f"Player {i+1}", key=f"player_input_{i}"))
                with cols[1]:
                    player_callsigns.append(st.text_input(f"Call Sign {i+1}", key=f"player_call_sign_{i}"))
                with cols[2]:
                    mech_inputs.append(st.selectbox(f"Mech {i+1}", MECHS, index=0, key=f"player_mech_{i}"))
            npc_mechs_text = st.text_area("NPC Mechs (one per line: Name:Type)", key="new_team_npc_mechs", height=80)
            init_points = st.number_input("Starting Points", value=0, step=1)
            submitted = st.form_submit_button("Create Team")
            if submitted:
                tier_choice = get_rank(int(init_points))
                # parse npc mechs
                npc_mechs = []
                for line in (npc_mechs_text or "").splitlines():
                    if not line.strip():
                        continue
                    parts = line.split(":", 1)
                    name = parts[0].strip()
                    mech_type = parts[1].strip() if len(parts) > 1 else ""
                    npc_mechs.append({"name": name, "mech": mech_type})
                ok = add_team(team_name, tier_choice, players_inputs, mech_inputs, init_points, player_callsigns, npc_mechs=npc_mechs)
                if ok:
                    st.success(f"Team '{team_name}' created and placed in tier: {tier_choice}.")

    # Team leaderboard and selection
    st.subheader("Team Leaderboard")
    if len(st.session_state.teams) == 0:
        st.info("No teams yet — create one using the form above.")
    else:
        teams_df = pd.DataFrame([{
            "Team": t["name"],
            "Tier": t["tier"],
            "Points": t["points"],
            "Players": ", ".join(t["players"])
        } for t in st.session_state.teams])
        teams_df = teams_df.sort_values(by="Points", ascending=False)
        st.dataframe(teams_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    if st.session_state.teams:
        st.subheader("Manage Teams")
        cols = st.columns([2, 1, 1])
        with cols[0]:
            team_select = st.selectbox("Select Team:", [t["name"] for t in st.session_state.teams], key="manage_team_select")
        with cols[1]:
            pts_delta = st.number_input("Add / Remove Points", value=0, step=1, key="points_delta")
        with cols[2]:
            apply_pts = st.button("Apply Points", key="apply_points")

        if team_select:
            selected = get_team_by_name(team_select)
            if selected:
                st.markdown(f"**{selected['name']}** — Tier: {selected['tier']} — Points: {selected['points']}")
                roster_display = ", ".join([f"{name} ({get_player_mech(selected, name)})" for name in selected["players"]])
                st.write(f"Players ({len(selected['players'])}/6): {roster_display}")
                st.write(f"Wins: {selected['wins']}  Losses: {selected['losses']}")

                st.markdown("---")
                st.subheader("Edit Team")
                edit_name = st.text_input("Team Name", selected["name"], key=f"edit_team_name_{selected['id']}")
                available_tiers = list(RANKS.keys())
                current_tier = selected.get("tier", available_tiers[0])
                tier_key = f"edit_team_tier_{selected['id']}"
                tier_cols = st.columns([5, 1, 1])
                with tier_cols[0]:
                    edit_tier = st.selectbox(
                        "Team Rank (Manual Override)",
                        available_tiers,
                        index=available_tiers.index(current_tier) if current_tier in available_tiers else 0,
                        key=tier_key
                    )
                with tier_cols[1]:
                    st.write("")
                    if st.button("Promote", key=f"promote_team_{selected['id']}"):
                        active_tier = st.session_state.get(tier_key, current_tier)
                        active_index = available_tiers.index(active_tier) if active_tier in available_tiers else 0
                        if active_index < len(available_tiers) - 1:
                            st.session_state[tier_key] = available_tiers[active_index + 1]
                        st.rerun()
                with tier_cols[2]:
                    st.write("")
                    if st.button("Demote", key=f"demote_team_{selected['id']}"):
                        active_tier = st.session_state.get(tier_key, current_tier)
                        active_index = available_tiers.index(active_tier) if active_tier in available_tiers else 0
                        if active_index > 0:
                            st.session_state[tier_key] = available_tiers[active_index - 1]
                        st.rerun()
                edit_points = st.number_input("Team Points", value=selected["points"], step=1, key=f"edit_team_points_{selected['id']}")
                player_cols = st.columns([2, 1, 1])
                edited_players = []
                edited_mechs = {}
                edited_callsigns = {}
                for i in range(6):
                    current_player = selected["players"][i] if i < len(selected["players"]) else ""
                    current_mech = get_player_mech(selected, current_player) or MECHS[0]
                    current_callsign = selected.get("player_callsigns", {}).get(current_player, "") if current_player else ""
                    with player_cols[0]:
                        player_name = st.text_input(f"Player {i+1}", value=current_player, key=f"edit_player_name_{selected['id']}_{i}")
                    with player_cols[1]:
                        player_callsign = st.text_input(f"Call Sign {i+1}", value=current_callsign, key=f"edit_player_call_sign_{selected['id']}_{i}")
                    with player_cols[2]:
                        player_mech = st.selectbox(f"Mech {i+1}", MECHS, index=MECHS.index(current_mech) if current_mech in MECHS else 0, key=f"edit_player_mech_{selected['id']}_{i}")
                    if player_name.strip():
                        edited_players.append(player_name.strip())
                        edited_mechs[player_name.strip()] = player_mech
                        edited_callsigns[player_name.strip()] = player_callsign.strip()
                # NPC mechs editing
                existing_npc_lines = []
                for npc in selected.get("npc_mechs", []):
                    if isinstance(npc, dict):
                        existing_npc_lines.append(f"{npc.get('name','')}: {npc.get('mech','')}")
                    else:
                        existing_npc_lines.append(str(npc))
                npc_mechs_text = st.text_area("NPC Mechs (one per line: Name:Type)", value="\n".join(existing_npc_lines), key=f"edit_npc_mechs_{selected['id']}")
                if st.button("Save Team Changes", key=f"save_team_changes_{selected['id']}"):
                    if not edit_name.strip():
                        st.error("Team name cannot be empty.")
                    elif any(t["name"].lower() == edit_name.strip().lower() and t["id"] != selected["id"] for t in st.session_state.teams):
                        st.error("Another team already uses that name.")
                    else:
                        # parse npc mechs text into list
                        npc_mechs_list = []
                        for line in (npc_mechs_text or "").splitlines():
                            if not line.strip():
                                continue
                            parts = line.split(":", 1)
                            n = parts[0].strip()
                            m = parts[1].strip() if len(parts) > 1 else ""
                            npc_mechs_list.append({"name": n, "mech": m})
                        update_team(
                            selected["id"],
                            name=edit_name.strip(),
                            tier=edit_tier,
                            points=edit_points,
                            players=edited_players,
                            player_mechs=edited_mechs,
                            player_callsigns=edited_callsigns,
                            npc_mechs=npc_mechs_list
                        )
                        st.success("Team updated successfully.")
                        st.rerun()

                st.markdown("---")
                st.subheader("Team Picture")
                selected_team_avatar = get_avatar_url_for_team(selected)
                st.image(selected_team_avatar, width=120)
                new_team_avatar = st.text_input("Team image URL", value=selected.get("avatar_url", ""), key=f"team_avatar_{selected['id']}")
                if st.button("Save Team Picture", key=f"save_team_avatar_{selected['id']}"):
                    selected["avatar_url"] = new_team_avatar.strip()
                    save_teams_to_disk(st.session_state.teams)
                    st.success("Team picture updated.")
                    st.rerun()

                st.markdown("---")
                st.subheader("Player Avatars")
                for player in selected["players"]:
                    mech_choice = get_player_mech(selected, player) or MECHS[0]
                    player_avatar = get_avatar_url_for_player(player)
                    st.write(f"**{player}** — {mech_choice}")
                    st.image(player_avatar, width=90)
                    new_player_avatar = st.text_input("Image URL", value=st.session_state.player_images.get(player, ""), key=f"player_avatar_{player}_{selected['id']}")
                    new_player_mech = st.selectbox("Select Mech", MECHS, index=MECHS.index(mech_choice) if mech_choice in MECHS else 0, key=f"player_mech_select_{player}_{selected['id']}")
                    if st.button(f"Save {player} Settings", key=f"save_player_settings_{player}_{selected['id']}"):
                        st.session_state.player_images[player] = new_player_avatar.strip()
                        selected.setdefault("player_mechs", {})[player] = new_player_mech
                        save_images_to_disk({"players": st.session_state.player_images, "teams": {}})
                        save_teams_to_disk(st.session_state.teams)
                        st.success(f"{player} picture and mech updated.")
                        st.rerun()

                col1, col2, col3 = st.columns(3)
                with col1:
                    add_pts = st.button("+ Points", key=f"add_{selected['id']}")
                with col2:
                    sub_pts = st.button("- Points", key=f"sub_{selected['id']}")
                with col3:
                    remove_team = st.button("Delete Team", key=f"del_{selected['id']}")

                if apply_pts and pts_delta != 0:
                    update_team_points(selected["id"], pts_delta)
                    st.rerun()

                if add_pts:
                    delta = st.number_input("Points to add", value=1, min_value=1, step=1, key=f"add_val_{selected['id']}")
                    update_team_points(selected["id"], delta)
                    st.rerun()

                if sub_pts:
                    delta = st.number_input("Points to remove", value=1, min_value=1, step=1, key=f"sub_val_{selected['id']}")
                    update_team_points(selected["id"], -delta)
                    st.rerun()

                if remove_team:
                    delete_team(selected["id"])
                    st.success(f"Team {selected['name']} deleted.")
                    st.rerun()

        st.markdown("---")
        st.subheader("Transfer Pilots")
        team_names = [t["name"] for t in st.session_state.teams]
        source_team_name = st.selectbox("Source Team", team_names, key="source_team")
        source_team = get_team_by_name(source_team_name)
        transfer_success = False

        if source_team:
            target_names = [name for name in team_names if name != source_team_name]
            if target_names:
                pilot_to_move = st.selectbox("Pilot to move", source_team["players"], key="pilot_to_move")
                target_team_name = st.selectbox("Destination Team", target_names, key="target_team")
                if st.button("Move Pilot", key="move_pilot"):
                    if move_pilot(pilot_to_move, source_team_name, target_team_name):
                        st.success(f"Moved {pilot_to_move} from {source_team_name} to {target_team_name}.")
                        st.rerun()
                    else:
                        st.error("Unable to move pilot. Ensure the destination team has fewer than 6 pilots.")
            else:
                st.info("Add a second team to enable pilot transfers.")

        st.markdown("---")
        st.subheader("Pilot Stats")
        all_pilots = sorted([player for t in st.session_state.teams for player in t["players"]])
        if all_pilots:
            selected_pilot = st.selectbox("Select Pilot", all_pilots, key="selected_pilot")
            pilot_team = next((t for t in st.session_state.teams if selected_pilot in t["players"]), None)
            profile = generate_player_profile(
                selected_pilot,
                team=pilot_team["name"] if pilot_team else None,
                points=pilot_team["points"] if pilot_team else 0,
                mech=get_player_mech(pilot_team, selected_pilot) if pilot_team else None
            )
            if profile:
                pilot_avatar = get_avatar_url_for_player(selected_pilot)
                with st.expander("Pilot Picture", expanded=True):
                    st.image(pilot_avatar, width=140)
                    new_avatar = st.text_input("Player image URL", value=st.session_state.player_images.get(selected_pilot, ""), key=f"profile_player_avatar_{selected_pilot}")
                    if st.button("Save Pilot Picture", key=f"save_profile_player_avatar_{selected_pilot}"):
                        st.session_state.player_images[selected_pilot] = new_avatar.strip()
                        save_images_to_disk({"players": st.session_state.player_images, "teams": {}})
                        st.success(f"{selected_pilot} picture updated.")
                        st.rerun()

                pcol1, pcol2, pcol3, pcol4 = st.columns(4)
                with pcol1:
                    st.metric("Rating", profile["Rating"])
                with pcol2:
                    st.metric("Rank", f"{RANKS[profile['Rank']]['icon']} {profile['Rank']}")
                with pcol3:
                    st.metric("Wins", profile["Wins"])
                with pcol4:
                    st.metric("Losses", profile["Losses"])

                st.write(f"**Team:** {profile['Team']}")
                st.write(f"**Main Mech:** {profile['Main Mech']}")
                st.write(f"**Win Rate:** {profile['Winrate']}")
                st.write(f"**Last Played:** {profile['Last Played']}")

                st.markdown("---")
                st.subheader("Recent Team Matches")
                history = get_team_matches(pilot_team["name"]) if pilot_team else []
                history_df = build_match_history_df(history)
                if not history_df.empty:
                    st.dataframe(history_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No recorded matches exist for this pilot's team yet.")
        else:
            st.info("No pilots have been assigned to teams yet.")
    else:
        st.info("No teams to manage yet. Create one using the form above.")

with tab8:
    st.header("Map Creator & Library")
    maps = st.session_state.maps if "maps" in st.session_state else []
    map_names = [m["name"] for m in maps]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Create / Import Maps")
        with st.form("create_map_form"):
            map_name = st.text_input("Map Name", key="new_map_name")
            map_description = st.text_area("Description", key="new_map_description", height=120)
            objective_1 = st.text_input("Mission Objective 1", key="new_map_obj_1")
            objective_2 = st.text_input("Mission Objective 2", key="new_map_obj_2")
            objective_3 = st.text_input("Mission Objective 3", key="new_map_obj_3")
            map_image_url = st.text_input("Map Image URL", key="new_map_image_url")
            deployment_image_url = st.text_input("Deployment Plan Image URL", key="new_map_deployment_image_url")
            special_reaction = st.text_input("Special Reaction", key="new_map_special_reaction")
            environment = st.text_input("Environment", key="new_map_environment")
            create_map = st.form_submit_button("Create Map")
            if create_map:
                objectives = [objective_1, objective_2, objective_3]
                success = add_map(map_name, map_description, objectives, map_image_url, deployment_image_url, special_reaction, environment)
                if success:
                    st.success(f"Map '{map_name}' saved.")
                    st.experimental_rerun()
                else:
                    st.error("Map name is required and must be unique.")

        st.markdown("---")
        st.subheader("Import Map JSON")
        uploaded_map_files = st.file_uploader(
            "Upload Comp Com or map JSON files",
            type=["json"],
            accept_multiple_files=True,
            key="import_map_files"
        )
        if uploaded_map_files:
            imported_maps = import_maps_from_files(uploaded_map_files)
            imported_count = 0
            for imported_map in imported_maps:
                if imported_map["name"] and not any(m["name"].lower() == imported_map["name"].lower() for m in st.session_state.maps):
                    st.session_state.maps.append({
                        "id": f"map_{len(st.session_state.maps) + 1}",
                        **imported_map
                    })
                    imported_count += 1
            if imported_count > 0:
                save_maps_to_disk(st.session_state.maps)
                st.success(f"Imported {imported_count} map(s) from JSON.")
                st.experimental_rerun()
            else:
                st.warning("No valid new maps were found in uploaded files.")

    with col2:
        st.subheader("Map Library")
        if maps:
            selected_map_name = st.selectbox("Select Map", ["New Map"] + map_names, key="selected_map_name")
            if selected_map_name and selected_map_name != "New Map":
                selected_map = get_map_by_name(selected_map_name)
                if selected_map:
                    st.markdown(f"### {selected_map['name']}")
                    if selected_map.get("image_url"):
                        st.image(selected_map["image_url"], caption="Map Image", use_column_width=True)
                    if selected_map.get("deployment_image_url"):
                        st.image(selected_map["deployment_image_url"], caption="Deployment Plan", use_column_width=True)
                    st.markdown("**Description**")
                    st.write(selected_map.get("description", "No description provided."))
                    st.markdown("**Mission Objectives**")
                    if selected_map.get("objectives"):
                        for idx, objective in enumerate(selected_map["objectives"], 1):
                            st.write(f"{idx}. {objective}")
                    else:
                        st.write("No objectives set.")
                    st.markdown("**Special Reaction**")
                    st.write(selected_map.get("special_reaction", "None"))
                    st.markdown("**Environment**")
                    st.write(selected_map.get("environment", "Unknown"))
                    if st.button("Delete Map", key=f"delete_map_{selected_map['id']}"):
                        if delete_map(selected_map["id"]):
                            st.success("Map deleted.")
                            st.experimental_rerun()
                        else:
                            st.error("Unable to delete map.")
        else:
            st.info("No maps created yet. Use the form on the left to add one.")

with tab9:
    st.header("Security Work")
    teams = st.session_state.teams if "teams" in st.session_state else DEFAULT_TEAMS
    team_names = [team["name"] for team in teams]
    pilot_names = [pilot["Username"] for pilot in get_all_pilots()]

    with st.expander("Miyo Security Work Settings", expanded=True):
        security_work_webhook = st.text_input(
            "Security Work Channel Webhook URL",
            value=st.session_state.get("security_work_webhook", st.session_state.get("match_results_webhook", DEFAULT_MATCH_RESULTS_WEBHOOK)),
            placeholder="Webhook created in Discord #security-work channel",
            key="security_work_webhook"
        )
        security_work_avatar = st.text_input(
            "Miyo Avatar URL (optional)",
            value=st.session_state.get("security_work_avatar", st.session_state.get("match_results_avatar", "")),
            key="security_work_avatar"
        )

    st.subheader("Log Security Mission")
    with st.form("security_work_form"):
        mission_name = st.text_input("Mission Name", key="security_mission_name")
        mission_description = st.text_area("Mission Description", key="security_mission_description", height=120)
        work_details = st.text_area("Work Completed", key="security_work_details", height=120)
        involved_teams = st.multiselect("Teams Involved", team_names, key="security_involved_teams")
        involved_pilots = st.multiselect("Pilots Involved", pilot_names, key="security_involved_pilots")

        pcol1, pcol2 = st.columns(2)
        with pcol1:
            team_points = st.number_input("League Points Per Team", value=0, step=1, key="security_team_points")
        with pcol2:
            pilot_points = st.number_input("League Points Per Pilot", value=0, step=1, key="security_pilot_points")

        submit_security = st.form_submit_button("Submit Mission To Security Work History")
        if submit_security:
            if not mission_name.strip():
                st.error("Mission name is required.")
            elif not mission_description.strip() and not work_details.strip():
                st.error("Please provide a mission description or work details.")
            else:
                team_updates = []
                pilot_updates = []

                if int(team_points) != 0:
                    for team_name in involved_teams:
                        team = get_team_by_name(team_name)
                        if team:
                            team["points"] = int(team.get("points", 0)) + int(team_points)
                            team_updates.append({
                                "team": team_name,
                                "points": int(team_points),
                                "new_points": int(team.get("points", 0))
                            })

                if int(pilot_points) != 0:
                    for pilot_name in involved_pilots:
                        pilot_team = next((t for t in st.session_state.teams if pilot_name in t.get("players", [])), None)
                        if pilot_team:
                            pilot_team["points"] = int(pilot_team.get("points", 0)) + int(pilot_points)
                            pilot_updates.append({
                                "pilot": pilot_name,
                                "team": pilot_team["name"],
                                "points": int(pilot_points),
                                "new_points": int(pilot_team.get("points", 0))
                            })

                if team_updates or pilot_updates:
                    save_teams_to_disk(st.session_state.teams)

                security_entry = {
                    "id": f"security_{len(st.session_state.security_work) + 1}",
                    "date": datetime.now().isoformat(),
                    "mission": mission_name.strip(),
                    "description": mission_description.strip(),
                    "work": work_details.strip(),
                    "teams": involved_teams,
                    "pilots": involved_pilots,
                    "team_points": int(team_points),
                    "pilot_points": int(pilot_points),
                    "team_updates": team_updates,
                    "pilot_updates": pilot_updates
                }
                st.session_state.security_work.append(security_entry)
                save_security_to_disk(st.session_state.security_work)

                webhook_to_use = security_work_webhook or st.session_state.get("match_results_webhook") or DEFAULT_MATCH_RESULTS_WEBHOOK
                if webhook_to_use:
                    content = format_security_work_message(security_entry)
                    discord_success, discord_msg = post_to_discord(
                        webhook_to_use,
                        content,
                        username="Miyo",
                        avatar_url=security_work_avatar
                    )
                    if discord_success:
                        st.success("Security work saved and Miyo posted the report to Discord.")
                    else:
                        st.warning(f"Security work saved, but Discord post failed: {discord_msg}")
                else:
                    st.success("Security work saved.")

                st.rerun()

    st.markdown("---")
    st.subheader("Security Work History")
    entries = sorted(st.session_state.security_work, key=lambda x: x.get("date", ""), reverse=True)
    if entries:
        history_df = pd.DataFrame([{
            "Date": datetime.fromisoformat(e["date"]).strftime("%Y-%m-%d %H:%M") if e.get("date") else "",
            "Mission": e.get("mission", ""),
            "Teams": ", ".join(e.get("teams", [])),
            "Pilots": ", ".join(e.get("pilots", [])),
            "Team Pts/Unit": e.get("team_points", 0),
            "Pilot Pts/Unit": e.get("pilot_points", 0)
        } for e in entries])
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        with st.expander("View Full Security Work Notes", expanded=False):
            for e in entries:
                st.markdown(f"**{e.get('mission', 'Untitled Mission')}** - {e.get('date', '')[:19]}")
                st.write(f"Description: {e.get('description', '')}")
                st.write(f"Work: {e.get('work', '')}")
                st.write(f"Teams: {', '.join(e.get('teams', [])) if e.get('teams') else 'None'}")
                st.write(f"Pilots: {', '.join(e.get('pilots', [])) if e.get('pilots') else 'None'}")
                st.markdown("---")
    else:
        st.info("No security work has been logged yet.")
