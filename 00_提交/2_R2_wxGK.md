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

## 第 1/4 条 · 4178 字符

▼▼▼ COPY FROM HERE ▼▼▼

We thank Reviewer $\color{blue}{\text{wxGK}}$ for recognizing that the paper separates three questions often conflated in early-warning evaluation, and for four precise questions, each of which we answered with a new analysis. Sections 1–4 answer Questions 1–4 in order. We respond to the concerns as follows.

*Line, table and section numbers refer to the submitted PDF. Tables A–D are new, and the revised appendix reports them in full.*

# 1. Drift of normal operation in the 3W positive control
We thank the reviewer for raising this question. We checked whether slow changes of a well during normal operation, the operating-state drift the reviewer describes, can explain why the test detects 43 of the 47 transitions, the stages that experts annotated between normal operation and each fault. We therefore designed the experiment below.

**1. Experiment.** If drift explains a detection, normal windows that lie as far from their normal reference as the tested window should be flagged just as often. We therefore compared each tested window with normal windows at the same distance from their reference, in two settings. In the first, the tested window is the first ten minutes of the transition, and the reference is an hour of normal operation that ends 30 minutes before the annotated start, so drift has little time to build up. A transition counts as detected when three consecutive 100-second windows are flagged, and the same rule applied to normal operation gives the false-alarm rate. In the second, the tested window is the last 100 seconds before the fault, as in the submission, which lies 0.2 to 166 hours after the normal data, and the normal windows at the same distances come from the long normal-only records of 3W. The test settings are those of the submission. Both settings need at least 3.5 hours of normal operation before the transition: an hour for the reference, then the placebo windows of the null, then an hour between those windows and the transition. All 19 records with that much, from 14 wells, are used. The other 28 have a median of 1.4 hours and at most 3.47, and 11 of the 47 have less than one hour, shorter than the reference alone, so no design that keeps the reference of the submission can cover all 47. The chronological split of App. B.1.2 needs less, about 2.6 hours, and 23 of the 47 records have it, of which the submission used 16, the first eight records by file name in each fault class. Counting all verification windows together, 529 of 1920 (27.6%, 95% interval 15.2–45.8% over wells) are rejected on the 23 records, against 300 of 1354 (22.2%) on the 16, where the 29.2% of the submission averages the records instead. The chronological split thus flags normal operation on the full set as well, which is why the adjacent design above answers the first part of the question.

**2. Results.** Drift does not explain the detections at the start of the transitions, but it can explain the detections far from the normal data (Table A).

Table A- 3W transitions detected by the test and expected from drift alone (19 records)
| **Tested window** | Gap to reference | Detected | Expected from drift |
| :--- | :---: | :---: | :---: |
| Transition start | 30–40 min | **11 / 19** | 0.8 / 19 |
| Before fault onset | 0.2–166 h | 15 / 19 | 10.3 / 19 |

Under the same rule, normal stretches are flagged in 4.1% of cases, so drift alone would give 0.8 of the 11 detections at the transition start. Normal windows as far from their reference as the windows before the fault are flagged in 49% to 75% of cases, so drift alone would give 10.3 of the 15 detections there. Drift thus explains almost none of the detections at the transition start but most of those in the submission. We chose the gap and the three-window rule among the variants of App. B.1.2 to keep false alarms low, and a single window without gap gives 10 of 19 against 4.9%. The revision adds this control, Table A, the variants and the chronological split on all 23 records to App. B.1.2, states in §4.1 and §5 that detections far from the normal reference cannot be separated from drift, and drops "recovering real precursors" (l.344).

*(Continued in 2/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 2/4 条 · 2368 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 1/4.)*

# 2. Onset-continuity check on PSM and SWaT
We thank the reviewer for this question. We checked whether the precursor-positive events of PSM and SWaT could come from onsets annotated slightly late, which turn 93% of precursor-free synthetic events into apparent precursors (Tab. 6). We therefore ran the experiment below.

**1. Experiment.** When an onset is annotated late, the window before it already contains the start of the anomaly, so the signal jumps a few steps before the annotated onset and not at it. The onset-continuity check of Tab. 8 looks for this pattern. For each event it compares the jump of the signal at the annotated onset with the jumps seen in normal operation of the same entity. An event is an onset jump when the jump at the onset is unusually large, as expected for a correct annotation. It is a boundary shift when the jump at the onset is ordinary but a large jump in the direction of the anomaly occurs a few steps earlier, as expected for a late annotation. Otherwise it is undetermined. On synthetic series the check labels 94.5% of late annotations as boundary shifts and 9.8% of correct ones (l.856–858). We applied it unchanged to the precursor-positive events of PSM and SWaT, and rerunning it on SMD reproduces Tab. 8.

**2. Results.** Most precursor-positive events of PSM and SWaT look like late annotations, unlike those of SMD (Table B).

Table B- Precursor-positive events by the onset-continuity check
| **Dataset** | Events | Onset jump | Boundary shift | Undetermined |
| :--- | :---: | :---: | :---: | :---: |
| SMD | 51 | 38 | 6 | 7 |
| PSM | 7 | 1 | **6** | 0 |
| SWaT | 9 | 2 | **7** | 0 |

In the boundary shifts the large jump lies 8 to 27 seconds before the annotated onset on SWaT and 4 to 41 minutes before it on PSM. On SMD 6 of 51 events are boundary shifts, close to the 9.8% the check assigns to correct annotations. The check is less reliable on PSM and SWaT, since events that change only after onset show an onset jump in 70% of cases on SMD but in 40% on PSM and 20% on SWaT. We therefore draw only the dataset-level conclusion that pre-onset evidence on PSM and SWaT cannot be separated from annotation offsets, so benchmark-level evidence rests mainly on SMD. The revision states this in §4.2 and adds Table B and the list of all 16 events to App. B.2.

*(Continued in 3/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 3/4 条 · 2812 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 2/4.)*

# 3. Separating score aggregation from training configuration
We thank the reviewer for this question. We checked whether the stronger results of per-machine iForest and of near-onset score peaks come from the training, from how scores are aggregated over a window, or from the different event sets and normal references of those analyses. We therefore ran the experiment below.

**1. Experiment.** On SMD we changed one factor at a time and kept everything else fixed. The training of iForest is either pooled over machines, as in Tab. 3, or per machine, as in Tab. 19, and iForest is the only detector with scores under both. The score of a window is either its mean over the 100 steps, as in Tab. 3, or its maximum over the final 50 steps, as in Tab. 17. The 51 precursor-positive events, the normal windows they are paired with, and the selection control are the same in all four settings. The selection control consists of the 355 normal windows that the test flags although no event follows. Since the precursor-positive events were also selected for looking different from normal operation, a detector shows precursor-specific discrimination only when its MPA on these events exceeds its MPA on the selection control.

**2. Results.** No combination separates the precursor-positive events from the selection control (Table C).

Table C- iForest MPA on SMD under each training and score (51 precursor-positive events, 355 selection-control windows)
| **Training, score** | Precursor events | Selection control | Difference [95% CI] |
| :--- | :---: | :---: | :---: |
| Pooled, mean | 0.553 | 0.524 | +0.029 [−0.064, 0.120] |
| Pooled, max | 0.575 | 0.557 | +0.017 [−0.074, 0.109] |
| Per-machine, mean | 0.602 | 0.678 | −0.076 [−0.163, 0.009] |
| Per-machine, max | 0.810 | 0.758 | +0.052 [−0.012, 0.112] |

Per-machine training raises both groups, by 0.05 and 0.15 with the mean and by 0.24 and 0.20 with the maximum, so it sharpens the response to any window that departs from normal operation. The near-onset maximum raises the precursor events more than the control under per-machine training, 0.21 against 0.08, consistent with evidence in the final minutes before onset, yet the difference to the control stays within its interval. Ordinary normal windows stay at 0.49 to 0.50 in all four settings, so the pairing is unbiased. The gap of 0.861 against 0.655 in §4.3 therefore came mainly from the different event set and normal reference of that experiment. Among the pooled detectors, only the near-onset peaks of LSTM-VAE exceed the selection control, 0.743 against 0.630 (Tab. 18). The revision replaces the per-machine comparison in the contributions (l.094), §4.3 (l.414–417), the limitations (l.467–469) and the conclusion (l.478) with Table C.

*(Continued in 4/4.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 4/4 条 · 3438 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 3/4.)*

# 4. Effect sizes excluded by the power analysis
We thank the reviewer for this question. We checked which effect sizes the data exclude, so that non-significance is not read as evidence of negligible discrimination. We therefore computed, for each benchmark, the smallest MPA the analysis detects with 80% power and the largest upper 95% bound of MPA over the seven detectors.

**1. Analysis.** MPA is the probability that a detector scores a precursor window above its matched normal window, so 0.5 is chance. The upper 95% bound of a detector's MPA is the largest value its data still allow. The smallest detectable MPA, from Tab. 14, is how large a true effect must be to be found in 80% of repetitions of the analysis, without and with the Bonferroni correction. Both use the precursor-positive events common to all seven detectors.

**2. Results.** The data exclude large discrimination on SMD and SWaT but leave small to moderate values open (Table D).

Table D- Smallest detectable MPA and largest upper bound of MPA over seven detectors
| **Dataset** | Precursor events | Smallest detectable MPA | Largest upper bound |
| :--- | :---: | :---: | :---: |
| SMD | 49 | 0.60 (0.66 corrected) | 0.656 |
| SWaT | 9 | 0.73 (0.85 corrected) | 0.672 |
| PSM | 6 | 0.79 (0.95 corrected) | 0.925 |

On SMD every upper bound is at most 0.656, so an MPA of 0.66 or more is excluded for all seven detectors, and on SWaT values above 0.672 are excluded. Values between 0.5 and about 0.65 remain possible on SMD, where the smallest detectable MPA of 0.60 also lies, so the data do not establish negligible discrimination. The closest case is A2P, an early-warning model, with MPA 0.573 and a difference to non-precursor events of +0.105 [0.013, 0.194], which is not significant after correction even when the correction covers only the seven SMD cells (q = 0.10). PSM has too few events to exclude any value of practical interest. The revision states these bounds next to every significance result in §4.3, reports the per-detector values in App. B.3, and limits the abstract (l.021–023) to the 21 SMD, PSM and SWaT combinations, stating that the upper bounds on SMD exclude an MPA of 0.66 or more.

# Summary of revisions
- **3W control in App. B.1.2, with its limit in §4.1 and §5.** App. B.1.2 now reports the detection of transition starts against normal operation shortly before them, with controls at the same distance, and §4.1 and §5 state that detections far from the normal reference cannot be separated from drift.
- **Onset-continuity check for PSM and SWaT in App. B.2 and §4.2.** We now report Table B and the list of events, and state that benchmark-level evidence rests mainly on SMD.
- **Training and aggregation in §4.3 and App. B.3.** We now report Table C in place of the per-machine comparison in the contributions, §4.3, the limitations and the conclusion.
- **Excluded effect sizes in the abstract, §4.3 and App. B.3.** We now report Table D and the per-detector values, state the bounds next to every significance result, and limit the abstract to the 21 SMD, PSM and SWaT combinations.

Following your suggestions, we will include these results and clarifications in the revised version. We hope these responses address most of your concerns, and we would be grateful if you would take them into account in your assessment. We are happy to clarify anything further during the discussion period.

▲▲▲ COPY TO HERE ▲▲▲
