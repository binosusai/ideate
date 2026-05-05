'use strict';

const crewData = {
  crewName: 'Ideate Investor Studio',
  crewTagline: 'A clear view of how specialized agents turn raw opportunities into decisions, prototypes, and launch-ready handoffs.',
  updateLabel: 'Refreshed for presentation',
  narrative:
    'This dashboard is intentionally static for the presentation layer: it shows the operating model, the orchestration hierarchy, and the quality signals behind the crew without exposing sprint-board mechanics.',
  stats: [
    { value: '07', label: 'specialist agents', note: 'from sourcing to delivery' },
    { value: '03', label: 'decision layers', note: 'director, operators, validators' },
    { value: '18h', label: 'prototype cycle', note: 'from intake to packaged POV' },
  ],
  flow: [
    {
      label: 'Intake',
      detail: 'Founder signal, market pull, or operator request enters the crew.',
    },
    {
      label: 'Synthesis',
      detail: 'Research and debate agents compress ambiguity into structured options.',
    },
    {
      label: 'Delivery',
      detail: 'Planning, build, review, and handoff produce a boardroom-ready package.',
    },
  ],
  hierarchy: {
    leader: {
      name: 'Crew Director',
      role: 'Orchestrates objectives, decides escalation, and approves the final storyline.',
      focus: 'Capital allocation signal, strategic framing, final coherence',
      tone: 'North-star judgement',
      badge: 'Command layer',
    },
    branches: [
      {
        name: 'Discovery Cell',
        function: 'Builds the first-principles view of the market and opportunity shape.',
        agents: [
          {
            name: 'Research Scout',
            type: 'Scout',
            status: 'Active now',
            summary: 'Surfaces market evidence, adjacent operators, and buyer pain.',
            outputs: ['Market map', 'Competitor compression', 'Demand cues'],
            handoff: 'Feeds Debate Strategist and Planning Architect',
          },
          {
            name: 'Pattern Librarian',
            type: 'Memory',
            status: 'Warm cache',
            summary: 'Connects prior ideas, transcripts, and historical experiments.',
            outputs: ['Pattern recalls', 'Failure analogs', 'Reusable playbooks'],
            handoff: 'Feeds the full crew with precedent',
          },
        ],
      },
      {
        name: 'Decision Cell',
        function: 'Converts evidence into conviction, tradeoffs, and action paths.',
        agents: [
          {
            name: 'Debate Strategist',
            type: 'Contrarian',
            status: 'In review loop',
            summary: 'Pressures the thesis, spots weak assumptions, and sharpens the bet.',
            outputs: ['Risk framing', 'Counter-positioning', 'Go / no-go argument'],
            handoff: 'Hands an investment-grade stance to the planner',
          },
          {
            name: 'Planning Architect',
            type: 'Planner',
            status: 'Ready',
            summary: 'Translates the chosen path into milestones, owners, and success gates.',
            outputs: ['Execution plan', 'Acceptance logic', 'Dependency map'],
            handoff: 'Feeds the build and review operators',
          },
        ],
      },
      {
        name: 'Delivery Cell',
        function: 'Packages the concept into a believable prototype and handoff artifact.',
        agents: [
          {
            name: 'Prototype Builder',
            type: 'Maker',
            status: 'Shipping',
            summary: 'Produces a concrete proof point that makes the opportunity feel real.',
            outputs: ['Working proof', 'Technical slice', 'Narrative demo'],
            handoff: 'Hands build evidence to review and packaging',
          },
          {
            name: 'Review Guardian',
            type: 'Validator',
            status: 'Watching',
            summary: 'Checks quality, credibility, and narrative consistency before reveal.',
            outputs: ['Quality flags', 'Credibility notes', 'Readiness verdict'],
            handoff: 'Approves investor-facing output',
          },
          {
            name: 'Handoff Narrator',
            type: 'Closer',
            status: 'Presenting',
            summary: 'Turns the output into a clean package for founders, operators, or investors.',
            outputs: ['Executive brief', 'Next-step memo', 'Decision packet'],
            handoff: 'Delivers the final artifact outward',
          },
        ],
      },
    ],
  },
  principles: [
    'Each agent owns a narrow decision surface and emits explicit handoffs.',
    'Validation is separated from generation so quality improves before persuasion begins.',
    'The hierarchy is designed to read like an operating company, not a toy chatbot swarm.',
  ],
  orgTree: {
    ceo: 'CEO · Sidd',
    md: 'Managing Director · Crew Operations',
    leaders: [
      {
        title: 'Engineering Managers',
        summary: 'Own reliability, delivery rhythm, and technical quality gates.',
      },
      {
        title: 'Product Managers',
        summary: 'Own market shaping, roadmap framing, and customer outcome signals.',
      },
      {
        title: 'Research Leads',
        summary: 'Own intelligence gathering, trend compression, and hypothesis strength.',
      },
      {
        title: 'Growth and Partnerships',
        summary: 'Own investor narrative, distribution channels, and strategic alliances.',
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

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
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

function orgLeaderCard(leader, index) {
  return `
    <article class="org-leader-card" style="animation-delay:${index * 140}ms">
      <h4>${escapeHtml(leader.title)}</h4>
      <p>${escapeHtml(leader.summary)}</p>
    </article>
  `;
}

function renderOrgTree() {
  orgTree.innerHTML = `
    <section class="org-tree-wrap" aria-label="Crew organizational hierarchy">
      <div class="org-tree-root">${escapeHtml(crewData.orgTree.ceo)}</div>
      <div class="org-tree-link" aria-hidden="true"></div>
      <div class="org-tree-md">${escapeHtml(crewData.orgTree.md)}</div>
      <div class="org-tree-branches" aria-hidden="true"></div>
      <div class="org-tree-grid">
        ${crewData.orgTree.leaders.map((leader, index) => orgLeaderCard(leader, index)).join('')}
      </div>
    </section>
  `;
}

function renderDashboard() {
  heroEyebrow.textContent = crewData.crewName;
  heroTitle.textContent = 'A visual operating model for your agent crew';
  heroText.textContent = crewData.crewTagline;
  heroNarrative.textContent = crewData.narrative;
  updatedLabel.textContent = crewData.updateLabel;

  summaryStats.innerHTML = crewData.stats.map(statCard).join('');
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
}

renderDashboard();
