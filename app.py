import os
import math
import requests
import json
import re
from functools import lru_cache
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# WARNING: Do not change this to 3.5, 3.6, or 3.8. Those models do not exist 
# and will cause a total API failure. 1.5-flash is the current stable version.
GEMINI_MODEL = "gemini-3.5-flash-lite" 

app = Flask(__name__)

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

@lru_cache(maxsize=256)
def get_coordinates(location_name):
    """Fetches OSM coordinates ONLY if we are certain it is on Earth."""
    if location_name.lower() == "earth":
        return None
    url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(location_name)}&format=json&limit=1"
    # Improved User-Agent to prevent aggressive OSM rate-limiting
    headers = {"User-Agent": "AbsurdProtocol_CosmicStack/1.1 (Caching Engine)"}
    try:
        response = requests.get(url, headers=headers, timeout=5).json()
        if response:
            return {"lat": float(response[0]["lat"]), "lon": float(response[0]["lon"]), "name": response[0]["name"]}
    except Exception as e:
        print(f"[!] OSM Geocoding Error: {e}")
    return None

def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Calculates exact Earth distance to bypass AI for local towns."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def clean_json_string(raw_string):
    """Strips Markdown wrappers and control characters that crash the JSON parser."""
    cleaned = re.sub(r'^```json', '', raw_string, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = re.sub(r'```$', '', cleaned, flags=re.MULTILINE)
    cleaned = cleaned.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    return cleaned.strip()

def fetch_gemini_json(prompt):
    """Helper to fetch strictly formatted JSON from Gemini."""
    if not GEMINI_API_KEY:
        print("[!] GEMINI_API_KEY is missing.")
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=35)
        
        # Catch API rejections (like Invalid API Key or Fake Model)
        if response.status_code != 200:
            print(f"[!] Gemini API HTTP Error {response.status_code}: {response.text}")
            return None
            
        res = response.json()
        if "candidates" in res and res["candidates"]:
            text_response = res["candidates"][0]["content"]["parts"][0]["text"].strip()
            return json.loads(clean_json_string(text_response))
    except Exception as e:
        print(f"[!] Gemini JSON Fetch Crash: {e}")
    return None

# =========================================================================
# ROUTES: FRONTEND
# =========================================================================

@app.route("/")
def home(): return render_template("index.html")

@app.route("/cosmic-stack")
def cosmic_stack(): return render_template("cosmic_stack.html")

@app.route("/rabbit-hole")
def rabbit_hole(): return render_template("rabbit_hole.html")

@app.route("/height-compare")
def height_compare(): return render_template("height_compare.html")

@app.route("/maker")
def maker_portfolio(): return render_template("maker.html")

# =========================================================================
# ROUTE: COSMIC STACK
# =========================================================================

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}
    p1 = str(data.get("origin", "")).strip()
    p2 = str(data.get("destination", "")).strip()
    obj_name = str(data.get("measurement_object", "")).strip()

    if not p1 or not p2 or not obj_name:
        return jsonify({"success": False, "error": "Missing input fields."}), 400

    is_same = p1.lower() == p2.lower()

    # AI analyzes FIRST to prevent OSM from turning "Moon" into a terrestrial village
    prompt = f"""
    Analyze: Origin: "{p1}", Destination: "{p2}", Object: "{obj_name}"
    1. Is Origin valid? (true/false)
    2. Is Origin located on Earth (like a city or country) or in space (like a planet, star, galaxy)? (Answer strictly 'earth' or 'space')
    3. Is Destination valid? (true/false)
    4. Is Destination located on Earth or in space? (Answer strictly 'earth' or 'space')
    5. Is Object valid? (true/false)
    6. Object's maximum major dimension in meters? (number)
    7. Physical distance between them in kilometers? (number. convert lightyears to km).
    Schema: {{"origin_valid": true, "origin_type": "space", "destination_valid": true, "destination_type": "earth", "object_valid": true, "distance_km": 384400.0, "object_dimension_meters": 35.5}}
    """
    
    ai_data = fetch_gemini_json(prompt)
    if not ai_data:
        return jsonify({"success": False, "error": "API communication failed. Check server logs."}), 500

    errors = []
    if not ai_data.get("origin_valid"): errors.append("starting point")
    if not ai_data.get("destination_valid"): errors.append("destination point")
    if not ai_data.get("object_valid"): errors.append("object name")

    if errors:
        msg = " and ".join(errors)
        return jsonify({"success": False, "error": f"Please enter a valid {msg}."}), 400

    # ONLY check OSM if AI confirmed they are Earth locations
    is_p1_earth = ai_data.get("origin_type", "earth") == "earth"
    is_p2_earth = ai_data.get("destination_type", "earth") == "earth"
    
    coords1 = get_coordinates(p1) if is_p1_earth else None
    coords2 = get_coordinates(p2) if is_p2_earth else None
    
    is_terrestrial = bool(coords1 and coords2)

    # Use Haversine if both are local earth coords, otherwise use AI distance
    if is_same:
        dist_km = 0.0
    elif is_terrestrial:
        dist_km = haversine_distance_km(coords1["lat"], coords1["lon"], coords2["lat"], coords2["lon"])
    else:
        dist_km = float(ai_data.get("distance_km", 0))

    dimension_meters = float(ai_data.get("object_dimension_meters", 1.0))
    
    mode = "interplanetary"
    origin_meta = {"name": p1.title(), "type": "planet"}
    dest_meta = {"name": p2.title(), "type": "planet"}

    if is_terrestrial:
        mode = "terrestrial"
        origin_meta = {"name": coords1["name"], "coords": coords1, "type": "city"}
        dest_meta = {"name": coords2["name"], "coords": coords2, "type": "city"}
    elif coords1:
        mode = "hybrid"
        origin_meta = {"name": coords1["name"], "coords": coords1, "type": "city"}
    elif coords2:
        mode = "hybrid"
        dest_meta = {"name": coords2["name"], "coords": coords2, "type": "city"}

    dist_meters = dist_km * 1000.0
    total_count = math.ceil(dist_meters / dimension_meters) if dimension_meters > 0 else 0

    return jsonify({
        "success": True, "mode": mode, "distance_km": round(dist_km, 2), "distance_meters": round(dist_meters, 2),
        "total_count": total_count, "object": {"name": obj_name.title(), "dimension_meters": dimension_meters},
        "origin": origin_meta, "destination": dest_meta
    })

# =========================================================================
# ROUTE: RABBIT HOLE 
# =========================================================================

@app.route("/api/rabbit/generate", methods=["GET"])
def rabbit_generate():
    try:
        wiki_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&generator=random&grnnamespace=0&prop=info|extracts&exintro=false&explaintext=true"
        wiki_res = requests.get(wiki_url, headers={"User-Agent": "AbsurdProtocolApp/1.0"}, timeout=45).json()
        pages = wiki_res.get("query", {}).get("pages", {})
        page = list(pages.values())[0]
        wiki_title = page.get("title", "Historical Event")
        # Increased Wikipedia extract grab to 8000 characters
        wiki_extract = page.get("extract", "")[:8000] 

        prompt = f"""
        Here is text from Wikipedia about '{wiki_title}':
        {wiki_extract}

        Format this into a 3-chamber narrative. 
        
        CRITICAL INSTRUCTIONS:
        1. Each 'upper_content' and 'lower_content' MUST be long-form, highly detailed paragraphs of at least 150 words each. Do NOT summarize too heavily; provide rich, deep context so it fills the screen.
        2. You MUST ONLY ask questions in the 'mcqs' and 'descriptive' arrays where the EXACT answer is explicitly written in the chamber text you just generated. If the user cannot find the answer by reading your generated text, you fail.

        Schema:
        {{
          "topic": "{wiki_title}",
          "pages": [
            {{ "page": 1, "title": "Chamber 1", "upper_content": "Long detailed paragraph...", "lower_content": "Long detailed paragraph..." }},
            {{ "page": 2, "title": "Chamber 2", "upper_content": "Long detailed paragraph...", "lower_content": "Long detailed paragraph..." }},
            {{ "page": 3, "title": "Chamber 3", "upper_content": "Long detailed paragraph...", "lower_content": "Long detailed paragraph..." }}
          ],
          "mcqs": [
            {{"q": "Question?", "options": ["Correct", "Wrong1", "Wrong2", "Wrong3"], "answer": "Correct"}}
          ],
          "descriptive": [
            {{"q": "Question?", "keywords": ["keyword1", "keyword2"]}}
          ]
        }}
        CRITICAL: Exactly 8 MCQs and 2 descriptive. Escape all double quotes inside your strings using \\". Do not use markdown.
        """
        
        for attempt in range(2):
            ai_data = fetch_gemini_json(prompt)
            if ai_data: return jsonify({"success": True, "data": ai_data})
            
        raise Exception("AI returned empty or invalid JSON twice.")
            
    except Exception as e:
        print(f"[!] Rabbit Gen Exception: {e}")
        return jsonify({"success": False, "error": "Generation failed."})

@app.route("/api/rabbit/roast", methods=["POST"])
def rabbit_roast():
    body = request.get_json() or {}
    score = body.get("score", 0)
    total = body.get("total", 10)
    peeks = body.get("peeks", 0)
    topic = body.get("topic", "the subject")
    pct = int((score / total) * 100) if total > 0 else 0

    if body.get("rage_quit", False):
        return jsonify({"success": True, "roast": "Score: 0%. Rage quitting already? Your attention span lasted approximately 8 seconds before requiring emergency stimulation.", "pct": 0})

    prompt = f"""
    Write a biting, ruthless 4-to-5 sentence comedic roast to a web user who scored exactly {pct}% ({score}/{total}) on a reading memory quiz after reading about '{topic}'.
    Always start the roast directly with 'Score: {pct}%.' followed by the roast text. 
    User cheated by peeking at other tabs {peeks} times. You MUST mock them heavily for their peek attempts if peeks > 0.
    Output ONLY the string text. Do not format with markdown.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15).json()
        if "candidates" in res and res["candidates"]:
            roast_text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
            if not roast_text.startswith(f"Score: {pct}%"):
                roast_text = f"Score: {pct}%. " + roast_text
            return jsonify({"success": True, "roast": roast_text, "pct": pct})
    except Exception as e:
        print(f"Roast crash: {e}")
        
    return jsonify({"success": True, "roast": f"Score: {pct}%. The AI crashed trying to comprehend your score.", "pct": pct})

# =========================================================================
# ROUTE: HEIGHT COMPARE
# =========================================================================

@app.route("/api/height-compare", methods=["POST"])
def api_height_compare():
    data = request.get_json() or {}
    celeb_name = str(data.get("celebrity", "")).strip()
    user_height_str = str(data.get("user_height", "")).strip()

    try:
        user_height_cm = float(user_height_str)
        if user_height_cm <= 0: raise ValueError
    except ValueError:
        return jsonify({"success": False, "error": "Invalid height."}), 400

    prompt = f"""
    Analyze: "{celeb_name}"
    1. Is this a real, widely known famous person or historical figure? (true/false)
    2. If true, what is their height in centimeters? (number only). If false, return 0.
    Schema: {{"is_valid": true, "height_cm": 175.0}}
    """
    
    ai_data = fetch_gemini_json(prompt)
    if not ai_data:
        return jsonify({"success": False, "error": "API communication failed. Check server logs."}), 500
    if not ai_data.get("is_valid"):
        return jsonify({"success": False, "error": "Please enter the name of an actual celebrity, check the input."}), 400

    celeb_height_cm = float(ai_data.get("height_cm", 175.0))

    image_url = None
    wiki_title = celeb_name.title()
    try:
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1&generator=search&gsrsearch={requests.utils.quote(celeb_name)}&gsrlimit=1&prop=pageimages&pithumbsize=600&pilicense=any"
        wiki_res = requests.get(wiki_url, headers={"User-Agent": "HeightApp/1.0"}, timeout=5).json()
        pages = wiki_res.get("query", {}).get("pages", {})
        for _, pdata in pages.items():
            wiki_title = pdata.get("title", wiki_title)
            if "thumbnail" in pdata: image_url = pdata["thumbnail"].get("source")
            break
    except Exception:
        pass

    diff = round(user_height_cm - celeb_height_cm, 1)

    return jsonify({
        "success": True, "celebrity": {"name": wiki_title, "height_cm": celeb_height_cm, "image_url": image_url},
        "user": {"height_cm": user_height_cm}, "diff_cm": diff,
        "comparison_text": f"You are {abs(diff)} cm {'taller' if diff > 0 else 'shorter'} than {wiki_title}." if diff != 0 else f"You are exactly the same height as {wiki_title}!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)