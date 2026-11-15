# 回复 Reviewer pSK8（Rating 1 / Conf 4；技术贡献 / 指标 / presentation / 7 条 minor） — 提交版

> **这个文件就是源，直接改它。** 改完在 `6_Rebuttal/iclr_2027/` 跑 `/usr/bin/python3 sync.py`（或双击 `同步.command`），
> 会自动按 OpenReview 上限重新分条并刷新网站。改前的版本存在 `00_提交/.bak/`。
> 改的时候**忽略分条标记**，把它当一整篇看就行 —— 重跑脚本会重新切。
> 引用：正文写 `[a]` / `[a, Thm. 9]`；新条目随便写进任何一个 `# References` 块（`> [a] 论文标题`），
> 脚本会给每条帖子末尾补上这条帖子引过的条目，各帖里的 References 不用手动维护。
>
> 用 OpenReview 的 `Official Comment` 发：审稿人回复发在对应 review 下，0 号发在论坛顶层。单条上限 5000 字符，当前共 6 条。
> **发帖顺序：6/6 → 5/6 → 4/6 → 3/6 → 2/6 → 1/6 倒序贴**，页面才会正序显示。
> 每条只复制 `▼▼▼ COPY FROM HERE ▼▼▼` 与 `▲▲▲ COPY TO HERE ▲▲▲` 之间的内容，不含标记行。


---

## 第 1/6 条 · 4050 字符

▼▼▼ COPY FROM HERE ▼▼▼

We thank Reviewer $\color{green}{\text{pSK8}}$ for finding the problem very interesting and understudied, for reading the paper several times, and for stating concretely which changes would improve the presentation. We respond to the concerns as follows.

*Line, table and section numbers refer to the submitted PDF, and appendix sections to the revised PDF. Tables F–J are new, and "answer n" refers to section n of this response.*

# 1. Validation of the precursor detectability test
We thank the reviewer for this concern, which helped us explain the technical choices more completely. The revision states the reasoning behind the test step by step and adds a new experiment that checks whether the deviations it detects are useful for recognizing a coming fault.

The reasoning has four steps. First, §3.2 defines the test statistic $T$, and App. A.2 and App. B.1.3 explain why we built a dedicated test instead of an existing change-point or self-supervised detector (answer 6). Second, 3W is the one public dataset with independently annotated transitions before each fault, and the test detects 43 of its 47 transitions (§4.1). Third, a counterfactual ablation, described below, checks that the detected deviations carry information about the coming fault. Fourth, on the five public benchmarks, several of which were built for anomaly detection and adapted to prediction by shifting labels, the test finds deviations before onset in only 70 of 500 events. Because real multivariate event datasets for early warning are scarce, the revision also releases DeviceWarning-162, 162 events on 48 devices with 207 normal reference sequences, as supplementary material with its description in App. C. It does not change the results of the submission.

**1. Experiment.** For each of the 47 3W records, we replaced the mean level and the linear trend of the series before the fault by those of normal operation of the same well, which weakens the detected deviation and keeps the other fluctuations. Positives are the last 100 samples before the stable fault of each record, and negatives are 8 normal windows of the same length from the same record, 47 positives and 376 negatives in total. All metrics are computed at the window level without point adjustment, for common anomaly detection, anomaly prediction and supervised classification models.

**2. Results.** After the ablation the test flags none of the 47 transitions instead of 43, and every model moves toward chance (Table F).

Table F- Window-level results on 3W with the original and the ablated input (original → ablated), 47 windows before the fault and 376 normal windows
| **Model** | AUROC | AUPRC | Recall | Precision | F1 | MPA |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| iForest | 0.795 → 0.587 | 0.453 → 0.216 | 0.787 → 0.319 | 0.230 → 0.108 | 0.356 → 0.161 | 0.823 → 0.600 |
| DAGMM | 0.783 → 0.597 | 0.594 → 0.269 | 0.830 → 0.511 | 0.163 → 0.107 | 0.273 → 0.177 | 0.806 → 0.630 |
| USAD | 0.972 → 0.626 | 0.885 → 0.330 | 1.000 → 0.532 | 0.168 → 0.097 | 0.287 → 0.164 | 0.989 → 0.689 |
| LSTM-VAE | 0.967 → 0.657 | 0.875 → 0.342 | 1.000 → 0.553 | 0.162 → 0.097 | 0.279 → 0.165 | 0.976 → 0.689 |
| AnomTrans | 0.623 → 0.579 | 0.314 → 0.221 | 0.553 → 0.234 | 0.271 → 0.136 | 0.364 → 0.172 | 0.672 → 0.585 |
| FCM | 0.949 → 0.664 | 0.822 → 0.318 | 0.979 → 0.574 | 0.175 → 0.111 | 0.297 → 0.186 | 0.973 → 0.673 |
| A2P | 0.895 → 0.588 | 0.768 → 0.288 | 0.894 → 0.234 | 0.300 → 0.101 | 0.449 → 0.141 | 0.934 → 0.590 |
| HGB | 0.874 → 0.568 | 0.399 → 0.143 | 0.660 → 0.149 | 0.408 → 0.135 | 0.504 → 0.141 | 0.880 → 0.573 |
| RF | 0.883 → 0.638 | 0.474 → 0.158 | 0.511 → 0.021 | 0.421 → 0.029 | 0.462 → 0.025 | 0.896 → 0.681 |

AUROC and MPA move toward 0.5 for every model, and AUPRC, recall and F1 all fall, so the level and trend that the test detects contribute to recognizing the window before a fault. The revision adds this ablation to App. B.1.4, and answer 2 and answer 8 compare MPA with the range-based, affiliation and VUS metrics.

*(Continued in 2/6.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 2/6 条 · 4419 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 1/6.)*

# 2. Range-based, affiliation and VUS metrics
We thank the reviewer for this suggestion. MPA asks whether a detector separates a test-positive candidate window from matched normal windows of the same device. Range-F1 [d] and Affiliation-F1 [e] need a target interval and score how alarms cover it or relate to it in time, and VUS [f] needs point-wise scores and a target interval and integrates over thresholds and tolerances. RQ1 shows that a candidate window deviates from normal operation, but not at which points or for how long the precursor is present. Labeling all 100 points of a positive window as targets therefore assumes a precursor interval that the evidence does not support, even when the evaluation stops at onset. We evaluated the adapted metrics where this assumption can be checked, on 3W with its independently annotated transitions, and in a controlled setting (answer 8).

**1. Experiment.** For each 3W record, the 100 normal samples before the annotated transition (label 0) and the first 100 samples of the transition (label 1) form a 200-sample interval that ends before the stable fault, on which we compute Range-F1, Affiliation-F1, VUS and the point-wise false positive rate. For the window-level metrics, the first 100 samples of the transition form a positive window and 8 normal windows of the same record form its controls, 47 positive and 376 normal windows, for matched MPA, Window-F1 and the window false positive rate. All evaluation ranges and tolerance zones end before the stable fault, so responses after the fault earn no credit.

**2. Results.** Adapted in this way, Range-F1, Affiliation-F1 and VUS describe interval coverage, timing and tolerance, and they complement MPA (Table G).

Table G- Metrics on 3W with all evaluation ranges ending before the stable fault (FPR is the false positive rate per point or per window)
| **Model** | MPA | Window-F1 | Range-F1 | Affiliation-F1 | VUS-ROC | VUS-PR | Point FPR | Window FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| iForest | 0.625 | 0.218 | 0.365 | 0.480 | 0.627 | 0.702 | 0.238 | 0.375 |
| DAGMM | 0.795 | 0.235 | 0.491 | 0.601 | 0.765 | 0.809 | 0.509 | 0.596 |
| USAD | 0.838 | 0.239 | 0.596 | 0.703 | 0.831 | 0.866 | 0.629 | 0.678 |
| LSTM-VAE | 0.822 | 0.227 | 0.546 | 0.722 | 0.820 | 0.841 | 0.587 | 0.684 |
| AnomTrans | 0.593 | 0.216 | 0.272 | 0.348 | 0.617 | 0.682 | 0.157 | 0.226 |
| FCM | 0.814 | 0.239 | 0.600 | 0.682 | 0.798 | 0.872 | 0.565 | 0.641 |
| A2P | 0.633 | 0.212 | 0.284 | 0.314 | 0.694 | 0.824 | 0.261 | 0.301 |

Each metric measures a different aspect, so their absolute values are not directly comparable. The experiment turns the annotated normal and transition stages of 3W into labels 0 and 1. The other benchmarks have no independent precursor stage, and labeling whole candidate windows there would add an untested assumption on time, which is why the paper reports MPA. The revision adds this comparison to App. B.5.6.

# 3. Definitions of non-standard terms
We thank the reviewer for pointing out that the paper was hard to read on first pass. The revision rewrites the text throughout, gives formal definitions of the proposed concepts in the abstract and the introduction, and points to the appendix at every place in the main text that relies on it. The definitions of onset (answer 11), the rejection rate (answer 15) and exchangeability (answer 14) are examples.

# 4. Reasons for design decisions
We thank the reviewer for this point. The revision states the reason for each decision where it is made and points to the appendix where details are given. For the example of line 299, the setup of §4.1 now states that the experiment covers all eight morphologies, that Fig. 3(a) shows five representative ones to avoid overlapping curves, and that Table 5 in App. B.1.1 reports all eight (answer 16).

# References

> [d] Nesime Tatbul, Tae Jun Lee, Stan Zdonik, Mejbah Alam, and Justin Gottschlich. Precision and Recall for Time Series. NeurIPS, 2018.
>
> [e] Alexis Huet, José Manuel Navarro, and Dario Rossi. Local Evaluation of Time Series Anomaly Detection Algorithms. KDD, 2022.
>
> [f] John Paparrizos, Paul Boniol, Themis Palpanas, Ruey S. Tsay, Aaron J. Elmore, and Michael J. Franklin. Volume Under the Surface: A New Accuracy Evaluation Measure for Time-Series Anomaly Detection. PVLDB, 2022.

*(Continued in 3/6.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 3/6 条 · 4714 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 2/6.)*

# 5. Windows after onset
We thank the reviewer for this suggestion. Technically, the first $W$ points after onset can be used to predict how the anomaly develops, but this is a different task from the early warning studied in the paper. The work is motivated by industrial systems such as high-end equipment and precision manufacturing, where anomalies lower yield, damage equipment and stop production, so a warning must come before the anomaly starts to leave time for intervention. Setting $P _{e}(W) = [t _{e}, t _{e}+W)$ uses data already labeled as anomalous to predict later parts of the same event. This serves the prediction of anomaly development or fault escalation, which has its own practical value, but it cannot tell whether detectable evidence exists before the anomaly starts and whether models use it to warn early. The test already evaluates the post-onset interval of equal length, and 223 of the 293 benchmark events with a detected change are detected only there (l.365). The revision therefore keeps the candidate precursor window before onset, which separates early warning from detection and prediction after onset.

# 6. Detection with models outside the descriptor family
We thank the reviewer for this question. We agree that no method based on a finite set of features or a specific detection mechanism can guarantee to find every precursor, so the results of the test describe the evidence that this mechanism detects. To check the test and the effect of the detection mechanism, we compared it with three representative methods, Online Kernel CUSUM [a], a kernel change-point method, MMDEW [b], an efficient online change-point method based on maximum mean discrepancy over exponential windows, and TS2Vec [c], a self-supervised representation of time series.

**1. Experiment.** All methods use the same candidate windows and the same split of normal data for fitting, calibration and verification, and their thresholds are calibrated on the same normal controls. We count detections on the 47 3W transitions and on the 500 benchmark events, and the overlap with the events our test detects.

**2. Results.** At similar false positive rates on normal data, our test detects the most deviations before onset, on 3W and on the benchmarks (Table H).

Table H- Detections of the precursor test and three alternative detectors under the same windows and calibration, with the overlap with our test and the false positive rate (FPR) on normal windows
| **Method** | 3W detected | Overlap | FPR | Benchmarks detected | Overlap | FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Our test | **43/47** | -- | 5.03% | **70/500** | -- | 4.58% |
| Online Kernel CUSUM | 40/47 | 40/43 | 4.81% | 42/500 | 35/70 | 5.02% |
| MMDEW | 33/47 | 31/43 | 4.50% | 32/500 | 28/70 | 4.73% |
| TS2Vec | 42/47 | 39/43 | 7.53% | 63/500 | 57/70 | 4.72% |

The mechanisms explain the differences. Online Kernel CUSUM accumulates evidence of a distribution change and suits newly appearing changes during monitoring. MMDEW compares distributions over exponential windows and suits abrupt changes and drift at several time scales. TS2Vec learns a representation that can capture changes outside predefined statistics, but its detections depend on whether the representation keeps the relevant information and on the scoring that follows. Our test checks local changes and the overall deviation from normal operation together, so it adapts to precursors of uncertain form and duration. The change branch captures new changes of mean, variability, trend and dependence between variables, and the deviation branch captures an abnormal state that has already formed and persists, even when the candidate window contains no new change point. Its multi-scale descriptors also explain which change in the data drives a detection, and independent normal controls calibrate its significance. We do not claim that the statistic covers every precursor or outperforms existing methods on every type of change, and change-point and self-supervised detectors can replace it as the evidence component for other data. The revision adds this comparison to App. B.1.3.

# References

> [a] Song Wei and Yao Xie. Online Kernel CUSUM for Change-Point Detection. Journal of the Royal Statistical Society Series B, 2026.
>
> [b] Florian Kalinke, Marco Heyden, Georg Gntuni, Edouard Fouché, and Klemens Böhm. Maximum Mean Discrepancy on Exponential Windows for Online Change Detection. TMLR, 2025.
>
> [c] Zhihan Yue, Yujing Wang, Juanyong Duan, Tianmeng Yang, Congrui Huang, Yunhai Tong, and Bixiong Xu. TS2Vec: Towards Universal Representation of Time Series. AAAI, 2022.

*(Continued in 4/6.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 4/6 条 · 4294 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 3/6.)*

# 7. Rejection rates by lead
We thank the reviewer for pointing out this gap between the text and the figures. The revision extends Table 2, which reported the rejection rate at lead 0, with the event rejection rates of the five benchmarks at leads of 10, 50, 100 and 200 steps, and its caption states the time unit of each dataset and how the rates are computed (Table I).

Table I- Event rejection rate $r _\ell$ at lead $\ell$ (one step is one minute, and one second on SWaT) and normal rejection rate $r _n$, as now in Table 2
| **Dataset** | $r _0$ | $r _{10}$ | $r _{50}$ | $r _{100}$ | $r _{200}$ | $r _n$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| SMD | 0.159 | 0.075 | 0.056 | 0.027 | 0.039 | 0.047 |
| MSL | 0.029 | 0.086 | 0.029 | 0.088 | 0.030 | 0.046 |
| SMAP | 0.030 | 0.045 | 0.060 | 0.106 | 0.045 | 0.045 |
| PSM | 0.156 | 0.178 | 0.182 | 0.091 | 0.095 | 0.034 |
| SWaT | 0.273 | 0.364 | 0.091 | 0.152 | 0.000 | 0.037 |

Fig. 4 is unchanged and still shows the excess of the event rejection rate over the normal rejection rate with its significance. The revised text and caption distinguish the event rejection rate of Table 2 from the excess of Fig. 4, and every number quoted in the text now refers to Table 2. For 3W, the text adds that over the ten leads from 0 to 200 seconds the rejection rate is 0.936 at 10 and 20 seconds and 0.915 at the other eight.

# 8. Reliability of MPA
We thank the reviewer for this question. MPA was designed to measure, for events whose window before onset deviates detectably, whether a model separates the candidate window from normal windows of the same device. Unlike the other metrics, it needs neither the position and duration of the precursor inside the window nor an alarm threshold (answer 2). Since real datasets have no point-wise precursor ground truth, we compared MPA with the other metrics in a controlled scoring experiment, where every metric has the labels it needs.

**1. Experiment.** We set a candidate precursor window of 32 points as the positive target and all other points before the anomaly as normal negatives, which gives window labels for Window-F1 and the interval and point labels that Range-F1, Affiliation-F1 and VUS need. We then generated model scores for several cases, with 20 independent repetitions of 16 simulated cases each. Normal point scores follow a normal distribution with mean 0 and variance 1. The weak and strong precursor responses shift the mean of the precursor window by 0.25 and 1.0, and the post-onset response scores high only after the anomaly starts.

**2. Results.** All five metrics rise as the precursor response strengthens, but only MPA has a fixed chance level of 0.5, and the strict pre-onset versions of the F1 metrics give no credit to a response after onset (Table J).

Table J- Controlled comparison of metrics on the same predefined target, four representative scoring cases
| **Scoring case** | MPA | Window-F1 | Range-F1 | Affiliation-F1 | VUS-PR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Random scores | 0.500 | 0.092 | 0.228 | 0.653 | 0.223 |
| Weak precursor response | 0.842 | 0.513 | 0.306 | 0.697 | 0.267 |
| Strong precursor response | 1.000 | 0.893 | 0.478 | 0.826 | 0.470 |
| Response only after onset | 0.500 | 0.000 | 0.000 | 0.000 | 0.201 |

With random scores, Affiliation-F1 still reaches 0.653 and VUS-PR 0.223, so these metrics have their own baselines that cannot be compared with the 0.5 of MPA. When the model responds only after onset, MPA stays at 0.5 and Window-F1, Range-F1 and Affiliation-F1 restricted to the time before onset are 0, so these adjusted metrics also deny late alarms credit for early warning. MPA also matches its probabilistic meaning. With a mean shift of 0.25 in a 32-point window, the theoretical probability that a precursor window outscores its matched normal window is 0.8413, and the measured MPA is 0.8419. With reliable point-wise precursor ground truth, the adjusted metrics proposed by the reviewer can therefore also evaluate precursor detection. Real datasets lack such labels, so the paper uses MPA to evaluate how models separate candidate precursor windows from matched normal windows. The revision adds this experiment to App. B.5.5.

*(Continued in 5/6.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 5/6 条 · 4754 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 4/6.)*

# 9. Interval-averaged F1
We thank the reviewer for this suggestion. We computed Window-F1 on the same window-averaged scores as MPA, with the classification threshold calibrated on independent normal data. With the model scores fixed, raising the ratio of normal to precursor windows from 1:1 to 20:1 lowers Window-F1 from 0.800 to 0.167, while MPA stays at 0.750. Window-F1 thus evaluates window classification at a given threshold and depends on the class ratio, and MPA evaluates the ranking of matched windows without a fixed threshold.

# 10. Precursors on real time series
We thank the reviewer for this suggestion. App. B.2.1 now shows real 3W time series, with the raw signals of representative channels, the annotated normal, transition and fault stages, and the windows flagged by the test, so the reader can see when the test responds and to which change in the signal. Besides records whose transition is detected, it shows records with many rejections during normal operation next to records with few or none. Aligning the raw signals, the stages and the test results shows how changes of level or trend trigger the test and how changes during normal operation can lead to false rejections. These real cases complement the synthetic experiments and show both how the test responds and where it fails.

# 11. Definition of onset
The second paragraph of the introduction now defines the onset as the time at which an annotated anomaly event starts, the first time step of the anomaly interval. Pre-onset refers to the interval before this time, and near-onset to the time just before it. These definitions agree with the problem setting of §3.1.

# 12. The word causal
To avoid confusion, the revision removes the wording causal detector.

# 13. Answers to the research questions in §4
We thank the reviewer for this appreciation of the research questions. The revision reorganizes §4 so that its results map onto RQ1 to RQ3 and answers each question directly. For RQ1, 70 of the 500 evaluable events of the five benchmarks show a detectable deviation before onset. For RQ2, after multiple-testing correction no mean score of the 35 model and dataset combinations separates precursor windows significantly, while some local peaks near onset provide additional separation, which shows the limits of several common benchmarks for evaluating early warning. For RQ3, with scores and thresholds unchanged, point adjustment raises the mean Shifted-warning F1 from 0.036 to 0.177 without changing when any alarm is raised.

# 14. Exchangeability
We thank the reviewer for this suggestion. §3.2 and §3.3 now explain the meaning, the theoretical basis and the conditions of the two exchangeability assumptions. The first serves the precursor detectability test. If nothing special happens before an anomaly, the statistic $T$ of the event window and those of the placebo windows from normal operation are exchangeable, so the event statistic is not systematically larger. The empirical p-value from its rank then keeps the probability of declaring a normal window significant at or below the level $\alpha$, as for conformal p-values [g] and [h]. The second serves MPA. If the scores of a precursor window and of a matched normal window are exchangeable under the null, each is higher with the same probability, ties count one half, and the expected MPA is 0.5. The revision also states when these results hold. Overlapping windows and changing operating conditions can break exchangeability, and selecting P events with the test can give a model a higher MPA only because it detects large normal fluctuations. The paper therefore measures the actual rejection rate on held-out normal windows and uses test-positive normal pseudo-events as a selection control, which checks whether a model separates more than the selection itself explains.

# 15. Rejection rate at l.213
§3.2 now explains the rejection rate and gives its formula. A rejection means rejecting the null hypothesis that the change of the time-series features between the candidate window before onset and its reference window, or its deviation from the normal state, stays within the variation of placebo windows in normal operation. When the p-value is at most 0.05, the null is rejected and the window shows a statistically detectable deviation before onset. The rejection rate is the share of evaluable events whose candidate window is rejected.

# References

> [g] Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. Algorithmic Learning in a Random World. Springer, 2005.
>
> [h] Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan J. Tibshirani, and Larry Wasserman. Distribution-Free Predictive Inference for Regression. JASA, 2018.

*(Continued in 6/6.)*

▲▲▲ COPY TO HERE ▲▲▲


---

## 第 6/6 条 · 2770 字符

▼▼▼ COPY FROM HERE ▼▼▼

*(Continuation of 5/6.)*

# 16. Morphologies in Fig. 3
The setup of §4.1 now states that the experiment covers all eight precursor morphologies and that Fig. 3(a) shows five representative ones to avoid overlapping curves, namely level change, slow drift, variance change, spectral change and change of nonlinear dependence. These five cover different types of change and different levels of difficulty for the test. Table 5 in App. B.1.1 reports all eight morphologies at four injection strengths, including jumps, autocorrelation and linear dependence, and the main text now points to it.

# 17. Eligibility of 500 of 537 events
§3.1 and §4.2 now state the eligibility criterion. An event of the five benchmarks is eligible when the complete 100 samples before its onset lie inside one entity and overlap no other annotated anomaly interval. Of the 537 annotated events, 37 have no complete and uncontaminated interval before onset and are excluded, 7 on SMD, 1 on MSL, 0 on SMAP, 27 on PSM and 2 on SWaT. This selection depends only on data availability and the annotated intervals, not on whether the test finds a precursor, so all 500 remaining events enter the test and are then divided into P, I and O.

# Summary of revisions
- **Reasoning and counterfactual ablation in §3.2, App. A.2 and App. B.1.4.** We now state how the test is validated step by step and report Table F.
- **Alternative detection mechanisms in App. B.1.3.** We now compare the test with Online Kernel CUSUM, MMDEW and TS2Vec (Table H).
- **Range-based, affiliation and VUS metrics in App. B.5.5 and App. B.5.6.** We now report the controlled comparison of Table J and the 3W comparison of Table G.
- **Rejection rates by lead in Table 2 and §4.2.** We now report leads 10, 50, 100 and 200 and the 3W rates at every lead.
- **Real 3W series in App. B.2.1.** We now show raw signals, stages and flagged windows, including failure cases.
- **Definitions and wording in the abstract, §1, §3.1 and §3.2.** We now define onset, the rejection rate and both exchangeability assumptions, and remove the wording causal detector.
- **Research questions in §4.** We now answer RQ1 to RQ3 at the end of their results.
- **Morphologies and eligibility in §4.1, §3.1 and §4.2.** We now explain the five morphologies of Fig. 3(a) and the eligibility criterion with the excluded events per dataset.
- **New dataset in App. C.** We now describe DeviceWarning-162, released as supplementary material.

Following your suggestions, we will include these results and clarifications in the revised version. We hope these responses address most of your concerns, and we would be grateful if you would take them into account in your assessment. We are happy to clarify anything further during the discussion period.

▲▲▲ COPY TO HERE ▲▲▲
