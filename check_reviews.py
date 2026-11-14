#!/usr/bin/env python3
"""两道核对，sync.py 每次同步前也会跑。

    /usr/bin/python3 check_reviews.py

① REVIEWS.md 是不是 OpenReview 原文的逐字拷贝。
   文末「核对」表里的哈希是 2026-11-06 在浏览器里对 API 原文算的
   （字段压缩空白后 SHA-256 前 12 位）。这里对本地文件重算一遍，逐格比对。
   手抄、编辑器自动改引号、误删一句，都会让对应那格变 ✗。
   只比内容不比空白：审稿人原文里的行尾空格和 Tab 缩进在 markdown 里不可见，
   抄的时候保不住，也不影响意思。

② 00_提交/ 里每段引用审稿人的话，是不是出自**那位**审稿人。
   收件人张冠李戴是 rebuttal 的头号事故（../CLAUDE.md §4b）：把 wxGK 的原话
   贴进回 pSK8 的帖子，或者引用时顺手改了一个词，肉眼很难看出来。
   回复文件名里带审稿人 ID（`2_R2_wxGK.md`），引用块的第一行是 `> **W1a.** …`；
   每个引用块去掉标签后必须是该审稿人 review 的连续子串（同样压缩空白）。
   全局回复和 Summary 没有单一收件人，引用只要求出自三份里的任意一份。
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ["Paper Summary", "Critical Strengths", "Critical Weaknesses", "Questions For Authors"]


def h(text):
    norm = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]


def flat(text):
    return re.sub(r"\s+", " ", text).strip()


def check_hashes(body, table):
    expected = {}
    for row in re.findall(r"^\| (\w{4}) \| `(\w+)` \| `(\w+)` \| `(\w+)` \| `(\w+)` \|$", table, re.M):
        expected[row[0]] = dict(zip(FIELDS, row[1:]))

    bad, reviews = 0, {}
    for chunk in re.split(r"\n---\n", body):
        m = re.search(r"^## R\d · Reviewer (\w+)", chunk, re.M)
        if not m:
            continue
        who = m.group(1)
        got, texts = {}, []
        for title, sec in re.findall(r"^### (.+?)\n(.*?)(?=^### |\Z)", chunk, re.M | re.S):
            if title in FIELDS:
                got[title] = h(sec)
                texts.append(sec)
        reviews[who] = flat(" ".join(texts))
        for f in FIELDS:
            want = expected.get(who, {}).get(f)
            ok = want is not None and got.get(f) == want
            bad += not ok
            if not ok:
                print(f"  ✗ {who}  {f:22s} {got.get(f, '缺')}  vs  API {want}")
    print(f"① REVIEWS.md 与 API 原文：{len(reviews)} 份 × {len(FIELDS)} 字段，"
          + ("全部一致" if not bad else f"{bad} 格对不上"))
    return bad, reviews


# 引用块：连续的 `>` 行；第一行以 `**标签.**` 开头的才算「引用审稿人」。
# 参考文献也用 `>`，但不以粗体标签开头，所以不会被误抓。
QUOTE_RE = re.compile(r"(?:^>.*\n?)+", re.M)
LABEL_RE = re.compile(r"\*\*([\w.\- ]+?)\.?\*\*(?:\s*\((?:[^)]*)\))?\s*")


def check_quotes(reviews):
    bad = n = 0
    for f in sorted((HERE / "00_提交").glob("*.md")):
        owner = next((who for who in reviews if who in f.name), None)
        pool = {owner: reviews[owner]} if owner else reviews
        text = f.read_text(encoding="utf-8")
        for block in QUOTE_RE.findall(text):
            lines = [re.sub(r"^> ?", "", ln) for ln in block.rstrip("\n").split("\n")]
            # 一个引用块里可能并排放 W 和 Q（`> **W1.** …` 空引用行 `> **Q1.** …`），逐段拆开查
            for para in re.split(r"\n\s*\n", "\n".join(lines)):
                m = LABEL_RE.match(para.strip())
                if not m:
                    continue
                label, quote = m.group(1), flat(para.strip()[m.end():])
                # 全局回复里 `> **Tery.** …` 这种以审稿人 ID 为标签的，只在那一位的 review 里找
                src = {label: reviews[label]} if label in reviews else pool
                # 我们自己在引用里加的省略号：只要每一截都在原文里就算过
                pieces = [p.strip() for p in re.split(r"\s*(?:\[…\]|\[\.\.\.\]|…)\s*", quote) if p.strip()]
                if not pieces:
                    continue
                n += 1
                hit = [who for who, txt in src.items() if all(p in txt for p in pieces)]
                if not hit:
                    bad += 1
                    where = f"{'/'.join(src)} 的 review" if len(src) == 1 else "三份 review"
                    print(f"  ✗ {f.name} · {label}：在{where}里找不到这段原文")
                    print(f"      「{quote[:90]}{'…' if len(quote) > 90 else ''}」")
    print(f"② 00_提交/ 里引用审稿人原话 {n} 处：" + ("全部出自对应审稿人" if not bad else f"{bad} 处对不上"))
    return bad


def main():
    text = (HERE / "REVIEWS.md").read_text(encoding="utf-8")
    body, _, table = text.partition("## 核对")
    bad1, reviews = check_hashes(body, table)
    bad2 = check_quotes(reviews) if (HERE / "00_提交").is_dir() else 0
    print("\n✅ 两道核对都通过" if not (bad1 or bad2) else "\n❌ 有对不上的，见上")
    return 1 if (bad1 or bad2) else 0


if __name__ == "__main__":
    sys.exit(main())
