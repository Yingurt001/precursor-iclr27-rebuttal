# Precursor ICLR 2027 Rebuttal · 总控

> 建于 2026-11-06（审稿放出当天）。结构照 `Klein++/6_Rebuttal/neurips_2026/`，
> 文件命名和 `Klein++/6_Rebuttal/iclr_2027/`（KNN++ 同一届）对齐。
> 进本目录先读：`SUBMISSION_POINTER.md` → `TRACKER.md` → 本文件。写回复前读 `../rules/GLOBAL_REBUTTAL_RULES.md` 全文。

## 一、现状

《When Early Is Not Early: The Precursor Illusion in Time-Series Anomaly Detection》，投稿 #32929，
forum `giZMDfJFwO`（https://openreview.net/forum?id=giZMDfJFwO）。张赢二作。

| 审稿人 | Rating | Confidence | 一句话 |
|---|---|---|---|
| **Tery** | **3** Weak acceptance | **1** | 自称没资格审、已告知 AC；夸可读性「best in my batch」和 RQ 框架；只问 Σ̃ 和 placebo-calibrated 是什么 |
| **wxGK** | **3** Weak acceptance | 3 | 夸三问分离和 PA 记功的受控隔离；要检验效度（3W 漂移、PSM / SWaT 边界偏移）和负结果的解读（聚合 / 训练配置、功效） |
| **pSK8** | **1** Clear rejection | 4 | presentation 打 1；技术贡献有限（检验的选择没验证、MPA 没和 range / affiliation / VUS 比）；**写明 presentation 实质改善就改 weak reject** |

均分 2.33。量表已知 1 = Clear rejection、2 = Weak rejection（KNN++ 那篇见到）、3 = Weak acceptance，最高几分没核到。
截至 11-06 论坛里没有 AC 评论。

## 二、时间线（iclr.cc/Conferences/2027/AuthorGuidelines，11-06 读取；OpenReview invitation 11-06 读取）

| 日期 | 事 |
|---|---|
| 11-05 | 审稿放出（我们这三条的 mdate 是 11-06 12:28 UTC） |
| **11-18 AoE** | 讨论期结束；**修订稿最后上传**（`Rebuttal_Revision` 截止 = 11-19 11:59 UTC = 11-19 11:59 英国时间）。讨论期正文上限 **10 页**，严格执行；系统自动出 pdfdiff |
| 11-19～12-16 | 审稿人和 AC 闭门讨论 |
| 12-16 | 放榜 |

作者指南原话要点：审稿人和 AC **不必读每一版修订**、可以忽略「与原稿差别很大」的改动，所以**改了什么必须在回复里说清**。单条评论有字数上限、条数不限。

## 三、要交的东西

OpenReview 上作者能用的入口只有两个（11-06 从 invitation 接口读到）：

- **`Official Comment`**：单条 **5000 字符**、支持 markdown。readers 必选 PC + SAC，可选 AC / 全体审稿人 / 单个审稿人 / 作者。**没有 Everyone 选项**，讨论期内并不公开。
- **`Rebuttal_Revision`**：上传修订稿 PDF + 补充材料，可改 title / abstract。

| # | 入口 · 发在哪 · readers | 唯一源 | 状态 |
|---|---|---|---|
| 0 | `Official Comment` · 论坛顶层 · AC + 全体审稿人 | `00_提交/0_全局总回复.md` | 骨架 |
| 1 | `Official Comment` · Tery 的 review 下 · AC + 全体审稿人 | `00_提交/1_R1_Tery.md` | 骨架 |
| 2 | `Official Comment` · wxGK 的 review 下 · 同上 | `00_提交/2_R2_wxGK.md` | 骨架 |
| 3 | `Official Comment` · pSK8 的 review 下 · 同上 | `00_提交/3_R3_pSK8.md` | 骨架 |
| 4 | `Official Comment` · 论坛顶层 · Summary of Revisions（修订稿传完后发） | `00_提交/4_Summary_of_Revisions.md` | 骨架 |
| 5 | `Rebuttal_Revision` · 修订稿 PDF（10 页） | `../../5_Submission/_overleaf_6aaa95c6/`（**改之前先 `git fetch`**，合作者也在改） | — |

readers 建议选「AC + 全体审稿人」：让 wxGK 看到我们怎么回 pSK8，反过来也一样，交叉点只需讲一遍。这是建议，发之前作者定。

## 四、工作流：改 → 跑一下 → 复制（与 Klein neurips_2026 相同）

```
改 00_提交/*.md                    ← 唯一源，忽略分条标记，当一整篇写
        ↓  /usr/bin/python3 sync.py      （或双击 同步.command）
   ① 解包 → 按 5000 字符重新分条 → 写回同一文件（改前版本进 00_提交/.bak/，留 10 份）
   ② 重建 06_网站/index.html（左边线程树 + 审稿原文 + 每条帖子字数）
   ③ 报字符数 / 超限告警
```

- `sync.py --check` 只检查不写；`--no-site` 不重建网站。
- 复制规则：每条只复制 `▼▼▼ COPY FROM HERE ▼▼▼` 和 `▲▲▲ COPY TO HERE ▲▲▲` 之间的部分，**倒序发帖**（最后一条先发），页面才会正序显示。
- 工作台端口 **8778**（Klein 的是 8777，两边能同时开）。
- 用 `/usr/bin/python3` 跑：anaconda 的 python3 曾经一启动就被杀（记忆 `env_python3_killed`）。

## 五、提交前必须过的三道检查

1. `/usr/bin/python3 check_reviews.py` —— REVIEWS.md 仍与 API 原文逐字一致（引用审稿人原话都从这里抄）。
2. **念出声核对**（`../CLAUDE.md` §4b）：`reviewer ID ↔ 分数 ↔ 文件名 ↔ 发在哪条 review 下 ↔ 正文 W/Q 内容`，五者一致才发。
3. `../rules/GLOBAL_REBUTTAL_RULES.md` 的提交前 checklist + 黑名单 grep。

## 六、文件夹

```
iclr_2027/
├── README.md                 ← 英文概览（GitHub 首页）
├── OVERVIEW.zh.md            ← 本文件，中文总控
├── SUBMISSION_POINTER.md     ← 审稿人看的是哪一版（冻结 PDF + 补充材料）
├── REVIEWS.md                ← 三份审稿逐字原文（含 LaTeX），文末带核对哈希
├── check_reviews.py          ← 重算哈希，核对 REVIEWS.md 没被改过
├── TRACKER.md                ← 一条意见一行（24 行），类型初判 + 关联到回顾和 AAAI 旧账
├── 00_rebuttal前回顾_2026-11-04.md  ← 放分前的自查：数字口径、措辞问题、能快速补的 7 件事
├── 00_提交/                   ← 唯一源，改这里也从这里贴
├── sync.py · 同步.command      ← 重新分条 + 重建网站
├── 06_网站/                   ← 本地工作台（build_site.py 读 ../REVIEWS.md + ../00_提交/）
├── evidence_packets/         ← 论文全文_抽取.txt（带页边行号，grep 用）+ 每个数字的出处核对
├── new_results/              ← rebuttal 期新实验的**指针**（实验本身走 ../../3_Experiments/ 立 E-nnn）
├── MANUSCRIPT_CHANGES.md     ← 回复里承诺的正文修改，一条一行
├── CITATIONS.md              ← rebuttal 期新增引用
└── _archive/
```

与 `../aaai_2027/` 的差别：那次 Phase 1 直接拒、没有 rebuttal 窗口，那边的 TRACKER 是改投清单。
它的 25 条在本届 TRACKER 的「关联」列里按 `AAAI R1-W1` 这样引用。

## 七、下一步

1. 张赢（和学姐）过一遍 `TRACKER.md`，定每条的处置：补跑 / 澄清 / 承认 / 改稿。
2. 规则库和 Klein 上游有漂移（11-06 跑 `_tools/check-rebuttal-rules.sh`：`GLOBAL_REBUTTAL_RULES.md` 本地 327 行 vs 上游 383 行，`UPDATE_PROCESS.md` 88 vs 196），起草前先看 diff 决定拿不拿。
3. 要跑东西的几条（R2-1、R2-2、R2-3、R3-2、R3-11），按项目规矩先写三行再开 `E-nnn`；回顾 §4.4 #1 已经算好的（SMD 7 格内 BH）可以直接用。
4. pSK8 的涨分只看修订稿：先定 presentation 改哪几处，再写回复。
