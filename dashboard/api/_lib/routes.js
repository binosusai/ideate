'use strict';

const { requireDashboardAuth } = require('./auth');
const { methodNotAllowed, sendError } = require('./http');

async function protectedGet(req, res, handler) {
  if (req.method !== 'GET') {
    methodNotAllowed(res, ['GET']);
    return;
  }

  try {
    requireDashboardAuth(req);
    await handler(req, res);
  } catch (error) {
    sendError(res, error);
  }
}

async function protectedPost(req, res, handler) {
  if (req.method !== 'POST') {
    methodNotAllowed(res, ['POST']);
    return;
  }

  try {
    requireDashboardAuth(req);
    await handler(req, res);
  } catch (error) {
    sendError(res, error);
  }
}

function bodyObject(req) {
  if (!req.body) return {};
  if (typeof req.body === 'object') return req.body;
  try {
    const parsed = JSON.parse(String(req.body));
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch (_error) {
    return {};
  }
}

function firstQueryValue(value) {
  return Array.isArray(value) ? value[0] : value;
}

function intQueryValue(value, fallback) {
  const raw = firstQueryValue(value);
  const parsed = Number.parseInt(String(raw || ''), 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

module.exports = {
  bodyObject,
  firstQueryValue,
  intQueryValue,
  protectedGet,
  protectedPost,
};
