# ICLR 2027 #32929 rebuttal 工作台（两位作者共享的私有仓库）

**读者是人和 Claude。** 回复 3 位审稿人 + 全局回复 + Summary of Revisions 的草稿都在这里。截止 **11-18 AoE**。

## 唯一源

`00_提交/` 里每份 md 就是一位审稿人的回复（`0_全局总回复` · `1_R1_Tery` · `2_R2_wxGK` · `3_R3_pSK8` · `4_Summary_of_Revisions`）。
网页工作台、分帖都从这里生成，只改这里。

## 怎么改（每次都按这个顺序）

1. `git pull`
2. 改 `00_提交/*.md` 里 `▼▼▼ COPY FROM HERE ▼▼▼` 和 `▲▲▲ COPY TO HERE ▲▲▲` 之间的正文。
   「第 n/m 条」、续接句、帖子边界都不用管，脚本会按 OpenReview 5000 字符上限重新切。
3. 跑 `python3 sync.py`（Mac 上也可以双击 `同步.command`）。看到「✅ 全部就绪」才算好；看到 ❌ 先修。
4. 看网页：`python3 06_网站/serve.py 8778`，打开 http://localhost:8778/index.html。
   网页里也能直接改字，但那些改动只存在自己电脑上、不进 git，**以 md 为准**。
5. `git add 00_提交 …` → `git commit` → `git push`

## 分工、同步与批注

- 协作者在自己的分支上改：`git switch -c <名字缩写>/<主题>`，push 后开 Pull Request。
- 仓库主人在 PR 里看改动、留言、合并到 `main`。
- **批注**：在 GitHub 的 PR 页面点「Files changed」，在某一行左边点「+」就能留言；两人都能回复，讨论完点 Resolve。
- 两人别同时改同一节。动手前在 PR 或聊天里说一声，可以少很多冲突。

## 写法规矩（全文见 `参考/GLOBAL_REBUTTAL_RULES.md`）

- 每一节的结构：`# n. 标题` → 第一段先感谢，再说我们查了什么 → `**1. Experiment.**` 一段讲做了什么 → `**2. Results.**` 一句结论 + 一张短表 + 一段解释，最后一句交代论文怎么改。
- 表：表题写在表上方，形如 `Table A- …`，一两行；表字母在几份回复里连续编号（现在 wxGK 用 A–D，pSK8 用 E–J）。
- 正文不用冒号、破折号、问号，不引审稿人原话。
- 行号、表号一律指投稿版 PDF：`参考/32929_When_Early_Is_Not_Early_.pdf`；带行号的全文在 `evidence_packets/论文全文_抽取.txt`。
- 新数字必须能追到实验：`new_results/README.md` 列了每个数字来自哪个实验（实验本身在仓库主人本地，不在这个仓库里）。

## 其他文件

| 文件 | 是什么 |
|---|---|
| `REVIEWS.md` | 审稿意见原文（逐字，带核对哈希，别改） |
| `TRACKER.md` | 每条意见一行：怎么处理、证据在哪、状态 |
| `MANUSCRIPT_CHANGES.md` | 回复里答应要改的论文正文清单（论文 tex 不在这个仓库） |
| `CITATIONS.md` | 回复里新引的文献 |
| `参考/` | 投稿版 PDF 和写作规则的快照，只读 |

不进仓库的：备份 `.bak/`、生成的网页 `06_网站/index.html`、网页里的本地改动 `06_网站/edits/`。
