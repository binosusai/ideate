'use strict';

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

module.exports = async (req, res) => {
  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const clientSecret = process.env.GITHUB_OAUTH_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    res.status(500).json({ error: 'Missing GitHub OAuth app environment variables.' });
    return;
  }

  const code = typeof req.query.code === 'string' ? req.query.code : '';
  const state = typeof req.query.state === 'string' ? req.query.state : '';
  const cookies = parseCookies(req.headers.cookie || '');

  if (!code || !state || state !== cookies.ideate_gh_oauth_state) {
    res.status(401).json({ error: 'Invalid OAuth state.' });
    return;
  }

  try {
    const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
      }),
    });

    const tokenPayload = await tokenResponse.json().catch(() => ({}));
    if (!tokenResponse.ok || !tokenPayload.access_token) {
      const reason = tokenPayload.error_description || tokenPayload.error || 'OAuth exchange failed';
      res.status(401).json({ error: reason });
      return;
    }

    res.setHeader('Set-Cookie', [
      'ideate_gh_oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0',
      `ideate_gh_token=${encodeURIComponent(tokenPayload.access_token)}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000`,
    ]);
    res.writeHead(302, { Location: '/?auth=connected' });
    res.end();
  } catch (error) {
    const message = error instanceof Error ? error.message : 'OAuth callback failed';
    res.status(502).json({ error: message });
  }
};
