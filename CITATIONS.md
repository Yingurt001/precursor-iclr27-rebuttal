# rebuttal 期新增引用的用途表

**只登记 rebuttal 期新引的。** 投稿时就在引的，以冻结版 PDF 的参考文献表为准
（bib 源在 `../../5_Submission/_overleaf_6aaa95c6/references.bib`，提交后合作者可能改过 key，引之前对一下）。

| key | 用途（在哪个回答里干什么） | 对应意见 | 已入库 | 已读 |
|---|---|---|---|---|
| `gretton2012kernel`（待建） | pSK8 回复 §6：核检验的 MMD 统计量和中位数带宽 | R3-7 | ✗ | ✗ |
| `tatbul2018precision`（待建） | pSK8 回复 §2：range-based P/R，审稿人点名 | R3-3 | ✗ | ✗ |
| `vovk2005algorithmic`（待建） | pSK8 回复 §14：可交换性下 conformal p 值有效 | R3-15 | ✗ | ✗ |
| `lei2018distribution`（待建） | pSK8 回复 §14：split-conformal | R3-15 | ✗ | ✗ |
| `huet2022local`（已在 bib） | pSK8 回复 §2：affiliation | R3-3 | 投稿时已引 | — |
| `paparrizos2022vus`（已在 bib） | pSK8 回复 §2：VUS | R3-3 | 投稿时已引 | — |

## 可能要新增的（11-06 查 `references.bib` 时发现缺）

| 文献 | 为什么可能要 | 现状 |
|---|---|---|
| Tatbul et al. 2018，range-based precision / recall | pSK8 W1b / Q4b 点名 range-based；他原文还留了「#todo Tatbul」 | bib 里**没有**（有 VUS `paparrizos2022vus`、affiliation `huet2022local`、`wagner2023timesead`） |
| split-conformal / 可交换性的原始出处 | pSK8 m4：event-placebo exchangeability「没有引用」 | bib 里**没有**任何 conformal 条目 |

**引之前必须读过。** 不引没读过的论文，这是审稿人最容易一问就露的地方。

## 新增文献走完五步，一步都不能跳

```
① 进文献库    bash ../../_Literature/_tools/ingest-paper.sh <PDF> <paper_key> "<标题>" "<作者>" "<出处>"
② 写 library.bib          （上一步自动做掉）
③ 建项目文献笔记          ../../4_Precursor Notes/项目文献笔记/<key>/NOTE.md　← 要引就得先读
④ 登记本表                这条引用在哪个回答里干什么用
⑤ 进修订稿的 references.bib（Overleaf，先 git fetch）
```

**不建 `rebuttal_temp_papers/`。**「临时」是文献需求的状态，不是 PDF 的存储位置。
