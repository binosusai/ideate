'use strict';

const { listIdeas } = require('../_lib/db');
const { firstQueryValue, intQueryValue, protectedGet } = require('../_lib/routes');

module.exports = async (req, res) => {
  await protectedGet(req, res, async () => {
    const ideas = await listIdeas({
      status: String(firstQueryValue(req.query.status) || '').trim(),
      reviewStatus: String(firstQueryValue(req.query.review_status || req.query.reviewStatus) || '').trim(),
      q: String(firstQueryValue(req.query.q) || '').trim(),
      limit: intQueryValue(req.query.limit, 50),
    });

    res.status(200).json({ ideas });
  });
};
