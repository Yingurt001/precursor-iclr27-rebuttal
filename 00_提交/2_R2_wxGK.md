# 回复 Reviewer wxGK（Rating 3 / Conf 3；3W 漂移 / 边界偏移 / 聚合与训练配置 / 功效） — 提交版

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

## 第 1/4 条 · 2542 字符

▼▼▼ COPY FROM HERE ▼▼▼

We thank Reviewer $\color{blue}{\text{wxGK}}$ for recognizing that the paper separates three questions often conflated in early-warning evaluation, and for four precise questions, each of which we answered with a new analysis. Sections 1–4 answer Questions 1–4 in order. We respond to the concerns as follows.

*Line, table and section numbers refer to the submitted PDF, and appendix sections to the revised PDF. Tables A–E are new, and the revised appendix reports them in full.*

# 1. The 3W positive control under a local normal reference
We thank the reviewer for raising this question. We checked where the 29.2% of rejected verification windows comes from, and whether the 3W detections hold on all 47 records when the placebo null is built from normal operation just before each transition.

**1. Experiment.** For each of the 47 records, we kept the target window before the fault, the test statistic and the significance threshold of the submission, and built the placebo null only from the last 300, 900 or 1800 seconds of normal operation before the annotated transition. For the records of the chronological split, we also plotted the raw signals of representative channels together with the normal reference, the annotated transition, the fault and the windows that the test flags.

**2. Results.** With the local null, the test detects 45, 45 and 43 of the 47 transitions for references of 300, 900 and 1800 seconds, against 43 in the submission (Table A).

Table A- 3W transitions detected on all 47 records when the placebo null comes from normal operation just before each transition
| **Normal reference** | Records | Detected | Rate |
| :--- | :---: | :---: | :---: |
| Submission | 47 | 43 | 91.5% |
| Last 300 s | 47 | 45 | 95.7% |
| Last 900 s | 47 | 45 | 95.7% |
| Last 1800 s | 47 | 43 | 91.5% |

With 900 seconds, 42 of the 43 records detected in the submission stay detected and 3 of the other 4 become detected, so the detection rate holds on all 47 records and is stable across the reference lengths we compared. The 29.2% is the equal-weight average of the rejection rates of the 16 records of the chronological split. These rates differ strongly between records, and the record with the highest rate reaches 100%. In the records we inspected, the signals in the flagged windows change visibly relative to the normal reference, although the labels of the dataset do not mark these changes. The revision adds Table A to App. B.1.2 and the raw signals with the flagged windows to App. B.2.1.

*(Continued in 2/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 2/4 条 · 2163 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 1/4.)*

# 2. Onset-continuity check on PSM and SWaT
We thank the reviewer for this question. We applied the onset-continuity check of Tab. 8 to all precursor-positive events of PSM and SWaT and counted how many it classifies as boundary shifts.

**1. Experiment.** An event is an onset jump when the jump at the annotated onset exceeds the 95th percentile of jumps in fully normal neighborhoods. It is a boundary shift when the jump at the onset stays below this threshold, but a jump at least three steps earlier, within 45 steps before the onset, exceeds it and points in the direction of the change after onset. Other events are unclassified. On synthetic series this rule identifies 94.5% of the apparent precursors created by late annotation, and it labels 84.5% of correctly annotated precursors as onset jumps and 9.8% as boundary shifts. We kept the original precursor-positive events unchanged and reran SMD as a check.

**2. Results.** The check classifies 5 of the 7 precursor-positive events of PSM and 7 of the 9 of SWaT as boundary shifts (Table B).

Table B- Precursor-positive events by the onset-continuity check. Tab. 3 counts 49 SMD and 6 PSM events, those scored by all seven detectors.
| **Dataset** | Events | Onset jump | Boundary shift | Unclassified |
| :--- | :---: | :---: | :---: | :---: |
| SMD | 51 | 38 | 6 | 7 |
| PSM | 7 | 1 | **5** | 1 |
| SWaT | 9 | 2 | **7** | 0 |

The SMD counts reproduce Tab. 8. Boundary shifts are 71.4% of the PSM events and 77.8% of the SWaT events, with the earlier jump 4 to 41 minutes before the annotated onset on PSM and 8 to 27 seconds before it on SWaT. A boundary shift is a diagnosis from the shape of the signal. A change before the annotated onset can come from a late label or from the development of the fault itself, and the unclassified events also show a deviation before onset. The revision therefore reports deviation detection, boundary diagnosis and precursor interpretation separately, keeps the qualification of App. B.3.2 on the placebo pool for the dataset-level significance of PSM and SWaT, and adds PSM and SWaT to Tab. 8 in App. B.2.3.

*(Continued in 3/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 3/4 条 · 2827 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 2/4.)*

# 3. Separating score aggregation from training configuration
We thank the reviewer for this question. We ran two paired designs, each with the precursor events and normal controls fixed, that change either the score aggregation or the training configuration.

**1. Experiment.** For aggregation, we used the original scores on the 49 common P events of SMD and the 20 original normal controls of each event, and applied the same aggregation to the candidate window and to its controls, without retraining or redrawing controls. Intervals come from resampling machines, and q-values from BH correction over 21 paired comparisons. For training, a separate controlled experiment compares pooled and per-machine training of iForest and LSTM-VAE on the same 51 P events and normal controls, with three seeds, a budget of 4096 normal windows per model and the 100-step mean.

**2. Results.** For LSTM-VAE, the maximum over the final 50 steps raises MPA from 0.561 to 0.750, while shortening the mean from 100 to 50 steps changes it only from 0.534 to 0.561, and per-machine training leaves both detectors unchanged (Tables C and D).

Table C- Paired changes in LSTM-VAE MPA on the 49 common SMD P events, with intervals over machines and BH q-values over 21 comparisons
| **Comparison** | Change in MPA | 95% interval | q |
| :--- | :---: | :---: | :---: |
| Final 50 mean minus 100-step mean | +0.028 | [−0.001, 0.061] | 0.359 |
| Final 50 maximum minus final 50 mean | **+0.189** | [0.119, 0.258] | **0.0013** |
| Final 50 maximum minus 100-step mean | **+0.216** | [0.140, 0.290] | **0.0013** |

Table D- MPA under pooled and per-machine training with the same budget, events and controls, three seeds
| **Detector** | Pooled | Per-machine | Difference [95% interval] |
| :--- | :---: | :---: | :---: |
| iForest | 0.611 | 0.600 | −0.011 [−0.071, 0.060] |
| LSTM-VAE | 0.680 | 0.691 | +0.011 [−0.027, 0.066] |

The near-onset gain of LSTM-VAE thus comes from the maximum, which keeps short high scores, more than from a window closer to onset, and this confirms the near-onset score peaks reported in the submission. In the training design both intervals contain zero, and its absolute MPA is not compared with the submitted models. The normal reference has its own effect. With the same per-machine iForest, events and mean aggregation, replacing the training-period normal reference by a test-period one lowers MPA from 0.780 to 0.634, a paired difference of −0.146 [−0.203, −0.083]. §4.3 of the submission states that the per-machine iForest experiment changes training, event set and normal reference together, and the revision limits the negative results to the evaluated training, normal reference and mean aggregation. Tables C and D are added to App. B.4.3 and App. B.4.5.

*(Continued in 4/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 4/4 条 · 3701 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 3/4.)*

# 4. Effect sizes excluded by the power analysis
We thank the reviewer for this question. We computed which effect sizes the current data can detect, which effect sizes the confidence bounds exclude, and whether the intervals establish negligible discrimination.

**1. Analysis.** MPA is the probability that a detector scores a precursor window above its matched normal window, so 0.5 is chance. The smallest detectable MPA is the true MPA at which the analysis detects an effect with probability 0.8, under the power assumptions of the submission. The Bonferroni column serves power planning, while significance in the main experiment uses BH. The upper 95% bound is the largest MPA the data still allow, computed with event-level resampling as in the submission and with machine-level resampling for correlated events of the same machine. To test negligible discrimination, we took [0.45, 0.55] as an example near-chance range and checked whether the machine-level 90% interval of each detector lies inside it.

**2. Results.** On SMD the bounds constrain large effects such as an MPA of 0.70 but leave values around 0.60 open, and no detector falls inside the near-chance range, so the results do not establish negligible discrimination (Table E).

Table E- Smallest detectable MPA and largest upper 95% bound of MPA over the seven detectors, on the P events common to all seven
| **Dataset** | Common P events | Smallest detectable MPA | Bonferroni | Largest upper bound |
| :--- | :---: | :---: | :---: | :---: |
| SMD | 49 | 0.602 | 0.657 | 0.656 |
| SWaT | 9 | 0.729 | 0.853 | 0.672 |
| PSM | 6 | 0.791 | 0.948 | 0.925 |

On SMD the largest upper bound is 0.656 with event-level resampling and 0.669 with machine-level resampling. A2P, for example, has MPA 0.5735 with interval [0.4918, 0.6561], which contains 0.5 and also allows 0.60, and the intervals of LSTM-VAE, DAGMM and iForest also allow 0.60. On SWaT the bound of 0.672 allows moderate effects, and on PSM the bound of 0.925 allows strong ones. PSM would need a true MPA of about 0.791 for an 80% chance of detection, so non-significance on PSM and SWaT is compatible with some positive discrimination that the current number of events cannot detect reliably. None of the six non-degenerate SMD detectors has its 90% interval inside [0.45, 0.55]. The paired comparisons of Anomaly Transformer are all ties on this event set, so its zero-width interval is not used. The results of §4.3 therefore show that no positive discrimination survives correction in the evaluated settings. The revision uses "not statistically significant" in the abstract, states these bounds in §4.3, and reports the machine-level check and the equivalence analysis in App. B.4.1.

# Summary of revisions
- **3W control under a local normal reference in App. B.1.2 and App. B.2.1.** We now report Table A on all 47 records, and the raw signals with the flagged windows of the chronological split.
- **Onset-continuity check for PSM and SWaT in App. B.2.3.** Tab. 8 now includes PSM and SWaT, and App. B.3.2 keeps the qualification on the placebo pool.
- **Aggregation and training in App. B.4.3 and App. B.4.5.** We now report Tables C and D and the effect of the normal reference.
- **Excluded effect sizes in the abstract, §4.3 and App. B.4.1.** We now report Table E, the machine-level bound and the equivalence analysis.

Following your suggestions, we will include these results and clarifications in the revised version. We hope these responses address most of your concerns, and we would be grateful if you would take them into account in your assessment. We are happy to clarify anything further during the discussion period.

▲▲▲ COPY TO HERE ▲▲▲
