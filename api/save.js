// Vercel Serverless Function — handles GitHub save atomically
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  const { skills, token } = req.body || {};
  if (!skills || !token) return res.status(400).json({ error: 'Missing skills or token' });

  const REPO = 'tbj88/skill-hub-site';
  const BRANCH = 'main';

  try {
    const data = { skills, updatedAt: new Date().toISOString() };
    const content = Buffer.from(JSON.stringify(data, null, 2)).toString('base64');
    const api = `https://api.github.com/repos/${REPO}/contents/skills.json`;

    // Get current SHA
    let sha = '';
    try {
      const r = await fetch(api + '?ref=' + BRANCH, {
        headers: { Authorization: 'token ' + token, Accept: 'application/vnd.github+json' }
      });
      if (r.ok) { const d = await r.json(); sha = d.sha; }
    } catch(e) {}

    // Write with retries
    for (let i = 0; i < 5; i++) {
      if (i > 0) {
        // Re-fetch SHA
        try {
          const r = await fetch(api + '?ref=' + BRANCH, {
            headers: { Authorization: 'token ' + token }
          });
          if (r.ok) { const d = await r.json(); sha = d.sha; }
        } catch(e) {}
        await new Promise(r => setTimeout(r, 1000 + Math.random() * 2000));
      }

      const r = await fetch(api, {
        method: 'PUT',
        headers: {
          Authorization: 'token ' + token,
          Accept: 'application/vnd.github+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: `save: ${skills.length} skills`, content, branch: BRANCH, sha })
      });

      if (r.ok) {
        return res.json({ ok: true, msg: `Saved ${skills.length} skills` });
      }
      if (r.status !== 409 && r.status !== 422) {
        const e = await r.text().catch(() => '');
        return res.status(500).json({ ok: false, msg: 'HTTP ' + r.status + ' ' + e.slice(0, 200) });
      }
    }

    return res.status(409).json({ ok: false, msg: 'Version conflict' });
  } catch(e) {
    return res.status(500).json({ ok: false, msg: e.message });
  }
}
