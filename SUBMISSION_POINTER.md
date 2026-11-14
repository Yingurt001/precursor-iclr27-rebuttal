# 审稿人看的是哪一版

**rebuttal 期的一切引用（页码、行号、章节号、表号）都以这份快照为准。**

```
../../5_Submission/iclr2027_frozen/2026-09-26_iclr27_submitted/   （只读）
├── 32929_When_Early_Is_Not_Early_.pdf      ← ⭐ 审稿人手上的正文，22 页，09-26 10:38 BST 编译
├── 2026-09-26_supplement_submission.zip    ← 补充材料（代码 + README）
└── README.md                               ← 冻结说明
```

| 文件 | sha256 前 16 位 | 说明 |
|---|---|---|
| `32929_When_Early_Is_Not_Early_.pdf` | `20ec5c90e0092188` | 与 `~/Downloads/` 原件一致（11-04 冻结时核过） |
| `2026-09-26_supplement_submission.zip` | `c78876b5e252305f` | **是否就是 OpenReview 上那份还没核**（要下载 OpenReview 附件比对，下载前先问张赢） |

grep 用的全文：`evidence_packets/论文全文_抽取.txt`（`pdftotext -layout`，每行开头是 PDF 页边行号）。

## ⛔ 不要拿工作副本回答

| 东西 | 位置 | 和提交版的关系 |
|---|---|---|
| Overleaf 本地 clone | `../../5_Submission/_overleaf_6aaa95c6/`，HEAD `7d83337` | **比提交版早约 6.5 小时**，句级差约 40 处，原 Table 3、4 合并，后面表号都减 1。改修订稿从这里出发，但对审稿人说的行号表号一律查冻结 PDF |
| `../../5_Submission/iclr2027/` | 连的是**旧** Overleaf 项目 `6aa18524…`，停在 09-14 | 数字是旧的，别用 |
| 学姐版本 | `../../5_Submission/学姐版本/` | 数值一致，结构和摘要主线不同（回顾 §3） |

## 提交版数字（旧值不要再用）

| 量 | 旧值 | 提交版 |
|---|---|---|
| 事件数 | 538 / 496 / 69 | **537 / 500 / 70** |
| Detection F1，无 PA → PA | 0.186 → 0.549 | **0.179 → 0.551** |
| Shifted F1，无 PA → PA | — | **0.036 → 0.177** |

## 提交事实

| | |
|---|---|
| 会议 | ICLR 2027 |
| Submission Number | 32929 |
| Forum | https://openreview.net/forum?id=giZMDfJFwO |
| 作者顺序 | Yue Yang · Ying Zhang · Yiwen Yan · Chen Zhang |
| Primary area | datasets and benchmarks |
| 提交后 | 09-26 提交；10-05 有一次 Edit（mdate），内容是否变过未核 |
