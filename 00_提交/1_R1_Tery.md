# 回复 Reviewer Tery（Rating 3 / Conf 1；placebo 是什么 / Eq. 1 的 Σ̃） — 提交版

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

## 第 1/1 条 · 2896 字符

▼▼▼ COPY FROM HERE ▼▼▼

We thank Reviewer $\color{red}{\text{Tery}}$ for the kind words on the readability of the paper and on stating the research questions from the outset. We respond to the concerns as follows.

*Line, table and section numbers refer to the submitted PDF.*

# 1. Meaning of placebo-calibrated
The reviewer is right that the abstract (l.015) and the contributions (l.085) use the term before §3.2 defines it. The revision defines it at its first use in the abstract and again at the start of §3.2, in the terms below.

**1. Placebo windows.** A placebo is a pseudo-onset placed inside normal operation of the same entity, at least $H _{\text{guard}}$ steps away from every annotated event (l.156, l.205). At each pseudo-onset we compute the same statistic $T$ on windows of the same length as at a real onset. The placebo statistics therefore show how large $T$ becomes when no event follows.

**2. Calibration.** The p-value of an event is the rank of its statistic among the placebo statistics of its entity (Eq. 2),

$$p _{e,\ell} = \frac{1 + \sum _{m=1} ^{M _0} \mathbb{1}\big[T ^{(0)} _{i,m} \ge T _{e}\big]}{M _0 + 1},$$

and the event counts as precursor-positive when $p _{e,0} \le 0.05$. A held-out set of normal windows, used neither to fit the descriptors nor to build the null, measures how often the same rule rejects a window that precedes no event (l.211–213). This placebo rejection rate is 0.034 to 0.047 on the five benchmarks (Tab. 2), and every event rejection rate is read against it. On SMD, for example, the test rejects 15.9% of events and 4.7% of held-out normal windows.

# 2. The matrix in Eq. 1
Yes, $\tilde{\Sigma} _{i}$ is a covariance matrix. It is the covariance of the 12-dimensional descriptor vector $\phi$ over the normal-only fit windows of entity $i$, regularized for numerical stability as

$$\tilde{\Sigma} _{i} = (1-\lambda)\,\hat{\Sigma} _{i} + \lambda\,\operatorname{diag}(\hat{\Sigma} _{i}) + \rho I, \qquad \lambda = 0.10, \quad \rho = 10 ^{-6}.$$

$T _{\text{dev}}$ in Eq. 1 is thus the Mahalanobis distance of the candidate window from the normal regime of its entity. The submission names the matrix in one clause before Eq. 1 (l.195), gives the formula only in App. A.2 (l.692–693) and the constants in Tab. 1 (l.291). The revision states the formula and the constants directly below Eq. 1.

# Summary of revisions
- **Placebo calibration in the abstract and §3.2.** We now define placebo windows and the held-out placebo rejection rate at their first use.
- **Covariance in Eq. 1.** We now give the regularized covariance and its constants directly below Eq. 1.

Following your suggestions, we will include these clarifications in the revised version. We hope these responses address your questions, and we would be grateful if you would take them into account in your assessment. We are happy to clarify anything further during the discussion period.

▲▲▲ COPY TO HERE ▲▲▲
