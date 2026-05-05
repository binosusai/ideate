'use strict';

const crypto = require('node:crypto');

function buildBaseUrl(req) {
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const proto = req.headers['x-forwarded-proto'] || (host && host.includes('localhost') ? 'http' : 'https');
  return `${proto}://${host}`;
}

module.exports = async (req, res) => {
  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  if (!clientId) {
    res.status(500).json({ error: 'Missing GITHUB_OAUTH_CLIENT_ID in Vercel environment variables.' });
    return;
  }

  const state = crypto.randomBytes(24).toString('hex');
  const baseUrl = buildBaseUrl(req);
  const redirectUri = `${baseUrl}/api/auth/github/callback`;

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'repo read:org',
    state,
  });

  res.setHeader('Set-Cookie', [
    `ideate_gh_oauth_state=${encodeURIComponent(state)}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=600`,
  ]);
  res.writeHead(302, { Location: `https://github.com/login/oauth/authorize?${params.toString()}` });
  res.end();
};
