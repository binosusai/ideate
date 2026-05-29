'use strict';

const { HttpError } = require('./http');

function repoName() {
  const repo = process.env.IDEATE_TASKS_REPO || process.env.GITHUB_REPOSITORY || '';
  if (!repo || !repo.includes('/')) {
    throw new HttpError(503, 'GitHub repository is not configured.', 'github_repo_not_configured');
  }
  return repo;
}

function githubToken() {
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
  if (!token) {
    throw new HttpError(503, 'GitHub token is not configured.', 'github_token_not_configured');
  }
  return token;
}

async function dispatchPocWorkflow(ideaId) {
  return dispatchPipelineWorkflow(ideaId, {
    stages: 'poc',
  });
}

async function dispatchReviewWorkflow(ideaId, decision, feedback = '') {
  const normalizedDecision = String(decision || '').trim();
  if (!['approve', 'revise'].includes(normalizedDecision)) {
    throw new HttpError(422, 'Review decision must be approve or revise.', 'invalid_review_decision');
  }
  return dispatchPipelineWorkflow(ideaId, {
    stages: 'review',
    review_outcome: normalizedDecision,
    review_feedback: String(feedback || '').trim(),
  });
}

async function dispatchPipelineWorkflow(ideaId, inputs) {
  const repo = repoName();
  const token = githubToken();
  const workflow = process.env.IDEATE_PIPELINE_WORKFLOW || 'pipeline.yml';
  const ref = process.env.IDEATE_PIPELINE_REF || process.env.VERCEL_GIT_COMMIT_REF || 'main';
  const response = await fetch(`https://api.github.com/repos/${repo}/actions/workflows/${workflow}/dispatches`, {
    method: 'POST',
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'ideate-dashboard',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    body: JSON.stringify({
      ref,
      inputs: {
        idea_id: String(ideaId),
        force_refresh_stages: 'false',
        ...inputs,
      },
    }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const detail = payload && payload.message ? ` ${payload.message}` : '';
    throw new HttpError(502, `GitHub workflow dispatch failed.${detail}`, 'github_dispatch_failed');
  }

  return { repo, workflow, ref };
}

module.exports = {
  dispatchPocWorkflow,
  dispatchReviewWorkflow,
};
