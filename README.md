
# Project Name: THE ABSURD PROTOCOL 🎯

An interactive suite of digital curiosities.

## Basic Details
### Team Name: FlashBang


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
shows the height comparison page. Ther user entered Narendra Modi as celebrity, and their height, it shows the comparison.
<img width="1920" height="1080" alt="Taylor_swift_compare" src="https://github.com/user-attachments/assets/d3f97716-50c5-4459-9f41-0037b61a3ebc" />
Another example of the comparison. This time with Taylor Swift

<img width="1920" height="1080" alt="rabbit_hole_1" src="https://github.com/user-attachments/assets/8bed4db0-3d99-4f1c-a250-0e2d6e41bda3" />
<img width="1920" height="1080" alt="rabbit_hole_2" src="https://github.com/user-attachments/assets/af702d63-bb83-44a0-84fb-1d095f9f6e31" />
These screenshots show the randomly picked article shown on the rabbit_hole page. The idea is to actually read through the article and remember it.
<img width="1920" height="1080" alt="rabbit_hole_exit" src="https://github.com/user-attachments/assets/96e5aefd-34e3-4b59-bbb3-7ff336e1d28b" />
This is the exit messge shown after clicking through 3 buttons and reading through around 9 paragraphs. Tells the user to close the tab and go to home page.

<img width="1920" height="1080" alt="rabbit_hole_quiz_1" src="https://github.com/user-attachments/assets/62a32840-b650-4723-a723-11c88a5c5169" />
<img width="1920" height="1080" alt="rabbit_hole_quiz_2" src="https://github.com/user-attachments/assets/2bbb8232-20e3-4a81-9aca-170a0794c5fe" />

After the user gets back from rabbit_hole page, this is the rapid questions he/she will be asked to answer. There are 8 MCQ questions and 2 short descriptive questions based on the article showed earlier in the rabbit_hole page. Some questions are designed to ask from the paragraphs below the button of the next page.
There is 8 seconds timer for MCQ and 15 seconds timer for descriptive questions.

<img width="1920" height="1080" alt="attention_span_roast" src="https://github.com/user-attachments/assets/6e9b25ae-7063-46ce-843d-99d31ef41ff4" />
After the user answers the questions, based on the number of correct answers, the user gets roasted for the attention span and short term memory he/she has.

<img width="1920" height="1080" alt="terminal locked" src="https://github.com/user-attachments/assets/987f8931-06f3-49ae-acb5-b752133e6916" />
While the rabbit_hole page is running the home page is locked.
<img width="1920" height="1080" alt="rage_quit" src="https://github.com/user-attachments/assets/dab45d2a-01cf-42e7-a95a-ff7a77b7d985" />
If the user directly closes the rabit_hole page, they get criticized.


# Diagrams
```text
+----------------------------------------------------------------------------------------------------+
|                                     CLIENT LAYER (Browser)                                         |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ index.html (Digital Hub) ]                                                                      |
|     |-- Three.js Interactive LED Sphere (Raycasting, Dynamic Emoji Face Shader, Gaze Tracking)     |
|     |-- Decoupled 3D Orbit Carousel Navigation Buttons                                              |
|     |-- BroadcastChannel Cross-Tab Synchronizer (Lockdown Protocol & Anti-Cheat Tab Tracking)      |
|     \-- Rapid-Fire Quiz & Roast Modal Interface                                                  |
|                                                                                                    |
|       |                                 |                                 |                        |
|       v                                 v                                 v                        |
|  [ cosmic_stack.html ]           [ rabbit_hole.html ]             [ height_compare.html ]          |
|  - Distance & Unit Inputs        - 3-Chamber Narrative Reader     - Celebrity & User Height Inputs |
|  - Real-Time 3D Stack View       - Secret Escape Interaction      - Proportional Mannequin & Image |
|                                                                                                    |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                                            HTTP / JSON   |   REST APIs
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                    APPLICATION LAYER (Flask Backend)                               |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ app.py Routing & Processing Engine ]                                                            |
|     |                                                                                              |
|     +---> /api/calculate (Cosmic Stack)                                                            |
|     |      |-- Resolves Earth-to-Earth coordinates via Haversine Formula                           |
|     |      |-- Computes Interplanetary distances using Astronomical Ephemeris Baselines            |
|     |      \-- Normalizes target object real-world dimensions into cumulative units                |
|     |                                                                                              |
|     +---> /api/rabbit/generate & /api/rabbit/roast (Rabbit Hole)                                   |
|     |      |-- Assembles 3-Chamber deep-dive narrative structures with MCQ & descriptive puzzles   |
|     |      |-- Evaluates user retention scores, timeout triggers, and tab-peeking counts           |
|     |      \-- Generates context-aware comedic roasting responses                                  |
|     |                                                                                              |
|     \---> /api/height-compare (Height Scale)                                                       |
|            |-- Extracts verified celebrity heights in centimeters                                  |
|            \-- Calculates relative scale factors & differential laser offsets                      |
|                                                                                                    |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                                          Outbound HTTPS | Requests
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                      EXTERNAL SERVICES & APIS                                      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  +---------------------------+  +----------------------------+  +-------------------------------+  |
|  | Google Gemini API         |  | Wikipedia REST API         |  | OpenStreetMap (Nominatim API) |  |
|  |---------------------------|  |----------------------------|  |-------------------------------|  |
|  | - Dimension extraction    |  | - Official page thumbnail  |  | - Geographic forward lookup   |  |
|  | - Historical content JSON |  |   image resolution         |  | - Latitude / longitude        |  |
|  | - Adaptive roasts         |  | - Entity disambiguation    |  |   spatial coordinates         |  |
|  +---------------------------+  +----------------------------+  +-------------------------------+  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
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



