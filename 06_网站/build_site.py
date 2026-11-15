#!/usr/bin/env python3
"""把 00_提交/ 的回复和 REVIEWS.md 的审稿原文打包成一个自包含的 HTML 工作台。

    cd 06_网站 && /usr/bin/python3 build_site.py

输出 index.html：无外部依赖（KaTeX / marked / 字体全部内联），双击就能开。
从 Klein++/6_Rebuttal/neurips_2026/06_网站/ 移植（2026-11-06），两处不同：
  · 审稿原文读本届的 ../REVIEWS.md（逐字、带核对哈希），不读 cases/ 里的存档 —— 原文只留一份；
  · 线程表换成 ICLR 2027 #32929 的三位审稿人 + 全局回复 + Summary of Revisions。
"""
import base64
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONF = HERE.parent                      # .../6_Rebuttal/iclr_2027 —— 本届会议的产物
SUBMIT = CONF / "00_提交"
REVIEWS = CONF / "REVIEWS.md"
ASSETS = HERE / "assets"

LIMIT = 5000
# ICLR 2027 表单的分项；其余（Flag For Ethics Review）不往页面上放
KEEP_FIELDS = ["Rating", "Confidence", "Presentation", "Informativeness", "Soundness"]


def short_field(v: str) -> str:
    """`1: Difficult to follow despite careful reading.` → `1: Difficult to follow despite careful reading`"""
    parts = v.split(": ", 1)
    if len(parts) == 2:
        return f"{parts[0]}: " + re.split(r"[.]\s", parts[1], 1)[0].strip().rstrip(".")
    return v


# ── REVIEWS.md → 结构化审稿意见 ──────────────────────────────
def parse_reviews(path: Path) -> dict:
    """REVIEWS.md 的每份审稿是一个 `---` 分隔的块：

        ## R1 · Reviewer Tery · Rating 3 · Confidence 1
        - **Note ID:** `rfrdUo7k1m`
        - **Rating** — 3: Weak acceptance
        ### Paper Summary
        …
    """
    text = path.read_text(encoding="utf-8").split("## 核对", 1)[0]
    notes = {}
    for chunk in re.split(r"\n---\n", text):
        m = re.search(r"^## R\d · Reviewer (\w+)", chunk, re.M)
        if not m:
            continue
        key = m.group(1)

        fields = {}
        for k, v in re.findall(r"^- \*\*(.+?)\*\* — (.+)$", chunk, re.M):
            if k in KEEP_FIELDS:
                fields[k] = short_field(v.strip())

        blocks = []
        for title, sec in re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", chunk, re.M | re.S):
            if sec.strip():
                blocks.append({"title": title.strip(), "md": sec.strip()})

        note = re.search(r"\*\*Note ID:\*\* `(\w+)`", chunk)
        rating = re.match(r"(\d+)", fields.get("Rating", ""))
        notes[key] = {
            "fields": fields,
            "blocks": blocks,
            "noteId": note.group(1) if note else None,
            "rating": int(rating.group(1)) if rating else None,
        }
    return notes


# ── 00_提交/*.md → 一条条帖子 ────────────────────────────────
def parse_posts(path: Path) -> list:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return [p.strip() for p in
            re.findall(r"(?:▼▼▼ COPY FROM HERE ▼▼▼|>>>>> COPY FROM HERE)\n(.*?)\n(?:▲▲▲ COPY TO HERE ▲▲▲|<<<<< COPY TO HERE)", text, re.S)]


# ── KaTeX 的字体全部转成 data URI 塞进 CSS ───────────────────
def inline_katex_css() -> str:
    css = (ASSETS / "katex.min.css").read_text(encoding="utf-8")

    def swap(m):
        name = m.group(1)
        blob = (ASSETS / "fonts" / f"{name}.woff2").read_bytes()
        b64 = base64.b64encode(blob).decode()
        return f'src:url(data:font/woff2;base64,{b64}) format("woff2")'

    css, n = re.subn(r'src:url\(fonts/([\w-]+)\.woff2\)[^}]*', swap, css)
    print(f"  内联字体 {n} 个")
    return css


def reconcile_store(threads):
    """00_提交/ 是唯一源：网页存盘里与新构建不一致的线程，归档后剔除。

    工作台每次改动会自动 POST 一份快照到 edits/store.json，而页面加载时**优先读它**。
    于是只要在网页上打开过某条线程，那份快照就会一直盖住后续所有重建。
    （Klein 2026-08-04 就这么卡住过——致谢信改了两轮，网页上纹丝不动。）
    源文件是唯一源，所以这里让构建结果赢；被顶掉的快照写进 edits/.stale/ 不丢。
    """
    store_path = HERE / "edits" / "store.json"
    if not store_path.exists():
        return
    try:
        store = json.loads(store_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ⚠️ edits/store.json 读不动，跳过对账：{e}")
        return

    fresh = {t["id"]: t["posts"] for t in threads}
    stale = [tid for tid, v in store.items()
             if isinstance(v, dict) and tid in fresh and v.get("posts") != fresh[tid]]
    if not stale:
        return

    attic = HERE / "edits" / ".stale"
    attic.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%m%d-%H%M%S")
    for tid in stale:
        (attic / f"{tid}.{stamp}.json").write_text(
            json.dumps(store[tid], ensure_ascii=False, indent=1), encoding="utf-8")
        store.pop(tid)
        (HERE / "edits" / f"{tid}.md").unlink(missing_ok=True)
    # 留一个标记，存档就不会变空。页面读到空存档会当成「第一次起服务」，
    # 把浏览器 localStorage 里的旧副本搬回磁盘，刚剔掉的旧快照就又回来了（11-15 wxGK 这样被盖过两次）
    store["__reconciled"] = stamp
    store_path.write_text(json.dumps(store, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ▸ 网页存盘与源文件不一致，已让源文件生效：{', '.join(stale)}"
          f"（旧快照存到 edits/.stale/）")


def attach_section_notes(threads):
    """../逐节评审.md：`## <线程> §<节号>` 下有 判断 / 评审 / 还差 三个字段，显示在工作台右栏审稿人原话下面。"""
    path = HERE.parent / "逐节评审.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    notes = {}
    for m in re.finditer(r"^## (\S+) §(\d+)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        who, sec, body = m.group(1), m.group(2), m.group(3)
        field = lambda k: (re.search(rf"^{k}[:：]\s*(.*)$", body, re.M) or [None, ""])[1].strip()
        block = re.search(r"^还差[:：]\s*(.*?)(?=^\S+[:：]|\Z)", body, re.M | re.S)
        missing = [l[2:].strip() for l in (block.group(1).splitlines() if block else []) if l.startswith("- ") and l[2:].strip() != "无"]
        notes.setdefault(who, {})[sec] = {"verdict": field("判断"), "review": field("评审"), "missing": missing}
    for t in threads:
        mine = notes.get(t["id"])
        if not mine:
            continue
        t["sectionNotes"] = mine
        heads = {re.match(r"(\d+)\.", h).group(1) for p in t["posts"] for h in re.findall(r"^# (\d+\.)", p, re.M)}
        lost = sorted(set(mine) - heads, key=int)
        bad = [f"§{k}" for k, v in mine.items() if v["verdict"] not in ("答到", "部分", "没答到")]
        print(f"  逐节评审 {t['id']:6s} {len(mine)} 节" + (f"  ⚠️ 回复里找不到 §{lost}" if lost else "")
              + (f"  ⚠️ 判断不是 答到/部分/没答到：{bad}" if bad else ""))


def attach_questions(threads):
    """questions.json 只存定位片段；原文从 REVIEWS.md 逐字取出，挂到每条线程的 questions 上。"""
    qpath = HERE / "questions.json"
    if not qpath.exists():
        return
    mapping = json.loads(qpath.read_text(encoding="utf-8"))
    text = REVIEWS.read_text(encoding="utf-8")
    blocks = dict(zip(*[iter(re.split(r"^## R\d · Reviewer (\w+).*$", text, flags=re.M)[1:])] * 2))
    split = r"\n\s*\n|\n(?=- )|\n(?=Q\d)|\n(?=\d\. )|\n(?=\t\d\. )"
    for t in threads:
        sections = mapping.get(t["id"])
        if not sections:
            continue
        paras = [x.strip() for x in re.split(split, blocks.get(t.get("reviewer") or t["id"], "")) if x.strip()]
        out, missing = {}, []
        for sec, items in sections.items():
            for it in items:
                hit = [x for x in paras if x.startswith(it["start"])]
                if len(hit) != 1:
                    missing.append(f"§{sec} {it['label']}")
                    continue
                q = hit[0]
                if it.get("sentence"):
                    q = " ".join(x for x in re.split(r"(?<=[.?!])\s+", q) if it["sentence"] in x)
                q = re.sub(r"^(- |\d+\. |Q\d+[a-c]?( \[[^\]]+\])?:\s*)", "", q)
                out.setdefault(sec, []).append({"label": it["label"], "text": q, "zh": it.get("zh", "")})
        t["questions"] = out
        n = sum(len(v) for v in out.values())
        print(f"  审稿人原话 {t['id']:5s} {n} 段" + (f"  ⚠️ 找不到：{', '.join(missing)}" if missing else ""))


def main():
    notes = parse_reviews(REVIEWS)
    print(f"  解析审稿意见 {len(notes)} 份：{', '.join(notes)}")

    # (线程 id, 分组, 左栏短名, 标题, 对应哪份审稿, 源文件)
    specs = [
        ("general", "论坛顶层", "全局回复", "全局回复 · 致 AC 与全体审稿人", "", "0_全局总回复.md"),
        ("Tery", "审稿人回复", "Tery", "回复 Reviewer Tery", "Tery", "1_R1_Tery.md"),
        ("wxGK", "审稿人回复", "wxGK", "回复 Reviewer wxGK", "wxGK", "2_R2_wxGK.md"),
        ("pSK8", "审稿人回复", "pSK8", "回复 Reviewer pSK8", "pSK8", "3_R3_pSK8.md"),
        ("pSK8zh", "审稿人回复", "pSK8 中文稿", "回复 Reviewer pSK8 · 学姐中文稿（对照用）", "pSK8", "3b_R3_pSK8_学姐中文稿.md"),
        ("revisions", "修订稿", "Summary", "Summary of Revisions in the Updated Manuscript", "", "4_Summary_of_Revisions.md"),
    ]

    threads = []
    for tid, group, short, title, note_key, fname in specs:
        posts = parse_posts(SUBMIT / fname)
        note = notes.get(note_key, {})
        over = [i + 1 for i, p in enumerate(posts) if len(p) > LIMIT]
        print(f"  {fname:28s} {len(posts):2d} 条 · 最长 {max(map(len, posts), default=0):5d} 字符"
              + (f" ⚠️ 超限: {over}" if over else ""))
        threads.append({
            "id": tid, "group": group, "short": short, "title": title, "reviewer": note_key or None,
            "file": f"00_提交/{fname}",
            "rating": note.get("rating"), "noteId": note.get("noteId"),
            "review": {"fields": note.get("fields", {}), "blocks": note.get("blocks", [])} if note else None,
            "posts": posts, "origin": posts,
        })

    threads.append({
        "id": "scratch", "group": "工具", "short": "草稿板",
        "title": "草稿板 · 随手粘贴渲染", "rating": None, "noteId": None, "file": None,
        "review": None, "posts": [""], "origin": None,
    })

    reconcile_store(threads)
    attach_questions(threads)
    attach_section_notes(threads)

    data = json.dumps({"threads": threads}, ensure_ascii=False)
    base = (HERE / "template.html").read_text(encoding="utf-8")
    for token, value in [
        ("__KATEX_CSS__", inline_katex_css()),
        ("__KATEX_JS__", (ASSETS / "katex.min.js").read_text(encoding="utf-8")),
        ("__MARKED_JS__", (ASSETS / "marked.min.js").read_text(encoding="utf-8")),
    ]:
        base = base.replace(token, value, 1)
    html = base.replace("__DATA__", data.replace("</", "<\\/"), 1)

    out = HERE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"\n✅ {out}  ({out.stat().st_size / 1024:.0f} KB)")
    build_web(base, threads)


def build_web(base, threads):
    """线上网页版（../web/，部署到 Vercel）：页面里不放任何稿件、审稿内容和论文标题，登录后才从 /api/data 取。
    审稿原文、审稿人原话、线程清单写进 web/api/_static.js（只有服务端读得到）；回复稿和批注由服务端从 GitHub 现读。"""
    web = HERE.parent / "web"
    if not (web / "src" / "gate.html").exists():
        return
    import subprocess
    url = subprocess.run(["git", "-C", str(HERE.parent), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    if not m:
        print("  ⚠️ 网页版：读不到 GitHub 仓库地址，跳过")
        return
    venue = re.search(r'<span class="venue">(.*?)</span>', base).group(1)
    title = re.search(r"<h1>(.*?)</h1>", base).group(1)
    people = json.loads((HERE / "people.json").read_text(encoding="utf-8")).get("people", [])
    static = {
        "repo": {"owner": m.group(1), "name": m.group(2), "branch": "main"},
        "notesDir": "06_网站/批注",
        "meta": {"venue": venue, "title": title},
        "people": [{k: p[k] for k in ("id", "label", "github") if k in p} for p in people],
        "threads": [{k: v for k, v in t.items() if k not in ("posts", "origin")} for t in threads],
    }
    (web / "api" / "_static.js").write_text(
        "// 由 06_网站/build_site.py 生成，别手改。只在服务端用，不会发给没登录的浏览器。\n"
        "module.exports = " + json.dumps(static, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    page = (base
            .replace(re.search(r"<title>.*?</title>", base).group(0), '<title>Rebuttal 工作台</title>\n<meta name="robots" content="noindex, nofollow">', 1)
            .replace(f'<span class="venue">{venue}</span>', '<span class="venue" id="venue"></span>', 1)
            .replace(f"<h1>{title}</h1>", '<h1 id="ptitle">Rebuttal 工作台</h1>', 1)
            .replace("<script>\nconst DATA = __DATA__;", '<script type="text/plain" id="app">\nconst DATA = window.__WEB_DATA__;', 1)
            .replace('const STORE = "precursor-iclr27-rebuttal-v1";', 'const STORE = "rb-ws-v1";', 1))
    for leak in ["__DATA__", title, venue, "precursor-iclr27"] + [t["reviewer"] for t in threads if t.get("reviewer")]:
        assert leak not in page, f"网页版里漏了能认出项目的字样：{leak}"
    for word in ["Klein", "ICLR", "Precursor", "OpenReview ID"]:      # 字体的 base64 里可能碰巧有这些字母，只查独立成词的
        assert not re.search(rf"(?<![A-Za-z0-9+/=]){word}(?![A-Za-z0-9+/=])", page), f"网页版里有「{word}」，公开页面别留能认出作者或投稿的字样"
    page += "\n" + (web / "src" / "gate.html").read_text(encoding="utf-8")
    (web / "index.html").write_text(page, encoding="utf-8")
    print(f"✅ 网页版 {web / 'index.html'}（部署：cd web && vercel deploy --prod）")


if __name__ == "__main__":
    main()
