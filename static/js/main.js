const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x020408);

const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.set(0, 5, 28);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

const ambLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
dirLight.position.set(15, 25, 20);
scene.add(dirLight);

const activeStageGroup = new THREE.Group();
scene.add(activeStageGroup);

let currentStackMeshes = [];
let fillProgress = 0;

function latLonToVector3(lat, lon, radius) {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (lon + 180) * (Math.PI / 180);
  return new THREE.Vector3(
    -(radius * Math.sin(phi) * Math.cos(theta)),
    radius * Math.cos(phi),
    radius * Math.sin(phi) * Math.sin(theta)
  );
}

const textureLoader = new THREE.TextureLoader();
const earthAlbedoMap = textureLoader.load('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg');

function createPinMesh() {
  const pinGroup = new THREE.Group();
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffcc00 }));
  head.position.y = 1.0;
  pinGroup.add(head);
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.0, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
  stem.position.y = 0.5;
  pinGroup.add(stem);
  return pinGroup;
}

// Procedural Planet Hash Generator
function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
  return hash;
}

function generateColor(hash) {
  const h = Math.abs(hash) % 360;
  return `hsl(${h}, 50%, 50%)`;
}

// Fixed Planet Color Mapping Dictionary
const PLANET_COLORS = {
  sun: '#FFF200',
  'mercury': '#888888',
  'venus': '#E3BB7B',
  'mars': '#C1440E',
  'jupiter': '#D8CA9D',
  'saturn': '#E2BF7D',
  'uranus': '#4B70DD',
  'neptune': '#274687',
  'pluto': '#C2B280'
};

function createPlanetTexture(name) {
  const key = name.toLowerCase();
  
  const canvas = document.createElement('canvas');
  canvas.width = 512; canvas.height = 256;
  const ctx = canvas.getContext('2d');
  
  if (key === 'moon') {
    // Moon: Highlands (#A1A1A1) and Maria (#4A4A4A)
    ctx.fillStyle = '#A1A1A1';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#4A4A4A';
    for (let i = 0; i < 35; i++) {
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      ctx.beginPath(); 
      ctx.arc(x, y, 15 + Math.random() * 35, 0, Math.PI * 2); 
      ctx.fill();
    }
  } else if (PLANET_COLORS[key]) {
    // Listed Planets with predefined hex colors and maintaining the procedural dot pattern style
    ctx.fillStyle = PLANET_COLORS[key];
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
    for (let i = 0; i < 35; i++) {
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      ctx.beginPath(); 
      ctx.arc(x, y, 10 + Math.random() * 30, 0, Math.PI * 2); 
      ctx.fill();
    }
  } else {
    // Fallback: Fully random procedural colors based on name string for unlisted objects
    const hash = hashCode(key);
    ctx.fillStyle = generateColor(hash);
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = generateColor(hash * 2);
    for (let i = 0; i < 40; i++) {
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      ctx.beginPath(); ctx.arc(x, y, 10 + Math.random() * 30, 0, Math.PI * 2); ctx.fill();
    }
  }
  
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

function createPlanetMesh(name, radius) {
  const key = name.toLowerCase();
  if (key === 'earth') {
    const geo = new THREE.SphereGeometry(radius, 64, 64);
    const mat = new THREE.MeshStandardMaterial({ map: earthAlbedoMap, roughness: 0.6, metalness: 0.1 });
    return new THREE.Mesh(geo, mat);
  }
  const geo = new THREE.SphereGeometry(radius, 32, 32);
  const mat = new THREE.MeshStandardMaterial({ map: createPlanetTexture(name), roughness: 0.7 });
  return new THREE.Mesh(geo, mat);
}

function renderScene(data) {
  const sampleCount = 30;
  const startX = -11.0;
  const endX = 11.0;
  const planetRadius = 2.5;

  function buildStraightBridge() {
    const edgeStart = startX + 2.6; 
    const edgeEnd = endX - 2.6;
    for (let i = 0; i < sampleCount; i++) {
      const t = (i + 1) / (sampleCount + 1);
      const x = THREE.MathUtils.lerp(edgeStart, edgeEnd, t);
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.22, 0.22), new THREE.MeshStandardMaterial({ color: 0x223344, roughness: 0.4 }));
      mesh.position.set(x, 0, 0);
      activeStageGroup.add(mesh);
      currentStackMeshes.push(mesh);
    }
  }

  if (data.mode === "terrestrial") {
    document.getElementById('stageLegend').textContent = `Mode: Earth-to-Earth (${data.origin.name} → ${data.destination.name})`;

    const earth1 = createPlanetMesh('earth', planetRadius);
    earth1.position.set(startX, 0, 0);
    const v1 = latLonToVector3(data.origin.coords.lat, data.origin.coords.lon, planetRadius);
    const pin1 = createPinMesh();
    pin1.position.copy(v1);
    pin1.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v1.clone().normalize());
    earth1.add(pin1);
    earth1.quaternion.setFromUnitVectors(v1.clone().normalize(), new THREE.Vector3(0, 0, 1));
    activeStageGroup.add(earth1);

    const earth2 = createPlanetMesh('earth', planetRadius);
    earth2.position.set(endX, 0, 0);
    const v2 = latLonToVector3(data.destination.coords.lat, data.destination.coords.lon, planetRadius);
    const pin2 = createPinMesh();
    pin2.position.copy(v2);
    pin2.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v2.clone().normalize());
    earth2.add(pin2);
    earth2.quaternion.setFromUnitVectors(v2.clone().normalize(), new THREE.Vector3(0, 0, 1));
    activeStageGroup.add(earth2);

    buildStraightBridge();
  } else if (data.mode === "hybrid") {
    document.getElementById('stageLegend').textContent = `Mode: Hybrid (${data.origin.name} → ${data.destination.name})`;
    const isOriginCity = data.origin.type === "city";
    
    if (isOriginCity) {
      const earth = createPlanetMesh('earth', planetRadius);
      earth.position.set(startX, 0, 0);
      const v = latLonToVector3(data.origin.coords.lat, data.origin.coords.lon, planetRadius);
      const pin = createPinMesh();
      pin.position.copy(v);
      pin.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v.clone().normalize());
      earth.add(pin);
      earth.quaternion.setFromUnitVectors(v.clone().normalize(), new THREE.Vector3(0, 0, 1));
      activeStageGroup.add(earth);
    } else {
      const planet = createPlanetMesh(data.origin.name, planetRadius);
      planet.position.set(startX, 0, 0);
      activeStageGroup.add(planet);
    }

    if (!isOriginCity) {
      const earth = createPlanetMesh('earth', planetRadius);
      earth.position.set(endX, 0, 0);
      const v = latLonToVector3(data.destination.coords.lat, data.destination.coords.lon, planetRadius);
      const pin = createPinMesh();
      pin.position.copy(v);
      pin.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v.clone().normalize());
      earth.add(pin);
      earth.quaternion.setFromUnitVectors(v.clone().normalize(), new THREE.Vector3(0, 0, 1));
      activeStageGroup.add(earth);
    } else {
      const planet = createPlanetMesh(data.destination.name, planetRadius);
      planet.position.set(endX, 0, 0);
      activeStageGroup.add(planet);
    }
    buildStraightBridge();
  } else {
    document.getElementById('stageLegend').textContent = `Mode: Space (${data.origin.name} → ${data.destination.name})`;

    const planet1 = createPlanetMesh(data.origin.name, planetRadius);
    planet1.position.set(startX, 0, 0);
    activeStageGroup.add(planet1);

    const planet2 = createPlanetMesh(data.destination.name, 2.0); 
    planet2.position.set(endX, 0, 0);
    activeStageGroup.add(planet2);
    buildStraightBridge();
  }
}

function animate() {
  requestAnimationFrame(animate);

  if (currentStackMeshes.length > 0) {
    fillProgress += 0.012; 
    if (fillProgress > 1.3) fillProgress = 0; 
    
    const visibleLimit = Math.floor(Math.min(fillProgress, 1.0) * currentStackMeshes.length);
    currentStackMeshes.forEach((mesh, idx) => {
      if (idx <= visibleLimit) {
        mesh.material.color.setHex(0x00ffff);
        mesh.material.emissive.setHex(0x0088cc);
      } else {
        mesh.material.color.setHex(0x223344);
        mesh.material.emissive.setHex(0x000000);
      }
    });
  }
  renderer.render(scene, camera);
}
animate();

const findOutBtn = document.getElementById('findOutBtn');

findOutBtn.addEventListener('click', async () => {
  const headline = document.getElementById('resultHeadline');
  
  // UI Reset Fix
  headline.textContent = "Calculating distance & stack...";
  document.getElementById('statCount').textContent = "--";
  document.getElementById('statDistance').textContent = "--";
  document.getElementById('statStride').textContent = "--";
  document.getElementById('stageLegend').textContent = "Awaiting response...";
  
  // Clear the 3D visual immediately
  while (activeStageGroup.children.length > 0) {
    activeStageGroup.remove(activeStageGroup.children[0]);
  }
  currentStackMeshes = [];

  findOutBtn.disabled = true;
  
  try {
    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        origin: document.getElementById('originInput').value,
        destination: document.getElementById('destInput').value,
        measurement_object: document.getElementById('objectInput').value
      })
    });

    const data = await res.json();
    if (!data.success) {
      headline.textContent = data.error || "Error calculating.";
      return;
    }

    headline.innerHTML = `It takes <span class="highlight">${data.total_count.toLocaleString()}</span> ${data.object.name}s to span from ${data.origin.name} to ${data.destination.name}.`;
    document.getElementById('statCount').textContent = data.total_count.toLocaleString();
    document.getElementById('statDistance').textContent = `${data.distance_km.toLocaleString()} km`;
    document.getElementById('statStride').textContent = `${data.object.dimension_meters} m`;

    renderScene(data);
  } catch (err) {
    console.error("Calculation failed:", err);
    headline.textContent = "Server connection error.";
  } finally {
    findOutBtn.disabled = false;
  }
});

window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});