'use strict';

const { HttpError } = require('../_lib/http');
const { getIdeaById, latestArtifacts, recentDecisions } = require('../_lib/db');
const { firstQueryValue, protectedGet } = require('../_lib/routes');

const DETAIL_ARTIFACT_KINDS = [
  'research',
  'debate',
  'plan',
  'poc_quality_score',
  'poc_improvement_loop',
  'poc_report',
  'handoff',
];

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

    res.status(200).json({
      idea,
      artifacts,
      decisions,
    });
  });
};
