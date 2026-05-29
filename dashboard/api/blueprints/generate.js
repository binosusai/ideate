'use strict';

const { generateBlueprint } = require('../_lib/blueprint');
const { bodyObject, protectedPost } = require('../_lib/routes');

module.exports = async (req, res) => {
  await protectedPost(req, res, async () => {
    const body = bodyObject(req);
    const signal = String(body.signal || body.idea || '').trim();
    const result = await generateBlueprint(signal);
    res.status(200).json(result);
  });
};
