# Precursor · ICLR 2027 #32929 · 审稿原文

> 2026-11-06 从 OpenReview API（`api2.openreview.net/notes?forum=giZMDfJFwO`，张赢已登录的 Chrome）逐字取回，
> 字段原样保留 markdown 和 LaTeX，**不改一个字**（审稿人自己的笔误也照留，如 pSK8 Q4b 的 `#todo Tatbul`）。
> 网页渲染版会把 `$A_e = [t_e, u_e]$` 这类公式拆碎，引用以本文件为准。
> 逐字核对：每个字段压缩空白后的 SHA-256 前 12 位与 API 原文一致（见文末「核对」）。
> forum：https://openreview.net/forum?id=giZMDfJFwO · 三条 review 的 mdate 都是 2026-11-06 12:28 UTC（放出时间）；
> 放出后审稿人没有改过稿（`notes/edits` 每条只有一次放出时的 Edit，不含内容改动）。
> 截至取回时，论坛里只有投稿本身和三条 Official Review，没有 AC 评论。

| 顺序 | 审稿人 | note id | Rating | Confidence | Presentation | Informativeness | Soundness | 提交时间 (UTC) |
|---|---|---|---|---|---|---|---|---|
| R1 | **Tery** | `rfrdUo7k1m` | **3: Weak acceptance** | **1** | 3 | 1 | 2 | 10-19 16:43 |
| R2 | **wxGK** | `PAR0OzOilS` | **3: Weak acceptance** | 3 | 3 | 2 | 2 | 10-20 02:24 |
| R3 | **pSK8** | `My7LYUsrDR` | **1: Clear rejection** | **4** | **1** | 2 | 3 | 10-21 18:37 |

R 号按提交时间排（与 `../aaai_2027/REVIEWS.md` 同一规矩）。**引用时写审稿人 ID，不写 R 号**，避免张冠李戴。

各分项的文字标签（网页原文）：

- Rating　1 = Clear rejection · 3 = Weak acceptance（KNN++ 那篇见到 2 = Weak rejection；最高几分没核到，invitation 接口拿不到）
- Presentation　1 = Difficult to follow despite careful reading. · 3 = Clear and easy to follow.
- Informativeness　1 = I learned little or nothing new from this paper. · 2 = I learned something interesting or useful.
- Soundness　2 = I have minor or fixable concerns about the paper’s soundness. · 3 = I have no substantive concerns about the paper’s soundness.
- Confidence　1 = I do not have sufficient expertise to assess this submission reliably and have alerted the AC. · 3 = I am familiar with this topic and its relevant literature. · 4 = I have substantial direct research experience on this topic.

---

## R1 · Reviewer Tery · Rating 3 · Confidence 1

- **Note ID:** `rfrdUo7k1m`
- **Rating** — 3: Weak acceptance
- **Confidence** — 1: I do not have sufficient expertise to assess this submission reliably and have alerted the AC.
- **Presentation** — 3: Clear and easy to follow.
- **Informativeness** — 1: I learned little or nothing new from this paper.
- **Soundness** — 2: I have minor or fixable concerns about the paper’s soundness.
- **Flag For Ethics Review** — No

### Paper Summary

**I deliberately didn't use an LLM to understand the paper, since it would still camouflage my educated guess. I hope the authors understand that this review will be less useful than the others from a technical standpoint. I, however, want to praise the readability of this paper: it's the best in my batch.**

The authors identify the "precursor illusion" in time-series anomaly detection, where standard evaluation protocols extend target windows into pre-onset periods and use Point Adjustment (PA). This allows late alarms to falsely receive "early warning" credit without verifying whether pre-onset evidence actually exists. Then, they propose a placebo-calibrated (what is this?) framework to test for genuine precursor evidence using a descriptor family, introduce Matched-window Precursor AUC (MPA) to evaluate whether frozen detector scores exploit this evidence, and isolate evaluation effects while keeping detector outputs fixed.

### Critical Strengths

The paper is well-structured, and I love that you framed your research questions right from the get-go. It provides the reader with structure and immediately manages expectations. I'm in no position, however, to review this paper in confidence, as already stated. Hence, I'm giving it a weak accept, and leave it to my fellow reviewers to adjust the scoring. I appreciate the authors addressing the point adjustment problem in anomaly detection.

### Critical Weaknesses

None that I could identify.

### Questions For Authors

Is $\mathbf{\tilde{\sum}_i}^{-1}$ in Eq. 1 a covariance matrix? I'm not sure I followed the notation carefully, but I haven't seen it defined anywhere in the section.

---

## R2 · Reviewer wxGK · Rating 3 · Confidence 3

- **Note ID:** `PAR0OzOilS`
- **Rating** — 3: Weak acceptance
- **Confidence** — 3: I am familiar with this topic and its relevant literature.
- **Presentation** — 3: Clear and easy to follow.
- **Informativeness** — 2: I learned something interesting or useful.
- **Soundness** — 2: I have minor or fixable concerns about the paper’s soundness.
- **Flag For Ethics Review** — No

### Paper Summary

- This paper investigates the precursor illusion in time-series anomaly detection, where temporally shifted labels and point adjustment may credit reactive detections as early warnings without establishing detectable pre-onset evidence.

- The authors propose a model-agnostic, placebo-calibrated framework that separates precursor detectability, model use of precursor evidence, and evaluation-protocol effects. The framework tests pre-onset deviations against matched normal operation, evaluates frozen causal detector scores using matched-window precursor AUC (MPA), and compares evaluation protocols while preserving scores and thresholds.

- Experiments detect evidence in 43 of 47 annotated 3W transitions, but pre-onset deviations in only 70 of 500 evaluable events across five benchmarks, about 49 above the placebo expectation. None of the 35 benchmark mean-score MPA comparisons is significant after multiple-testing correction, whereas all seven detectors distinguish the 3W transitions; only the near-onset score peaks of LSTM-VAE separate SMD precursor windows beyond a selection control. Point adjustment substantially inflates warning F1 without changing alarm timing, and input-blind alarms at matched rates obtain higher adjusted F1 than every detector.

### Critical Strengths

**1. Separation of precursor detectability from alarm timing**

- The paper separates three questions often conflated in early-warning evaluation: whether pre-onset intervals contain detectable evidence, whether detector scores exploit it, and how evaluation protocols credit alarms. This exposes a limitation of benchmarks that define pre-onset targets by temporal proximity without verifying their distinguishability from normal operation.



**2. Controlled isolation of credit transfer across onset**

- Through trace- and threshold-preserving comparisons, the paper isolates the effects of evaluation targets and point adjustment while keeping detector scores and normalization fixed. It demonstrates that post-onset alarms can receive pre-onset warning credit without earlier detection, and that input-blind alarms at matched rates can outperform the evaluated detectors under point adjustment.

### Critical Weaknesses

**1. Limited predictive interpretation and robustness of precursor evidence**

- The test detects evidence in 43 of 47 annotated 3W transitions (§4.1), but 29.2% of pre-transition verification windows are also rejected under a separate chronological split (Appendix B.1.2). Since the test identifies deviations rather than necessarily fault-specific precursors (§5), the positive-control results may partly reflect operating-state drift.

- A five-step delayed onset produces 93% apparent precursors in precursor-free synthetic events (§4.1; Table 6). Although an onset-continuity check is reported for SMD (Table 8), corresponding benchmark checks are not reported for PSM or SWaT, whose dataset-level significance is also sensitive to placebo-pool assumptions (§4.2; Appendix B.2.2).



**2. Incomplete interpretation of negative model results**

- None of the 35 benchmark mean-score MPA comparisons is significant after correction (§4.3; Table 3), yet near-onset LSTM-VAE scores and per-machine iForest exhibit stronger discrimination (§4.3; Tables 18–19). This leaves the effects of temporal aggregation and experimental configuration insufficiently isolated.

- Statistical power further limits interpretation: the minimum detectable MPA on SMD is approximately 0.60–0.66 (§4.3), while PSM and SWaT have few precursor-positive events (Tables 2 and 14). Non-significance therefore does not establish that detectors cannot exploit precursor evidence.

### Questions For Authors

**Q1. Predictive interpretation of precursor evidence (Weakness 1)**

- Under the chronological split, 29.2% of pre-transition verification windows are rejected (Appendix B.1.2). Does the 43/47 recovery on 3W hold when the placebo null is constructed from normal operation immediately preceding each transition? Could this analysis be extended from the 16-record subset to all 47 evaluable instances?


**Q2. Robustness of benchmark precursor classifications (Weakness 1)**

- Could the authors apply the onset-continuity check (Table 8) to precursor-positive events in PSM and SWaT and report how many are classified as boundary shifts?



**Q3. Attribution of negative MPA results (Weakness 2)**

- Although none of the 35 benchmark mean-score MPA comparisons is significant after correction (§4.3; Table 3), stronger discrimination appears in near-onset LSTM-VAE and per-machine iForest analyses (Tables 18–19). Could the authors isolate the effects of temporal score aggregation and training configuration while keeping the precursor event set and normal reference fixed?



**Q4. Statistical power and interpretation of non-significance (Weakness 2)**

- Given the minimum detectable MPA of approximately 0.60–0.66 on SMD and the small precursor-positive sets for PSM and SWaT (Tables 2 and 14), could the authors clarify which effect sizes are excluded by the reported bounds, including the upper 95% bounds of at most 0.656 on SMD, and distinguish non-significance from evidence of negligible precursor discrimination (Abstract; §4.3)?

---

## R3 · Reviewer pSK8 · Rating 1 · Confidence 4

- **Note ID:** `My7LYUsrDR`
- **Rating** — 1: Clear rejection
- **Confidence** — 4: I have substantial direct research experience on this topic.
- **Presentation** — 1: Difficult to follow despite careful reading.
- **Informativeness** — 2: I learned something interesting or useful.
- **Soundness** — 3: I have no substantive concerns about the paper’s soundness.
- **Flag For Ethics Review** — No

### Paper Summary

Time series anomaly detection is reactive: it can only be detected once the anomaly appears. This paper instead looks at precursor detection, where the goal is to detect the anomaly before it actually happens. To this end, the paper first introduces a test to see whether an anomaly has an actual detectable precursor, and show that this is often not the case in many real world benchmarks. Additionally, the authors introduce MPA, a new evaluation metric for precursor detection.

### Critical Strengths

1. **Interesting problem.** The tackled problem is very interesting, and understudied in the general literature, which mostly focuses on anomaly detection, after the event has already happened. While I believe that such reactive anomaly detection is already useful in many applications, since it helps flagging events of interest which do not necessarily break the system, adding an additional focus on precursors shifts the problem in an interesting direction.

### Critical Weaknesses

1. **Technical contribution.** The technical contribution of this paper is quite limited. A statistical test is proposed to check whether there is a precursor, but this test contains many choices which were not validated. Similarly, the proposed evaluation metric MPA was only compared to pointwise and point-adjusted F1 scores, while neglecting the potential to adapt more recent anomaly detection metrics (range-based, affiliation, VUS) for evaluating precursors.  

2. **Presentation.** It was very hard to understand the paper and it took several iterations for me to be able to understand and evaluate the quality of the work. In general, there were two types of issues which prevented me understanding the paper. 
	1. There were many terms and concepts introduced that are non-standard and non-trivial, but assumed to be. The text then continues to use these without giving a clear interpretation or formal definition of the concept. Only by thoroughly reading the text, you understand the concept, and then you can re-read the text to actually know what is happening. An academic paper should be understandable after one read, with a second read only being necessary to verify the deeper technical details. 
	2. Sometimes decisions were made without clear argumentation why it was made. This only rises questions to a reader, which can be prevented easily. In some cases, a (partial) answer is in the appendix, but then there is no clear reference to the appendix in the main text (e.g., line 299, why only 5 morphologies, all results are in appendix, and there is an appendix reference but only at the end of the results of section 4.1 without any details). While more explicit references would help, argumentation in the main body would be better since it should be understandable by itself even without appendix.

### Questions For Authors

Detailed review: In the current state, I would reject this paper. Although an interesting problem is investigated, the limited technical contribution and poor presentation make me believe that the paper is not yet ready. If the presentation is substantially improved during rebuttal, I would update my rating to a weak reject, since I feel like the technical contribution can not be changed substantially within a limited time frame. I do believe, however, that this is interesting work that could benefit from additional work and rigour. 

Below, I first list the main questions I had while reading your paper, after which I give some small comments and suggestions that could be useful for a camera-ready version/next iteration. 

Q1: Your test measures whether there is a precursor in the existing benchmarks. For an anomalous event $A_e = [t_e, u_e]$ and width $W$, would it be possible to set $P_e(W) =  [t_e, t_e + W)$ and the remaining anomaly is then $A_e' = [t_e + W, u_e]$ (where you deal with anomalous intervals that are shorter than $W$)?

Q2: The precursor test (section 3.2) in some sense boils down to computing a shift in features/sequence characteristics of two consecutive windows. How do you guarantee this test catches all the precursors, since it can also be interpreted as a model to detect precursors? Additionally, why did you not use any other model (change point detection, self-supervised model, ...) to verify whether the pre-onset window is a visible precursor? 

Q3 [smaller question]: is it possible that some information is missing from table 2 and figure 4? Section 4.3 refers to these results for the discussion, but mentions things like "On SMD, the rejection rate halves within 10 minutes" and "On 3W, it stays above 0.91 at every level up to 200 seconds". However, these tables and figures do not show absolute rejection rates at different time intervals of the onset (and no results at all about 3W). I quickly scanned the appendix B2 but could also not find this information.

Q4: The related work section mentions that "Pointwise F1 poorly represents interval-valued anomalies, whereas point adjustment may substantially inflate performance by counting an entire segment as detected after a single hit" (line131). To deal with this, MPA is introduced to better measure whether the precursor is detected. I have several questions regarding this: 
Q4a: Did you evaluate whether MPA is more reliable than other metrics? Now, you only show the results using MPA without actually evaluating it. 
Q4b: Why did you not evaluate using existing anomaly detection metrics (such as range-based, affiliation-based, VUS, which were referenced)? You could also apply minor adjustments to these to not take into account late detections (e.g., for affiliation, you could make sure that the affiliation regions always and at an anomaly). In addition, the #todo Tatbul. 
Q4c: to avoid MPA being a pointwise metric, you average the anomaly scores across an anomalous interval. Could you also do this for F1, in which case it could also be a reliable metric for precursor detection? 

Q5: Can you show the precursors on real time series? Now you only show some trivial synthetic examples. It would be interesting to see some of the samples in which there is a precursor according to the test and some samples in which the test fails. 

Minor comments/suggestions: 
- The abstract and introduction (especially first paragraph) assume a precise definition of the anomaly onset and pre-onset and near-onset, without actually defining it. A short description of what the "onset" means would be helpful. You could, for example, also interpret it as the complete anomalous event. The $t_e$ notation also does not necessarily help, because it is not clear that $t_e$ is the start of the anomalous event. 
- Throughout the text, it was several times mentioned that the detectors are causal without any further explanations. However, most of the anomaly detectors do not leverage causal relations. I suggest dropping causality from the text, to avoid this ambiguity and simplify the text. 
- The research questions are very nicely posed and come back through the methodology. This unfortunately stops at the experimental evaluation (section 4), where you would expect the questions to be answered. I believe this part can be restructured. The main thing would be to formulate a clear and explicit answer to the research questions, beyond simply mentioning the numbers in the tables. 
- Several non-trivial concepts (event-placebo exchangeability, paired window exchangeability) are mentioned in passing, followed by some theoretical claim. There is no additional explanation as to why the claim follows the concept, nor is there a reference for the concept. Adding this would substantially improve understanding. 
- Line 213: a simple intuition about what the rejection rate is (i.e., the percentage of R and Q that are rejected from showing a difference) would help the understanding. I could also be useful to add an (inline) formula of this. 
- In fig. 3: there are only 5 out of 8 morphologies tested, without argumentation or clear reference to section B1.1 where all morphologies are shown. It would be useful to already explicitly mention in the setup of section 4.2 that this information is available in appendix, but also an argumentation as to why the specific subset of morphologies is shown and not everything. 
- Line 355: discuss why are only 500 out of 537 events eligible. It is not clear what the criteria for being eligible is. It is not having a precursor, since otherwise all 500 events would be in $P$.

---

## 核对（API 原文 vs 本文件）

压缩空白（`\s+` → 单个空格、去首尾）后取 SHA-256 前 12 位。`check_reviews.py` 重算本文件这一侧。

| 审稿人 | Paper Summary | Critical Strengths | Critical Weaknesses | Questions For Authors |
|---|---|---|---|---|
| Tery | `b66dbc97ed5d` | `7f64c8beb95f` | `f34f133e4b8a` | `a72171cde6f0` |
| wxGK | `6917079ff049` | `75f517ed13b1` | `c30914ccc5fd` | `573b50d93011` |
| pSK8 | `c0743453d5dc` | `d8f43151830e` | `9bf9a922a414` | `fd469f66e652` |
