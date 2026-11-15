// 网页版工作台的后端公共部分：口令、GitHub 读写、md 分条文件的解析与重建、多人同时改时的合并。
// 文件名以 _ 开头，Vercel 不把它当成接口。
const crypto = require("crypto");
const STATIC = require("./_static.js");

const OWNER = STATIC.repo.owner, NAME = STATIC.repo.name;
const BRANCH = process.env.BRANCH || STATIC.repo.branch;     // 只在本地测试时用临时分支覆盖
const OPEN = "▼▼▼ COPY FROM HERE ▼▼▼";
const CLOSE = "▲▲▲ COPY TO HERE ▲▲▲";
const POST_RE = /(?:▼▼▼ COPY FROM HERE ▼▼▼|>>>>> COPY FROM HERE)\n([\s\S]*?)\n(?:▲▲▲ COPY TO HERE ▲▲▲|<<<<< COPY TO HERE)/g;
const LIMIT = 5000;
const len = s => Array.from(s).length;          // 和 Python 的 len() 一样按字符数

// ── 口令 ─────────────────────────────────────────────
function authed(req) {
  const want = process.env.PASSCODE || "";
  const got = String(req.headers["x-passcode"] || "");
  if (!want) return false;
  const h = s => crypto.createHash("sha256").update(s).digest();
  return crypto.timingSafeEqual(h(want), h(got));
}
function who(req) {
  const id = String(req.headers["x-who"] || "");
  return STATIC.people.find(p => p.id === id) || null;
}
function guard(req, res) {
  if (!process.env.GITHUB_TOKEN) { res.status(500).json({ error: "服务端还没配 GITHUB_TOKEN" }); return false; }
  if (!authed(req)) { res.status(401).json({ error: "口令不对" }); return false; }
  return true;
}

// ── GitHub ───────────────────────────────────────────
async function gh(path, opts = {}) {
  const r = await fetch("https://api.github.com" + path, {
    ...opts,
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "rebuttal-workbench",
      ...(opts.headers || {}),
    },
  });
  const body = await r.json().catch(() => ({}));
  return { status: r.status, body };
}

// 一次 GraphQL 取回所有回复稿和全部批注（blob 的 oid 就是写回时要带的 sha）
async function readAll() {
  const files = STATIC.threads.filter(t => t.file);
  const parts = files.map((t, i) => `f${i}: object(expression: ${JSON.stringify(`${BRANCH}:${t.file}`)}) { ... on Blob { text oid } }`);
  parts.push(`notes: object(expression: ${JSON.stringify(`${BRANCH}:${STATIC.notesDir}`)}) { ... on Tree { entries { name object { ... on Blob { text } } } } }`);
  const query = `query { repository(owner: ${JSON.stringify(OWNER)}, name: ${JSON.stringify(NAME)}) { ${parts.join("\n")} } }`;
  const { status, body } = await gh("/graphql", { method: "POST", body: JSON.stringify({ query }) });
  if (status !== 200 || !body.data) throw new Error("读 GitHub 失败：" + status + " " + JSON.stringify(body.errors || body.message || ""));
  const repo = body.data.repository;
  const posts = {};
  files.forEach((t, i) => {
    const b = repo["f" + i];
    posts[t.id] = b ? { text: b.text, sha: b.oid, posts: parsePosts(b.text) } : { text: "", sha: null, posts: [] };
  });
  const events = [];
  ((repo.notes && repo.notes.entries) || []).forEach(e => {
    if (!e.name.endsWith(".json") || !e.object || e.object.text == null) return;
    try { events.push(JSON.parse(e.object.text)); } catch (err) { /* 坏文件跳过 */ }
  });
  return { posts, events };
}

async function readOne(file) {
  const p = "/repos/" + OWNER + "/" + NAME + "/contents/" + file.split("/").map(encodeURIComponent).join("/") + "?ref=" + BRANCH;
  const { status, body } = await gh(p);
  if (status !== 200) throw new Error("读文件失败：" + status);
  const text = Buffer.from(body.content, "base64").toString("utf8");
  return { text, sha: body.sha, posts: parsePosts(text) };
}

async function writeOne(file, text, sha, message, person) {
  const p = "/repos/" + OWNER + "/" + NAME + "/contents/" + file.split("/").map(encodeURIComponent).join("/");
  const author = person ? { name: `${person.label}（网页）`, email: `${person.github || person.id}@users.noreply.github.com` } : undefined;
  const payload = { message, content: Buffer.from(text, "utf8").toString("base64"), branch: BRANCH, ...(sha ? { sha } : {}), ...(author ? { author } : {}) };
  return gh(p, { method: "PUT", body: JSON.stringify(payload) });
}

// ── md 分条文件 ──────────────────────────────────────
function parsePosts(text) {
  return Array.from(String(text || "").matchAll(POST_RE), m => m[1].trim());
}
// 写回格式与 sync.py 完全一致：头部说明 + 「---」+「## 第 i/n 条 · N 字符」+ 复制标记
function buildFile(oldText, posts) {
  const n = posts.length;
  const at = oldText.search(/^## 第 1\/\d+ 条/m);
  let head = (at >= 0 ? oldText.slice(0, at) : oldText).replace(/\s+$/, "").replace(/\n-{3,}$/, "").replace(/\s+$/, "") + "\n";
  head = head.replace(/当前共 \d+ 条/, `当前共 ${n} 条`)
             .replace(/发帖顺序：[^*\n]*? 倒序贴/, `发帖顺序：${Array.from({ length: n }, (_, k) => `${n - k}/${n}`).join(" → ")} 倒序贴`);
  const out = [head];
  posts.forEach((txt, k) => {
    const flag = len(txt) < LIMIT ? "" : "  ⚠️ 超限，需手工拆";
    out.push(`\n\n---\n\n## 第 ${k + 1}/${n} 条 · ${len(txt)} 字符${flag}\n\n${OPEN}\n\n${txt}\n\n${CLOSE}\n`);
  });
  return out.join("");
}

// ── 合并：base = 这个人打开页面时的版本，mine = 他现在的版本，theirs = GitHub 上最新的 ──
function merge(base, mine, theirs) {
  const eq = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
  if (eq(theirs, base)) return { posts: mine, merged: [], conflicts: [] };
  if (eq(mine, base) || eq(mine, theirs)) return { posts: theirs, merged: theirs.map((_, i) => i).filter(i => theirs[i] !== base[i]), conflicts: [] };
  if (base.length === mine.length && base.length === theirs.length) {
    const posts = [], merged = [], conflicts = [];
    base.forEach((b, i) => {
      if (mine[i] === b) { posts.push(theirs[i]); if (theirs[i] !== b) merged.push(i); }
      else if (theirs[i] === b || theirs[i] === mine[i]) posts.push(mine[i]);
      else { posts.push(mine[i]); conflicts.push(i); }        // 两边都改了同一条：以后保存的为准，另一版留在 GitHub 历史里
    });
    return { posts, merged, conflicts };
  }
  return { posts: mine, merged: [], conflicts: ["all"] };     // 两边都增删过帖子，没法逐条对齐
}

function noteFile(author) {
  const now = new Date();
  const p = n => String(n).padStart(2, "0");
  const stamp = `${now.getUTCFullYear()}${p(now.getUTCMonth() + 1)}${p(now.getUTCDate())}T${p(now.getUTCHours())}${p(now.getUTCMinutes())}${p(now.getUTCSeconds())}Z`;
  return { id: `${stamp}_${author}_${crypto.randomBytes(3).toString("hex")}`, time: now.toISOString().replace(/\.\d{3}Z$/, "+00:00") };
}

module.exports = { STATIC, guard, who, readAll, readOne, writeOne, parsePosts, buildFile, merge, noteFile, LIMIT };
