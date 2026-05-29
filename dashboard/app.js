'use strict';

const crewData = {
  crewName: 'Ideate Observatory',
  crewTagline: 'A quiet product studio where rough signals become blueprints, proposals, prototypes, and execution-ready handoffs.',
  updateLabel: 'Phase 1',
  narrative:
    'Draft the signal, shape the blueprint, then let the Ideate crew pressure-test the work before anything graduates to Minions.',
  stats: [
    { value: '19', label: 'predefined agents', note: 'wired into CLI stages' },
    { value: '06', label: 'workflow stages', note: 'research through handoff' },
    { value: '01', label: 'coordinator loop', note: 'synthesis after each crew run' },
  ],
  flow: [
    {
      label: 'Signal',
      detail: 'A one-line opportunity enters the observatory and becomes structured product intent.',
    },
    {
      label: 'Blueprint',
      detail: 'AI expands the idea into problem, users, MVP, risks, metrics, and open questions.',
    },
    {
      label: 'Expedition',
      detail: 'Research, debate, planning, proposal, POC, and review unlock the next phase.',
    },
  ],
  hierarchy: {
    leader: {
      name: 'Ideate CLI Coordinator',
      role: 'Loads the idea, runs the current stage crew, stores artifacts, and advances workflow status.',
      focus: 'Idea state, stage execution, artifact persistence',
      tone: 'Deterministic orchestration',
      badge: 'Command layer',
    },
    branches: [
      {
        name: 'Research Crew',
        function: 'Creates the research artifact and frames buyer, user, and feasibility signals.',
        agents: [
          {
            name: 'Market Researcher',
            type: 'Research',
            status: 'Stage agent',
            summary: 'Identifies the narrowest buyer segment, alternatives, willingness-to-pay signals, and entry wedge.',
            outputs: ['Buyer segment', 'Market signal', 'Entry wedge'],
            handoff: 'Feeds the debate crew with commercial context',
          },
          {
            name: 'User Researcher',
            type: 'Research',
            status: 'Stage agent',
            summary: 'Maps the user trigger, current workaround, sharpest pain, and minimum useful first-run workflow.',
            outputs: ['User trigger', 'Pain map', 'First workflow'],
            handoff: 'Feeds the debate crew with user context',
          },
          {
            name: 'Technical Scout',
            type: 'Research',
            status: 'Stage agent',
            summary: 'Assesses whether a credible MVP can be built quickly and what must be mocked.',
            outputs: ['MVP feasibility', 'Blockers', 'Mock strategy'],
            handoff: 'Feeds the debate crew with build constraints',
          },
        ],
      },
      {
        name: 'Debate Crew',
        function: 'Pressure-tests the idea before planning work begins.',
        agents: [
          {
            name: 'Advocate',
            type: 'Debate',
            status: 'Stage agent',
            summary: 'Argues why the idea deserves a POC now.',
            outputs: ['Why now', 'Upside case', 'Momentum signal'],
            handoff: 'Balances the skeptic and strategist positions',
          },
          {
            name: 'Skeptic',
            type: 'Debate',
            status: 'Stage agent',
            summary: 'Attacks assumptions, risk, and opportunity cost.',
            outputs: ['Risk framing', 'Weak assumptions', 'Kill criteria'],
            handoff: 'Keeps the plan honest',
          },
          {
            name: 'Builder',
            type: 'Debate',
            status: 'Stage agent',
            summary: 'Finds the smallest credible build path.',
            outputs: ['Build path', 'Scope limit', 'Demo slice'],
            handoff: 'Feeds planning with implementation shape',
          },
          {
            name: 'Strategist',
            type: 'Debate',
            status: 'Stage agent',
            summary: 'Ranks the idea against focus, money potential, and timing.',
            outputs: ['Priority read', 'Timing call', 'Go/no-go stance'],
            handoff: 'Feeds planning with decision posture',
          },
        ],
      },
      {
        name: 'Planning Crew',
        function: 'Converts the refined idea into MVP workflow, implementation shape, and acceptance checks.',
        agents: [
          {
            name: 'Product Planner',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Turns the refined idea into an MVP workflow.',
            outputs: ['MVP workflow', 'Milestones', 'Success gates'],
            handoff: 'Feeds the implementation plan',
          },
          {
            name: 'POC Coder',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines the smallest working local proof of concept.',
            outputs: ['Local proof', 'Runnable slice', 'Code path'],
            handoff: 'Guides POC generation',
          },
          {
            name: 'Frontend Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines the first usable interface for the POC.',
            outputs: ['UI shape', 'Primary screen', 'Interaction path'],
            handoff: 'Guides frontend implementation',
          },
          {
            name: 'Backend Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines API and local persistence needs for the POC.',
            outputs: ['API shape', 'Data flow', 'Runtime needs'],
            handoff: 'Guides backend implementation',
          },
          {
            name: 'Auth Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Chooses the auth posture for local POC and production handoff.',
            outputs: ['Auth posture', 'Secret handling', 'Access notes'],
            handoff: 'Guides security defaults',
          },
          {
            name: 'Database Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Chooses local and deployable database defaults.',
            outputs: ['Schema notes', 'Storage default', 'Migration posture'],
            handoff: 'Guides persistence implementation',
          },
          {
            name: 'Infra Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines deployment shape and infrastructure notes.',
            outputs: ['Infra shape', 'Deploy notes', 'Service choices'],
            handoff: 'Guides deployment packaging',
          },
          {
            name: 'DevOps Engineer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines automation, checks, and deployment notes.',
            outputs: ['CI checks', 'Automation', 'Runbook notes'],
            handoff: 'Guides repo and workflow setup',
          },
          {
            name: 'OpenSpec Writer',
            type: 'Planning',
            status: 'Stage agent',
            summary: 'Defines implementation requirements and acceptance checks.',
            outputs: ['Requirements', 'Acceptance checks', 'Task outline'],
            handoff: 'Feeds OpenSpec artifacts',
          },
        ],
      },
      {
        name: 'Delivery Gates',
        function: 'Turns approved plans into a POC, review loop, and handoff bundle.',
        agents: [
          {
            name: 'POC Builder',
            type: 'Delivery',
            status: 'Gate agent',
            summary: 'Writes or updates the runnable proof of concept.',
            outputs: ['POC files', 'Quality rubric', 'Score report'],
            handoff: 'Feeds review',
          },
          {
            name: 'Reviewer',
            type: 'Delivery',
            status: 'Gate agent',
            summary: 'Marks the POC as approved or requests revision feedback.',
            outputs: ['Review state', 'Revision feedback', 'Iteration count'],
            handoff: 'Feeds another loop or final handoff',
          },
          {
            name: 'Handoff Packager',
            type: 'Delivery',
            status: 'Gate agent',
            summary: 'Packages final context for the next engineering crew.',
            outputs: ['Handoff brief', 'POC location', 'Next-step context'],
            handoff: 'Delivers the final artifact bundle',
          },
        ],
      },
    ],
  },
  principles: [
    'Each agent owns a narrow decision surface and emits explicit handoffs.',
    'Validation is separated from generation so quality improves before persuasion begins.',
    'The hierarchy mirrors the Ideate CLI stages so operators can see where each artifact comes from.',
  ],
  agentTree: {
    name: 'idea CLI',
    meta: 'root command',
    children: [
      {
        name: 'Store + Coordinator',
        meta: 'loads idea, runs stage, writes artifacts',
        children: [
          {
            name: 'Research Crew',
            meta: 'crew-research artifact',
            children: [
              { name: 'Market Researcher', meta: 'buyer and market signal' },
              { name: 'User Researcher', meta: 'workflow and pain' },
              { name: 'Technical Scout', meta: 'MVP feasibility' },
            ],
          },
          {
            name: 'Debate Crew',
            meta: 'crew-debate artifact',
            children: [
              { name: 'Advocate', meta: 'why now' },
              { name: 'Skeptic', meta: 'risks and weak assumptions' },
              { name: 'Builder', meta: 'smallest credible build' },
              { name: 'Strategist', meta: 'priority and timing' },
            ],
          },
          {
            name: 'Planning Crew',
            meta: 'crew-planning artifact',
            children: [
              {
                name: 'Product Track',
                meta: 'workflow and acceptance',
                children: [
                  { name: 'Product Planner', meta: 'MVP workflow' },
                  { name: 'OpenSpec Writer', meta: 'requirements and checks' },
                ],
              },
              {
                name: 'Build Track',
                meta: 'implementation shape',
                children: [
                  { name: 'POC Coder', meta: 'local proof' },
                  { name: 'Frontend Engineer', meta: 'first usable UI' },
                  { name: 'Backend Engineer', meta: 'API shape' },
                  { name: 'Database Engineer', meta: 'persistence defaults' },
                ],
              },
              {
                name: 'Platform Track',
                meta: 'operational readiness',
                children: [
                  { name: 'Auth Engineer', meta: 'auth posture' },
                  { name: 'Infra Engineer', meta: 'deploy shape' },
                  { name: 'DevOps Engineer', meta: 'checks and automation' },
                ],
              },
            ],
          },
          {
            name: 'Delivery Gates',
            meta: 'prototype, review, handoff',
            children: [
              { name: 'POC Builder', meta: 'writes proof of concept' },
              { name: 'Reviewer', meta: 'approval or revision loop' },
              { name: 'Handoff Packager', meta: 'packages next crew context' },
            ],
          },
        ],
      },
    ],
  },
};

const summaryStats = document.getElementById('summary-stats');
const flowRail = document.getElementById('flow-rail');
const crewTree = document.getElementById('crew-tree');
const orgTree = document.getElementById('org-tree');
const principleList = document.getElementById('principle-list');
const heroEyebrow = document.getElementById('hero-eyebrow');
const heroTitle = document.getElementById('hero-title');
const heroText = document.getElementById('hero-text');
const heroNarrative = document.getElementById('hero-narrative');
const updatedLabel = document.getElementById('updated-label');
const boardStatus = document.getElementById('board-status');
const adminTokenInput = document.getElementById('admin-token');
const saveTokenButton = document.getElementById('save-token');
const clearTokenButton = document.getElementById('clear-token');
const ideaSearch = document.getElementById('idea-search');
const statusFilter = document.getElementById('status-filter');
const reviewFilter = document.getElementById('review-filter');
const refreshBoardButton = document.getElementById('refresh-board');
const ideaList = document.getElementById('idea-list');
const ideaDetail = document.getElementById('idea-detail');
const pendingReviewList = document.getElementById('pending-review-list');
const pendingCount = document.getElementById('pending-count');
const signalConsole = document.getElementById('signal-console');
const ideaSignal = document.getElementById('idea-signal');
const dossierState = document.getElementById('dossier-state');
const dossierTitle = document.getElementById('dossier-title');
const dossierGrid = document.getElementById('dossier-grid');
const missionTrack = document.getElementById('mission-track');
const blueprintEditor = document.getElementById('blueprint-editor');
const validateBlueprintButton = document.getElementById('validate-blueprint');
const createIdeaButton = document.getElementById('create-idea');
const blueprintStatus = document.getElementById('blueprint-status');
const capsuleReadiness = document.getElementById('capsule-readiness');

const boardState = {
  token: sessionStorage.getItem('ideate.dashboard.token') || '',
  ideas: [],
  pendingReviews: [],
  selectedIdeaId: null,
  selectedDetail: null,
  loading: false,
};

const defaultSignal = 'A local-first tool that turns contractor quotes into clean comparisons and negotiation notes.';

const dossierFields = [
  ['problem', 'Messy quotes are hard to compare because scope, exclusions, timing, and pricing are hidden in different formats.'],
  ['target user', 'Homeowners and small property managers choosing between local contractors.'],
  ['mvp', 'Paste three quotes, normalize line items, flag gaps, and generate negotiation questions.'],
  ['risk', 'Quote formats vary wildly, so the first POC should use guided extraction and editable fields.'],
];

const missionStages = [
  'Signal',
  'Blueprint',
  'Research',
  'Debate',
  'Proposal',
  'POC',
  'Minions',
];

let currentBlueprint = null;

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function signalTitle(text) {
  const cleaned = String(text || '').trim();
  if (!cleaned) return 'Untitled signal';
  const words = cleaned
    .replace(/[^\w\s-]/g, '')
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 7);
  if (!words.length) return 'Untitled signal';
  return words
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

function inferDossier(text) {
  const value = String(text || defaultSignal).trim();
  const lower = value.toLowerCase();
  const user = lower.includes('developer') || lower.includes('agent')
    ? 'Builders and technical operators who need repeatable agent-backed execution.'
    : lower.includes('invoice')
      ? 'Independent consultants and agencies managing client follow-up.'
      : lower.includes('contractor')
        ? 'Homeowners and property managers comparing high-stakes local services.'
        : 'Focused operators with a repeated workflow that needs a sharper first version.';

  const mvp = lower.includes('github') || lower.includes('oss')
    ? 'Ingest candidate work, rank the best opportunity, and produce an implementation-ready brief.'
    : lower.includes('proxy') || lower.includes('api')
      ? 'Create a local ledger, enforce no-fly zones, and export a portable handoff bundle.'
      : 'Capture the workflow, create one useful output, and keep every field editable before proposal generation.';

  return [
    ['problem', value],
    ['target user', user],
    ['mvp', mvp],
    ['risk', 'The POC must prove one meaningful before/after instead of presenting polished agent theater.'],
  ];
}

function fallbackBlueprint(text) {
  const fields = inferDossier(text);
  return {
    title: signalTitle(text),
    category: 'money',
    why: String(text || defaultSignal).trim(),
    details: {
      domain: fields.find(([label]) => label === 'target user')?.[1] || 'workflow productivity',
      problem: { statement: String(text || defaultSignal).trim() },
      target_users: ['builders', 'operators'],
      use_cases: [{ name: 'First useful workflow', flow: ['capture', 'normalize', 'review', 'run POC'] }],
      technology: {},
      constraints: ['local-first by default', 'no paid services required for the first POC'],
      mvp: { must_have: ['blueprint preview', 'runnable local POC', 'deployment path'] },
      acceptance_criteria: ['POC runs locally', 'deployment path is documented'],
      success_metrics: ['local run completion', 'POC acceptance'],
      monetization: { model: 'free first, paid execution upgrades later' },
      differentiation: ['runnable POC capsule instead of static AI text'],
      risks: ['over-polishing before proving the core workflow'],
      open_questions: ['Which integration is mandatory first?'],
      ecosystem: {
        frontend: 'static-html',
        backend: 'python-stdlib-api',
        database: 'sqlite-local',
        auth: 'none-local',
        deploy: {
          frontend: 'vercel-static',
          backend: 'aws-python-api',
          database: 'neon-postgres',
        },
        repo: 'github',
        project_management: 'github-projects',
      },
    },
  };
}

function blueprintToDossierFields(blueprint) {
  const details = blueprint && blueprint.details ? blueprint.details : {};
  const problem = details.problem && typeof details.problem === 'object'
    ? details.problem.statement || JSON.stringify(details.problem)
    : details.problem || blueprint.why || '';
  const users = Array.isArray(details.target_users) ? details.target_users.join(', ') : '';
  const mvp = details.mvp && typeof details.mvp === 'object'
    ? (details.mvp.must_have || details.mvp.scope || JSON.stringify(details.mvp))
    : details.mvp || '';
  const risk = Array.isArray(details.risks) ? details.risks[0] : details.risks || '';
  return [
    ['problem', problem],
    ['target user', users || 'Focused operators with repeated workflows.'],
    ['mvp', Array.isArray(mvp) ? mvp.join(', ') : String(mvp || 'One useful local workflow.')],
    ['risk', String(risk || 'The POC must prove a meaningful before/after.')],
  ];
}

function setBlueprintStatus(message, tone = 'neutral') {
  if (!blueprintStatus) return;
  blueprintStatus.textContent = message || '';
  blueprintStatus.dataset.tone = tone;
}

function setCurrentBlueprint(blueprint, source = 'draft') {
  currentBlueprint = blueprint;
  if (blueprintEditor) {
    blueprintEditor.value = JSON.stringify(blueprint, null, 2);
  }
  renderDossier(blueprintToDossierFields(blueprint), blueprint.title || 'Untitled signal');
  renderCapsuleReadiness(blueprint);
  setBlueprintStatus(`Blueprint ready (${source}).`, source.includes('fallback') ? 'warn' : 'success');
}

function parseEditorBlueprint() {
  if (!blueprintEditor) return currentBlueprint;
  try {
    return JSON.parse(blueprintEditor.value || '{}');
  } catch (error) {
    setBlueprintStatus(`Blueprint JSON is invalid: ${error.message}`, 'error');
    return null;
  }
}

function renderCapsuleReadiness(blueprint) {
  if (!capsuleReadiness) return;
  const ecosystem = blueprint && blueprint.details && blueprint.details.ecosystem ? blueprint.details.ecosystem : {};
  const deploy = ecosystem.deploy || {};
  const items = [
    ['Local runner', 'run-local.sh'],
    ['Smoke check', 'scripts/smoke_check.py'],
    ['Frontend', ecosystem.frontend || 'static-html'],
    ['Backend', ecosystem.backend || 'python-stdlib-api'],
    ['Deploy', [deploy.frontend, deploy.backend, deploy.database].filter(Boolean).join(' + ') || 'vercel + aws + neon'],
  ];
  capsuleReadiness.innerHTML = `
    <div class="capsule-title">POC capsule readiness</div>
    ${items.map(([label, value]) => `
      <div class="capsule-row">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
      </div>
    `).join('')}
  `;
}

function renderDossier(fields = dossierFields, title = 'Contractor Quote Comparison') {
  if (!dossierGrid || !missionTrack || !dossierTitle || !dossierState) return;
  dossierTitle.textContent = title;
  dossierState.textContent = 'Blueprint draft';
  dossierGrid.innerHTML = fields
    .map(([label, detail], index) => `
      <article class="dossier-cell" style="animation-delay:${index * 70}ms">
        <span>${escapeHtml(label)}</span>
        <p>${escapeHtml(detail)}</p>
      </article>
    `)
    .join('');
  missionTrack.innerHTML = missionStages
    .map((stage, index) => `
      <div class="mission-step${index < 2 ? ' is-lit' : ''}">
        <span>${String(index + 1).padStart(2, '0')}</span>
        <strong>${escapeHtml(stage)}</strong>
      </div>
    `)
    .join('');
}

function statCard(stat) {
  return `
    <article class="stat-card">
      <div class="stat-value">${escapeHtml(stat.value)}</div>
      <div class="stat-label">${escapeHtml(stat.label)}</div>
      <p class="stat-note">${escapeHtml(stat.note)}</p>
    </article>
  `;
}

function flowStep(step, index) {
  return `
    <article class="flow-step" style="animation-delay:${index * 90}ms">
      <div class="flow-index">0${index + 1}</div>
      <h3>${escapeHtml(step.label)}</h3>
      <p>${escapeHtml(step.detail)}</p>
    </article>
  `;
}

function agentCard(agent, index) {
  const outputs = agent.outputs
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join('');

  return `
    <article class="crew-agent-card" style="animation-delay:${index * 80}ms">
      <div class="crew-agent-head">
        <div>
          <p class="crew-agent-type">${escapeHtml(agent.type)}</p>
          <h4>${escapeHtml(agent.name)}</h4>
        </div>
        <span class="crew-agent-status">${escapeHtml(agent.status)}</span>
      </div>
      <p class="crew-agent-summary">${escapeHtml(agent.summary)}</p>
      <ul class="crew-agent-outputs">${outputs}</ul>
      <div class="crew-agent-handoff">${escapeHtml(agent.handoff)}</div>
    </article>
  `;
}

function branchCard(branch, index) {
  return `
    <section class="crew-branch" style="animation-delay:${index * 110}ms">
      <div class="crew-branch-head">
        <p class="crew-branch-kicker">Cell ${index + 1}</p>
        <h3>${escapeHtml(branch.name)}</h3>
        <p>${escapeHtml(branch.function)}</p>
      </div>
      <div class="crew-agent-grid">
        ${branch.agents.map((agent, agentIndex) => agentCard(agent, agentIndex)).join('')}
      </div>
    </section>
  `;
}

function agentTreeNode(node, depth = 0) {
  const children = Array.isArray(node.children) && node.children.length
    ? `<div class="agent-tree-children">${node.children.map((child) => agentTreeNode(child, depth + 1)).join('')}</div>`
    : '';

  return `
    <div class="agent-tree-node depth-${depth}">
      <div class="agent-tree-card">
        <strong>${escapeHtml(node.name)}</strong>
        <span>${escapeHtml(node.meta)}</span>
      </div>
      ${children}
    </div>
  `;
}

function renderOrgTree() {
  orgTree.innerHTML = `
    <section class="agent-tree-wrap" aria-label="Ideate CLI agent hierarchy">
      ${agentTreeNode(crewData.agentTree)}
    </section>
  `;
}

function renderDashboard() {
  heroEyebrow.textContent = crewData.crewName;
  heroTitle.textContent = 'Turn a rough idea into a serious blueprint';
  heroText.textContent = crewData.crewTagline;
  heroNarrative.textContent = crewData.narrative;
  updatedLabel.textContent = crewData.updateLabel;

  if (summaryStats) summaryStats.innerHTML = crewData.stats.map(statCard).join('');
  flowRail.innerHTML = crewData.flow.map(flowStep).join('');
  principleList.innerHTML = crewData.principles
    .map((principle) => `<li>${escapeHtml(principle)}</li>`)
    .join('');

  renderOrgTree();

  const leader = crewData.hierarchy.leader;
  crewTree.innerHTML = `
    <section class="crew-leader-card">
      <div class="crew-leader-topline">${escapeHtml(leader.badge)}</div>
      <h2>${escapeHtml(leader.name)}</h2>
      <p class="crew-leader-role">${escapeHtml(leader.role)}</p>
      <div class="crew-leader-meta">
        <div>
          <span>Primary focus</span>
          <strong>${escapeHtml(leader.focus)}</strong>
        </div>
        <div>
          <span>Operating tone</span>
          <strong>${escapeHtml(leader.tone)}</strong>
        </div>
      </div>
    </section>
    <div class="crew-tree-branches">
      ${crewData.hierarchy.branches.map(branchCard).join('')}
    </div>
  `;
  renderDossier();
  setCurrentBlueprint(fallbackBlueprint(defaultSignal), 'static draft');
}

renderDashboard();

function initSignalConsole() {
  if (!signalConsole || !ideaSignal) return;
  ideaSignal.value = defaultSignal;
  signalConsole.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = ideaSignal.value.trim() || defaultSignal;
    setBlueprintStatus('Generating blueprint...', 'neutral');
    try {
      const payload = await apiFetch('/api/blueprints/generate', {
        method: 'POST',
        body: JSON.stringify({ signal: text }),
      });
      setCurrentBlueprint(payload.blueprint, payload.source || 'api');
    } catch (error) {
      setCurrentBlueprint(fallbackBlueprint(text), 'static fallback');
      setBlueprintStatus(`${boardErrorMessage(error)} Using local draft preview.`, 'warn');
    }
  });

  if (validateBlueprintButton) {
    validateBlueprintButton.addEventListener('click', async () => {
      const blueprint = parseEditorBlueprint();
      if (!blueprint) return;
      setBlueprintStatus('Validating blueprint...', 'neutral');
      try {
        const payload = await apiFetch('/api/blueprints/validate', {
          method: 'POST',
          body: JSON.stringify({ blueprint }),
        });
        setCurrentBlueprint(payload.blueprint, 'validated');
      } catch (error) {
        setBlueprintStatus(boardErrorMessage(error), 'error');
      }
    });
  }

  if (createIdeaButton) {
    createIdeaButton.addEventListener('click', async () => {
      const blueprint = parseEditorBlueprint();
      if (!blueprint) return;
      setBlueprintStatus('Creating idea...', 'neutral');
      try {
        const payload = await apiFetch('/api/ideas/create', {
          method: 'POST',
          body: JSON.stringify({ blueprint }),
        });
        setBlueprintStatus(`Idea created: ${payload.idea.title}`, 'success');
        await loadBoard({ selectFirst: true });
      } catch (error) {
        setBlueprintStatus(boardErrorMessage(error), 'error');
      }
    });
  }
}

initSignalConsole();

function statusBadge(value) {
  const label = String(value || 'new').replace(/_/g, ' ');
  return `<span class="status-badge status-${escapeHtml(value || 'new')}">${escapeHtml(label)}</span>`;
}

function setBoardStatus(message, tone = 'neutral') {
  if (!boardStatus) return;
  boardStatus.textContent = message || '';
  boardStatus.dataset.tone = tone;
}

function boardErrorMessage(error) {
  if (error && error.code === 'auth_not_configured') {
    return 'Server is missing IDEATE_DASHBOARD_ADMIN_TOKEN. Export it in the same terminal that starts the dashboard, then restart npm run start:vercel.';
  }
  if (error && error.code === 'database_not_configured') {
    return 'Server is missing DATABASE_URL. Export it in the same terminal that starts the dashboard, then restart npm run start:vercel.';
  }
  if (error && error.code === 'github_repo_not_configured') {
    return 'GitHub repository is not configured. Set IDEATE_TASKS_REPO or GITHUB_REPOSITORY for the dashboard server.';
  }
  if (error && error.code === 'github_token_not_configured') {
    return 'GitHub token is not configured. Set GH_TOKEN or GITHUB_TOKEN for the dashboard server.';
  }
  if (error && error.code === 'github_dispatch_failed') {
    return error.message;
  }
  if (error && error.status === 401) {
    const path = error.path ? ` for ${error.path}` : '';
    return `Dashboard authorization required${path}. Paste the same admin token that the server was started with.`;
  }
  return error && error.message ? error.message : 'Dashboard request failed.';
}

function authHeaders() {
  return boardState.token ? { Authorization: `Bearer ${boardState.token}` } : {};
}

async function apiFetch(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    throw new Error(`Expected JSON from ${path}, but the dev server returned ${contentType || 'an unknown content type'}.`);
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.error || `Request failed with ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.code = payload.code;
    error.path = path;
    throw error;
  }
  return payload;
}

function ideaTitle(idea) {
  return idea && idea.title ? idea.title : `Idea ${idea && idea.id ? idea.id : ''}`;
}

function renderIdeaRows() {
  if (!ideaList) return;
  if (!boardState.ideas.length) {
    ideaList.innerHTML = `
      <tr>
        <td colspan="4" class="empty-cell">No ideas match the current board filters.</td>
      </tr>
    `;
    return;
  }

  ideaList.innerHTML = boardState.ideas
    .map((idea) => {
      const selected = Number(idea.id) === Number(boardState.selectedIdeaId) ? ' is-selected' : '';
      return `
        <tr class="idea-row${selected}" data-idea-id="${escapeHtml(idea.id)}" tabindex="0">
          <td>
            <strong>${escapeHtml(ideaTitle(idea))}</strong>
            <span>${escapeHtml(idea.domain || idea.slug || '')}</span>
          </td>
          <td>${statusBadge(idea.status)}</td>
          <td>${statusBadge(idea.review_status)}</td>
          <td>${escapeHtml(Math.round(Number(idea.score || 0)))}</td>
        </tr>
      `;
    })
    .join('');
}

function artifactPreview(artifacts) {
  const normalizedArtifacts = withProposalArtifact(boardState.selectedDetail && boardState.selectedDetail.idea, artifacts);
  const artifactOrder = [
    'proposal',
    'openspec_proposal',
    'plan',
    'research',
    'debate',
    'openspec_design',
    'openspec_tasks',
    'openspec_spec',
    'poc_report',
    'poc_quality_score',
    'poc_improvement_loop',
    'handoff',
  ];
  const entries = Object.entries(normalizedArtifacts || {}).sort(([left], [right]) => {
    const leftIndex = artifactOrder.includes(left) ? artifactOrder.indexOf(left) : artifactOrder.length;
    const rightIndex = artifactOrder.includes(right) ? artifactOrder.indexOf(right) : artifactOrder.length;
    return leftIndex - rightIndex || left.localeCompare(right);
  });
  if (!entries.length) {
    return '<p class="detail-muted">No artifacts stored for this idea yet.</p>';
  }
  return entries
    .map(([kind, artifact]) => {
      const text = String(artifact.content || '');
      const preview = text.slice(0, 220).replace(/\s+/g, ' ').trim();
      const label = kind === 'openspec_proposal' ? 'proposal' : kind.replace(/_/g, ' ');
      const open = kind === 'proposal' || kind === 'openspec_proposal' ? ' open' : '';
      return `
        <details class="artifact-preview"${open}>
          <summary>
            <span>${escapeHtml(label)}</span>
            <small>${escapeHtml(preview)}${text.length > 220 ? '...' : ''}</small>
          </summary>
          <pre>${escapeHtml(text)}</pre>
        </details>
      `;
    })
    .join('');
}

function artifactContent(artifacts, kind) {
  return artifacts && artifacts[kind] && artifacts[kind].content ? String(artifacts[kind].content) : '';
}

function withProposalArtifact(idea, artifacts) {
  const out = { ...(artifacts || {}) };
  if (out.proposal || out.openspec_proposal) return out;

  const research = artifactContent(out, 'research');
  const debate = artifactContent(out, 'debate');
  const plan = artifactContent(out, 'plan');
  if (!research && !debate && !plan) return out;

  const title = idea && idea.title ? idea.title : 'Selected idea';
  const lines = [
    `# Proposal: ${title}`,
    '',
    '## Approval Question',
    'Approve this proposal to build the first POC for the idea.',
    '',
    '## Proposal Summary',
    plan || 'No implementation plan artifact is available yet.',
    research ? `\n## Research\n\n${research}` : '',
    debate ? `\n## Debate\n\n${debate}` : '',
  ].filter(Boolean);

  out.proposal = {
    content: lines.join('\n'),
    created_at: idea && idea.updated_at ? idea.updated_at : '',
  };
  return out;
}

function decisionsPreview(decisions) {
  if (!Array.isArray(decisions) || !decisions.length) {
    return '<p class="detail-muted">No dashboard decisions recorded.</p>';
  }
  return decisions
    .slice(0, 5)
    .map((decision) => `
      <li>
        <strong>${escapeHtml(decision.decision)}</strong>
        <span>${escapeHtml(decision.rationale || '')}</span>
      </li>
    `)
    .join('');
}

function renderDetail() {
  if (!ideaDetail) return;
  const detail = boardState.selectedDetail;
  if (!detail || !detail.idea) {
    ideaDetail.innerHTML = `
      <div class="detail-empty">
        <p class="section-kicker">Detail</p>
        <h4>Select an idea</h4>
      </div>
    `;
    return;
  }

  const idea = detail.idea;
  const canStartPoc = idea.status === 'planned' || idea.status === 'approved';
  const canReviewPoc = idea.review_status === 'pending_review' || (idea.status === 'poc' && idea.review_status === 'new');
  const startPocLabel = idea.status === 'planned' ? 'Approve proposal & build POC' : 'Build POC';

  ideaDetail.innerHTML = `
    <div class="detail-top">
      <div>
        <p class="section-kicker">Idea detail</p>
        <h4>${escapeHtml(idea.title)}</h4>
      </div>
      <div class="detail-badges">
        ${statusBadge(idea.status)}
        ${statusBadge(idea.review_status)}
      </div>
    </div>
    <div class="detail-meta">
      <span>Score ${escapeHtml(Math.round(Number(idea.score || 0)))}</span>
      <span>${escapeHtml(idea.category || '')}</span>
      <span>${escapeHtml(idea.slug || '')}</span>
    </div>
    <div class="decision-controls">
      <textarea id="review-feedback" class="feedback-input" rows="4" placeholder="Feedback or rationale">${escapeHtml(idea.review_feedback || '')}</textarea>
      <div class="decision-actions">
        <button class="icon-action primary" type="button" data-action="approve-plan" ${canStartPoc ? '' : 'disabled'}>${startPocLabel}</button>
        <button class="icon-action primary" type="button" data-action="approve-poc" ${canReviewPoc ? '' : 'disabled'}>Approve POC</button>
        <button class="icon-action danger" type="button" data-action="revise-poc" ${canReviewPoc ? '' : 'disabled'}>Request revision</button>
      </div>
    </div>
    <div class="detail-section">
      <h5>Proposal and artifacts</h5>
      <div class="artifact-list">${artifactPreview(detail.artifacts)}</div>
    </div>
    <div class="detail-section">
      <h5>Decisions</h5>
      <ul class="decision-list">${decisionsPreview(detail.decisions)}</ul>
    </div>
  `;
}

function renderPendingReviews() {
  if (!pendingReviewList || !pendingCount) return;
  const plannedApprovals = boardState.ideas.filter((idea) => idea.status === 'planned');
  const staleReviews = boardState.ideas.filter((idea) => idea.status === 'poc' && idea.review_status === 'new');
  const waitingCount = plannedApprovals.length + boardState.pendingReviews.length + staleReviews.length;
  pendingCount.textContent = `${waitingCount} waiting`;
  if (!waitingCount) {
    pendingReviewList.innerHTML = '<p class="detail-muted">No planned ideas or POCs are waiting for approval.</p>';
    return;
  }

  const planItems = plannedApprovals
    .map((idea) => `
      <button class="pending-item" type="button" data-idea-id="${escapeHtml(idea.id)}">
        <small>Awaiting POC approval</small>
        <strong>${escapeHtml(idea.title)}</strong>
        <span>${escapeHtml(idea.slug || '')}</span>
      </button>
    `)
    .join('');

  const reviewItems = boardState.pendingReviews
    .map((review) => `
      <button class="pending-item" type="button" data-idea-id="${escapeHtml(review.idea.id)}">
        <small>POC awaiting review</small>
        <strong>${escapeHtml(review.idea.title)}</strong>
        <span>${escapeHtml(review.idea.slug || '')}</span>
      </button>
    `)
    .join('');

  const staleReviewItems = staleReviews
    .map((idea) => `
      <button class="pending-item" type="button" data-idea-id="${escapeHtml(idea.id)}">
        <small>POC awaiting review</small>
        <strong>${escapeHtml(idea.title)}</strong>
        <span>${escapeHtml(idea.slug || '')}</span>
      </button>
    `)
    .join('');

  pendingReviewList.innerHTML = planItems + reviewItems + staleReviewItems;
}

function boardQuery() {
  const params = new URLSearchParams();
  if (statusFilter && statusFilter.value) params.set('status', statusFilter.value);
  if (reviewFilter && reviewFilter.value) params.set('review_status', reviewFilter.value);
  if (ideaSearch && ideaSearch.value.trim()) params.set('q', ideaSearch.value.trim());
  params.set('limit', '75');
  return params.toString();
}

async function loadIdeaDetail(ideaId) {
  boardState.selectedIdeaId = Number(ideaId);
  renderIdeaRows();
  const detail = await apiFetch(`/api/ideas/${ideaId}`);
  boardState.selectedDetail = detail;
  renderDetail();
}

async function loadBoard({ selectFirst = false } = {}) {
  if (!ideaList) return;
  boardState.loading = true;
  setBoardStatus('Loading board...', 'neutral');
  try {
    const [ideasPayload, pendingPayload] = await Promise.all([
      apiFetch(`/api/ideas?${boardQuery()}`),
      apiFetch('/api/reviews/pending'),
    ]);
    boardState.ideas = ideasPayload.ideas || [];
    boardState.pendingReviews = pendingPayload.reviews || [];
    renderIdeaRows();
    renderPendingReviews();

    const nextIdeaId = selectFirst && boardState.ideas[0] ? boardState.ideas[0].id : boardState.selectedIdeaId;
    if (nextIdeaId) {
      await loadIdeaDetail(nextIdeaId);
    } else {
      boardState.selectedDetail = null;
      renderDetail();
    }
    setBoardStatus(`Board synced with Neon: ${boardState.ideas.length} ideas, ${boardState.pendingReviews.length} pending reviews.`, 'success');
  } catch (error) {
    renderIdeaRows();
    renderPendingReviews();
    renderDetail();
    const tone = error.status === 401 || error.status === 503 ? 'warn' : 'error';
    setBoardStatus(boardErrorMessage(error), tone);
  } finally {
    boardState.loading = false;
  }
}

async function mutateSelected(action) {
  const detail = boardState.selectedDetail;
  if (!detail || !detail.idea) return;
  const ideaId = detail.idea.id;
  const feedbackInput = document.getElementById('review-feedback');
  const feedback = feedbackInput ? feedbackInput.value.trim() : '';

  setBoardStatus('Dispatching workflow...', 'neutral');
  try {
    if (action === 'approve-plan') {
      await apiFetch(`/api/ideas/${ideaId}/start-poc`, {
        method: 'POST',
        body: JSON.stringify({ rationale: feedback }),
      });
    }
    if (action === 'approve-poc') {
      await apiFetch(`/api/ideas/${ideaId}/dispatch-review`, {
        method: 'POST',
        body: JSON.stringify({ decision: 'approve', feedback }),
      });
    }
    if (action === 'revise-poc') {
      await apiFetch(`/api/ideas/${ideaId}/dispatch-review`, {
        method: 'POST',
        body: JSON.stringify({ decision: 'revise', feedback }),
      });
    }
    await loadBoard();
    await loadIdeaDetail(ideaId);
    const successMessage = action === 'approve-plan'
      ? 'Proposal approved. POC workflow dispatched.'
      : 'POC review workflow dispatched.';
    setBoardStatus(successMessage, 'success');
  } catch (error) {
    setBoardStatus(boardErrorMessage(error), error.status === 409 ? 'warn' : 'error');
  }
}

function initApprovalBoard() {
  if (!ideaList) return;
  adminTokenInput.value = boardState.token;
  renderDetail();

  saveTokenButton.addEventListener('click', () => {
    boardState.token = adminTokenInput.value.trim();
    sessionStorage.setItem('ideate.dashboard.token', boardState.token);
    loadBoard({ selectFirst: true });
  });

  clearTokenButton.addEventListener('click', () => {
    boardState.token = '';
    adminTokenInput.value = '';
    sessionStorage.removeItem('ideate.dashboard.token');
    setBoardStatus('Dashboard token cleared.', 'warn');
  });

  refreshBoardButton.addEventListener('click', () => loadBoard({ selectFirst: !boardState.selectedIdeaId }));
  [ideaSearch, statusFilter, reviewFilter].forEach((control) => {
    control.addEventListener('change', () => loadBoard({ selectFirst: true }));
  });
  ideaSearch.addEventListener('input', () => {
    window.clearTimeout(ideaSearch._boardTimer);
    ideaSearch._boardTimer = window.setTimeout(() => loadBoard({ selectFirst: true }), 350);
  });

  ideaList.addEventListener('click', (event) => {
    const row = event.target.closest('[data-idea-id]');
    if (row) loadIdeaDetail(row.dataset.ideaId).catch((error) => setBoardStatus(error.message, 'error'));
  });
  ideaList.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    const row = event.target.closest('[data-idea-id]');
    if (row) {
      event.preventDefault();
      loadIdeaDetail(row.dataset.ideaId).catch((error) => setBoardStatus(error.message, 'error'));
    }
  });

  pendingReviewList.addEventListener('click', (event) => {
    const item = event.target.closest('[data-idea-id]');
    if (item) loadIdeaDetail(item.dataset.ideaId).catch((error) => setBoardStatus(error.message, 'error'));
  });

  ideaDetail.addEventListener('click', (event) => {
    const button = event.target.closest('[data-action]');
    if (button && !button.disabled) mutateSelected(button.dataset.action);
  });

  loadBoard({ selectFirst: true });
}

initApprovalBoard();
