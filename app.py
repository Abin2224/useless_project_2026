import os
import math
import requests
import re
import json
import random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

# =========================================================================
# COSMIC STACK (PRESERVED)
# =========================================================================
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
        return fallback_size

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"What is the average length or height in meters of '{object_name}'? Respond with STRICTLY a single number and absolutely no other text, symbols, or units. For example, if it is 1.85 meters, respond exactly with: 1.85"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        if "candidates" in res and res["candidates"]:
            text_response = res["candidates"][0]["content"]["parts"][0]["text"].strip()
            match = re.search(r"[-+]?\d*\.\d+|\d+", text_response)
            if match:
                return float(match.group())
        return fallback_size
    except Exception as e:
        return fallback_size

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cosmic-stack")
def cosmic_stack():
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

    if is_p1_planet and is_p2_planet:
        mode = "planetary"
        if (p1 == "earth" and p2 == "moon") or (p1 == "moon" and p2 == "earth"):
            dist_km = 384400.0
        else:
            dist_km = abs(PLANETS_KM[p1] - PLANETS_KM[p2])
        origin_meta = {"name": p1.title(), "type": "planet"}
        dest_meta = {"name": p2.title(), "type": "planet"}

    elif not is_p1_planet and not is_p2_planet:
        mode = "terrestrial"
        coords1 = get_coordinates(p1)
        coords2 = get_coordinates(p2)
        if not coords1 or not coords2:
            return jsonify({"success": False, "error": "Could not find one of the Earth locations."}), 400
        
        dist_km = haversine_distance_km(coords1["lat"], coords1["lon"], coords2["lat"], coords2["lon"])
        origin_meta = {"name": coords1["name"], "coords": coords1, "type": "city"}
        dest_meta = {"name": coords2["name"], "coords": coords2, "type": "city"}

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
    total_count = math.ceil(dist_meters / dimension_meters) if dimension_meters > 0 else 0

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

# =========================================================================
# RABBIT HOLE (HIGH-DENSITY MULTI-PARAGRAPH CONTENT)
# =========================================================================
FALLBACK_TOPICS = [
    {
        "topic": "The Great Emu War of 1932",
        "pages": [
            {
                "page": 1,
                "title": "Chamber 1: The Outnumbered Frontier",
                "upper_content": "Following the devastation of World War I, thousands of Australian veterans were given marginal grazing land in Western Australia to cultivate wheat crops. As the Great Depression set in by October 1932, the farmers faced an unprecedented ecological invasion: roughly 20,000 adult emus migrated from central inland regions toward coastal farmlands searching for water supplies following their annual breeding cycle. The flightless birds tore through protective wire fencing and decimated square miles of harvestable wheat.\n\nWith agricultural ruin imminent, the veteran farmers formed a deputation and met directly with the Minister of Defence, Sir George Pearce. Accustomed to modern military hardware, the settlers lobbied for artillery support to eradicate the massive herds. Pearce approved the deployment under the strict condition that machine guns and ammunition be handled exclusively by military personnel, while the local farmers financed the rations and transport.",
                "lower_content": "Command of the tactical detachment was entrusted to Major G.P.W. Meredith of the Seventh Heavy Battery of the Royal Australian Artillery. Meredith arrived in Campion on November 2, 1932, bringing along Sergeant S. McMurray, Gunner J. O'Halloran, two Lewis automatic machine guns, and 10,000 rounds of .303 caliber ammunition.\n\nInitial intelligence suggested the birds could be corralled into tight ambushes. However, the soldiers immediately encountered unpredictable guerrilla maneuvers from the flock. The massive birds split into agile splinter units of a dozen birds each, outrunning the gunners across loose red sand and making concentrated bursts nearly impossible."
            },
            {
                "page": 2,
                "title": "Chamber 2: Mechanical Failures and Desert Defeat",
                "upper_content": "On November 4, Major Meredith established an ambush position near a crucial water dam where over 1,000 emus were seen congregating. The gunners withheld their fire until the flock came within 100 meters of the muzzle line. As Meredith gave the order to open fire, the Lewis gun managed to discharge only twelve rounds before a heavy particulate jam locked the bolt assembly.\n\nThe startled flock scattered into the shrubbery in less than fifteen seconds, leaving only a dozen dead birds behind. Dust and airborne grit from the arid environment continuously contaminated the magazine cylinders, causing catastrophic weapon failures. Facing mounting embarrassment in federal parliament, Meredith ordered an experimental tactic: mounting one of the heavy Lewis machine guns onto the flatbed of a modified Ford truck to pursue the birds across the open plain.",
                "lower_content": "The motorized experiment failed disastrously. The Ford truck was unable to negotiate the rough terrain, logs, and hidden rabbit burrows at high speeds. The passenger gunner was jostled so severely that not a single aimed shot could be fired, and the chase ended abruptly when an evasive emu became entangled in the truck's steering link, sending the vehicle careening off-course.\n\nBy November 8, parliament recalled the military. Official reports logged that 2,500 rounds of ammunition had been expended with scarcely 200 birds dispatched. Major Meredith remarked with begrudging awe that each emu possessed the invulnerability of a battle tank, capable of sustaining multiple bullet strikes while running away at 50 kilometers per hour."
            },
            {
                "page": 3,
                "title": "Chamber 3: The Ceasefire and the Bounty Solution",
                "upper_content": "A second offensive was authorized a week later on November 13 under intense political pressure from the Western Australian Premier. Meredith's team resumed fire through December 2, claiming approximately 986 kills from another 9,860 rounds expended—an inefficient ratio of ten rounds of heavy ammunition for every confirmed casualty.\n\nOpposition politician A.E. Green ridiculed the campaign on the floor of the House of Representatives, asking sarcastically whether medals should be struck for the surviving emus who had decisively routed the Australian military. The army was ordered to execute an unceremonious total withdrawal.",
                "lower_content": "Instead of military expeditions, the Australian government implemented a direct civilian bounty system in 1934. Local farmers armed with light hunting rifles accomplished what heavy artillery could not: during a single six-month window in 1934, more than 57,034 individual bounties were successfully claimed.\n\nThe military never engaged the avian population again, cementing the operation as one of the most bizarre and one-sided logistical defeats in modern Commonwealth history."
            }
        ],
        "mcqs": [
            {"q": "Roughly how many emus invaded Western Australian wheat farms in October 1932?", "options": ["20,000", "5,000", "50,000", "2,000"], "answer": "20,000"},
            {"q": "What military unit was assigned to the operation under Major G.P.W. Meredith?", "options": ["Royal Australian Artillery", "Imperial Camel Corps", "Desert Scouts", "7th Light Horse"], "answer": "Royal Australian Artillery"},
            {"q": "What specific model of automatic machine gun was issued to the soldiers?", "options": ["Lewis gun", "Maxim gun", "Vickers gun", "Bren gun"], "answer": "Lewis gun"},
            {"q": "On what date did Major Meredith arrive in Campion with his detachment?", "options": ["November 2, 1932", "October 14, 1932", "December 1, 1932", "August 12, 1931"], "answer": "November 2, 1932"},
            {"q": "How many rounds did the machine gun fire at the dam ambush before jamming?", "options": ["Only 12 rounds", "Over 500 rounds", "Zero rounds", "Exactly 250 rounds"], "answer": "Only 12 rounds"},
            {"q": "What mechanical disaster stopped the truck pursuit across the outback plain?", "options": ["An emu tangled in the steering link", "The engine overheated", "A tire burst on a rock", "The fuel tank ruptured"], "answer": "An emu tangled in the steering link"},
            {"q": "Roughly how many rounds had been fired before the temporary recall on November 8?", "options": ["2,500 rounds", "10,000 rounds", "500 rounds", "50,000 rounds"], "answer": "2,500 rounds"},
            {"q": "How many bounties were successfully claimed by local settlers in six months of 1934?", "options": ["57,034", "12,400", "100,000", "5,200"], "answer": "57,034"}
        ],
        "descriptive": [
            {"q": "What was the surname of the Defence Minister who approved the military deployment?", "keywords": ["pearce", "george pearce"]},
            {"q": "What speed (in km/h) could the emus reach when sprinting across the rough terrain?", "keywords": ["50", "50 km/h", "50km/h", "50 kph"]}
        ]
    }
]

@app.route("/rabbit-hole")
def rabbit_hole():
    return render_template("rabbit_hole.html")

@app.route("/api/rabbit/generate", methods=["GET"])
def rabbit_generate():
    selected_fallback = random.choice(FALLBACK_TOPICS)

    if not GEMINI_API_KEY:
        return jsonify({"success": True, "data": selected_fallback})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = """
Generate a high-density 3-chamber deep-dive historical narrative in JSON.
Schema:
{
  "topic": "Topic Title",
  "pages": [
    {
      "page": 1,
      "title": "Chamber 1: Title",
      "upper_content": "Two substantial paragraphs totaling 150 words.",
      "lower_content": "Two substantial paragraphs totaling 150 words with specific names and numbers."
    },
    {
      "page": 2,
      "title": "Chamber 2: Title",
      "upper_content": "Two substantial paragraphs totaling 150 words.",
      "lower_content": "Two substantial paragraphs totaling 150 words with specific names and numbers."
    },
    {
      "page": 3,
      "title": "Chamber 3: Title",
      "upper_content": "Two substantial paragraphs totaling 150 words.",
      "lower_content": "Two substantial paragraphs totaling 150 words with specific names and numbers."
    }
  ],
  "mcqs": [
    {"q": "Question", "options": ["Correct", "A", "B", "C"], "answer": "Correct"}
  ],
  "descriptive": [
    {"q": "Question", "keywords": ["answer1", "answer2"]}
  ]
}
Requirements: Exactly 8 items in 'mcqs', exactly 2 in 'descriptive'. Place multiple answers in lower_content. Strictly JSON.
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=6).json()
        if "candidates" not in res or not res["candidates"]:
            return jsonify({"success": True, "data": selected_fallback})

        text_content = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        return jsonify({"success": True, "data": json.loads(text_content)})
    except Exception as e:
        print(f"[!] Rabbit Gen Exception: {e}. Serving fallback.")
        return jsonify({"success": True, "data": selected_fallback})

@app.route("/api/rabbit/roast", methods=["POST"])
def rabbit_roast():
    body = request.get_json() or {}
    score = body.get("score", 0)
    total = body.get("total", 10)
    peeks = body.get("peeks", 0)
    rage_quit = body.get("rage_quit", False)
    topic = body.get("topic", "the subject")

    pct = int((score / total) * 100) if total > 0 else 0

    if rage_quit:
        rage_roasts = [
            "We detected you closing or ditching the tab. Your dopamine receptors are completely fried. Go outside, leave your phone behind, and touch a tree.",
            "Rage quitting already? Your attention span lasted approximately 8 seconds before requiring emergency stimulation. Sit in timeout.",
            "You closed the window because a few paragraphs looked like a doctoral dissertation to your fried brain. Ten seconds in the penalty box for you."
        ]
        return jsonify({"success": True, "roast": random.choice(rage_roasts), "tier": "rage_quit", "pct": 0})

    tier_roasts = {
        0: f"Score: {pct}%. Remarkable. You stared at {topic} with the cognitive retention of a goldfish swimming backward. Even guessing randomly yields better results.",
        10: f"Score: {pct}%. You managed to get one question right, presumably by a blind muscle spasm on your trackpad. A true triumph of sensory decay.",
        20: f"Score: {pct}%. Your brain treated the paragraphs like Terms of Service agreements: scrolled past with complete, willful ignorance.",
        30: f"Score: {pct}%. You clearly saw the middle button, panicked at the sight of letters, clicked immediately, and ignored the rest of the universe.",
        40: f"Score: {pct}%. Skimming champion of the century. You caught a few stray nouns while your mind drifted toward what to eat for dinner.",
        50: f"Score: {pct}%. You made it halfway before your brain demanded a split-screen Subway Surfers gameplay video with soap cutting audio just to survive.",
        60: f"Score: {pct}%. Not completely hopeless, but your concentration snapped the second any paragraph exceeded three sentences.",
        70: f"Score: {pct}%. A respectable showing. You actually read most of it, but missed the fine print because your finger was itching to click out.",
        80: f"Score: {pct}%. Impressive focus. You almost outsmarted the trap, missing just a tiny detail tucked beneath the fold.",
        90: f"Score: {pct}%. Nearly flawless. You resisted the urge to skim and actually absorbed the obscure trivia like a scholar.",
        100: f"Score: {pct}%. Congratulations. You have the patience of a Shaolin monk, nerves of cold titanium, and unquestionably way too much free time. Here is your exit."
    }

    # Find closest bucket key
    closest_key = min(tier_roasts.keys(), key=lambda k: abs(k - pct))
    fallback = tier_roasts[closest_key]

    if not GEMINI_API_KEY:
        return jsonify({"success": True, "roast": fallback, "pct": pct})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
Write a biting, funny 2-sentence comedic roast to a web user who scored exactly {pct}% ({score}/{total}) on an attention span memory quiz after reading about '{topic}'.
Always start the roast directly with 'Score: {pct}%.' followed by the roast text.
User peeks back to home tab: {peeks}.
Keep it strictly under 3 sentences. Output ONLY the roast text.
"""
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=4).json()
        roast_text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not roast_text.startswith(f"Score: {pct}%"):
            roast_text = f"Score: {pct}%. " + roast_text
        return jsonify({"success": True, "roast": roast_text, "pct": pct})
    except Exception:
        return jsonify({"success": True, "roast": fallback, "pct": pct})

if __name__ == "__main__":
    app.run(debug=True, port=5000)