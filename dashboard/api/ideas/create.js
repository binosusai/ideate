'use strict';

const { createIdeaFromBlueprint, compactIdea } = require('../_lib/db');
const { bodyObject, protectedPost } = require('../_lib/routes');

module.exports = async (req, res) => {
  await protectedPost(req, res, async () => {
    const body = bodyObject(req);
    const result = await createIdeaFromBlueprint(body.blueprint || body);
    res.status(201).json({
      idea: compactIdea(result.idea),
      blueprint: result.blueprint,
    });
  });
};
