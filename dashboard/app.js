/* global */
'use strict';

// ─── Constants ─────────────────────────────────────────────────────────────

const CONFIG_KEY = 'ideate_dashboard_v1';
const POLL_INTERVAL = 30_000; // 30 s

const STAGES = [
  { key: 'research', label: 'Research',  icon: '◎' },
  { key: 'debate',   label: 'Debate',    icon: '◈' },
  { key: 'planning', label: 'Planning',  icon: '◧' },
  { key: 'poc',      label: 'POC Build', icon: '◉' },
  { key: 'review',   label: 'Review',    icon: '◐' },
  { key: 'handoff',  label: 'Handoff',   icon: '◇' },
];

const STATUS_LABEL = {
  todo:        'waiting',
  in_progress: 'working',
  done:        'done',
};

// ─── State ──────────────────────────────────────────────────────────────────

let config      = null;
let pollTimer   = null;
let prevData    = null; // for change detection

// ─── DOM refs ───────────────────────────────────────────────────────────────

const overlay      = document.getElementById('overlay');
const liveIndicator= document.getElementById('live-indicator');
const liveLabel    = document.getElementById('live-label');
const lastUpdated  = document.getElementById('last-updated');
const pipelineTrack= document.getElementById('pipeline-track');
const configForm   = document.getElementById('config-form');
const repoInput    = document.getElementById('repo-input');
const tokenInput   = document.getElementById('token-input');
const ideaInput    = document.getElementById('idea-input');
const settingsBtn  = document.getElementById('settings-btn');

// ─── Config persistence ──────────────────────────────────────────────────────

function loadConfig() {
  try {
    const raw = localStorage.getItem(CONFIG_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function saveConfig(c) {
  localStorage.setItem(CONFIG_KEY, JSON.stringify(c));
}

// ─── Overlay ─────────────────────────────────────────────────────────────────

function showOverlay() {
  overlay.classList.add('visible');
}

function hideOverlay() {
  overlay.classList.remove('visible');
}

// ─── GitHub fetch ────────────────────────────────────────────────────────────

async function fetchIssues({ repo, token, ideaId }) {
  const headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const url = `https://api.github.com/repos/${repo}/issues?labels=ideate-task&state=all&per_page=100`;
  const res = await fetch(url, { headers });

  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.message || `GitHub ${res.status}`);
  }

  const issues = await res.json();
  if (!Array.isArray(issues)) throw new Error('Unexpected GitHub response.');

  // Client-side filter by idea ID
  if (ideaId) {
    return issues.filter(issue =>
      issue.labels.some(l => l.name === `idea:${ideaId}`)
    );
  }
  return issues;
}

// ─── Parse ───────────────────────────────────────────────────────────────────

function parseIssue(issue) {
  const labelNames = issue.labels.map(l => l.name);

  const stageLabel = labelNames.find(l => l.startsWith('stage:'));
  const stage = stageLabel ? stageLabel.slice('stage:'.length) : 'unknown';

  let status = 'todo';
  if (labelNames.includes('task:in-progress')) status = 'in_progress';
  else if (labelNames.includes('task:done'))    status = 'done';

  // Title format: "Idea 1 | Research | Market Researcher"
  const parts = issue.title.split(' | ');
  const agentName = parts.length >= 3 ? parts[2].trim() : issue.title;

  const ideaLabel = labelNames.find(l => l.startsWith('idea:'));
  const ideaId = ideaLabel ? ideaLabel.slice('idea:'.length) : '?';

  return { stage, status, agentName, ideaId, url: issue.html_url, id: issue.id };
}

function groupByStage(parsedIssues) {
  const grouped = {};
  for (const s of STAGES) grouped[s.key] = [];
  for (const issue of parsedIssues) {
    if (grouped[issue.stage] !== undefined) {
      grouped[issue.stage].push(issue);
    }
  }
  return grouped;
}

// ─── Render ───────────────────────────────────────────────────────────────────

function agentCardHTML(agent, delay) {
  const statusLabel = STATUS_LABEL[agent.status] || agent.status;
  return `
    <a
      class="agent-card ${agent.status}"
      href="${agent.url}"
      target="_blank"
      rel="noopener noreferrer"
      style="animation-delay: ${delay}ms"
    >
      <span class="agent-name">${escapeHTML(agent.agentName)}</span>
      <span class="agent-status-chip">${statusLabel}</span>
    </a>
  `;
}

function stageColHTML(stage, agents, colDelay) {
  const active = agents.filter(a => a.status === 'in_progress').length;
  const done   = agents.filter(a => a.status === 'done').length;

  const activeBadge = active > 0
    ? `<span class="stage-active-badge">${active} active</span>`
    : '';

  const agentCards = agents.length === 0
    ? `<div class="stage-empty">no agents yet</div>`
    : agents
        .map((a, i) => agentCardHTML(a, i * 40))
        .join('');

  return `
    <div class="stage-col" style="animation-delay: ${colDelay}ms">
      <div class="stage-header">
        <span class="stage-icon">${stage.icon}</span>
        <span class="stage-name">${stage.label}</span>
        ${activeBadge}
      </div>
      <div class="agent-list">${agentCards}</div>
      <div class="stage-footer">
        <span class="stage-progress">${done}/${agents.length}</span>
      </div>
    </div>
  `;
}

function renderPipeline(grouped) {
  // Stringify for change detection — skip re-render if nothing changed
  const snapshot = JSON.stringify(grouped);
  if (snapshot === prevData) return;
  prevData = snapshot;

  pipelineTrack.innerHTML = STAGES
    .map((s, i) => stageColHTML(s, grouped[s.key] || [], i * 60))
    .join('');
}

function renderEmpty() {
  pipelineTrack.innerHTML = STAGES
    .map((s, i) => stageColHTML(s, [], i * 60))
    .join('');
}

// ─── Polling ──────────────────────────────────────────────────────────────────

function setLoading() {
  liveIndicator.classList.add('loading');
  liveIndicator.classList.remove('error');
  liveLabel.textContent = 'syncing';
}

function setLive() {
  liveIndicator.classList.remove('loading', 'error');
  liveLabel.textContent = 'live';
  const now = new Date();
  lastUpdated.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}

function setError(msg) {
  liveIndicator.classList.remove('loading');
  liveIndicator.classList.add('error');
  liveLabel.textContent = 'error';
  lastUpdated.textContent = msg.slice(0, 40);
}

async function refresh() {
  if (!config) return;
  setLoading();
  try {
    const issues = await fetchIssues(config);
    const parsed = issues.map(parseIssue);
    const grouped = groupByStage(parsed);
    renderPipeline(grouped);
    setLive();
  } catch (err) {
    setError(err.message || 'connection failed');
    console.error('[ideate dashboard]', err);
  }
}

function startPolling() {
  stopPolling();
  refresh();
  pollTimer = setInterval(refresh, POLL_INTERVAL);
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

// ─── Events ───────────────────────────────────────────────────────────────────

configForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const repo   = repoInput.value.trim();
  const token  = tokenInput.value.trim() || null;
  const ideaId = ideaInput.value.trim() || null;

  if (!repo || !repo.includes('/')) {
    repoInput.focus();
    repoInput.style.borderColor = '#ef4444';
    setTimeout(() => repoInput.style.borderColor = '', 1200);
    return;
  }

  config = { repo, token, ideaId };
  saveConfig(config);
  prevData = null; // force re-render after config change
  hideOverlay();
  startPolling();
});

settingsBtn.addEventListener('click', () => {
  if (config) {
    repoInput.value  = config.repo  || '';
    ideaInput.value  = config.ideaId || '';
    // Don't pre-fill token for security
  }
  showOverlay();
});

// Close overlay on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && overlay.classList.contains('visible') && config) {
    hideOverlay();
  }
});

// ─── Utils ───────────────────────────────────────────────────────────────────

function escapeHTML(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function pad(n) { return String(n).padStart(2, '0'); }

// ─── Boot ─────────────────────────────────────────────────────────────────────

config = loadConfig();
if (config) {
  repoInput.value  = config.repo  || '';
  ideaInput.value  = config.ideaId || '';
  renderEmpty();
  startPolling();
} else {
  renderEmpty();
  showOverlay();
}
