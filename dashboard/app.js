'use strict';

const crewData = {
  crewName: 'Ideate Investor Studio',
  crewTagline: 'A clear view of how specialized agents turn raw opportunities into decisions, prototypes, and launch-ready handoffs.',
  updateLabel: 'CLI agent map',
  narrative:
    'This dashboard shows the predefined Ideate CLI agent structure: each idea moves through staged crews, coordinator synthesis, approval gates, and prototype handoff.',
  stats: [
    { value: '19', label: 'predefined agents', note: 'wired into CLI stages' },
    { value: '06', label: 'workflow stages', note: 'research through handoff' },
    { value: '01', label: 'coordinator loop', note: 'synthesis after each crew run' },
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
  heroTitle.textContent = 'A hierarchical map of the Ideate CLI agent crew';
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
