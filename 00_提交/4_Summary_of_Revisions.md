# Summary of Revisions（Official Comment，论坛顶层，修订稿传完后发） — 提交版

> **这个文件就是源，直接改它。** 改完在 `6_Rebuttal/iclr_2027/` 跑 `/usr/bin/python3 sync.py`（或双击 `同步.command`），
> 会自动按 OpenReview 上限重新分条并刷新网站。改前的版本存在 `00_提交/.bak/`。
> 改的时候**忽略分条标记**，把它当一整篇看就行 —— 重跑脚本会重新切。
> 引用：正文写 `[a]` / `[a, Thm. 9]`；新条目随便写进任何一个 `# References` 块（`> [a] 论文标题`），
> 脚本会给每条帖子末尾补上这条帖子引过的条目，各帖里的 References 不用手动维护。
>
> 用 OpenReview 的 `Official Comment` 发：审稿人回复发在对应 review 下，0 号发在论坛顶层。单条上限 5000 字符，当前共 1 条。
> **发帖顺序：1/1 倒序贴**，页面才会正序显示。
> 每条只复制 `▼▼▼ COPY FROM HERE ▼▼▼` 与 `▲▲▲ COPY TO HERE ▲▲▲` 之间的内容，不含标记行。


---

## 第 1/1 条 · 2898 字符

▼▼▼ COPY FROM HERE ▼▼▼

# Summary of Revisions in the Updated Manuscript

We have uploaded the revised manuscript, and the pdfdiff on OpenReview shows every change. The main text stays within 10 pages, and new results are in the appendix with a pointer from the main text. The changes, with the reviewers who asked for them, are listed below.

**Validity of the test**

- **Local normal reference on 3W in App. B.1.2.** We now report the detections on all 47 records with the placebo null built from the last 300, 900 or 1800 seconds of normal operation before each transition (wxGK).
- **Alternative detection mechanisms in App. B.1.3.** We now compare the test with Online Kernel CUSUM, MMDEW and TS2Vec on 3W and on the five benchmarks (pSK8).
- **Counterfactual ablation in App. B.1.4.** We now report how removing the detected level and trend changes the test and nine models on 3W (pSK8).
- **Real 3W series in App. B.2.1.** We now show raw signals, annotated stages and flagged windows, including records with many rejections during normal operation (wxGK, pSK8).
- **Onset continuity for PSM and SWaT in App. B.2.3.** Tab. 8 now includes PSM and SWaT (wxGK).
- **Rejection rates by lead in Table 2 and §4.2.** We now report leads of 10, 50, 100 and 200 steps and the 3W rates at every lead (pSK8).

**Model results and metrics**

- **Aggregation and training in App. B.4.3 and App. B.4.5.** We now report paired changes of aggregation with fixed scores, events and controls, pooled against per-machine training under the same budget, and the effect of the normal reference (wxGK).
- **Excluded effect sizes in the abstract, §4.3 and App. B.4.1.** We now report the machine-level bound and the equivalence analysis next to the significance results (wxGK).
- **MPA and existing metrics in App. B.5.5 and App. B.5.6.** We now compare MPA with Window-F1, Range-F1, Affiliation-F1 and VUS in a controlled setting and on 3W (pSK8).

**Presentation**

- **Definitions in the abstract, §1, §3.1 and §3.2.** We now define onset, placebo calibration, the rejection rate with its formula and both exchangeability assumptions with references, and give the regularized covariance below Eq. 1 (Tery, pSK8).
- **Reasoning of the test in §3.2 and App. A.2.** We now explain why the test checks local changes and deviation from normal operation together (pSK8).
- **Research questions in §4.** We now answer RQ1 to RQ3 at the end of their results (pSK8).
- **Morphologies and eligibility in §4.1, §3.1 and §4.2.** We now explain the five morphologies of Fig. 3(a) and the eligibility criterion with the excluded events per dataset (pSK8).
- **Wording.** We now avoid the wording causal detector (pSK8).

**New resource**

- **DeviceWarning-162 in App. C.** We now describe a dataset of 162 events on 48 devices with 207 normal reference sequences, released as supplementary material, and report RQ1 to RQ3 on it in App. C.5 (pSK8).

▲▲▲ COPY TO HERE ▲▲▲
