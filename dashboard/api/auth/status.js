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
  const cookies = parseCookies(req.headers.cookie || '');
  const hasServerToken = Boolean(process.env.GITHUB_TOKEN || process.env.GH_TOKEN);
  const hasUserToken = Boolean(cookies.ideate_gh_token);
  const loggedIn = hasServerToken || hasUserToken;

  res.status(200).json({
    loggedIn,
    mode: hasServerToken ? 'server-token' : hasUserToken ? 'github-oauth' : 'anonymous',
  });
};
