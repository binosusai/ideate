'use strict';

module.exports = async (req, res) => {
  res.setHeader('Set-Cookie', [
    'ideate_gh_token=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0',
    'ideate_gh_oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0',
  ]);
  res.writeHead(302, { Location: '/?auth=signed-out' });
  res.end();
};
