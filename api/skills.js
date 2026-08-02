// Vercel Serverless Function — proxy Gitee API (no CORS issues)
const REPO = 'tbj88/skill-hub-site';
const GITEE = 'https://gitee.com/api/v5/repos/' + REPO;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const token = req.headers.authorization?.replace('Bearer ', '') || '';

  try {
    if (req.method === 'GET') {
      // Read skills.json
      const r = await fetch(GITEE + '/contents/skills.json?ref=main', {
        headers: token ? { Authorization: 'token ' + token } : {}
      });
      if (!r.ok) return res.status(r.status).json({ error: 'Gitee API error' });
      const d = await r.json();
      const json = decodeURIComponent(escape(Buffer.from(d.content, 'base64').toString()));
      return res.json(JSON.parse(json));
    }

    if (req.method === 'POST') {
      // Save skills.json
      const { skills } = req.body;
      if (!skills || !token) return res.status(400).json({ error: 'Missing skills or token' });
      const data = { skills, updatedAt: new Date().toISOString() };
      const content = Buffer.from(JSON.stringify(data, null, 2)).toString('base64');

      // Get SHA
      let sha = '';
      try {
        const r = await fetch(GITEE + '/contents/skills.json?ref=main', {
          headers: { Authorization: 'token ' + token }
        });
        if (r.ok) { const d = await r.json(); sha = d.sha; }
      } catch(e) {}

      // Write with retry
      for (let i = 0; i < 5; i++) {
        if (i > 0) {
          try {
            const r = await fetch(GITEE + '/contents/skills.json?ref=main', {
              headers: { Authorization: 'token ' + token }
            });
            if (r.ok) { const d = await r.json(); sha = d.sha; }
          } catch(e) {}
          await new Promise(r => setTimeout(r, 1000 + Math.random() * 2000));
        }

        const r = await fetch(GITEE + '/contents/skills.json', {
          method: 'PUT',
          headers: { Authorization: 'token ' + token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ access_token: token, content, message: `save: ${skills.length} skills`, branch: 'main', sha })
        });

        if (r.ok) return res.json({ ok: true, msg: `Saved ${skills.length} skills` });
        if (r.status !== 400 && r.status !== 409) {
          return res.status(r.status).json({ error: 'Gitee API error ' + r.status });
        }
      }
      return res.status(409).json({ error: 'Conflict after retries' });
    }

    res.status(405).json({ error: 'Method not allowed' });
  } catch(e) {
    res.status(500).json({ error: e.message });
  }
}
