# rebuttal 期新结果 · 只放指针

**不在这里跑实验，也不放数据。** 补实验回 `../../../3_Experiments/` 立 `E-nnn`（验证型要预注册，探索型不许出 verdict），
这里一行一个指针，指向 `result.json`。回复里引用的每个新数字，都要能从这张表走到文件。

| TRACKER 行 | 实验 | 类型 | result.json | 回复里用在哪 | 状态 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |
| —（11-10 作业 ①，无对应 TRACKER 行） | `E-011_event-level-alarm-precursor-overlap` | 探索 | `../../../3_Experiments/E-011_event-level-alarm-precursor-overlap/results/result.json` | 未定（表格版：`../evidence_packets/11-10_①重合度.md`） | 已出结果 |
| R2-1（wxGK W1a / Q1） | `E-013_3w-matched-gap-reference-false-alarm` | 验证（C-005） | `../../../3_Experiments/E-013_3w-matched-gap-reference-false-alarm/results/result.json` | wxGK 回复 §1 表 A（正常窗口误报） | 已出结果：G0 支持，G1 / G4 / G8 无结论，总判无结论 |
| R2-1（11-10 作业 ⑧） | `E-012_3w-time-thirds-rejected-window-evidence` | 探索 | `../../../3_Experiments/E-012_3w-time-thirds-rejected-window-evidence/results/result.json` | 未定（表格版：`../evidence_packets/11-10_⑧误判窗口证据.md`） | 已出结果 |
| R2-1（wxGK Q1 检出那一半） | `E-022_3w-adjacent-reference-recovery` | 探索 | `../../../3_Experiments/E-022_3w-adjacent-reference-recovery/results/result.json` | wxGK 回复 §1 表 A（过渡起点 / 故障前检出）；figures/ 46 张原始曲线；全局回复 §1.3 | 已出结果 |
| R2-1（wxGK Q1 同距离对照） | `E-023_3w-long-normal-matched-gap-placebo` | 探索 | `../../../3_Experiments/E-023_3w-long-normal-matched-gap-placebo/results/result.json` | wxGK 回复 §1 表 A 第 4、5 行（49–75%，预期 10.3）；全局回复 §1.3；附带 operator_check / fault_controls_at_start（未进回复） | 已出结果 |
| R2-1（wxGK Q1 参照空隙 × 段长） | `E-024_3w-reference-guard-and-scan-length` | 探索 | `../../../3_Experiments/E-024_3w-reference-guard-and-scan-length/results/result.json` | 附录变体表（空 30 分钟单窗口 12/19、5.6%） | 已出结果 |
| R2-1（wxGK Q1 判定规则） | `E-025_3w-scan-decision-rules` | 探索 | `../../../3_Experiments/E-025_3w-scan-decision-rules/results/result.json` | wxGK 回复 §1 表 A 第 1、2 行（空 30 分钟 + 10 分钟 + 连续 3 窗口：11/19、4.1% [0.7%, 9.0%]）；全局回复 §1.3 | 已出结果 |
| —（11-13 杨悦会：为什么 100）· R3-8 | `E-014_rq1-window-scale-and-lead-range` | 探索 | `../../../3_Experiments/E-014_rq1-window-scale-and-lead-range/results/result.json` | pSK8 回复表 I、J；全局回复 §3 | 已出结果 |
| —（11-13 杨悦会，模型侧） | `E-015_rq2-mpa-window-length` | 探索 | `../../../3_Experiments/E-015_rq2-mpa-window-length/results/result.json` | 未用（1000 步的模型结果先不主动讲） | 已出结果 |
| R2-2（wxGK W1b / Q2） | `E-016_onset-continuity-psm-swat` | 探索 | `../../../3_Experiments/E-016_onset-continuity-psm-swat/results/result.json` | wxGK 回复 §2 表 B；全局回复 §1.4 | 已出结果 |
| R3-7（pSK8 Q2） | `E-017_descriptor-free-kernel-test` | 探索 | `../../../3_Experiments/E-017_descriptor-free-kernel-test/results/result.json` | pSK8 回复表 H；全局回复 §1.1 | 已出结果 |
| R3-11（pSK8 Q5） | `E-018_real-sequence-examples` | 探索（只出图） | `../../../3_Experiments/E-018_real-sequence-examples/results/result.json` | pSK8 回复 §10 | 已出图 |
| R3-2（pSK8 W1a） | `E-019_robustness-corrected-split-import` | 基建（导入 09-23 已有结果） | `../../../3_Experiments/E-019_robustness-corrected-split-import/results/result.json` | pSK8 回复表 E；全局回复 §1.2 | 已导入、已核对 |
| R2-3（wxGK W2a / Q3） | `E-020_smd-training-vs-aggregation-2x2` | 探索 | `../../../3_Experiments/E-020_smd-training-vs-aggregation-2x2/results/result.json` | wxGK 回复 §3 表 C；全局回复 §2.1 | 已出结果 |
| R3-3 · R3-9（pSK8 W1b / Q4） | `E-021_truncated-auc-vs-mpa` | 探索 | `../../../3_Experiments/E-021_truncated-auc-vs-mpa/results/result.json` | pSK8 回复表 F、§8；全局回复 §2.3 | 已出结果 |

## TRACKER 里标了 `实验` 的（11-06 初判，做不做由作者定）

| TRACKER 行 | 要什么 | 估计成本 | 回顾里的现成条目 |
|---|---|---|---|
| R2-1 | 3W：placebo 改用每个过渡紧邻之前的正常段；16 条 → 47 条 | 只跑检验，CPU | — |
| R2-2 | Tab. 8 的 onset 连续性检查扩到 PSM、SWaT 的 P 事件 | 只跑检验，CPU | §4.4 #3 附近 |
| R2-3 | 固定 P 事件集和正常参照，隔离「分数聚合」与「训练配置」 | 要 pooled 训练的 dump（先确认 Leonardo 上还在） | §4.4 #2 |
| R3-2 | 修正切分下重跑描述子稳健性，报数据集层面结果 + Jaccard | 只跑检验，CPU | §4.4 #3 |
| R3-3（可选） | 截断在 onset 的 affiliation / VUS 作对照 | 用现有分数，不训模型 | — |
| R3-7（可选） | 变点检测作为另一种「可见前兆」判据 | 只跑检验，CPU | — |
| R3-11 | 真实序列样例图（P / O 各几例 + 3W） | 只画图 | — |

已经算好、可以直接用的：回顾 §4.4 #1（SMD 7 格内 BH：MPA^P 最小 q = 0.32，ΔMPA 最小 q = 0.10，出自 E-004 CSV）。
按项目规矩，开 `E-nnn` 前先写三行（问题 / 判据 / 对照）。
