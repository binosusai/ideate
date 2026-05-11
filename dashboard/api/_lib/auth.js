'use strict';

const { HttpError } = require('./http');

function parseCookies(cookieHeader) {
  const out = {};
  if (!cookieHeader) return out;
  for (const item of cookieHeader.split(';')) {
    const idx = item.indexOf('=');
    if (idx === -1) continue;
    const key = item.slice(0, idx).trim();
    const value = item.slice(idx + 1).trim();
    out[key] = decodeURIComponent(value);
  }
  return out;
}

function bearerToken(req) {
  const header = req.headers.authorization || req.headers.Authorization || '';
  const match = /^Bearer\s+(.+)$/i.exec(String(header).trim());
  return match ? match[1].trim() : '';
}

function dashboardToken(req) {
  const cookies = parseCookies(req.headers.cookie || '');
  return bearerToken(req) || cookies.ideate_dashboard_token || '';
}

function requireDashboardAuth(req) {
  const expected = process.env.IDEATE_DASHBOARD_ADMIN_TOKEN || '';
  if (!expected) {
    throw new HttpError(503, 'Dashboard admin auth is not configured.', 'auth_not_configured');
  }
  if (dashboardToken(req) !== expected) {
    throw new HttpError(401, 'Dashboard authorization required.', 'unauthorized');
  }
}

module.exports = {
  dashboardToken,
  parseCookies,
  requireDashboardAuth,
};
