// ---- Layout constants: single source of truth for the baseline system ----
const STAGE_HEIGHT_PX = 480;      // must match .stage-wrapper height in CSS
const BASELINE_OFFSET_PX = 70;    // distance from stage floor up to the 0cm line (space reserved for labels)
const TOP_PADDING_PX = 20;        // breathing room above the tallest figure
const MAX_FIGURE_PX = STAGE_HEIGHT_PX - BASELINE_OFFSET_PX - TOP_PADDING_PX; // 390px available for figure height
const RULER_TICK_COUNT = 6;       // fixed number of labels, e.g. 0,1,2,3,4,5 × interval

// Pin both figure-frames to the same baseline, once, on load
function initFrames() {
  document.querySelectorAll('.figure-frame').forEach(frame => {
    frame.style.bottom = `${BASELINE_OFFSET_PX}px`;
    frame.style.height = `${MAX_FIGURE_PX}px`;
  });
}
initFrames();

// Build (or rebuild) the ruler with a fixed tick count, scaled to rangeMax
function buildRuler(rangeMax, pxPerCm) {
  const grid = document.getElementById('measurementGrid');
  grid.innerHTML = '';
  const tickInterval = rangeMax / (RULER_TICK_COUNT - 1);

  for (let i = 0; i < RULER_TICK_COUNT; i++) {
    const cmVal = Math.round(i * tickInterval);
    const bottomPx = BASELINE_OFFSET_PX + cmVal * pxPerCm;

    const line = document.createElement('div');
    line.className = 'ruler-line' + (i === 0 ? ' baseline-tick' : '');
    line.style.bottom = `${bottomPx}px`;
    line.innerHTML = `
      <span class="ruler-label">${cmVal} cm</span>
      <span class="ruler-label">${cmVal} cm</span>
    `;
    grid.appendChild(line);
  }
}

// Initial ruler before any comparison has been run
buildRuler(200, MAX_FIGURE_PX / 200);

const compareBtn = document.getElementById('compareBtn');

compareBtn.addEventListener('click', async () => {
  const celebInput = document.getElementById('celebInput').value.trim();
  const heightInput = document.getElementById('heightInput').value.trim();
  const headline = document.getElementById('resultHeadline');
  const subtext = document.getElementById('resultSubtext');

  const userHeightVal = parseFloat(heightInput);

  if (isNaN(userHeightVal) || userHeightVal <= 0) {
    headline.textContent = "Invalid Height";
    subtext.textContent = "Please enter a valid height greater than 0 cm.";
    document.getElementById('mannequinImg').style.height = '0px';
    document.getElementById('laserGuideLine').style.display = 'none';
    return;
  }

  if (!celebInput) {
    headline.textContent = "Missing Input";
    subtext.textContent = "Please fill in the celebrity name field.";
    return;
  }

  headline.textContent = `Analyzing dimensions for ${celebInput}...`;
  subtext.textContent = "Contacting archives...";

  compareBtn.disabled = true;

  try {
    const res = await fetch('/api/height-compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ celebrity: celebInput, user_height: userHeightVal })
    });

    const data = await res.json();
    if (!data.success) {
      headline.textContent = "Error processing data.";
      subtext.textContent = data.error || "Lookup failed. Please verify your input.";
      return;
    }

    const celeb = data.celebrity;
    const user = data.user;

    // 1. Update Labels
    document.getElementById('celebNameDisplay').textContent = celeb.name.toUpperCase();
    document.getElementById('celebHeightDisplay').textContent = `${celeb.height_cm} cm`;
    document.getElementById('userHeightDisplay').textContent = `${user.height_cm} cm`;

    // 2. Compute a single shared scale for this comparison, with headroom,
    //    rounded to a clean 10cm boundary so ruler labels look sane.
    const tallerCm = Math.max(celeb.height_cm, user.height_cm);
    const rangeMax = Math.ceil((tallerCm * 1.08) / 10) * 10;
    const pxPerCm = MAX_FIGURE_PX / rangeMax;

    // 3. Rebuild the ruler to match this comparison's scale
    buildRuler(rangeMax, pxPerCm);

    // 4. Scale User Mannequin — height only; bottom is fixed by initFrames()
    const userPx = Math.round(user.height_cm * pxPerCm);
    document.getElementById('mannequinImg').style.height = `${userPx}px`;

    // 5. Scale Celebrity Image / placeholder — same shared pxPerCm
    const celebPx = Math.round(celeb.height_cm * pxPerCm);
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

    // 6. Laser pinned to the TOP of the mannequin, from the shared baseline
    const laser = document.getElementById('laserGuideLine');
    laser.style.display = 'block';
    laser.style.bottom = `${BASELINE_OFFSET_PX + userPx}px`;

    // 7. Output comparison text
    headline.innerHTML = `<span class="highlight">${data.comparison_text}</span>`;
    subtext.textContent = `${celeb.name} stands at ${celeb.height_cm} cm while you measure ${user.height_cm} cm.`;

  } catch (err) {
    console.error("Comparison error:", err);
    headline.textContent = "Server Error";
    subtext.textContent = "Failed to communicate with calculation service.";
  } finally {
    compareBtn.disabled = false;
  }
});