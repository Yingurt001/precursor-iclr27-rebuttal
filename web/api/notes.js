// GET /api/notes：全部批注；POST /api/notes：新写一条（一条一个文件，几个人同时写也不会冲突）。
// 文件格式与本地 06_网站/serve.py 写的一样。
const { STATIC, guard, who, readAll, writeOne, noteFile } = require("./_lib.js");
const TYPES = new Set(["note", "reply", "resolve", "reopen"]);

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (!guard(req, res)) return;
  const person = who(req);
  try {
    if (req.method === "GET") {
      const live = await readAll();
      res.status(200).json({ me: person ? person.id : null, people: STATIC.people, events: live.events });
      return;
    }
    if (req.method !== "POST") { res.status(405).json({ error: "只收 GET / POST" }); return; }
    const d = req.body || {};
    if (!TYPES.has(d.type)) { res.status(400).json({ error: "type 只能是 note / reply / resolve / reopen" }); return; }
    if (!person || d.author !== person.id) { res.status(400).json({ error: "批注身份和登录身份对不上" }); return; }
    const { id, time } = noteFile(person.id);
    const ev = {
      id, type: d.type, author: person.id, time,
      thread: String(d.thread || "").slice(0, 64), key: String(d.key || "").slice(0, 32),
      quote: String(d.quote || "").slice(0, 200), text: String(d.text || "").slice(0, 4000),
      parent: String(d.parent || "").slice(0, 80),
    };
    const w = await writeOne(`${STATIC.notesDir}/${id}.json`, JSON.stringify(ev, null, 1), null, `notes: ${person.label} (${d.type})`, person);
    if (w.status !== 201 && w.status !== 200) throw new Error("写批注失败：" + w.status + " " + (w.body.message || ""));
    res.status(200).json({ ok: true, event: ev });
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
