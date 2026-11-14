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

## 第 1/1 条 · 2627 字符

▼▼▼ COPY FROM HERE ▼▼▼

# Summary of Revisions in the Updated Manuscript

〔改稿还没动：下面是回复里承诺的改动，等你批了清单、改完 tex 再按实际落点核一遍〕

We have uploaded the revised manuscript, and the pdfdiff on OpenReview shows every change. The main text stays within 10 pages, and new results are in the appendix with a pointer from the main text. The changes, with the reviewers who asked for them, are listed below.

**Validity of the test**

- **Descriptor-free kernel test in App. B.2.** We now compare the descriptor test with a kernel test on all benchmark events and 3W transitions (pSK8).
- **Sensitivity under the corrected split in App. B.2.** We now report each setting of Tab. 1 varied one at a time, with the overlap of the SMD P sets (pSK8).
- **3W control in §4.1, App. B.1.2 and §5.** We now report the detection of transition starts against the adjacent normal hour, controls at matched distance from long normal records, and the limits of detections far from the normal reference (wxGK).
- **Onset continuity for PSM and SWaT in App. B.2 and §4.2.** We now report the check of Tab. 8 for all benchmarks with P events (wxGK).
- **Absolute rejection rates in App. B.2 and Fig. 4.** We now report the rejection rate for every dataset and lead, including 3W (pSK8).
- **Window length in §4.2 and App. A.3.** We now state the eligibility criterion, the number of events per pre-onset span, and the results at longer spans (pSK8). 〔待定③〕

**Model results and metrics**

- **Training and aggregation in §4.3 and App. B.3.** We now isolate the two factors with a fixed event set and normal reference, and revise the contributions, limitations and conclusion accordingly (wxGK).
- **Excluded effect sizes in the abstract and §4.3.** We now state the upper bounds and the minimum detectable MPA with every significance result (wxGK).
- **Onset-truncated AUC in §4.3 and App. B.3.** We now compare MPA with a threshold-free AUC that excludes late detections (pSK8).

**Presentation**

- **Definitions in the abstract, §1 and §3.** We now define every non-standard term at its first use, including exchangeability with references and the rejection rate with its formula (Tery, pSK8).
- **Reasons for design decisions in §3–4.** We now state the reason where each decision is made, and Fig. 3(a) shows all eight morphologies (pSK8).
- **Research questions in §4.** We now end each results section with the answer to its research question (pSK8).
- **Real-series examples in App. B.2.** We now show nine randomly drawn events and 3W transitions (pSK8).
- **Wording.** We now write online instead of causal, and distinguish precursor evidence from early detection in §3.1 (pSK8).

▲▲▲ COPY TO HERE ▲▲▲
