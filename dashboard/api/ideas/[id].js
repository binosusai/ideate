'use strict';

const { HttpError } = require('../_lib/http');
const { getIdeaById, latestArtifacts, recentDecisions } = require('../_lib/db');
const { firstQueryValue, protectedGet } = require('../_lib/routes');

const DETAIL_ARTIFACT_KINDS = [
  'research',
  'debate',
  'plan',
  'openspec_proposal',
  'openspec_design',
  'openspec_tasks',
  'openspec_spec',
  'poc_quality_score',
  'poc_improvement_loop',
  'poc_report',
  'handoff',
];

function artifactText(artifacts, kind) {
  return artifacts[kind] && artifacts[kind].content ? String(artifacts[kind].content) : '';
}

function synthesizeProposal(idea, artifacts) {
  const research = artifactText(artifacts, 'research');
  const debate = artifactText(artifacts, 'debate');
  const plan = artifactText(artifacts, 'plan');
  if (!research && !debate && !plan) return null;
  const lines = [
    `# Proposal: ${idea.title}`,
    '',
    '## Approval Question',
    'Approve this proposal to build the first POC for the idea.',
    '',
    '## Idea',
    `- Lifecycle: ${idea.status}`,
    `- Review: ${idea.review_status}`,
    `- Score: ${idea.score}`,
    idea.domain ? `- Domain: ${idea.domain}` : '',
    '',
    research ? `## Research\n\n${research}` : '',
    debate ? `## Debate\n\n${debate}` : '',
    plan ? `## Implementation Plan\n\n${plan}` : '',
  ].filter(Boolean);
  return lines.join('\n');
}

function parseIdeaId(req) {
  const value = firstQueryValue(req.query.id);
  const id = Number.parseInt(String(value || ''), 10);
  if (!Number.isInteger(id) || id <= 0) {
    throw new HttpError(400, 'A valid idea id is required.', 'invalid_idea_id');
  }
  return id;
}

module.exports = async (req, res) => {
  await protectedGet(req, res, async () => {
    const ideaId = parseIdeaId(req);
    const idea = await getIdeaById(ideaId);
    if (!idea) {
      throw new HttpError(404, 'Idea not found.', 'idea_not_found');
    }

    const [artifacts, decisions] = await Promise.all([
      latestArtifacts(ideaId, DETAIL_ARTIFACT_KINDS),
      recentDecisions(ideaId, 12),
    ]);
    if (!artifacts.openspec_proposal) {
      const proposal = synthesizeProposal(idea, artifacts);
      if (proposal) {
        artifacts.proposal = { content: proposal, created_at: idea.updated_at };
      }
    }

    res.status(200).json({
      idea,
      artifacts,
      decisions,
    });
  });
};
