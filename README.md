<img width="1535" height="777" alt="Height_compare" src="https://github.com/user-attachments/assets/8950ac19-d46f-483d-b922-0631b699b3ac" /><img width="1536" height="777" alt="Home_page" src="https://github.com/user-attachments/assets/4d245978-b3ad-46d2-a6d5-29d3861f862e" /><img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# [Project Name] 🎯
THE ABSURD PROTOCOL
An interactive suite of digital curiosities.

## Basic Details
### Team Name: [FlashBang]


### Team Members
- Team Lead: Abin dev E K - RIT

### Project Description
This project includes a cute las Vegas sphere replica, height comparison with celebrities, web rabbit hole to test the user's patience, and finally an option to display how many different things like coins, bus might be needed to reach from a point to another if they're stacked on top of each other.

### The Problem (that doesn't exist)
Every human being needs to find the number of coins or school buses it takes to reach from one point to another if the coins or school buses or anythhing are stacked on top of each other. Get an idea of the user's attention span. The height comparison with a celebrity.

### The Solution (that nobody asked for)
Find the distance between the end points, divide that with the average length of the measurement object, we get the number.
Get roasted about the attention span based on the score the user scores

## Technical Details
### Technologies/Components Used
For Software:
- Languages used : Python, JavaScript, HTML5
- Frameworks used : Flask (included entirely for unnecessary architectural weight)
- Libraries used : Three.js,Requests
- Tools used : APIs: Google Gemini API, Development & Environment: VS Code, Git, GitHub, Python Virtual Environment (venv), Browser Developer Tools

For Hardware:
- [List main components]
- [List specifications]
- [List tools required]

### Implementation
 Backend Framework & Routes: Built with Flask, handling core API endpoints such as /api/height-compare, /    api/calculate, /api/rabbit/generate, and /api/rabbit/roast.

 Client-Server Communication: Utilizes asynchronous JavaScript fetch() calls transmitting JSON payloads between the frontend scripts (height_compare.js, main.js) and backend routes.

 Data Sources: Integrates the Wikipedia API for celebrity height and image retrieval, alongside OpenStreetMap Nominatim for geocoding calculations.

 Notable Logic: Employs dynamic pixel-to-centimeter scaling (pxPerCm), baseline offset mapping, and synchronized viewport rendering to keep mannequin and celebrity visuals perfectly aligned with the background grid.

# Installation
Clone the project repository using git clone https://github.com/Abin2224/useless_project_2026.
Verify that Python 3.8 or higher is installed on your system.
Install project dependencies by running pip install -r requirements.txt.
Set up the required environment configuration by creating a .env file in the root directory.

# Run
Configure your API key in the .env file using the exact literal variable name read by the application: GEMINI_API_KEY=your_api_key (retrieved in code via load_dotenv() and os.environ.get("GEMINI_API_KEY")).

Start the application server by executing python app.py.

Open your browser and navigate to Flask's default localhost URL and port: [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Project Documentation
For Software:

# Screenshots (Add at least 3)
!<img width="1536" height="777" alt="Home_page" src="https://github.com/user-attachments/assets/2e93d85d-8f1c-4574-ad5f-50dc81c9d76a" />

This is the homepage or the landing page of the project

!<img width="1521" height="582" alt="cosmic_stack_2" src="https://github.com/user-attachments/assets/8c01ea81-a922-48ba-94df-e2d443815a2a" />
<img width="1523" height="743" alt="cosmic stack_1" src="https://github.com/user-attachments/assets/b5a850cf-1fa6-4cd0-9084-2ded6887c443" />
These images show the working of cosmic stack. How many objects does it take to reach from a point to another point.
The point can either be a planet or a location on earth

<img width="1536" height="775" alt="sphere_face_1" src="https://github.com/user-attachments/assets/167c9856-c46c-4d46-b444-08f5a5c5cf97" />
Shows the cute face of the sphere

<img width="1535" height="777" alt="Height_compare" src="https://github.com/user-attachments/assets/fd2cb731-6fe5-48a5-aec1-fc42f1a478b2" />
shows the height comparison page. Ther user entered Narendra Modi as celebrity, and their height, it shows the comparison

# Diagrams
graph TD
    subgraph Client["CLIENT LAYER (Browser)"]
        Hub["index.html (Digital Hub)"]
        Hub --> HubFeatures["-- Three.js Interactive LED Sphere (Raycasting, Dynamic Emoji Face Shader, Gaze Tracking)<br>-- Decoupled 3D Orbit Carousel Navigation Buttons<br>-- BroadcastChannel Cross-Tab Synchronizer (Lockdown Protocol & Anti-Cheat Tab Tracking)<br>-- Rapid-Fire Quiz & Roast Modal Interface"]
        
        Hub --> Cosmic["cosmic_stack.html<br>- Distance & Unit Inputs<br>- Real-Time 3D Stack View"]
        Hub --> Rabbit["rabbit_hole.html<br>- 3-Chamber Narrative Reader<br>- Secret Escape Interaction"]
        Hub --> Height["height_compare.html<br>- Celebrity & User Height Inputs<br>- Proportional Mannequin & Image"]
    end

    subgraph Backend["APPLICATION LAYER (Flask Backend)"]
        Engine["app.py Routing & Processing Engine"]
        
        Engine --> Calc["/api/calculate (Cosmic Stack)<br>-- Resolves Earth-to-Earth coordinates via Haversine Formula<br>-- Computes Interplanetary distances using Astronomical Ephemeris Baselines<br>-- Normalizes target object real-world dimensions into cumulative units"]
        Engine --> RabbitApi["/api/rabbit/generate & /api/rabbit/roast (Rabbit Hole)<br>-- Assembles 3-Chamber deep-dive narrative structures with MCQ & descriptive puzzles<br>-- Evaluates user retention scores, timeout triggers, and tab-peeking counts<br>-- Generates context-aware comedic roasting responses"]
        Engine --> HeightApi["/api/height-compare (Height Scale)<br>-- Extracts verified celebrity heights in centimeters<br>-- Calculates relative scale factors & differential laser offsets"]
    end

    subgraph External["EXTERNAL SERVICES & APIS"]
        Gemini["Google Gemini API<br>- Dimension extraction<br>- Historical content JSON<br>- Adaptive roasts"]
        Wiki["Wikipedia REST API<br>- Official page thumbnail<br> image resolution<br>- Entity disambiguation"]
        OSM["OpenStreetMap (Nominatim API)<br>- Geographic forward lookup<br>- Latitude / longitude<br> spatial coordinates"]
    end

    Client -- "HTTP / JSON & REST APIs" --> Backend
    Backend -- "Outbound HTTPS Requests" --> External
The workflow explains itself...

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
https://drive.google.com/drive/folders/1lVFibwE4uU582yV62L8ZP-TPCtAkZHvD
It demonstrates all of the features of the project

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
ABIN DEV E K -> ALL


---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



