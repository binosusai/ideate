'use strict';

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const repoFromEnv = process.env.IDEATE_TASKS_REPO;
  const repoFromQuery = typeof req.query.repo === 'string' ? req.query.repo.trim() : '';
  const repo = repoFromEnv || repoFromQuery;

  if (!repo || !repo.includes('/')) {
    res.status(400).json({
      error: 'Missing repository configuration. Set IDEATE_TASKS_REPO in Vercel env, or pass repo query parameter as owner/repo.',
    });
    return;
  }

  const ideaId = typeof req.query.ideaId === 'string' ? req.query.ideaId.trim() : '';
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;

  const headers = {
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'ideate-dashboard',
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const url = `https://api.github.com/repos/${repo}/issues?labels=ideate-task&state=all&per_page=100`;

  try {
    const response = await fetch(url, { headers });
    const payload = await response.json().catch(() => ({}));

    if (!response.ok) {
      const message = payload && payload.message ? payload.message : `GitHub ${response.status}`;
      res.status(response.status).json({ error: message });
      return;
    }

    if (!Array.isArray(payload)) {
      res.status(502).json({ error: 'Unexpected response from GitHub API.' });
      return;
    }

    const filtered = ideaId
      ? payload.filter((issue) =>
          Array.isArray(issue.labels) && issue.labels.some((label) => label && label.name === `idea:${ideaId}`)
        )
      : payload;

    res.status(200).json(filtered);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown proxy error';
    res.status(502).json({ error: message });
  }
};
