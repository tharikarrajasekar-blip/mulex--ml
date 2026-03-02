// --- AML CHART (lazy init) ---
let amlChartInstance = null;
function initAMLChart() {
  if (amlChartInstance) return;
  const ctx = document.getElementById('amlChart');
  if (!ctx) return;
  amlChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['LAYERING','STRUCTURING','SMURFING','DISPERSION','CIRCULAR'],
      datasets: [{ label: 'Detections', data: [4,7,2,9,3],
        backgroundColor: ['#ff2244','#ff9900','#ff2244','#ff2244','#ff9900'], borderWidth: 0 }]
    },
    options: {
      responsive: true, plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color:'#6a9fc0', font:{family:'Share Tech Mono',size:9} }, grid:{color:'rgba(0,212,255,0.05)'} },
        y: { ticks: { color:'#6a9fc0', font:{family:'Share Tech Mono',size:9} }, grid:{color:'rgba(0,212,255,0.05)'} }
      }
    }
  });
}

// --- BIO CHART (lazy init) ---
let bioChartInstance = null;
function initBioChart() {
  if (bioChartInstance) return;
  const ctx = document.getElementById('bioChart');
  if (!ctx) return;
  const data = { labels: [], datasets: [{ label:'Mouse Velocity', data:[],
    borderColor:'#00d4ff', tension:0.4, pointRadius:0, borderWidth:1.5 }] };
  bioChartInstance = new Chart(ctx, {
    type:'line', data,
    options: {
      animation:false, responsive:true, plugins:{legend:{display:false}},
      scales: {
        x: { display:false },
        y: { ticks:{color:'#6a9fc0',font:{family:'Share Tech Mono',size:9}}, grid:{color:'rgba(0,212,255,0.05)'} }
      }
    }
  });
}

// ─── INIT ───
let userRole = 'ADMIN';
let voiceMuted = false;
let bioTypingData = [];
let mouseMoveHistory = [];
let lastMouseX = 0, lastMouseY = 0, lastMouseTime = Date.now();
let authFace = false, authLiveness = false, authVoice = false;

// Clock
setInterval(() => {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString('en-IN');
}, 1000);

// ─── LOGIN ───
function login() {
  userRole = document.getElementById('role').value;
  document.getElementById('loginPage').style.display = 'none';
  document.getElementById('mainApp').style.display = 'block';
  document.getElementById('roleTag').textContent = userRole;
  document.getElementById('sidebarRole').textContent = 'ROLE: ' + userRole;

  if (userRole === 'INVESTIGATOR') {
    document.getElementById('navAML').style.display = 'none';
  }

  initDashboard();
  // graph drawn on demand
  // bioChart initialized lazily
  startLiveFeed();
  populateAlerts();
  startWebSocketSim();
  setTimeout(() => speak('Welcome to MuleX AI. ' + userRole + ' session initiated. All systems operational.'), 500);
}

// ─── SECTION SWITCH ───
function showSection(id, el) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  if (el) el.classList.add('active');

  const titles = {
    dashboard: 'UNIFIED RISK DASHBOARD',
    trust: 'TRUST SCORING ENGINE',
    kyc: 'AI KYC VERIFICATION',
    auth: 'DEEPFAKE AUTHENTICATION',
    fraud: 'FRAUD DETECTION ENGINE',
    aml: 'AML MONITORING',
    biometrics: 'BEHAVIORAL BIOMETRICS',
    graph: 'MULE NETWORK GRAPH',
    alerts: 'ALERT PRIORITIZATION',
    explain: 'EXPLAINABLE AI'
  };
  document.getElementById('pageTitle').textContent = titles[id] || id.toUpperCase();

  if (id === 'graph') drawGraph();
  if (id === 'aml') initAMLChart();
  if (id === 'biometrics') initBioChart();
  if (id === 'geomap') setTimeout(() => initLeafletMap(), 120);
  if (id === 'aml') initAMLChart();
  if (id === 'biometrics') initBioChart();
}

// ─── DASHBOARD ───
function initDashboard() {
  // Fraud trend chart
  new Chart(document.getElementById('fraudChart'), {
    type: 'line',
    data: {
      labels: ['MON','TUE','WED','THU','FRI','SAT','SUN'],
      datasets: [{
        label: 'Fraud Cases',
        data: [3, 7, 4, 9, 6, 11, 8],
        borderColor: '#ff2244',
        backgroundColor: 'rgba(255,34,68,0.08)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#ff2244',
        pointRadius: 4
      }, {
        label: 'Blocked',
        data: [2, 5, 3, 7, 5, 9, 7],
        borderColor: '#00d4ff',
        backgroundColor: 'rgba(0,212,255,0.05)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#00d4ff',
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 10 } } } },
      scales: {
        x: { ticks: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 10 } }, grid: { color: 'rgba(0,212,255,0.05)' } },
        y: { ticks: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 10 } }, grid: { color: 'rgba(0,212,255,0.05)' } }
      }
    }
  });

  // Risk donut
  new Chart(document.getElementById('riskDonut'), {
    type: 'doughnut',
    data: {
      labels: ['Safe','Medium','High','Critical'],
      datasets: [{ data: [68, 18, 9, 5], backgroundColor: ['#00ff88','#00d4ff','#ff9900','#ff2244'], borderWidth: 0 }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 10 } } } }
    }
  });

  // amlChart initialized lazily in showSection

  // Alert table
  const alerts = [
    { acc: 'ACC-9087-XK', score: 94, type: 'MULE NETWORK', time: '14:32:11', status: 'BLOCKED' },
    { acc: 'ACC-3312-BB', score: 88, type: 'AML LAYERING', time: '14:28:05', status: 'UNDER REVIEW' },
    { acc: 'ACC-7741-ZQ', score: 82, type: 'DEEPFAKE AUTH', time: '14:19:44', status: 'FLAGGED' },
    { acc: 'ACC-5503-PQ', score: 76, type: 'VELOCITY SPIKE', time: '14:11:02', status: 'MONITORING' },
  ];

  const tbody = document.getElementById('dashAlertTable');
  alerts.forEach(a => {
    const statusClass = a.status === 'BLOCKED' ? 'badge-danger' : a.status === 'UNDER REVIEW' ? 'badge-warn' : a.status === 'FLAGGED' ? 'badge-warn' : 'badge-info';
    const scoreColor = a.score > 85 ? 'danger' : 'warn';
    tbody.innerHTML += `
      <tr>
        <td style="font-family:var(--font-mono);color:var(--accent)">${a.acc}</td>
        <td><span style="font-family:var(--font-head);color:var(--${scoreColor});font-size:16px">${a.score}</span></td>
        <td style="font-family:var(--font-mono);font-size:11px;color:var(--text2)">${a.type}</td>
        <td style="font-family:var(--font-mono);font-size:11px;color:var(--text2)">${a.time}</td>
        <td><span class="badge ${statusClass}">${a.status}</span></td>
        <td><button class="btn" style="padding:4px 10px;font-size:9px" onclick="showSHAP()">EXPLAIN</button></td>
      </tr>`;
  });
}

// ─── LIVE FEED ───
const feedMessages = [
  { text: 'TXN ₹1,200 · ACC-1103 · Mumbai → APPROVED', type: 'safe' },
  { text: 'TXN ₹95,000 · ACC-9087 · Delhi → FLAGGED HIGH VELOCITY', type: 'warn' },
  { text: 'LOGIN ATTEMPT · ACC-3312 · IP 192.168.4.20 → DEEPFAKE DETECTED', type: 'danger' },
  { text: 'TXN ₹500 · ACC-2201 · Chennai → APPROVED', type: 'safe' },
  { text: 'KYC UPLOAD · ACC-7741 · Document Tampering → BLOCKED', type: 'danger' },
  { text: 'TXN ₹48,000 · ACC-5503 · Pune → STEP-UP AUTH REQUIRED', type: 'warn' },
  { text: 'AML ALERT · ACC-8800 · Layering Pattern → STR GENERATED', type: 'danger' },
  { text: 'TXN ₹220 · ACC-0042 · Bengaluru → APPROVED', type: 'safe' },
];

function startLiveFeed() {
  let i = 0;
  const feed = document.getElementById('liveFeed');
  const fraudFeed = document.getElementById('fraudFeed');
  setInterval(() => {
    const m = feedMessages[i % feedMessages.length];
    const time = new Date().toLocaleTimeString('en-IN');
    const line = `<div class="feed-line"><span class="time">[${time}]</span><span class="${m.type}">${m.text}</span></div>`;
    if (feed) { feed.innerHTML = line + feed.innerHTML; if (feed.children.length > 20) feed.lastChild.remove(); }
    if (fraudFeed) { fraudFeed.innerHTML = line + fraudFeed.innerHTML; if (fraudFeed.children.length > 20) fraudFeed.lastChild.remove(); }
    i++;
  }, 2500);
}

// ─── TRUST ENGINE ───
function updateSlider(key) {
  document.getElementById('v_' + key).textContent = document.getElementById('sl_' + key).value;
}

function calculateTrust() {
  const i = +document.getElementById('sl_identity').value;
  const a = +document.getElementById('sl_auth').value;
  const t = +document.getElementById('sl_txn').value;
  const n = +document.getElementById('sl_network').value;
  const b = +document.getElementById('sl_behavior').value;
  const score = (i * 0.2 + a * 0.2 + t * 0.25 + n * 0.2 + b * 0.15);

  document.getElementById('trustScoreNum').textContent = score.toFixed(0);
  drawTrustRing(score);

  const dec = document.getElementById('trustDecision');
  dec.style.display = 'block';
  if (score > 75) { dec.className = 'trust-decision approve'; dec.textContent = '✓ APPROVE'; }
  else if (score > 50) { dec.className = 'trust-decision stepup'; dec.textContent = '⬬ STEP-UP AUTH'; }
  else { dec.className = 'trust-decision block'; dec.textContent = '✕ BLOCK'; }

  document.getElementById('trustDetails').classList.add('show');
  document.getElementById('td_identity').textContent = (i * 0.2).toFixed(1);
  document.getElementById('td_auth').textContent = (a * 0.2).toFixed(1);
  document.getElementById('td_txn').textContent = (t * 0.25).toFixed(1);
  document.getElementById('td_network').textContent = (n * 0.2).toFixed(1);
}

function drawTrustRing(score) {
  const canvas = document.getElementById('trustRingCanvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 160, 160);
  const angle = (score / 100) * Math.PI * 2 - Math.PI / 2;
  ctx.beginPath();
  ctx.arc(80, 80, 65, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(0,212,255,0.1)';
  ctx.lineWidth = 8;
  ctx.stroke();
  const color = score > 75 ? '#00ff88' : score > 50 ? '#ff9900' : '#ff2244';
  ctx.beginPath();
  ctx.arc(80, 80, 65, -Math.PI / 2, angle);
  ctx.strokeStyle = color;
  ctx.lineWidth = 8;
  ctx.lineCap = 'round';
  ctx.stroke();
  document.getElementById('trustScoreNum').style.color = color;
}

// ─── KYC ───
function runKYC() {
  const modules = [
    { id: 'kyc_ocr', delay: 400, val: 'EXTRACTED ✓', cls: 'safe' },
    { id: 'kyc_tamper', delay: 800, val: 'NO TAMPER DETECTED ✓', cls: 'safe' },
    { id: 'kyc_synth', delay: 1200, val: 'REAL IDENTITY ✓', cls: 'safe' },
    { id: 'kyc_consent', delay: 1600, val: 'VALIDATED ✓', cls: 'safe' },
    { id: 'kyc_risk', delay: 2000, val: '12% — LOW RISK', cls: 'safe' },
    { id: 'kyc_verdict', delay: 2400, val: '✓ APPROVED', cls: 'safe' },
  ];
  modules.forEach(m => {
    setTimeout(() => {
      const el = document.getElementById(m.id);
      el.textContent = m.val;
      el.className = 'result-val ' + m.cls;
    }, m.delay);
  });
}

function triggerKYC() { runKYC(); }

// ─── AUTH ───
function scanFace() {
  document.getElementById('faceStatus').textContent = 'SCANNING...';
  setTimeout(() => {
    const ok = Math.random() > 0.2;
    document.getElementById('faceIcon').textContent = ok ? '✅' : '❌';
    document.getElementById('faceStatus').textContent = ok ? 'AUTHENTIC — NO DEEPFAKE' : '⚠ DEEPFAKE DETECTED';
    authFace = ok;
    checkAuthVerdict();
  }, 1500);
}

function checkLiveness() {
  document.getElementById('livenessStatus').textContent = 'ANALYZING...';
  setTimeout(() => {
    document.getElementById('livenessIcon').textContent = '✅';
    document.getElementById('livenessStatus').textContent = 'LIVENESS CONFIRMED';
    authLiveness = true;
    checkAuthVerdict();
  }, 1200);
}

function analyzeVoice() {
  document.getElementById('voiceStatus').textContent = 'ANALYZING...';
  setTimeout(() => {
    document.getElementById('voiceIcon').textContent = '✅';
    document.getElementById('voiceStatus').textContent = 'VOICE AUTHENTIC';
    authVoice = true;
    checkAuthVerdict();
  }, 1000);
}

function checkAuthVerdict() {
  if (authFace && authLiveness && authVoice) {
    document.getElementById('authVerdict').textContent = '✓ AUTHENTICATION SUCCESSFUL — ALL LAYERS PASSED';
    document.getElementById('authVerdict').style.color = 'var(--safe)';
  } else if (!authFace && authFace !== undefined) {
    document.getElementById('authVerdict').textContent = '✕ AUTHENTICATION FAILED — DEEPFAKE DETECTED';
    document.getElementById('authVerdict').style.color = 'var(--danger)';
    triggerAlert('Deepfake authentication attempt detected');
  }
}

// ─── FRAUD ENGINE ───
function simulateFraud() {
  const amount = +document.getElementById('txnAmount').value;
  const velocity = document.getElementById('txnVelocity').value;
  let prob = 0;
  if (amount > 50000) prob += 40;
  if (amount > 100000) prob += 20;
  if (velocity === 'high') prob += 35;
  if (velocity === 'medium') prob += 15;
  prob = Math.min(98, prob + Math.floor(Math.random() * 15));

  document.getElementById('fraudPercent').textContent = prob + '%';
  const color = prob > 75 ? '#ff2244' : prob > 50 ? '#ff9900' : '#00ff88';
  document.getElementById('fraudPercent').style.color = color;

  drawFraudGauge(prob);

  const res = document.getElementById('fraudResult');
  res.classList.add('show');
  res.innerHTML = `
    <div class="result-row"><span class="result-key">FRAUD PROBABILITY</span><span class="result-val ${prob > 75 ? 'danger' : prob > 50 ? 'warn' : 'safe'}">${prob}%</span></div>
    <div class="result-row"><span class="result-key">DECISION</span><span class="result-val ${prob > 75 ? 'danger' : 'warn'}">${prob > 75 ? '🔴 BLOCKED' : prob > 50 ? '🟠 STEP-UP AUTH' : '🟢 APPROVED'}</span></div>
    <div class="result-row"><span class="result-key">MODEL</span><span class="result-val">XGBoost v4.2</span></div>
    <div class="result-row"><span class="result-key">LATENCY</span><span class="result-val">48ms</span></div>
  `;

  if (prob > 75) {
    triggerAlert(`High fraud probability (${prob}%) — Transaction BLOCKED for ACC-9087-XK`);
  }
}

function drawFraudGauge(prob) {
  const canvas = document.getElementById('fraudGauge');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 200, 120);
  ctx.beginPath();
  ctx.arc(100, 100, 80, Math.PI, 0);
  ctx.strokeStyle = 'rgba(0,212,255,0.1)';
  ctx.lineWidth = 12;
  ctx.stroke();
  const angle = Math.PI + (prob / 100) * Math.PI;
  const color = prob > 75 ? '#ff2244' : prob > 50 ? '#ff9900' : '#00ff88';
  ctx.beginPath();
  ctx.arc(100, 100, 80, Math.PI, angle);
  ctx.strokeStyle = color;
  ctx.lineWidth = 12;
  ctx.lineCap = 'round';
  ctx.stroke();
}

// ─── AML CHART (lazy) ───
function initAMLChart() {
  if (amlChartInstance) return;
  const ctx = document.getElementById('amlChart');
  if (!ctx) return;
  amlChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['LAYERING','STRUCTURING','SMURFING','DISPERSION','CIRCULAR'],
      datasets: [{ label: 'Detections', data: [4, 7, 2, 9, 3], backgroundColor: ['#ff2244','#ff9900','#ff2244','#ff2244','#ff9900'], borderWidth: 0 }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 9 } }, grid: { color: 'rgba(0,212,255,0.05)' } },
        y: { ticks: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 9 } }, grid: { color: 'rgba(0,212,255,0.05)' } }
      }
    }
  });
}

// ─── AML ───
function runAML() {
  const account = document.getElementById('amlAccount').value;
  const res = document.getElementById('amlResult');
  res.classList.add('show');
  res.innerHTML = `
    <div class="result-row"><span class="result-key">LAYERING</span><span class="result-val danger">DETECTED ⚠</span></div>
    <div class="result-row"><span class="result-key">STRUCTURING</span><span class="result-val warn">POSSIBLE</span></div>
    <div class="result-row"><span class="result-key">FUND DISPERSION</span><span class="result-val danger">HIGH</span></div>
    <div class="result-row"><span class="result-key">STR STATUS</span><span class="result-val warn">AUTO-GENERATED</span></div>
    <div class="result-row"><span class="result-key">ACCOUNT</span><span class="result-val">${account}</span></div>
  `;
  speak('AML scan complete. Layering pattern detected on account ' + account + '. Suspicious Transaction Report auto-generated.');
}

function downloadSTR() {
  const account = document.getElementById('amlAccount').value;
  const content = `SUSPICIOUS TRANSACTION REPORT
==============================
Account: ${account}
Date: ${new Date().toLocaleDateString()}
Generated By: MuleX AI AML Engine v4.2

FINDINGS:
- Layering pattern detected
- High fund dispersion
- Cross-channel anomaly
- Circular transaction links

RECOMMENDATION: Immediate investigation required.
STR filed as per RBI guidelines.`;
  const blob = new Blob([content], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `STR_${account}_${Date.now()}.txt`;
  a.click();
}

// ─── BIOMETRICS ───
function analyzeBehavior() {
  const text = document.getElementById('bioInput').value;
  const wpm = Math.floor((text.split(' ').length / (Date.now() / 60000)) * 10);
  const clamped = Math.min(wpm, 120);
  document.getElementById('bioTyping').textContent = clamped + ' WPM';
  document.getElementById('bioTypingBar').style.width = (clamped / 120 * 100) + '%';
  if (clamped > 80) {
    document.getElementById('bioTypingStatus').textContent = 'VELOCITY ANOMALY DETECTED';
    document.getElementById('bioTypingStatus').style.color = 'var(--warn)';
  } else {
    document.getElementById('bioTypingStatus').textContent = 'NORMAL TYPING PATTERN';
    document.getElementById('bioTypingStatus').style.color = 'var(--safe)';
  }

  const bioFeed = document.getElementById('bioFeed');
  const time = new Date().toLocaleTimeString();
  bioFeed.innerHTML = `<div class="feed-line"><span class="time">[${time}]</span><span class="safe">Keystroke event captured — WPM: ${clamped}</span></div>` + bioFeed.innerHTML;
}

function initBioChart() {
  if (bioChartInstance) return;
  const ctx = document.getElementById('bioChart');
  if (!ctx) return;
  const data = { labels: [], datasets: [{ label: 'Mouse Velocity', data: [], borderColor: '#00d4ff', tension: 0.4, pointRadius: 0, borderWidth: 1.5 }] };
  bioChartInstance = new Chart(ctx, {
    type: 'line',
    data,
    options: {
      animation: false, responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { display: false },
        y: { ticks: { color: '#6a9fc0', font: { family: 'Share Tech Mono', size: 9 } }, grid: { color: 'rgba(0,212,255,0.05)' } }
      }
    }
  });
}

document.addEventListener('mousemove', e => {
  const now = Date.now();
  const dt = now - lastMouseTime;
  if (dt > 50) {
    const dx = e.clientX - lastMouseX, dy = e.clientY - lastMouseY;
    const vel = Math.sqrt(dx * dx + dy * dy) / (dt / 1000);
    const clamped = Math.min(Math.floor(vel), 2000);

    document.getElementById('bioMouse').textContent = clamped + ' px/s';
    const pct = Math.min(clamped / 2000 * 100, 100);
    document.getElementById('bioMouseBar').style.width = pct + '%';

    if (bioChartInstance) {
      const d = bioChartInstance.data;
      d.labels.push('');
      d.datasets[0].data.push(clamped);
      if (d.labels.length > 40) { d.labels.shift(); d.datasets[0].data.shift(); }
      bioChartInstance.update('none');
    }

    lastMouseX = e.clientX; lastMouseY = e.clientY; lastMouseTime = now;
  }
});

// ─── GRAPH ───
function drawGraph() {
  const container = document.getElementById('networkGraph');
  const nodes = new vis.DataSet([
    { id: 1, label: 'ACC-101', color: { background: '#003a1a', border: '#00ff88' }, font: { color: '#00ff88' } },
    { id: 2, label: 'ACC-202', color: { background: '#3a2000', border: '#ff9900' }, font: { color: '#ff9900' } },
    { id: 3, label: 'ACC-303', color: { background: '#3a0010', border: '#ff2244' }, font: { color: '#ff2244' } },
    { id: 4, label: 'ACC-404', color: { background: '#3a0010', border: '#ff2244' }, font: { color: '#ff2244' } },
    { id: 5, label: 'ACC-505', color: { background: '#3a2000', border: '#ff9900' }, font: { color: '#ff9900' } },
    { id: 6, label: 'ACC-606', color: { background: '#3a0010', border: '#ff2244' }, font: { color: '#ff2244' } },
    { id: 7, label: 'ACC-707', color: { background: '#003a1a', border: '#00ff88' }, font: { color: '#00ff88' } },
    { id: 8, label: 'ACC-808', color: { background: '#3a2000', border: '#ff9900' }, font: { color: '#ff9900' } },
  ]);

  const edges = new vis.DataSet([
    { from: 1, to: 2, color: { color: '#ff990066' } },
    { from: 2, to: 3, color: { color: '#ff224466' } },
    { from: 3, to: 4, color: { color: '#ff224466' } },
    { from: 4, to: 2, color: { color: '#ff224466' }, dashes: true },
    { from: 4, to: 6, color: { color: '#ff224466' } },
    { from: 5, to: 3, color: { color: '#ff990066' } },
    { from: 6, to: 3, color: { color: '#ff224466' }, dashes: true },
    { from: 7, to: 1, color: { color: '#00d4ff44' } },
    { from: 8, to: 5, color: { color: '#ff990066' } },
    { from: 3, to: 8, color: { color: '#ff224466' }, dashes: true },
    { from: 6, to: 8, color: { color: '#ff224466' } },
    { from: 2, to: 5, color: { color: '#ff990066' } },
  ]);

  new vis.Network(container, { nodes, edges }, {
    nodes: { shape: 'dot', size: 22, borderWidth: 2, font: { size: 12, face: 'Share Tech Mono' } },
    edges: { arrows: 'to', width: 1.5, smooth: { type: 'curvedCW', roundness: 0.2 } },
    physics: { stabilization: { iterations: 100 }, barnesHut: { gravitationalConstant: -5000, springLength: 150 } },
    background: { color: 'transparent' }
  });
}

function refreshGraph() {
  drawGraph();
  speak('Mule network graph refreshed. 3 circular transaction patterns detected.');
}

// ─── ALERTS TABLE ───
function populateAlerts() {
  const data = [
    { acc: 'ACC-9087-XK', score: 94, type: 'MULE NETWORK', time: '14:32:11', priority: 'CRITICAL', status: 'OPEN' },
    { acc: 'ACC-3312-BB', score: 88, type: 'AML LAYERING', time: '14:28:05', priority: 'HIGH', status: 'REVIEW' },
    { acc: 'ACC-7741-ZQ', score: 82, type: 'DEEPFAKE', time: '14:19:44', priority: 'HIGH', status: 'OPEN' },
    { acc: 'ACC-5503-PQ', score: 76, type: 'VELOCITY', time: '14:11:02', priority: 'MEDIUM', status: 'REVIEW' },
    { acc: 'ACC-2280-KK', score: 65, type: 'BIOMETRIC', time: '14:05:30', priority: 'MEDIUM', status: 'CLOSED' },
    { acc: 'ACC-1100-ZZ', score: 55, type: 'KYC FAIL', time: '13:58:12', priority: 'LOW', status: 'CLOSED' },
  ];

  const tbody = document.getElementById('alertTableBody');
  data.forEach((a, idx) => {
    const pc = a.priority === 'CRITICAL' ? 'badge-danger' : a.priority === 'HIGH' ? 'badge-danger' : a.priority === 'MEDIUM' ? 'badge-warn' : 'badge-info';
    const sc = a.status === 'OPEN' ? 'badge-danger' : a.status === 'REVIEW' ? 'badge-warn' : 'badge-safe';
    tbody.innerHTML += `
      <tr>
        <td style="font-family:var(--font-mono);color:var(--text2)">${idx + 1}</td>
        <td style="font-family:var(--font-mono);color:var(--accent)">${a.acc}</td>
        <td style="font-family:var(--font-head);color:${a.score > 85 ? 'var(--danger)' : 'var(--warn)'};;font-size:16px">${a.score}</td>
        <td style="font-family:var(--font-mono);font-size:11px">${a.type}</td>
        <td style="font-family:var(--font-mono);font-size:11px;color:var(--text2)">${a.time}</td>
        <td><span class="badge ${pc}">${a.priority}</span></td>
        <td><span class="badge ${sc}">${a.status}</span></td>
      </tr>`;
  });
}

// ─── ALERTS & VOICE ───
function triggerAlert(msg) {
  const overlay = document.getElementById('criticalOverlay');
  document.getElementById('criticalMsg').innerHTML = msg.toUpperCase() + '<br><span style="font-size:14px;opacity:0.8">IMMEDIATE INVESTIGATION REQUIRED</span>';
  overlay.classList.add('show');
  speak('CRITICAL ALERT. ' + msg + '. Immediate action required.');
  playSiren();

  const badge = document.getElementById('alertBadge');
  badge.textContent = (+badge.textContent + 1).toString();
}

function triggerVoiceOnly(msg) {
  speak(msg);
  const icon = document.getElementById('voicePanelIcon');
  icon.classList.add('speaking');
  document.getElementById('voiceLog').textContent = msg;
  setTimeout(() => icon.classList.remove('speaking'), 3000);
}

function dismissAlert() {
  document.getElementById('criticalOverlay').classList.remove('show');
}

function testAlert() {
  triggerAlert('Test critical alert. High risk mule account detected on network cluster 3.');
}

// --- VOICE ASSISTANT (robust, cross-browser, with mute) ---
let voiceReady = false;
let voiceQueue = [];
let isSpeaking = false;

function loadVoices() {
  return new Promise(resolve => {
    let voices = window.speechSynthesis.getVoices();
    if (voices.length) { resolve(voices); return; }
    window.speechSynthesis.addEventListener('voiceschanged', () => {
      resolve(window.speechSynthesis.getVoices());
    }, { once: true });
    setTimeout(() => resolve(window.speechSynthesis.getVoices()), 1500);
  });
}

function pickVoice(voices) {
  const preferred = [
    v => /en[-_]IN/i.test(v.lang),
    v => /en[-_]GB/i.test(v.lang),
    v => /en[-_]US/i.test(v.lang),
    v => /^en/i.test(v.lang),
    () => true
  ];
  for (const test of preferred) {
    const v = voices.find(test);
    if (v) return v;
  }
  return null;
}

let cachedVoice = null;
loadVoices().then(voices => {
  cachedVoice = pickVoice(voices);
  voiceReady = true;
});

function speak(msg) {
  if (!('speechSynthesis' in window) || !msg) return;
  if (voiceMuted) return; // Voice is muted

  if (voiceMuted) {
    const log = document.getElementById('voiceLog');
    if (log) log.textContent = 'MUTED: ' + msg.substring(0, 55) + (msg.length > 55 ? '...' : '');
    return;
  }

  const icon = document.getElementById('voicePanelIcon');
  const log  = document.getElementById('voiceLog');
  if (log)  log.textContent = msg;
  if (icon) icon.classList.add('speaking');

  window.speechSynthesis.cancel();

  const doSpeak = () => {
    const utt = new SpeechSynthesisUtterance(msg);
    if (cachedVoice) utt.voice = cachedVoice;
    utt.lang   = (cachedVoice && cachedVoice.lang) || 'en-US';
    utt.rate   = 0.92;
    utt.pitch  = 1.05;
    utt.volume = 1.0;

    const keepAlive = setInterval(() => {
      if (!window.speechSynthesis.speaking) clearInterval(keepAlive);
      else { window.speechSynthesis.pause(); window.speechSynthesis.resume(); }
    }, 10000);

    utt.onend = () => {
      clearInterval(keepAlive);
      isSpeaking = false;
      if (icon) icon.classList.remove('speaking');
    };
    utt.onerror = () => {
      clearInterval(keepAlive);
      isSpeaking = false;
      if (icon) icon.classList.remove('speaking');
    };

    isSpeaking = true;
    window.speechSynthesis.speak(utt);
  };

  if (!voiceReady || window.speechSynthesis.getVoices().length === 0) {
    loadVoices().then(voices => {
      if (!cachedVoice) cachedVoice = pickVoice(voices);
      setTimeout(doSpeak, 100);
    });
  } else {
    setTimeout(doSpeak, 80);
  }
}

function playSiren() {
  try { new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3').play().catch(() => {}); } catch (e) {}
}

function testVoice() {
  speak('MuleX AI voice assistant is active. All fraud detection systems are online and monitoring transactions.');
}

function testVoiceAlert() {
  speak('Critical alert. High risk mule account detected. Immediate investigation required.');
}

function stopVoice() {
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  isSpeaking = false;
  voiceQueue.length = 0;
  const icon = document.getElementById('voicePanelIcon');
  const log  = document.getElementById('voiceLog');
  if (icon) icon.classList.remove('speaking');
  if (log)  log.textContent = 'STOPPED';
}

// ─── VOICE ON/OFF TOGGLE ───
function toggleVoice() {
  voiceMuted = !voiceMuted;

  // Stop speech immediately on mute
  if (voiceMuted && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    isSpeaking = false;
    voiceQueue.length = 0;
  }

  syncAllToggleUI();
  showVoiceToast(voiceMuted ? '🔇 Voice Muted' : '🔊 Voice Enabled');

  // Announce if turned back on
  if (!voiceMuted) setTimeout(() => speak('Voice assistant is now active.'), 300);
}

// Sync every toggle widget across the page
function syncAllToggleUI() {
  // ── Topbar toggle ──
  const tbTrack  = document.getElementById('voiceToggleTrack');
  const tbThumb  = document.getElementById('voiceToggleThumb');
  const tbStatus = document.getElementById('voiceToggleStatus');
  const tbLabel  = document.getElementById('voiceToggleLabel');
  const tbWrap   = document.querySelector('.voice-toggle-wrap');

  if (tbTrack)  tbTrack.classList.toggle('muted', voiceMuted);
  if (tbThumb)  tbThumb.classList.toggle('muted', voiceMuted);
  if (tbStatus) {
    tbStatus.textContent = voiceMuted ? 'OFF' : 'ON';
    tbStatus.classList.toggle('muted', voiceMuted);
  }
  if (tbLabel) tbLabel.textContent = voiceMuted ? '🔇' : '🔊';
  if (tbWrap) {
    tbWrap.style.borderColor = voiceMuted
      ? 'rgba(255,34,68,0.5)' : 'rgba(0,212,255,0.2)';
    tbWrap.style.background  = voiceMuted
      ? 'rgba(255,34,68,0.07)' : 'rgba(0,212,255,0.04)';
  }

  // ── Alerts panel toggle ──
  const pTrack  = document.getElementById('mutePanelTrack');
  const pThumb  = document.getElementById('mutePanelThumb');
  const pLabel  = document.getElementById('mutePanelLabel');
  const pIcon   = document.getElementById('mutePanelIcon');
  const vIcon   = document.getElementById('voicePanelIcon');
  const vLog    = document.getElementById('voiceLog');

  if (pTrack) pTrack.classList.toggle('muted', voiceMuted);
  if (pThumb) pThumb.classList.toggle('muted', voiceMuted);
  if (pLabel) {
    pLabel.textContent = voiceMuted ? 'VOICE OFF' : 'VOICE ON';
    pLabel.classList.toggle('muted', voiceMuted);
  }
  if (pIcon) pIcon.textContent = voiceMuted ? '🔇' : '🔊';
  if (vIcon) vIcon.textContent = voiceMuted ? '🔇' : '🔊';
  if (vLog)  vLog.textContent  = voiceMuted
    ? '🔇 MUTED — All voice announcements silenced'
    : '🔊 ACTIVE — Monitoring for critical fraud alerts';
}

// Toast notification for toggle feedback
function showVoiceToast(msg) {
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.style.cssText = [
    'position:fixed','bottom:28px','right:28px','z-index:99999',
    'background:#0a1c30','border:1px solid var(--accent)',
    'color:var(--accent)','font-family:var(--font-mono)',
    'font-size:13px','letter-spacing:2px','padding:12px 22px',
    'box-shadow:0 0 24px rgba(0,212,255,0.3)',
    'clip-path:polygon(0 0,calc(100% - 8px) 0,100% 8px,100% 100%,8px 100%,0 calc(100% - 8px))',
    'animation:fadeIn 0.2s ease','transition:opacity 0.5s'
  ].join(';');
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; }, 1800);
  setTimeout(() => toast.remove(), 2400);
}


// ─── SHAP ───
function showSHAP() {
  const account = document.getElementById('explainAccount')?.value || 'ACC-9087-XK';
  document.getElementById('shapAccount').textContent = account;
  document.getElementById('shapOverlay').classList.add('show');
}

// ─── AUDIT LOG ───
function generateAuditLog() {
  const account = document.getElementById('explainAccount').value;
  const res = document.getElementById('auditResult');
  res.classList.add('show');
  res.innerHTML = `
    <div class="result-row"><span class="result-key">AUDIT ID</span><span class="result-val">AUD-${Math.random().toString(36).substr(2,8).toUpperCase()}</span></div>
    <div class="result-row"><span class="result-key">ACCOUNT</span><span class="result-val">${account}</span></div>
    <div class="result-row"><span class="result-key">TIMESTAMP</span><span class="result-val">${new Date().toLocaleString()}</span></div>
    <div class="result-row"><span class="result-key">MODEL USED</span><span class="result-val">XGBoost v4.2.1</span></div>
    <div class="result-row"><span class="result-key">STATUS</span><span class="result-val safe">LOGGED ✓</span></div>
  `;
}

// ─── WEBSOCKET SIMULATION ───
function startWebSocketSim() {
  setInterval(() => {
    const events = [
      'FRAUD: ACC-' + Math.floor(Math.random() * 9000 + 1000) + ' · Score ' + (Math.floor(Math.random() * 30) + 70),
      'AML: Layering detected on cluster ' + Math.floor(Math.random() * 9 + 1),
      'KYC: Document tampering on ACC-' + Math.floor(Math.random() * 9000 + 1000),
    ];
    const e = events[Math.floor(Math.random() * events.length)];
    const time = new Date().toLocaleTimeString();
    const feed = document.getElementById('liveFeed');
    if (feed) feed.innerHTML = `<div class="feed-line"><span class="time">[${time}]</span><span class="warn">⬡ WS: ${e}</span></div>` + feed.innerHTML;

    // Randomly trigger full alert
    if (Math.random() > 0.92) {
      triggerAlert('WebSocket: ' + e);
    }
  }, 8000);
}

// ══════════════════════════════════════════════
// --- GEO RISK MAP (Leaflet.js) ---
// ══════════════════════════════════════════════

let leafletMap = null;
let leafletHeatLayer = null;
let leafletMarkers = [];
let leafletMarkersGroup = null;
let leafletMapReady = false;
let currentLayer = 'both';
let geoFeedTimer = null;

const geoData = [
  { lat: 19.0760, lng: 72.8777, city: 'Mumbai',      state: 'Maharashtra', risk: 'CRITICAL', score: 94, type: 'MULE NETWORK',   txns: 312, acc: 'ACC-9087-XK', intensity: 1.0  },
  { lat: 28.6139, lng: 77.2090, city: 'New Delhi',   state: 'Delhi',       risk: 'CRITICAL', score: 91, type: 'AML LAYERING',   txns: 287, acc: 'ACC-3312-BB', intensity: 0.95 },
  { lat: 22.5726, lng: 88.3639, city: 'Kolkata',     state: 'West Bengal', risk: 'HIGH',     score: 85, type: 'DEEPFAKE AUTH',  txns: 194, acc: 'ACC-7741-ZQ', intensity: 0.80 },
  { lat: 12.9716, lng: 77.5946, city: 'Bengaluru',   state: 'Karnataka',   risk: 'HIGH',     score: 82, type: 'VELOCITY SPIKE', txns: 220, acc: 'ACC-5503-PQ', intensity: 0.75 },
  { lat: 13.0827, lng: 80.2707, city: 'Chennai',     state: 'Tamil Nadu',  risk: 'HIGH',     score: 79, type: 'SMURFING',       txns: 175, acc: 'ACC-2280-KK', intensity: 0.70 },
  { lat: 17.3850, lng: 78.4867, city: 'Hyderabad',   state: 'Telangana',   risk: 'MEDIUM',   score: 71, type: 'STRUCTURING',    txns: 143, acc: 'ACC-4410-HY', intensity: 0.60 },
  { lat: 23.0225, lng: 72.5714, city: 'Ahmedabad',   state: 'Gujarat',     risk: 'MEDIUM',   score: 68, type: 'CIRCULAR TXN',   txns: 98,  acc: 'ACC-6620-AH', intensity: 0.55 },
  { lat: 18.5204, lng: 73.8567, city: 'Pune',        state: 'Maharashtra', risk: 'MEDIUM',   score: 65, type: 'IP SHARING',     txns: 112, acc: 'ACC-7730-PN', intensity: 0.50 },
  { lat: 26.8467, lng: 80.9462, city: 'Lucknow',     state: 'UP',          risk: 'MEDIUM',   score: 61, type: 'KYC FRAUD',      txns: 87,  acc: 'ACC-8840-LK', intensity: 0.45 },
  { lat: 26.9124, lng: 75.7873, city: 'Jaipur',      state: 'Rajasthan',   risk: 'MEDIUM',   score: 63, type: 'VELOCITY',       txns: 76,  acc: 'ACC-3380-JP', intensity: 0.48 },
  { lat: 21.1458, lng: 79.0882, city: 'Nagpur',      state: 'Maharashtra', risk: 'LOW',      score: 45, type: 'MONITORING',     txns: 54,  acc: 'ACC-9950-NG', intensity: 0.30 },
  { lat: 25.5941, lng: 85.1376, city: 'Patna',       state: 'Bihar',       risk: 'LOW',      score: 42, type: 'WATCH LIST',     txns: 41,  acc: 'ACC-1060-PT', intensity: 0.25 },
  { lat: 11.0168, lng: 76.9558, city: 'Coimbatore',  state: 'Tamil Nadu',  risk: 'LOW',      score: 38, type: 'WATCH LIST',     txns: 29,  acc: 'ACC-2170-CB', intensity: 0.20 },
  { lat: 30.7333, lng: 76.7794, city: 'Chandigarh',  state: 'Punjab',      risk: 'LOW',      score: 35, type: 'WATCH LIST',     txns: 22,  acc: 'ACC-4490-CH', intensity: 0.18 },
  { lat: 23.2599, lng: 77.4126, city: 'Bhopal',      state: 'MP',          risk: 'MEDIUM',   score: 59, type: 'STRUCTURING',    txns: 65,  acc: 'ACC-5500-BP', intensity: 0.42 },
  { lat: 22.7196, lng: 75.8577, city: 'Indore',      state: 'MP',          risk: 'MEDIUM',   score: 57, type: 'CIRCULAR TXN',   txns: 58,  acc: 'ACC-6611-IN', intensity: 0.40 },
  { lat: 15.2993, lng: 74.1240, city: 'Goa',         state: 'Goa',         risk: 'LOW',      score: 32, type: 'MONITORING',     txns: 18,  acc: 'ACC-7722-GA', intensity: 0.15 },
  { lat: 20.2961, lng: 85.8245, city: 'Bhubaneswar', state: 'Odisha',      risk: 'LOW',      score: 40, type: 'WATCH LIST',     txns: 33,  acc: 'ACC-8833-BH', intensity: 0.22 },
];

function riskColor(risk) {
  return { CRITICAL:'#ff2244', HIGH:'#ff9900', MEDIUM:'#00d4ff', LOW:'#00ff88' }[risk] || '#00ff88';
}

function makeIcon(risk) {
  const c = riskColor(risk);
  const pulse = (risk === 'CRITICAL')
    ? '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;border:2px solid ' + c + ';animation:geoPulse 1.4s ease-out infinite;opacity:0.6;"></div>'
    : '';
  const svg = '<div style="position:relative;width:28px;height:36px;cursor:pointer;">' + pulse +
    '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="36" viewBox="0 0 28 36">' +
    '<path d="M14 0C6.3 0 0 6.3 0 14C0 24.5 14 36 14 36C14 36 28 24.5 28 14C28 6.3 21.7 0 14 0Z" fill="' + c + '" opacity="0.88"/>' +
    '<circle cx="14" cy="14" r="6" fill="rgba(0,0,0,0.45)"/>' +
    '<circle cx="14" cy="14" r="3" fill="' + c + '"/>' +
    '</svg></div>';
  return L.divIcon({ className:'', html:svg, iconSize:[28,36], iconAnchor:[14,36], popupAnchor:[0,-36] });
}

function initLeafletMap() {
  if (leafletMapReady) { leafletMap.invalidateSize(); return; }
  if (typeof L === 'undefined') { setTimeout(initLeafletMap, 300); return; }

  leafletMap = L.map('leafletMap', { center:[20.5937,78.9629], zoom:5, zoomControl:true, attributionControl:false });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom:19, subdomains:'abcd' }).addTo(leafletMap);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', { maxZoom:19, subdomains:'abcd', opacity:0.4 }).addTo(leafletMap);

  const heatPts = geoData.map(d => [d.lat, d.lng, d.intensity]);
  leafletHeatLayer = L.heatLayer(heatPts, {
    radius:55, blur:35, maxZoom:8, max:1.0,
    gradient:{ 0.0:'#00d4ff', 0.3:'#0066ff', 0.55:'#ff9900', 0.8:'#ff2244', 1.0:'#ff0033' }
  }).addTo(leafletMap);

  leafletMarkersGroup = L.layerGroup().addTo(leafletMap);
  geoData.forEach(d => {
    const c = riskColor(d.risk);
    const marker = L.marker([d.lat, d.lng], { icon: makeIcon(d.risk) });
    marker.bindPopup(
      '<div style="background:#071525;color:#c8e8ff;padding:14px 16px;min-width:220px;font-family:monospace;font-size:11px;border:1px solid ' + c + '44;border-radius:3px;">' +
      '<div style="font-size:13px;font-weight:bold;color:#00d4ff;letter-spacing:2px;margin-bottom:10px;">📍 ' + d.city.toUpperCase() + '</div>' +
      '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #0d2240;"><span style="color:#4a7a9b">RISK LEVEL</span><span style="color:' + c + ';font-weight:bold">' + d.risk + '</span></div>' +
      '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #0d2240;"><span style="color:#4a7a9b">FRAUD SCORE</span><span style="color:' + c + '">' + d.score + '/100</span></div>' +
      '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #0d2240;"><span style="color:#4a7a9b">FRAUD TYPE</span><span style="color:#c8e8ff">' + d.type + '</span></div>' +
      '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #0d2240;"><span style="color:#4a7a9b">FLAGGED TXNs</span><span style="color:#00d4ff">' + d.txns + '</span></div>' +
      '<div style="display:flex;justify-content:space-between;padding:4px 0;"><span style="color:#4a7a9b">ACCOUNT</span><span style="color:#00d4ff">' + d.acc + '</span></div>' +
      '</div>',
      { className:'mulex-popup', maxWidth:260 }
    );
    marker.on('click', () => showGeoInfo(d));
    leafletMarkersGroup.addLayer(marker);
    leafletMarkers.push(marker);
  });

  const styleTag = document.createElement('style');
  styleTag.textContent = '.mulex-popup .leaflet-popup-content-wrapper{background:transparent!important;box-shadow:0 0 20px rgba(0,212,255,0.25)!important;border-radius:3px!important;padding:0!important;}.mulex-popup .leaflet-popup-content{margin:0!important;}.mulex-popup .leaflet-popup-tip{background:#071525!important;}.leaflet-container{font-family:"Share Tech Mono",monospace;}@keyframes geoPulse{0%{transform:translate(-50%,-50%) scale(1);opacity:0.7;}100%{transform:translate(-50%,-50%) scale(2.4);opacity:0;}}';
  document.head.appendChild(styleTag);

  setMapLayer('both');
  leafletMapReady = true;
  leafletMap.invalidateSize();
  startGeoFeed();
}

function showGeoInfo(d) {
  const riskClass = { CRITICAL:'danger', HIGH:'warn', MEDIUM:'', LOW:'safe' }[d.risk] || '';
  document.getElementById('geoInfoPanel').innerHTML =
    '<div class="geo-info-row"><span class="geo-info-key">CITY / STATE</span><span class="geo-info-val">' + d.city + ', ' + d.state + '</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">RISK LEVEL</span><span class="geo-info-val ' + riskClass + '">' + d.risk + '</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">FRAUD SCORE</span><span class="geo-info-val ' + riskClass + '">' + d.score + ' / 100</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">FRAUD TYPE</span><span class="geo-info-val">' + d.type + '</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">FLAGGED TRANSACTIONS</span><span class="geo-info-val">' + d.txns + '</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">PRIMARY ACCOUNT</span><span class="geo-info-val">' + d.acc + '</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">COORDINATES</span><span class="geo-info-val">' + d.lat.toFixed(4) + 'N, ' + d.lng.toFixed(4) + 'E</span></div>' +
    '<div class="geo-info-row"><span class="geo-info-key">LAST UPDATED</span><span class="geo-info-val">' + new Date().toLocaleTimeString('en-IN') + '</span></div>';
  if (leafletMap) leafletMap.flyTo([d.lat, d.lng], 8, { animate:true, duration:1.2 });
}

function setMapLayer(layer) {
  currentLayer = layer;
  ['Heatmap','Markers','Both'].forEach(id => {
    const el = document.getElementById('btn' + id);
    if (el) el.classList.remove('map-btn-active');
  });
  const activeBtn = { heatmap:'btnHeatmap', markers:'btnMarkers', both:'btnBoth' }[layer];
  if (document.getElementById(activeBtn)) document.getElementById(activeBtn).classList.add('map-btn-active');
  if (!leafletMap) return;
  if (layer === 'heatmap') {
    if (!leafletMap.hasLayer(leafletHeatLayer)) leafletMap.addLayer(leafletHeatLayer);
    if (leafletMap.hasLayer(leafletMarkersGroup)) leafletMap.removeLayer(leafletMarkersGroup);
  } else if (layer === 'markers') {
    if (leafletMap.hasLayer(leafletHeatLayer)) leafletMap.removeLayer(leafletHeatLayer);
    if (!leafletMap.hasLayer(leafletMarkersGroup)) leafletMap.addLayer(leafletMarkersGroup);
  } else {
    if (!leafletMap.hasLayer(leafletHeatLayer)) leafletMap.addLayer(leafletHeatLayer);
    if (!leafletMap.hasLayer(leafletMarkersGroup)) leafletMap.addLayer(leafletMarkersGroup);
  }
}

function triggerGeoAlert() {
  const critical = geoData.filter(d => d.risk === 'CRITICAL');
  const d = critical[Math.floor(Math.random() * critical.length)];
  triggerAlert('GEO ALERT: Critical fraud cluster in ' + d.city + ' - ' + d.txns + ' flagged transactions');
  showGeoInfo(d);
  if (leafletMap) leafletMap.flyTo([d.lat, d.lng], 9, { animate:true, duration:1.5 });
}

function startGeoFeed() {
  if (geoFeedTimer) return;
  const txnTypes = ['TRANSFER','WITHDRAWAL','LOGIN','PAYMENT','KYC UPLOAD'];
  const statuses = [{ t:'APPROVED', c:'safe' }, { t:'FLAGGED', c:'warn' }, { t:'BLOCKED', c:'danger' }];
  geoFeedTimer = setInterval(() => {
    const feed = document.getElementById('geoFeed');
    if (!feed) return;
    const d   = geoData[Math.floor(Math.random() * geoData.length)];
    const type = txnTypes[Math.floor(Math.random() * txnTypes.length)];
    const amt  = Math.floor(Math.random() * 200000 + 500).toLocaleString('en-IN');
    const st   = statuses[Math.floor(Math.random() * statuses.length)];
    const time = new Date().toLocaleTimeString('en-IN');
    const acc  = 'ACC-' + Math.floor(Math.random() * 9000 + 1000);
    feed.innerHTML = '<div class="feed-line"><span class="time">[' + time + ']</span><span class="' + st.c + '">📍 ' + d.city + ' · ' + type + ' Rs.' + amt + ' · ' + acc + ' → ' + st.t + '</span></div>' + feed.innerHTML;
    if (feed.children.length > 22) feed.lastChild.remove();
  }, 2000);
}
