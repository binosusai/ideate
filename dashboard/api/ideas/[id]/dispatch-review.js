'use strict';

const { dispatchReviewWorkflow } = require('../../_lib/github');
const { HttpError } = require('../../_lib/http');
const { bodyObject, firstQueryValue, protectedPost } = require('../../_lib/routes');

function parseIdeaId(req) {
  const id = Number.parseInt(String(firstQueryValue(req.query.id) || ''), 10);
  if (!Number.isInteger(id) || id <= 0) {
    throw new HttpError(400, 'A valid idea id is required.', 'invalid_idea_id');
  }
  return id;
}

module.exports = async (req, res) => {
  await protectedPost(req, res, async () => {
    const ideaId = parseIdeaId(req);
    const body = bodyObject(req);
    const dispatch = await dispatchReviewWorkflow(ideaId, body.decision, body.feedback || '');
    res.status(200).json({ dispatch });
  });
};
