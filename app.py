import os
import math
import requests
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

PLANETS_KM = {
    "sun": 0, "mercury": 57900000, "venus": 108200000, "earth": 149600000,
    "moon": 149600000 + 384400, "mars": 227900000, "jupiter": 778500000,
    "saturn": 1433000000, "uranus": 2872500000, "neptune": 4495100000
}

def haversine_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def get_coordinates(location_name):
    url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
    headers = {"User-Agent": "CosmicStackApp/1.0"}
    try:
        response = requests.get(url, headers=headers).json()
        if response:
            return {"lat": float(response[0]["lat"]), "lon": float(response[0]["lon"]), "name": response[0]["name"]}
    except Exception as e:
        print(f"[!] OSM Geocoding Error: {e}")
    return None

def get_object_dimension(object_name):
    fallback_size = 1.0
    if not GEMINI_API_KEY:
        print("\n[!] WARNING: No Gemini API Key found in .env file! Using 1.0m fallback.\n")
        return fallback_size

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"What is the average length or height in meters of '{object_name}'? Respond with STRICTLY a single number and absolutely no other text, symbols, or units. For example, if it is 1.85 meters, respond exactly with: 1.85"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        
        if "error" in res:
            print(f"\n[!] GEMINI API ERROR: {res['error'].get('message', 'Unknown Error')}\n")
            return fallback_size
            
        if "candidates" not in res:
            print(f"\n[!] GEMINI BLOCKED REQUEST OR EMPTY: {res}\n")
            return fallback_size

        text_response = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        print(f"\n[+] Gemini returned: '{text_response}' for object '{object_name}'\n")
        
        match = re.search(r"[-+]?\d*\.\d+|\d+", text_response)
        if match:
            return float(match.group())
        return fallback_size
        
    except Exception as e:
        print(f"\n[!] API Parsing Exception: {e}\n")
        return fallback_size

@app.route("/")
def home():
    """Serves the main Las Vegas Sphere landing page"""
    return render_template("index.html")

@app.route("/cosmic-stack")
def cosmic_stack():
    """Serves the Cosmic Stack distance component"""
    return render_template("cosmic_stack.html")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}
    p1 = str(data.get("origin", "")).strip().lower()
    p2 = str(data.get("destination", "")).strip().lower()
    obj_name = str(data.get("measurement_object", "")).strip().lower()

    if not p1 or not p2 or not obj_name:
        return jsonify({"success": False, "error": "Missing input fields."}), 400

    dimension_meters = get_object_dimension(obj_name)

    is_p1_planet = p1 in PLANETS_KM
    is_p2_planet = p2 in PLANETS_KM

    # Scenario A: Two Planets
    if is_p1_planet and is_p2_planet:
        mode = "planetary"
        if (p1 == "earth" and p2 == "moon") or (p1 == "moon" and p2 == "earth"):
            dist_km = 384400.0
        else:
            dist_km = abs(PLANETS_KM[p1] - PLANETS_KM[p2])
        origin_meta = {"name": p1.title(), "type": "planet"}
        dest_meta = {"name": p2.title(), "type": "planet"}

    # Scenario B: Two Earth Locations
    elif not is_p1_planet and not is_p2_planet:
        mode = "terrestrial"
        coords1 = get_coordinates(p1)
        coords2 = get_coordinates(p2)
        if not coords1 or not coords2:
            return jsonify({"success": False, "error": "Could not find one of the Earth locations."}), 400
        
        dist_km = haversine_distance_km(coords1["lat"], coords1["lon"], coords2["lat"], coords2["lon"])
        origin_meta = {"name": coords1["name"], "coords": coords1, "type": "city"}
        dest_meta = {"name": coords2["name"], "coords": coords2, "type": "city"}

    # Scenario C: Hybrid
    else:
        mode = "hybrid"
        planet_key = p1 if is_p1_planet else p2
        city_key = p2 if is_p1_planet else p1
        city_coords = get_coordinates(city_key)
        
        if not city_coords:
            return jsonify({"success": False, "error": "Could not find the Earth location."}), 400

        dist_km = 384400.0 if planet_key == "moon" else abs(PLANETS_KM["earth"] - PLANETS_KM[planet_key])
        
        if is_p1_planet:
            origin_meta = {"name": planet_key.title(), "type": "planet"}
            dest_meta = {"name": city_coords["name"], "coords": city_coords, "type": "city"}
        else:
            origin_meta = {"name": city_coords["name"], "coords": city_coords, "type": "city"}
            dest_meta = {"name": planet_key.title(), "type": "planet"}

    dist_meters = dist_km * 1000.0
    total_count = math.ceil(dist_meters / dimension_meters)

    return jsonify({
        "success": True,
        "mode": mode,
        "distance_km": round(dist_km, 2),
        "distance_meters": round(dist_meters, 2),
        "total_count": total_count,
        "object": {"name": obj_name.title(), "dimension_meters": dimension_meters},
        "origin": origin_meta,
        "destination": dest_meta
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)