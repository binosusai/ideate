'use strict';

const { normalizeBlueprint } = require('../_lib/blueprint');
const { bodyObject, protectedPost } = require('../_lib/routes');

module.exports = async (req, res) => {
  await protectedPost(req, res, async () => {
    const body = bodyObject(req);
    const blueprint = normalizeBlueprint(body.blueprint || body);
    res.status(200).json({ blueprint });
  });
};
