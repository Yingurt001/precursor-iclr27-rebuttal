#!/usr/bin/env python3
"""00_提交/ 是唯一源。直接改那五个文件，然后跑这个脚本。

    /usr/bin/python3 sync.py              核对引用 + 就地重新分条 + 重建网站
    /usr/bin/python3 sync.py --check      只检查不写（看看改完会不会超限）
    /usr/bin/python3 sync.py --no-site    只重新分条，不动网站

从 Klein++/6_Rebuttal/neurips_2026/sync.py 移植（2026-11-06）。分条算法原样未动，
改的是 JOBS 表、布局契约，以及每次同步先跑 check_reviews.py（引用是否出自对应审稿人）。
2026-11-13 再从 Klein++/6_Rebuttal/iclr_2027/sync.py 同步 PV 式（模版 v3）的改动：每条帖子自动补
References、补完超限的帖子往后挪段（spill）、`# n.` 标题续片不补 cont.、收尾段不被切成孤帖、
备份轮换只认自己写的时间戳文件。

原理：提交版文件 = 头部说明 + 若干 `>>>>> COPY FROM HERE … <<<<< COPY TO HERE` 分条。
脚本把这些分条解包回一整篇正文（剥掉续接标记），按 OpenReview 5000 字符上限重新切，
再写回同一个文件。**解包 → 重排是无损的**，所以可以反复跑，结果稳定。

改之前的版本会存到 00_提交/.bak/，留最近 10 份。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))   # .../6_Rebuttal/iclr_2027
SUBMIT = os.path.join(HERE, "00_提交")
BAK = os.path.join(SUBMIT, ".bak")
SITE = os.path.join(HERE, "06_网站", "build_site.py")

LIMIT = 5000          # ICLR 2027 Official_Comment 的 maxLength（11-06 从 invitation 读到）
PACK = 4750           # 留出续接句的余量
SECTION_BREAK = 2500  # 当前帖已过这个长度、下一块是新的一节（# n.）时开新帖：每个回答从帖子开头开始（11-13 张赢要求）
SECTION_BREAK_FILES = {"2_R2_wxGK.md": 1000}   # 文件 → 门槛（当前帖已超过这么多字符就让新一节开新帖；开场白不到 1000，跟第 1 节同帖）
ACTIVE_SECTION_BREAK = None                # process() 按文件设定
KEEP_BAK = 10

JOBS = [
    ("0_全局总回复.md",
     "全局回复（Official Comment，论坛顶层，readers：AC + 全体审稿人）"),
    ("1_R1_Tery.md",
     "回复 Reviewer Tery（Rating 3 / Conf 1；placebo 是什么 / Eq. 1 的 Σ̃）"),
    ("2_R2_wxGK.md",
     "回复 Reviewer wxGK（Rating 3 / Conf 3；3W 漂移 / 边界偏移 / 聚合与训练配置 / 功效）"),
    ("3_R3_pSK8.md",
     "回复 Reviewer pSK8（Rating 1 / Conf 4；技术贡献 / 指标 / presentation / 7 条 minor）"),
    ("4_Summary_of_Revisions.md",
     "Summary of Revisions（Official Comment，论坛顶层，修订稿传完后发）"),
]

# 标记必须是 Markdown 里没有含义的字符。曾经用 `>>>>>`，但那是合法的五层嵌套引用，
# 在 WYSIWYG Markdown 编辑器里打开再保存会被拆成 `>>>>>` / `>>>>` / `>>>` 几行空引用
# （2026-07-31 R1 就这么坏过）。解析时两种都认，写出去一律用新的。
OPEN, CLOSE = "\u25bc\u25bc\u25bc COPY FROM HERE \u25bc\u25bc\u25bc", "\u25b2\u25b2\u25b2 COPY TO HERE \u25b2\u25b2\u25b2"
COPY_RE = re.compile(
    r"(?:\u25bc\u25bc\u25bc COPY FROM HERE \u25bc\u25bc\u25bc|>>>>> COPY FROM HERE)\n"
    r"(.*?)"
    r"\n(?:\u25b2\u25b2\u25b2 COPY TO HERE \u25b2\u25b2\u25b2|<<<<< COPY TO HERE)", re.S)


# ── 解包：提交版 → 一整篇正文 ────────────────────────────────
def unpack(text):
    """把分条还原成正文。剥掉脚本自己加的续接标记，用户写的内容一律不动。"""
    posts = COPY_RE.findall(text)
    if not posts:
        # 没有标记 = 用户直接贴了一整篇 markdown，整份当正文
        return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    out = []
    for p in posts:
        p = p.strip()
        # 出现在任何位置都剥掉：编辑器往返会把它们留在正文中间，不只在首尾
        p = re.sub(r"^\*\((?:Continuation of|Continued in) \d+/\d+\.\)\*[ \t]*$\n?", "", p, flags=re.M)
        p = re.sub(r"^\*\*(.+?) \(cont\.\)\*\*\n+", "", p, flags=re.M)
        # 裸的 `>>`/`>>>`/`>>>>` 空行会渲染成一串空的嵌套引用竖条，多半是编辑器把
        # 旧的 `>>>>> COPY FROM HERE` 拆开留下的残渣（2026-07-31 R1 那次）。
        # ⚠️ 只清两个以上的 `>`：单个 `>` 是引用块内部的段落分隔，删了会把
        # `> **W1.**` 和 `> **Q1.**` 挤成一段。我们的正文从不用嵌套引用。
        p = re.sub(r"^>{2,}[ \t]*$\n?", "", p, flags=re.M)
        out.append(p.strip())
    return "\n\n".join(out).strip()


# ── 引用：每条帖子自带 References（U-14，2026-11-09）──────────────
# 正文里用 [a] / [a, Thm. 9] / [a–d] 引用；条目写在任意一个 `**References**` 块里，
# 格式 `> [a] Author. Title. Venue Year.`。sync 把所有引用块摘出来合成一张表，
# 分条之后给每条帖子末尾补上「这条帖子里出现过的」条目——审稿人不用跨帖找。
REF_HEAD = "# References"                                         # 模版 v3：每条帖子末尾一个（PV 式）
REF_HEADS = ("# References", "## References", "**References**")  # 旧写法也认
REF_ENTRY = re.compile(r"^>\s*\[([a-z])\]\s+(.+?)\s*$")
CITE = re.compile(r"\[([a-z])(?:\s*[–-]\s*([a-z]))?(?=[\],])")
MATH = re.compile(r"\$[^$]*\$")


def strip_refs(text):
    """摘掉正文里所有引用块，返回 (正文, {字母: 条目})。
    只认「每行都是 `>` 或 `> [x] …`」的段落为条目，审稿人原话那种引用块不会被误吞。"""
    out, refs, skipping = [], {}, False
    for p in text.split("\n\n"):
        s = p.strip()
        first, _, rest = s.partition("\n")
        if first.strip() in REF_HEADS:
            # 标题单独成段，或像 PV 原文那样 `# References` 下一行紧接条目
            s = rest.strip()
            skipping = True
            if not s:
                continue
        if skipping:
            lines = [l.strip() for l in s.split("\n") if l.strip()]
            if lines and all(l == ">" or REF_ENTRY.match(l) for l in lines):
                for l in lines:
                    m = REF_ENTRY.match(l)
                    if m:
                        refs.setdefault(m.group(1), m.group(2))
                continue
            skipping = False
        out.append(p)
    return "\n\n".join(out).strip(), refs


def cites_in(text):
    t = MATH.sub(" ", text)          # 公式里的 [a, b] 是区间，不是引用
    found = set()
    for m in CITE.finditer(t):
        a, b = m.group(1), m.group(2)
        found.update(chr(c) for c in range(ord(a), ord(b) + 1)) if b else found.add(a)
    return found


def attach_refs(post, refs):
    """帖子末尾挂一个 `## References`，只列这条帖子里引过的条目（模版 v2，CorNet 每帖一个）。"""
    items = [f"> [{k}] {refs[k]}" for k in sorted(cites_in(post)) if k in refs]
    return post if not items else post + "\n\n" + REF_HEAD + "\n\n" + "\n>\n".join(items)


# ── 重排：正文 → 分条 ───────────────────────────────────────
def segments(body):
    """按一级/二级标题切块，标题跟着自己的正文走。"""
    blocks, cur = [], []
    for ln in body.split("\n"):
        if re.match(r"^#{1,2} ", ln) and cur:
            blocks.append("\n".join(cur).strip())
            cur = [ln]
        else:
            cur.append(ln)
    if cur:
        blocks.append("\n".join(cur).strip())
    return [b for b in blocks if b]


def paragraphs(b):
    """按空行切段，但 ```fenced``` 代码块整体算一段（ASCII 图不能被切断）。"""
    out, cur, fence = [], [], False
    for ln in b.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            cur.append(ln)
            continue
        if not fence and ln.strip() == "":
            if cur:
                out.append("\n".join(cur))
                cur = []
        else:
            cur.append(ln)
    if cur:
        out.append("\n".join(cur))
    return out


LIST_ITEM = re.compile(r"^(?:[-*+] |\d+[.)] )")


def split_list(para):
    """把一整块列表按顶层条目拆开；不是列表就原样返回。

    列表条目之间没有空行，所以 paragraphs() 会把整个列表当成一段。
    Summary of Revisions 那种十几条的列表因此单段就超 5000，怎么排都拆不动。
    条目的续行（缩进或空行后的续段）跟着自己的条目走。
    """
    lines = para.split("\n")
    if not LIST_ITEM.match(lines[0]):
        return [para]
    items, cur = [], []
    for ln in lines:
        if LIST_ITEM.match(ln) and cur:
            items.append("\n".join(cur))
            cur = [ln]
        else:
            cur.append(ln)
    if cur:
        items.append("\n".join(cur))
    return items if len(items) > 1 else [para]


def glue_leadins(paras):
    """`**n. 命名短语.**` 段和紧跟的 `Table X- …` 表（表题与表本体同段）粘成一个单位，切片时不拆开。
    11-13 wxGK §1：引语留在上一条末尾、表在下一条开头，审稿人看到的是没有引语的表。
    与 spill() 里 U-13 那条同一规则，这里管的是分块阶段。"""
    out = []
    for para in paras:
        if out and para.lstrip().startswith(("Table ", "Tab. ", "Figure ")) and out[-1].lstrip().startswith("**") \
                and not out[-1].lstrip().startswith(REF_HEADS):
            out[-1] = out[-1] + "\n\n" + para
        else:
            out.append(para)
    return out


def merge_orphan_tail(posts, refs):
    """最后一条只剩一段（多半是固定收尾段）时，塞得下就并回上一条。
    rebalance 只在上一条不到 PACK 的 70% 时才往回拉；上一条接近满时收尾段会被单独切成一条（11-13 wxGK）。
    这里按 LIMIT 判断（补完 References、加上续接标记后不超限才并）。"""
    if len(posts) < 2:
        return posts
    last = [x for x in posts[-1].split("\n\n") if x.strip()]
    if len(last) != 1:
        return posts
    merged = posts[-2] + "\n\n" + posts[-1]
    if len(attach_refs(merged, refs)) + 60 <= LIMIT:
        return posts[:-2] + [merged]
    return posts


def split_long(b, limit):
    """单个小节超长时按段落边界再切，标题留在第一片。代码块永不被切开。"""
    if len(b) <= limit:
        return [b]
    out, cur = [], ""
    paras = [x for p in paragraphs(b) for x in (split_list(p) if len(p) > limit else [p])]
    paras = glue_leadins(paras)
    for para in paras:
        cand = (cur + "\n\n" + para) if cur else para
        if cur and len(cand) > limit:
            out.append(cur)
            cur = para
        else:
            cur = cand
    if cur:
        out.append(cur)
    title = out[0].splitlines()[0].lstrip("#").strip()
    # PV 式标题 `# 1. …`（模版 v3）：续片不补 `**… (cont.)**`。它在 PV 骨架里看着像一个
    # 编号论点 `**1. …**`，而且两片常被排进同一条帖子（11-11 w1vu §1 踩到）。
    # 跨帖时帖子开头已有 `*(Continuation of k/n.)*`，够用。
    if re.match(r"^\d+\.\s", title):
        return out
    return [out[0]] + [f"**{title} (cont.)**\n\n" + x for x in out[1:]]


# 表题/图题：`Table R10:` `Tab. A:` `Figure 2:` `表 3：` 都算
CAPTION_RE = re.compile(r"^(?:Tab(?:le|\.)?|Fig(?:ure|\.)?|表|图)\s*[\w.\-]{0,8}\s*[:：]", re.I)


def unglue_captions(posts):
    """表题不许留在上一条末尾——它必须跟自己的表格待在同一条里。

    分条边界是按长度切的，很容易把 `Table R10: …` 甩在上一条结尾、表格本体留在下一条。
    审稿人看到的就是一条以孤零零表题收尾、下一条以 `|---|` 开头的帖子。
    """
    for i in range(len(posts) - 1):
        paras = posts[i].split("\n\n")
        tail = paras[-1].strip()
        # 只搬"光杆表题"：本身不含表格行，也不是唯一内容
        if len(paras) > 1 and "|" not in tail and CAPTION_RE.match(tail):
            posts[i] = "\n\n".join(paras[:-1]).rstrip()
            posts[i + 1] = tail + "\n\n" + posts[i + 1]
    return [p for p in posts if p.strip()]


TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")


def is_table(par):
    lines = [l for l in par.split("\n") if l.strip()]
    return bool(lines) and all(TABLE_ROW.match(l) for l in lines)


def unglue_tables(posts):
    """一条帖子不许以表格收尾。

    分条是按长度切的，很容易让表格落在一条的末尾、解读段落到下一条开头。
    审稿人读到的就是一张没有结论的表，而"表下必须紧跟解读"是我们的硬规则。
    先试着把末尾的表（连同 caption）推到下一条；推不动就反过来把下一条的
    第一段解读拉回来。修补时的上界用 LIMIT 而非 PACK——PACK 的余量是留给
    续接句的，而续接句只有二十几个字符。
    """
    CAP = LIMIT - 120

    def tail_table(par_list):
        """末尾若是表格，返回要搬走的段数，否则 0。"""
        if len(par_list) < 2 or not is_table(par_list[-1]):
            return 0
        take = 1
        if len(par_list) > take + 1 and CAPTION_RE.match(par_list[-take - 1].strip()):
            take += 1
        return take if len(par_list) > take else 0

    for i in range(len(posts) - 1):
        paras = posts[i].split("\n\n")
        take = tail_table(paras)
        if not take:
            continue
        moved = "\n\n".join(paras[-take:])
        if len(moved) + 2 + len(posts[i + 1]) <= CAP:          # 表往后搬
            posts[i] = "\n\n".join(paras[:-take]).rstrip()
            posts[i + 1] = moved + "\n\n" + posts[i + 1]
            continue
        nxt = posts[i + 1].split("\n\n")                      # 解读往前拉
        if nxt and not is_table(nxt[0]) and len(posts[i]) + 2 + len(nxt[0]) <= CAP:
            posts[i] = posts[i] + "\n\n" + nxt[0]
            posts[i + 1] = "\n\n".join(nxt[1:]).lstrip()
    return [p for p in posts if p.strip()]


LANDS_RE = re.compile(r"^\*Lands in:\*")
CONT_RE = re.compile(r"^\*\*.+ \(cont\.\)\*\*$")


def unglue_tails(posts):
    """一条帖子不许以 `*Lands in:*` 开头。

    它是一个回答的收尾行，只有一百来字符。被切到下一条，审稿人看到的就是
    "本条续接上一条" + 一行落地说明 + 下一个回答的标题——一条内容为零的续接帖，
    同时上一条的回答没有收尾。往前拉一行永远塞得下：PACK 留了 250 字符余量。

    ⚠️ 判断时要先跳过 `**A5 · … (cont.)**`：这行是 split_long 在分块阶段就
    写进正文的，所以帖子的第一段往往是它而不是 `*Lands in:*`。搬完之后这个
    续接标题必须一并删掉——正文已经全在上一条里，再顶着"续接"就是假的。
    """
    for i in range(1, len(posts)):
        paras = posts[i].split("\n\n")
        if paras and CONT_RE.match(paras[0].strip()):
            paras = paras[1:]
        if not paras or not LANDS_RE.match(paras[0].strip()):
            continue
        if len(posts[i - 1]) + 2 + len(paras[0]) <= LIMIT - 120:
            posts[i - 1] = posts[i - 1] + "\n\n" + paras[0]
            posts[i] = "\n\n".join(paras[1:]).lstrip()
    return [p for p in posts if p.strip()]


def rebalance(posts):
    """把后一条开头的段落往前拉，消掉只有两三行的残帖。

    split_long 是在不知道前面已经用掉多少字符的情况下预切的：开场白单独成块
    只有几百字符，紧跟的小节被切成接近上限的整片，于是贪心装箱只能让开场白
    独占一条。这里事后把下一条的开头往回搬，直到装不下为止。
    `**… (cont.)**` 续接标题必须留在原地，所以跳过它取下一段。
    """
    for i in range(len(posts) - 1):
        if len(posts[i]) >= PACK * 0.7:          # 已经装得差不多，别动
            continue
        while True:
            if not posts[i + 1].strip():         # 下一条已整条拉空，别再往上追加空段
                break
            nxt = posts[i + 1].split("\n\n")
            head = nxt[0] if nxt and CONT_RE.match(nxt[0].strip()) else None
            rest = glue_leadins(nxt[1:] if head else nxt)   # 引语和它的表一起拉，或都不拉
            # 最后一条只剩一段、又没有续接标题时也整段拉回来，空帖在下面被滤掉。
            # 11-10：收尾段（Following your suggestions …）被单独切成 300 字符的第 5/5 条。
            last = i + 1 == len(posts) - 1 and len(rest) == 1 and head is None
            if not rest or (len(rest) < 2 and not last) or len(posts[i]) + 2 + len(rest[0]) > PACK:
                break
            if starts_section(rest[0]) and len(posts[i]) >= (ACTIVE_SECTION_BREAK or 0):   # 新的一节不往上一帖拉
                break
            posts[i] += "\n\n" + rest[0]
            posts[i + 1] = "\n\n".join(([head] if head else []) + rest[1:])
    return [p for p in posts if p.strip()]


def starts_section(par):
    """`# 标题` 开头的一节；Summary of revisions / References 跟着上一节走，不算。"""
    if ACTIVE_SECTION_BREAK is None:
        return False
    m = re.match(r"^# (.+)", par.lstrip())
    return bool(m) and not m.group(1).strip().lower().startswith(("summary of revisions", "references"))


def pack(blocks):
    blocks = [x for b in blocks for x in split_long(b, PACK)]
    posts, cur = [], ""
    for b in blocks:
        cand = (cur + "\n\n" + b).strip() if cur else b
        if cur and (len(cand) > PACK or (starts_section(b) and len(cur) >= (ACTIVE_SECTION_BREAK or 0))):
            posts.append(cur)
            cur = b
        else:
            cur = cand
    if cur:
        posts.append(cur)
    return unglue_tails(unglue_tables(unglue_captions(rebalance(posts))))


def spill(posts, refs):
    """补上 References 后超限的帖子，把末尾段落挪到下一条开头。
    表格连同上一段的 `Table …` caption 一起挪；挪完不让标题行孤零零留在帖子末尾。"""
    i = 0
    while i < len(posts):
        while len(attach_refs(posts[i], refs)) + 60 > LIMIT:   # 60 = 两行续接标记
            paras = posts[i].split("\n\n")
            if len(paras) < 2:
                break
            k = len(paras) - 1
            if is_table(paras[k]) and k >= 1 and paras[k - 1].lstrip().startswith(("Table ", "Tab. ")):
                k -= 1
                # U-13：`**命名短语.**` 段后面接的就是它的证据表，两者不分帖
                if k >= 1 and paras[k - 1].lstrip().startswith("**") and not paras[k - 1].startswith(REF_HEADS):
                    k -= 1
            while k >= 1 and re.match(r"^#{1,2} ", paras[k - 1]):
                k -= 1
            if k == 0:
                break
            moved = "\n\n".join(paras[k:])
            posts[i] = "\n\n".join(paras[:k])
            if i + 1 < len(posts):
                posts[i + 1] = moved + "\n\n" + posts[i + 1]
            else:
                posts.append(moved)
        i += 1
    return posts


def render(desc, posts):
    n = len(posts)
    marked = []
    for i, txt in enumerate(posts):
        pre = f"*(Continuation of {i}/{n}.)*\n\n" if i > 0 else ""
        post = f"\n\n*(Continued in {i+2}/{n}.)*" if i < n - 1 else ""
        marked.append(pre + txt + post)

    order = " → ".join(f"{i}/{n}" for i in range(n, 0, -1))
    out = [f"""# {desc} — 提交版

> **这个文件就是源，直接改它。** 改完在 `6_Rebuttal/iclr_2027/` 跑 `/usr/bin/python3 sync.py`（或双击 `同步.command`），
> 会自动按 OpenReview 上限重新分条并刷新网站。改前的版本存在 `00_提交/.bak/`。
> 改的时候**忽略分条标记**，把它当一整篇看就行 —— 重跑脚本会重新切。
> 引用：正文写 `[a]` / `[a, Thm. 9]`；新条目随便写进任何一个 `# References` 块（`> [a] 论文标题`），
> 脚本会给每条帖子末尾补上这条帖子引过的条目，各帖里的 References 不用手动维护。
>
> 用 OpenReview 的 `Official Comment` 发：审稿人回复发在对应 review 下，0 号发在论坛顶层。单条上限 {LIMIT} 字符，当前共 {n} 条。
> **发帖顺序：{order} 倒序贴**，页面才会正序显示。
> 每条只复制 `{OPEN}` 与 `{CLOSE}` 之间的内容，不含标记行。
"""]
    for i, txt in enumerate(marked, 1):
        flag = "" if len(txt) < LIMIT else "  ⚠️ 超限，需手工拆"
        out.append(f"\n\n---\n\n## 第 {i}/{n} 条 · {len(txt)} 字符{flag}\n\n"
                   f"{OPEN}\n\n{txt}\n\n{CLOSE}\n")
    return "".join(out), marked


# ── 布局契约 ───────────────────────────────────────────────
# Klein 2026-08-02 重构时在 6_Rebuttal/ 和产物之间插进一层会议目录，脚本的相对路径没跟着改，
# 同步静默坏了两周 —— sync.py 自己全绿，崩的是它调用的下一环。
# 所以把「谁依赖哪一层」写成显式清单，每次同步先验一遍，让层级错位当场说人话。
NODE = os.path.dirname(HERE)          # .../6_Rebuttal —— 跨会议层（rules/ cases/）
PROJ = os.path.dirname(NODE)          # .../Precursor 项目 —— 项目层

LAYOUT = [
    # (路径, 这是什么, 谁依赖它)
    (SUBMIT, "00_提交/ 唯一源", "sync.py · build_site.py · check_reviews.py"),
    (os.path.join(HERE, "REVIEWS.md"), "审稿原文（逐字，带核对哈希）",
     "build_site.py 的审稿意见面板 · check_reviews.py"),
    (os.path.join(HERE, "06_网站", "template.html"), "网站模板", "build_site.py"),
    (os.path.join(NODE, "rules", "GLOBAL_REBUTTAL_RULES.md"), "规则库〔跨会议层〕", "写回复前必读", "optional"),
    (os.path.join(PROJ, "5_Submission", "iclr2027_frozen", "2026-09-26_iclr27_submitted",
                  "32929_When_Early_Is_Not_Early_.pdf"),
     "冻结投稿版 PDF〔项目层〕", "所有行号、表号引用", "optional"),
]


def preflight():
    """验布局契约。返回 True = 继续跑同步，False = 停下。"""
    # 11-14 与学姐共享 git 仓库：仓库里没有上层的规则库和投稿 PDF，只放了 参考/ 里的快照。
    # 标了 "optional" 的两项缺了只提醒、不拦同步。
    missing = []
    for item in LAYOUT:
        p, what, who = item[:3]
        if os.path.exists(p):
            continue
        if len(item) > 3 and item[3] == "optional":
            alt = os.path.join(HERE, "参考", os.path.basename(p))
            if not os.path.exists(alt):
                print(f"   ⚠️ 找不到{what}（{os.path.basename(p)}），只影响查阅，继续同步")
            continue
        missing.append((p, what, who))
    if not missing:
        return True

    print("\n⚠️ 布局契约不符 —— 多半是某一层被改名，或中间又插了一层目录：")
    for p, what, who in missing:
        print(f"   ✗ {what}")
        print(f"     期望在  {p}")
        print(f"     依赖它的 {who}")

    print("\n   路径修好再跑。只是网站模板暂缺的话，可以先用 --no-site。")
    return False


# ── 主流程 ─────────────────────────────────────────────────
def backup(path):
    os.makedirs(BAK, exist_ok=True)
    name = os.path.basename(path)[:-3]
    shutil.copy2(path, os.path.join(BAK, f"{name}.{time.strftime('%m%d-%H%M%S')}.md"))
    # 只轮换本函数自己写的 `名.MMDD-HHMMSS.md`。11-10 之前按前缀匹配，手工备份 `名.md.pre_*`
    # 也算进来且排在后面，攒满 KEEP_BAK 份后 sync 自己的备份一写完就被删掉。
    stamp = re.compile(re.escape(name) + r"\.\d{4}-\d{6}\.md$")
    olds = sorted(f for f in os.listdir(BAK) if stamp.match(f))
    for f in olds[:-KEEP_BAK]:
        os.remove(os.path.join(BAK, f))


def process(fname, desc, check):
    global ACTIVE_SECTION_BREAK
    ACTIVE_SECTION_BREAK = SECTION_BREAK_FILES.get(fname)
    path = os.path.join(SUBMIT, fname)
    if not os.path.exists(path):
        print(f"  {fname:34s} ⚠️ 文件不存在，跳过")
        return False
    old = open(path, encoding="utf-8").read()

    # 标记之外的内容会被 unpack 丢掉。用编辑器在文件末尾追加东西很容易踩到，
    # 而自检比的是 unpack 前后，看不见这种丢失，所以在这里显式拦一道。
    tail = old.rsplit(CLOSE, 1)[-1] if CLOSE in old else ""
    if len(tail.strip()) > 20:
        print(f"  {fname:34s} ⚠️ 最后一个 COPY 标记之后还有 {len(tail.strip())} 字符，"
              f"它们不在任何分条里、会被丢弃。请把这段移到标记内再跑。")
        return False

    body, refs = strip_refs(unpack(old))
    cited = cites_in(body)
    undefined, unused = sorted(cited - refs.keys()), sorted(refs.keys() - cited)
    if undefined:
        print(f"  {fname:34s} ⚠️ 正文引用了 {undefined}，但任何 References 块里都没有这几条")
    if unused:
        print(f"  {fname:34s} ❌ References 里的 {unused} 正文没引用，重排会把它们丢掉。"
              f"删掉这些条目或在正文里引用后再跑。")
        return False

    # 先按正文分条，再给每条补 References。补完超限的那条把末尾段落挪给下一条，
    # 只动这一条（压低全局装箱上限会把后面没引用的大段也切碎，11-09 试过从 5 条涨到 7 条）。
    posts = [attach_refs(p, refs) for p in merge_orphan_tail(spill(pack(segments(body)), refs), refs)]
    new, marked = render(desc, posts)

    # 无损自检：新文件解包、摘掉引用块后，正文和条目都必须和原来一致
    body2, refs2 = strip_refs(unpack(new))
    if re.sub(r"\s+", " ", body2) != re.sub(r"\s+", " ", body) or \
            {k: refs[k] for k in cited if k in refs} != refs2:
        print(f"  {fname:34s} ❌ 重排后内容对不上，已跳过不写。请报告这个文件。")
        return False

    over = [i + 1 for i, t in enumerate(marked) if len(t) >= LIMIT]
    longest = max((len(t) for t in marked), default=0)
    status = "✅" if not over else f"⚠️ 第 {over} 条超限"
    changed = new != old

    if check:
        print(f"  {fname:34s} {len(marked):2d} 条 · 最长 {longest:5d} · {status}"
              f" · {'会改写' if changed else '无变化'}")
        return bool(over)

    if changed:
        backup(path)
        open(path, "w", encoding="utf-8").write(new)
    print(f"  {fname:34s} {len(marked):2d} 条 · 最长 {longest:5d} · {status}"
          f" · {'已重排' if changed else '无变化'}")
    return bool(over)


def main():
    ap = argparse.ArgumentParser(description="00_提交/ 单源同步：就地重新分条 + 刷新网站")
    ap.add_argument("--check", action="store_true", help="只检查不写")
    ap.add_argument("--no-site", action="store_true", help="不重建网站")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)   # 否则子进程的输出会抢到前面

    if not preflight():
        return 1

    # 引用核对：审稿原文没被改过 + 每段引用出自对应审稿人。不拦同步（草稿期引用常常半截），只报。
    print("▸ 核对审稿原文与引用", flush=True)
    quotes_ok = subprocess.run([sys.executable, os.path.join(HERE, "check_reviews.py")]).returncode == 0
    print()

    print(f"▸ {'检查' if a.check else '重新分条'} 00_提交/")
    bad = sum(process(f, d, a.check) for f, d in JOBS)

    if not a.no_site and not a.check:
        print("\n▸ 重建网站 06_网站/index.html")
        r = subprocess.run([sys.executable, SITE], cwd=os.path.dirname(SITE))
        if r.returncode != 0:
            print("❌ 网站构建失败")
            return 1

    if bad:
        print(f"\n⚠️ 有 {bad} 份存在超限分条，贴之前先手工拆开。")
    if not quotes_ok:
        print("\n⚠️ 引用核对没过（见开头）。贴到 OpenReview 之前必须修好。")
    if not bad and quotes_ok:
        print("\n✅ 全部就绪。")
    return 0 if quotes_ok else 1


if __name__ == "__main__":
    sys.exit(main())
