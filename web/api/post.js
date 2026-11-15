// POST /api/post {thread, base, posts}：把一份回复稿写回 GitHub。
// 先读最新版，按条和别人的改动合并；GitHub 上的文件在这期间又变了（sha 对不上）就重来，最多三次。
const { STATIC, guard, who, readOne, writeOne, buildFile, merge } = require("./_lib.js");

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "只收 POST" }); return; }
  if (!guard(req, res)) return;
  const person = who(req);
  if (!person) { res.status(400).json({ error: "先选「你是谁」" }); return; }
  const { thread, base, posts } = req.body || {};
  const t = STATIC.threads.find(x => x.id === thread && x.file);
  const okList = a => Array.isArray(a) && a.length <= 30 && a.every(s => typeof s === "string" && s.length <= 20000);
  if (!t || !okList(base) || !okList(posts)) { res.status(400).json({ error: "请求不完整" }); return; }

  try {
    for (let attempt = 0; attempt < 3; attempt++) {
      const cur = await readOne(t.file);
      const m = merge(base, posts, cur.posts);
      const same = m.posts.length === cur.posts.length && m.posts.every((x, i) => x === cur.posts[i]);
      if (same) { res.status(200).json({ posts: m.posts, merged: m.merged, conflicts: m.conflicts, sha: cur.sha, wrote: false }); return; }
      const changed = m.posts.map((x, i) => (x !== cur.posts[i] ? i + 1 : 0)).filter(Boolean);
      const msg = `web: ${person.label} edited ${t.short}` + (changed.length && changed.length <= 5 ? ` (post ${changed.join(", ")})` : "");
      const w = await writeOne(t.file, buildFile(cur.text, m.posts), cur.sha, msg, person);
      if (w.status === 200 || w.status === 201) {
        res.status(200).json({ posts: m.posts, merged: m.merged, conflicts: m.conflicts, sha: w.body.content && w.body.content.sha, wrote: true });
        return;
      }
      if (w.status !== 409 && w.status !== 422) throw new Error("写 GitHub 失败：" + w.status + " " + (w.body.message || ""));
    }
    res.status(409).json({ error: "这份稿子刚被别人连续改了几次，刷新一下再改" });
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
