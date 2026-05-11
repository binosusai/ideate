'use strict';

const { listIdeas, latestArtifacts } = require('../_lib/db');
const { intQueryValue, protectedGet } = require('../_lib/routes');

const REVIEW_ARTIFACT_KINDS = [
  'poc_quality_score',
  'poc_improvement_loop',
  'poc_report',
];

module.exports = async (req, res) => {
  await protectedGet(req, res, async () => {
    const ideas = await listIdeas({
      reviewStatus: 'pending_review',
      limit: intQueryValue(req.query.limit, 50),
    });

    const reviews = await Promise.all(
      ideas.map(async (idea) => ({
        ...idea,
        artifacts: await latestArtifacts(idea.id, REVIEW_ARTIFACT_KINDS),
      })),
    );

    res.status(200).json({ reviews });
  });
};
