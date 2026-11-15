// GET /api/data：登录后才给数据。回复稿和批注每次都从 GitHub 现读，审稿原文和审稿人原话来自部署时生成的 _static.js。
const { STATIC, guard, who, readAll } = require("./_lib.js");

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (!guard(req, res)) return;
  try {
    const live = await readAll();
    const threads = STATIC.threads.map(t => {
      const { file, ...rest } = t;
      if (!file) return { ...rest, posts: [""], origin: null, sha: null };
      const f = live.posts[t.id];
      return { ...rest, posts: f.posts, origin: f.posts, sha: f.sha };
    });
    const me = who(req);
    res.status(200).json({ meta: STATIC.meta, threads, people: STATIC.people, me: me ? me.id : null, events: live.events });
  } catch (e) {
    console.error("[%s] %s", req.url, e && e.stack || e);          // 进 Vercel 日志，查问题用
    res.status(502).json({ error: String(e.message || e) });
  }
};
