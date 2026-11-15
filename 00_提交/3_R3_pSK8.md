# 回复 Reviewer pSK8（Rating 1 / Conf 4；技术贡献 / 指标 / presentation / 7 条 minor） — 提交版

> **这个文件就是源，直接改它。** 改完在 `6_Rebuttal/iclr_2027/` 跑 `/usr/bin/python3 sync.py`（或双击 `同步.command`），
> 会自动按 OpenReview 上限重新分条并刷新网站。改前的版本存在 `00_提交/.bak/`。
> 改的时候**忽略分条标记**，把它当一整篇看就行 —— 重跑脚本会重新切。
> 引用：正文写 `[a]` / `[a, Thm. 9]`；新条目随便写进任何一个 `# References` 块（`> [a] 论文标题`），
> 脚本会给每条帖子末尾补上这条帖子引过的条目，各帖里的 References 不用手动维护。
>
> 用 OpenReview 的 `Official Comment` 发：审稿人回复发在对应 review 下，0 号发在论坛顶层。单条上限 5000 字符，当前共 4 条。
> **发帖顺序：4/4 → 3/4 → 2/4 → 1/4 倒序贴**，页面才会正序显示。
> 每条只复制 `▼▼▼ COPY FROM HERE ▼▼▼` 与 `▲▲▲ COPY TO HERE ▲▲▲` 之间的内容，不含标记行。


---

## 第 1/4 条 · 4712 字符

▼▼▼ COPY FROM HERE ▼▼▼

We thank Reviewer $\color{green}{\text{pSK8}}$ for finding the problem very interesting and understudied, for reading the paper several times, and for stating concretely which changes would improve the presentation. We respond to the concerns as follows.

*Line, table and section numbers refer to the submitted PDF, and "answer N" refers to the numbered sections of this response. Tables are lettered after those of the response to Reviewer wxGK (A–D).*

# 1. Validation of the choices in the precursor detectability test
We thank the reviewer for this concern. We checked whether the conclusions of the test depend on its choices, all of which Tab. 1 fixes before any benchmark is evaluated. We therefore ran the checks below.

**1. Checks.** Each check probes the choices in a different way. Synthetic series with known answers measure how often the test fires without a precursor and how often it finds an injected one (Tab. 5). On the benchmarks we changed each setting of Tab. 1 on its own, keeping the others fixed, and recorded how many events the test flags and whether each dataset has more flagged events than its placebo rate. A kernel test that uses no descriptors replaces the descriptor family itself (answer 6).

**2. Results.** The dataset-level conclusions do not depend on any single choice (Table E).

Table E- Precursor-positive events when one setting of Tab. 1 is changed (five benchmarks; overlap = SMD events flagged in both settings divided by those flagged in either)
| **Setting** | Events flagged | Overlap on SMD |
| :--- | :---: | :---: |
| Primary (Tab. 1) | 70 | 1.00 |
| Scales {10, 25} / {50, 100} | 90 / 60 | 0.49 / 0.48 |
| Pool 200 / 400 | 86 / 72 | 0.67 / 0.75 |
| Shrinkage 0.01 / 0.50 | 73 / 71 | 0.79 / 0.91 |
| Guard 0 / 100 | 68 / 72 | 0.84 / 0.73 |
| Normal-only channel ranking | 70 | 0.92 |
| Three added descriptors | 71 | 1.00 |

On synthetic series the test fires on 6.0% of precursor-free events [4.2%, 8.4%], and at full strength it finds seven of the eight injected shapes with power above 0.95, the hardest being nonlinear dependence at 0.79. On the benchmarks the number of flagged events stays between 60 and 90 in every setting, and in every setting SMD, PSM and SWaT have more flagged events than their placebo rate while MSL and SMAP do not. Which SMD events are flagged changes most with the window scale, since shorter windows pick up shorter deviations, so the revision reports counts at the dataset level and states the scale with every count. The kernel test of answer 6 flags 36 of the 500 benchmark events, fewer than the descriptor test. The submission states the sensitivity result at l.396 without a table, and the only robustness file in its supplementary material predates a later correction of the calibration split, so the revision adds Table E to App. B.2, replaces that file, and points to all three checks from §3.2.

# 2. Comparison with range-based, affiliation and VUS metrics
We agree that these metrics can be adapted, and we followed the reviewer's suggestion. Range-based precision and recall of Tatbul et al. [b], the affiliation metrics of Huet et al. [c] and VUS of Paparrizos et al. [d] score alarms or scores against the annotated anomaly range, which begins at onset, so a detector earns credit by responding after onset. MPA asks whether scores in the pre-onset window exceed scores in matched normal windows. To exclude late detections, we computed a threshold-free ROC AUC whose positives are only the 100 points before onset of the P events, so no post-onset point can earn credit. The revision adds this comparison to §4.3 and App. B.3.

**1. Truncation changes the ranking of detectors.** On SWaT, the AUC with all anomaly points as positives ranks iForest, DAGMM and LSTM-VAE highest, and truncation at onset brings all three to or below chance (Table F).

Table F- Point-wise ROC AUC on SWaT against normal points, with all anomaly points or only the 100 points before onset of the P events as positives (scores of Tab. 3)
| **Model** | All anomaly points | **Before onset only** |
| :--- | :---: | :---: |
| iForest | 0.836 | 0.507 |
| DAGMM | 0.815 | 0.422 |
| LSTM-VAE | 0.797 | 0.372 |

# References

> [b] Nesime Tatbul, Tae Jun Lee, Stan Zdonik, Mejbah Alam, and Justin Gottschlich. Precision and Recall for Time Series. NeurIPS, 2018.
>
> [c] Alexis Huet, José Manuel Navarro, and Dario Rossi. Local Evaluation of Time Series Anomaly Detection Algorithms. KDD, 2022.
>
> [d] John Paparrizos, Paul Boniol, Themis Palpanas, Ruey S. Tsay, Aaron J. Elmore, and Michael J. Franklin. Volume Under the Surface: A New Accuracy Evaluation Measure for Time-Series Anomaly Detection. PVLDB, 2022.

*(Continued in 2/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 2/4 条 · 4585 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 1/4.)*

**2. Agreement with MPA.** Across the seven detectors, the onset-truncated AUC ranks the detectors as MPA does, with Spearman correlation 0.96 on SMD and 0.93 on PSM, and 0.67 on SWaT with its 9 P events. Adapted to exclude late detections, this metric family therefore reaches the conclusion of MPA, and unadapted it measures post-onset response.

# 3. Definitions of non-standard terms
The reviewer is right that several terms are used before they are defined. The revision defines each at its first use, as Table G lists.

Table G- Terms and where the revision defines them
| **Term** | Definition | Where |
| :--- | :--- | :--- |
| Onset $t _{e}$ | first step of the annotated anomaly $A _{e}$ | abstract, §1 |
| Pre-onset interval | $P _{e}(W) = [t _{e}-W, t _{e})$ | §1, §3.1 |
| Placebo, placebo rate | pseudo-onset in normal operation, held-out rejection rate | abstract, §3.2 |
| P, I, O events | evidence before onset, only after onset, neither | §3.2 |
| Exchangeability | answer 14 | §3.2, §3.3 |
| Selection control | flagged normal windows (answer 8) | §3.3 |
| Benchmark warnability | share of events with detectable pre-onset evidence | §1 |
| Online score (was causal) | $s _{i}(t) = f(x _{1:t})$ | §3.1 |

# 4. Reasons for design decisions
The reviewer is right that several decisions appear without their reason, or with the reason in an appendix that the main text does not point to. The revision states the reason where each decision is made, including the three below.

**1. Five of eight morphologies in Fig. 3.** Tab. 5 in App. B.1.1 reports all eight. The revision plots all eight in Fig. 3(a) and names Tab. 5 in the §4.1 setup.

**2. A window of 100 steps.** It is the longest window that keeps nearly all events evaluable (answer 17).

**3. Scales of 25 and 50 steps.** The candidate and reference windows of the larger scale together span the 100-step window used for MPA, so both analyses see the same interval (l.177–178).

# 5. Windows after onset
It is possible, and the test already evaluates this interval, but it measures early detection rather than precursors. Setting $P _{e}(W) = [t _{e}, t _{e}+W)$ asks how quickly an anomaly becomes visible after it starts, which is early detection. A precursor is evidence before $t _{e}$, which is the condition an early-warning benchmark needs. The test already evaluates the reviewer's interval. An event whose pre-onset window is not significant while its equal-length post-onset window is belongs to class I (l.220–221), and 223 of the 293 benchmark events with a detected change are in this class (l.365). The remaining anomaly $A' _{e} = [t _{e}+W, u _{e}]$ would then be the target of a detection-delay metric. The same geometry appears in Tab. 6, where an onset annotated late moves post-onset evidence into the pre-onset window and turns 93% of precursor-free synthetic events into apparent precursors. The revision states this distinction in §3.1.

# 6. Detection with models outside the descriptor family
We agree that a descriptor test cannot guarantee that it catches all precursors, and §5 states this limit (l.463). We addressed the question in two ways. RQ2 already applies seven learned detectors, and all of them separate the 3W transitions from normal operation with MPA of at least 0.68, while none separates benchmark P windows with mean scores (Tab. 3). Following the reviewer's suggestion, we also replaced the descriptor family by a descriptor-free kernel test and reran it on every event with the placebo calibration unchanged. The revision adds the kernel test to App. B.2.

**1. The kernel test.** It has a change-point branch, the largest maximum mean discrepancy (MMD) between the two sides of any split point inside the window, and a two-sample branch, the MMD between the window and 400 points of normal operation of the same entity, with a Gaussian kernel and median-heuristic bandwidth, following Gretton et al. [a]. Each branch is calibrated against the placebo windows of §3.2, and the two p-values are combined by Bonferroni.

Table H- Events detected by the descriptor test and by the kernel test (placebo rates 0.034 to 0.056 for both tests)
| **Events** | Descriptor test | **Kernel test** |
| :--- | :---: | :---: |
| 3W, before fault onset | 43 / 47 | **46 / 47** |
| 3W, before transition start | 11 / 47 | **19 / 47** |
| Five benchmarks | 70 / 500 | 36 / 500 |

# References

> [a] Arthur Gretton, Karsten M. Borgwardt, Malte J. Rasch, Bernhard Schölkopf, and Alexander Smola. A Kernel Two-Sample Test. JMLR, 2012.

*(Continued in 3/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 3/4 条 · 4487 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 2/4.)*

**2. Reading.** The kernel test is more sensitive than the descriptor test on the 3W transitions, where precursors are known to exist, and it finds fewer benchmark events. The sparsity of benchmark evidence therefore does not come from the choice of descriptors. Per dataset the kernel test detects 19 of 320 SMD, 4 of 35 MSL, 3 of 67 SMAP, 3 of 45 PSM and 7 of 33 SWaT events, and only SWaT exceeds its placebo rate ($p$ = 0.002). The two tests agree on 17 benchmark events.

# 7. Absolute rejection rates by lead
The reviewer is right. The two sentences at l.376–377, which are in §4.2, quote absolute rejection rates, whereas Fig. 4(b) shows only the excess over the placebo rate, and the 3W rates appear nowhere. Table I gives them, and the revision adds the full table for every dataset and lead to App. B.2 and states in the caption of Fig. 4 that it shows the excess.

Table I- Rejection rate by lead before onset (minutes for SMD and PSM, seconds for SWaT and 3W)
| **Dataset** | 0 | 10 | 50 | 200 | Placebo |
| :--- | :---: | :---: | :---: | :---: | :---: |
| SMD | 0.159 | 0.075 | 0.056 | 0.039 | 0.047 |
| PSM | 0.156 | 0.178 | 0.182 | 0.095 | 0.034 |
| SWaT | 0.273 | 0.364 | 0.091 | 0.000 | 0.037 |
| 3W | 0.915 | 0.936 | 0.915 | 0.915 | 0.050 |

On SMD the rate halves from 0.159 to 0.075 within 10 minutes and reaches 0.056 at 50 minutes, close to the placebo rate of 0.047. On 3W it stays between 0.915 and 0.936 at every lead from 0 to 200 seconds.

# 8. Validation of MPA
Yes, in two ways, a controlled validation with known ground truth and a comparison with an onset-truncated AUC on the benchmarks. Fig. 3(b) in §4.1 is the controlled validation, and the revision presents it as such. In synthetic events with known ground truth, every input-blind score (constant, random, time-only and post-onset-only) stays near 0.5, while a score that receives an increasing fraction of the injected precursor rises from 0.487 to 0.982. A metric for precursor discrimination needs both properties, no credit without pre-onset information and growth with that information. Point-adjusted F1 fails the first, since random alarms at matched rates reach 0.431 Shifted-warning F1 under PA, above every detector (Tab. 4). On the benchmarks, the onset-truncated AUC of answer 2 ranks the detectors as MPA does (Spearman 0.96 on SMD).

Table G lists the selection control, which is the set of normal windows that the test flags. A detector that scores deviations already separates these windows from other normal windows, so separation specific to precursor windows must exceed this level (l.412–413).

# 9. Interval-averaged F1
F1 can be computed on interval-averaged scores, and this removes the point-wise problem, but F1 still requires a threshold and counts alarms, so its value depends on the alarm rate. At a 5% point-wise rate, independent random alarms hit a 100-step interval with probability about 0.99, and under PA they outscore every detector (l.453–455, Tab. 4). MPA is the threshold-free form of the reviewer's suggestion. It compares the averaged score of each pre-onset interval with the averaged scores of matched normal intervals, and its chance level is 0.5 for any score (l.234). The revision adds this explanation to §3.3.

# 10. Precursors on real time series
Yes. The revision adds a figure to App. B.2 with nine real events drawn at random with a fixed seed, two P, two O and one I event from SMD, and two detected and two undetected 3W transitions. Each panel shows the onset, the window evaluated by the test and the three channels whose mean changes most between the last 100 steps and the 100 steps before, together with the verdict of the test.

# 11. Definition of onset
The onset $t _{e}$ is the first time step of an annotated anomaly interval $A _{e} = [t _{e}, u _{e}]$ (l.153). Pre-onset refers to times before $t _{e}$, and near-onset to the final steps of the 100-step pre-onset window. The revision gives these definitions in the abstract and in the first paragraph of §1.

# 12. The word causal
We use causal in the signal-processing sense, a score at time $t$ that uses only $x _{1:t}$ (l.180). We agree that the word suggests causal inference, and the revision replaces it by online throughout.

# 13. Answers to the research questions in §4
We agree. The revision ends §4.2, §4.3 and §4.4 with an explicit answer to RQ1, RQ2 and RQ3 in one or two sentences, in the order of the questions in §1.

*(Continued in 4/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 4/4 条 · 4844 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 3/4.)*

# 14. Exchangeability
The revision defines both notions where they are used and cites the conformal-inference results of Vovk et al. [e] and Lei et al. [f] that they rest on.

**1. Event–placebo exchangeability (§3.2, l.205–211).** If the pre-onset window of an event behaves like normal operation of its entity, its statistic $T _{e}$ and the placebo statistics $T ^{(0)} _{i,1}, \dots, T ^{(0)} _{i,M _0}$ are exchangeable, meaning that their joint distribution does not change when they are permuted. The rank of $T _{e}$ among them is then uniform, so the p-value of Eq. 2 satisfies $\Pr(p _{e,\ell} \le \alpha) \le \alpha$, which is the validity argument of conformal p-values [e].

**2. Paired-window exchangeability (§3.3, l.234).** If a score carries no information about the event, the score of the precursor window and those of its matched controls are exchangeable, so each comparison in Eq. 3 is won with probability one half and $\mathbb{E}[\text{MPA}] = 0.5$, also for a constant score (App. A.4, l.752).

# 15. Rejection rate at l.213
The revision adds the formula and its reading at l.213. For dataset $d$ with eligible events $E _{d}$ and held-out normal windows $V _{d}$,

$$\hat{r} _{d,\ell} = \frac{1}{|E _{d}|} \sum _{e \in E _{d}} D _{e}(\ell; \alpha), \qquad \hat{r} ^{(0)} _{d} = \frac{1}{|V _{d}|} \sum _{v \in V _{d}} D _{v}(\alpha),$$

that is, the share of events whose candidate window at lead $\ell$ is rejected, and the share of held-out normal windows rejected by the same rule. The excess $\hat{\eta} _{d,\ell} = \hat{r} _{d,\ell} - \hat{r} ^{(0)} _{d}$ is the share of events with evidence beyond what normal windows already produce.

# 16. Morphologies in Fig. 3
Tab. 5 in App. B.1.1 reports all eight morphologies at four strengths, and the weakest at full strength is nonlinear dependence (0.79). The revision plots all eight in Fig. 3(a) and names Tab. 5 in the §4.1 setup.

# 17. Eligibility of 500 of 537 events
〔待定③：下面按「只写 100 是数据决定的 + 附录表」起草，长窗口只放附录、不另做验证型实验〕

An event is eligible when the 100 steps before its onset, the candidate and reference windows at the largest scale, contain only normal points, with no earlier anomaly and no start of the series among them (l.159). Thirty-seven of the 537 events have fewer than 100 such steps. The same count explains the choice of 100 steps, since longer windows leave fewer events to evaluate (Table J). The revision states the criterion and Table J in §4.2 and App. A.3.

Table J- Events with at least the given number of clean steps before onset, out of 537
| **Clean steps** | 100 | 200 | 1000 | 2000 | 5000 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Events** | 500 | 474 | 307 | 157 | 49 |

We also ran the test with the candidate and reference windows extended to 2000 steps. On the 136 events evaluable at that span, the test flags 68, but only 6 of them are among the 17 flagged at 100 steps. On SMD the rejection rate at this span stays above the placebo rate even when the window ends 2000 steps before onset (0.125 against 0.052), the pattern of slow differences in operating state that a deviation test cannot separate from precursors (l.463–465). The revision therefore states every sparsity result for the 100 steps before onset and reports the longer spans in App. B.2.

# Summary of revisions
- **Validation of test choices in App. B.2 and §3.2.** We now report Table E and the kernel test of Table H, with pointers from §3.2.
- **Onset-truncated AUC in §4.3 and App. B.3.** We now compare MPA with a threshold-free AUC that excludes late detections.
- **Definitions and wording in the abstract, §1 and §3.** We now define every term of Table G at first use, with the formulas of answers 14 and 15, and write online instead of causal.
- **Reasons and answers in §3–4.** We now state the reason for each design decision where it is made, plot all eight morphologies in Fig. 3(a), and end each results section with the answer to its research question.
- **Rejection rates and examples in App. B.2.** We now report Table I for every dataset and lead and show nine randomly drawn real events.
- **Eligibility and window length in §4.2 and App. A.3.** We now state the criterion, Table J and the longer spans.

Following your suggestions, we will include these results and clarifications in the revised version. We hope these responses address most of your concerns, and we would be grateful if you would take them into account in your assessment. We are happy to clarify anything further during the discussion period.

# References

> [e] Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. Algorithmic Learning in a Random World. Springer, 2005.
>
> [f] Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan J. Tibshirani, and Larry Wasserman. Distribution-Free Predictive Inference for Regression. JASA, 2018.

▲▲▲ COPY TO HERE ▲▲▲
