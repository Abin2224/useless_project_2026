// Baseline stage scale: 220 cm maps to ~360 pixels
const STAGE_MAX_CM = 230;
const STAGE_PIXELS = 370;
const PX_PER_CM = STAGE_PIXELS / STAGE_MAX_CM;

// Build background tick ruler
const grid = document.getElementById('measurementGrid');
for (let cm = 50; cm <= 220; cm += 25) {
  const line = document.createElement('div');
  line.className = 'ruler-line';
  line.style.bottom = `${cm * PX_PER_CM}px`;
  line.innerHTML = `
    <span class="ruler-label">${cm} cm</span>
    <span class="ruler-label">${cm} cm</span>
  `;
  grid.appendChild(line);
}

document.getElementById('compareBtn').addEventListener('click', async () => {
  const celebInput = document.getElementById('celebInput').value.trim();
  const heightInput = document.getElementById('heightInput').value.trim();
  const headline = document.getElementById('resultHeadline');
  const subtext = document.getElementById('resultSubtext');

  if (!celebInput || !heightInput) {
    headline.textContent = "Please fill in both fields.";
    return;
  }

  headline.textContent = `Analyzing dimensions for ${celebInput}...`;

  try {
    const res = await fetch('/api/height-compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        celebrity: celebInput,
        user_height: heightInput
      })
    });

    const data = await res.json();
    if (!data.success) {
      headline.textContent = data.error || "Lookup failed.";
      return;
    }

    const celeb = data.celebrity;
    const user = data.user;

    // 1. Update Labels
    document.getElementById('celebNameDisplay').textContent = celeb.name.toUpperCase();
    document.getElementById('celebHeightDisplay').textContent = `${celeb.height_cm} cm`;
    document.getElementById('userHeightDisplay').textContent = `${user.height_cm} cm`;

    // 2. Scale User Mannequin
    const userPx = Math.round(user.height_cm * PX_PER_CM);
    const mannequin = document.getElementById('mannequinImg');
    mannequin.style.height = `${userPx}px`;

    // 3. Scale Celebrity Image
    const celebPx = Math.round(celeb.height_cm * PX_PER_CM);
    const celebImg = document.getElementById('celebImg');
    const placeholder = document.getElementById('celebPlaceholder');

    if (celeb.image_url) {
      celebImg.src = celeb.image_url;
      celebImg.style.height = `${celebPx}px`;
      celebImg.style.display = 'block';
      placeholder.style.display = 'none';
    } else {
      celebImg.style.display = 'none';
      placeholder.style.display = 'flex';
      placeholder.style.height = `${celebPx}px`;
      placeholder.textContent = `No photo available (${celeb.height_cm} cm)`;
    }

    // 4. Position Dynamic Laser Guide across tops
    const laser = document.getElementById('laserGuideLine');
    const laserHeightPx = Math.max(userPx, celebPx);
    laser.style.display = 'block';
    laser.style.bottom = `${laserHeightPx}px`;

    // 5. Output comparison text
    headline.innerHTML = `<span class="highlight">${data.comparison_text}</span>`;
    subtext.textContent = `${celeb.name} stands at ${celeb.height_cm} cm while you measure ${user.height_cm} cm.`;

  } catch (err) {
    console.error("Comparison error:", err);
    headline.textContent = "Server connection error.";
  }
});

// Trigger initial comparison on load
window.addEventListener('load', () => {
  document.getElementById('compareBtn').click();
});