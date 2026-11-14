# When Early Is Not Early

*Author response · ICLR 2027 · Submission 32929*

This repository holds the author response to *When Early Is Not Early: The Precursor Illusion in Time-Series Anomaly Detection* ([OpenReview](https://openreview.net/forum?id=giZMDfJFwO)).
The paper asks three questions of early-warning benchmarks: whether evidence exists before an anomaly begins, whether detectors use it, and how evaluation rules credit them.
Here are the replies, the analyses behind every new number, and the tooling that turns drafts into OpenReview posts.

## Reviews

| Reviewer | Rating | Confidence | Central concern |
| :--- | :---: | :---: | :--- |
| Tery | 3 · Weak accept | 1 | Definitions of placebo calibration and of the matrix in Eq. 1 |
| wxGK | 3 · Weak accept | 3 | Validity of the 3W control, annotation offsets, attribution of negative results, power |
| pSK8 | 1 · Clear reject | 4 | Validation of design choices, comparison with range-based metrics, presentation |

Responses and the revised PDF are due on **18 November 2026, AoE**. Decisions follow on 16 December.

## What the response establishes

| Question | Finding | Table |
| :--- | :--- | :---: |
| 3W control | Transition starts are detected in 11 of 19 records against 4.1% false alarms. Detections hours after the reference cannot be separated from drift. | A |
| Annotation offsets | 6 of 7 PSM and 7 of 9 SWaT precursor-positive events are boundary shifts, so benchmark-level evidence rests on SMD. | B |
| Attribution | No training or aggregation setting separates precursor events from the selection control. The per-machine claim is withdrawn. | C |
| Power | MPA of 0.66 or more is excluded on SMD. Small effects remain open. | D |
| Robustness | Varying each setting of Tab. 1 in turn yields 60 to 90 precursor-positive events. | E |
| Metrics | An AUC truncated at onset ranks detectors as MPA does, with Spearman 0.96 on SMD. | F |
| Descriptors | A descriptor-free kernel test finds 36 of 500 benchmark events, against 70 for the descriptor test. | H |

Every number traces to an experiment record listed in [`new_results/README.md`](new_results/README.md).

## Layout

```
00_提交/                  replies, one file per thread, the single source of truth
  0_全局总回复.md            general response
  1_R1_Tery.md  2_R2_wxGK.md  3_R3_pSK8.md
  4_Summary_of_Revisions.md
06_网站/                  local workbench, rendered from 00_提交/
REVIEWS.md               verbatim reviews with checksums
TRACKER.md               one row per point: disposition, evidence, status
MANUSCRIPT_CHANGES.md    revisions promised to the paper
new_results/             pointers from each new number to its experiment
evidence_packets/        line-numbered paper text and source notes
参考/                     submitted PDF and writing rules, read-only
sync.py                  splits replies at the 5,000-character limit and rebuilds the workbench
```

## Workflow

```bash
git pull
# edit 00_提交/*.md between the COPY markers
python3 sync.py                   # re-split, check citations, rebuild the workbench
python3 06_网站/serve.py 8778     # http://localhost:8778/index.html
git switch -c <initials>/<topic>  # collaborators work on a branch
git push                          # then open a pull request
```

Review happens on pull requests. Comment on any line under *Files changed*.
Agents read [`CLAUDE.md`](CLAUDE.md) for the editing rules.

## Conventions

Each section of a reply thanks the reviewer, states what was checked, describes the experiment, and reports one compact table with its reading and the resulting revision.
Line, table and section numbers refer to the submitted PDF. New tables are lettered across threads, A to D for wxGK and E to J for pSK8.
