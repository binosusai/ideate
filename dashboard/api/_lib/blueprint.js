'use strict';

const { HttpError } = require('./http');

const CATEGORIES = new Set(['money', 'personal']);

function slugify(value) {
  const slug = String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 72)
    .replace(/-+$/g, '');
  return slug || 'idea';
}

function normalizeCategory(value) {
  const raw = String(value || 'money').trim().toLowerCase();
  return CATEGORIES.has(raw) ? raw : 'money';
}

function asList(value) {
  if (Array.isArray(value)) return value.map((item) => String(item || '').trim()).filter(Boolean);
  if (value === undefined || value === null || value === '') return [];
  return [String(value).trim()].filter(Boolean);
}

function normalizeDetails(details = {}) {
  const source = details && typeof details === 'object' && !Array.isArray(details) ? details : { notes: details };
  return {
    domain: String(source.domain || '').trim(),
    problem: source.problem || { statement: '' },
    target_users: asList(source.target_users || source.users),
    use_cases: Array.isArray(source.use_cases) ? source.use_cases : [],
    technology: source.technology && typeof source.technology === 'object' ? source.technology : {},
    constraints: asList(source.constraints),
    mvp: source.mvp && typeof source.mvp === 'object' ? source.mvp : { must_have: asList(source.mvp) },
    acceptance_criteria: asList(source.acceptance_criteria),
    success_metrics: source.success_metrics || [],
    monetization: source.monetization && typeof source.monetization === 'object' ? source.monetization : {},
    differentiation: asList(source.differentiation),
    risks: asList(source.risks),
    open_questions: asList(source.open_questions),
    ecosystem: source.ecosystem && typeof source.ecosystem === 'object' ? source.ecosystem : defaultEcosystem(),
    ...Object.fromEntries(
      Object.entries(source).filter(([key]) => ![
        'domain',
        'problem',
        'target_users',
        'users',
        'use_cases',
        'technology',
        'constraints',
        'mvp',
        'acceptance_criteria',
        'success_metrics',
        'monetization',
        'differentiation',
        'risks',
        'open_questions',
        'ecosystem',
      ].includes(key)),
    ),
  };
}

function defaultEcosystem() {
  return {
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
  };
}

function normalizeBlueprint(input) {
  const payload = input && typeof input === 'object' ? input : {};
  const title = String(payload.title || '').trim();
  if (!title) {
    throw new HttpError(422, 'Blueprint requires a non-empty title.', 'invalid_blueprint');
  }
  const why = String(payload.why || '').trim();
  if (!why) {
    throw new HttpError(422, 'Blueprint requires a non-empty why.', 'invalid_blueprint');
  }

  return {
    title,
    category: normalizeCategory(payload.category),
    why,
    details: normalizeDetails(payload.details || {}),
  };
}

function deterministicBlueprint(signal) {
  const text = String(signal || '').trim();
  if (!text) {
    throw new HttpError(422, 'Idea text is required.', 'missing_signal');
  }
  const lower = text.toLowerCase();
  const title = text
    .replace(/[^\w\s-]/g, '')
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 8)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ') || 'New Product Idea';
  const domain = lower.includes('github') || lower.includes('oss')
    ? 'open-source contribution workflow'
    : lower.includes('invoice')
      ? 'invoice follow-up automation'
      : lower.includes('proxy') || lower.includes('api')
        ? 'developer tools and AI infrastructure'
        : 'workflow productivity';
  const targetUsers = lower.includes('contractor')
    ? ['homeowners', 'property managers']
    : lower.includes('developer') || lower.includes('github') || lower.includes('api')
      ? ['builders', 'technical operators']
      : ['solo founders', 'operators with repeated workflows'];
  return normalizeBlueprint({
    title,
    category: lower.includes('personal') ? 'personal' : 'money',
    why: text,
    details: {
      domain,
      problem: {
        statement: text,
      },
      target_users: targetUsers,
      use_cases: [
        {
          name: 'First useful workflow',
          flow: [
            'Capture the user input',
            'Normalize it into structured context',
            'Generate one useful output',
            'Let the user review and revise',
          ],
        },
      ],
      mvp: {
        must_have: [
          'single-screen intake',
          'structured output preview',
          'runnable local POC',
          'review loop',
        ],
      },
      acceptance_criteria: [
        'User can understand the generated blueprint',
        'POC runs locally with one command',
        'Deployment path is documented',
      ],
      success_metrics: ['local run completion', 'proposal approval rate', 'POC acceptance rate'],
      monetization: {
        model: 'free first, paid for higher-quality POCs and ecosystem integrations',
      },
      differentiation: ['turns rough ideas into runnable capsules', 'keeps ecosystem preferences explicit'],
      risks: ['POC may look polished before proving the core workflow'],
      open_questions: ['Which integrations are mandatory for the first useful version?'],
      ecosystem: defaultEcosystem(),
    },
  });
}

function blueprintSchema() {
  return {
    type: 'object',
    additionalProperties: false,
    required: ['title', 'category', 'why', 'details'],
    properties: {
      title: { type: 'string' },
      category: { type: 'string', enum: ['money', 'personal'] },
      why: { type: 'string' },
      details: {
        type: 'object',
        additionalProperties: true,
        required: [
          'domain',
          'problem',
          'target_users',
          'use_cases',
          'technology',
          'constraints',
          'mvp',
          'acceptance_criteria',
          'success_metrics',
          'monetization',
          'differentiation',
          'risks',
          'open_questions',
          'ecosystem',
        ],
        properties: {
          domain: { type: 'string' },
          problem: { type: 'object', additionalProperties: true },
          target_users: { type: 'array', items: { type: 'string' } },
          use_cases: { type: 'array', items: { type: 'object', additionalProperties: true } },
          technology: { type: 'object', additionalProperties: true },
          constraints: { type: 'array', items: { type: 'string' } },
          mvp: { type: 'object', additionalProperties: true },
          acceptance_criteria: { type: 'array', items: { type: 'string' } },
          success_metrics: { type: 'array', items: { type: 'string' } },
          monetization: { type: 'object', additionalProperties: true },
          differentiation: { type: 'array', items: { type: 'string' } },
          risks: { type: 'array', items: { type: 'string' } },
          open_questions: { type: 'array', items: { type: 'string' } },
          ecosystem: { type: 'object', additionalProperties: true },
        },
      },
    },
  };
}

async function generateBlueprint(signal) {
  const apiKey = process.env.OPENAI_API_KEY || '';
  if (!apiKey) {
    return { blueprint: deterministicBlueprint(signal), source: 'deterministic' };
  }

  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: process.env.IDEATE_BLUEPRINT_MODEL || 'gpt-4o-mini',
      input: [
        {
          role: 'system',
          content: 'Generate a practical product blueprint as JSON. Keep uncertain assumptions in open_questions. Prefer local-first POC defaults.',
        },
        {
          role: 'user',
          content: `Idea signal: ${String(signal || '').trim()}`,
        },
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'ideate_blueprint',
          strict: true,
          schema: blueprintSchema(),
        },
      },
    }),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    console.error('[dashboard-api] blueprint generation failed', { status: response.status, body: text.slice(0, 300) });
    return { blueprint: deterministicBlueprint(signal), source: 'deterministic-fallback' };
  }

  const payload = await response.json();
  const outputText = payload.output_text
    || (payload.output || [])
      .flatMap((item) => item.content || [])
      .find((item) => item.type === 'output_text')?.text
    || '';
  if (!outputText) {
    return { blueprint: deterministicBlueprint(signal), source: 'deterministic-fallback' };
  }
  return { blueprint: normalizeBlueprint(JSON.parse(outputText)), source: 'openai' };
}

module.exports = {
  blueprintSchema,
  defaultEcosystem,
  deterministicBlueprint,
  generateBlueprint,
  normalizeBlueprint,
  slugify,
};
