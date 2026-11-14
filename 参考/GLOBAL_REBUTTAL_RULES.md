# 全局 Rebuttal Rule

> 适用所有会议/期刊。**一句话总纲：审稿人明天期末考，只有 10 分钟看你的 rebuttal。**
> 下面每条都是这句的推论。
>
> 按**写作顺序**排列，写的时候从上往下走即可。
> 每条末尾方括号是出处：`实录A:n` / `实录B:n` = 你自己 `cases/` 下实录的行号，
> ⭐⭐⭐ AC meta-review 点名 · ⭐⭐ 审稿人明确涨分 · ⭐ 仅格式惯例。
>
> **本模板里的行号是占位的。** 规则本体可以直接用，但背书要换成你自己读过的实录 ——
> 见 [`UPDATE_PROCESS.md`](UPDATE_PROCESS.md)。没有背书的规则只是"我认为"。

## 骨架

一份回复 = **开场两句** + **若干个 `A n.` 回答** + **收尾三句**。
一个回答 = **标题 → 逐字重述问题 → 断言 → 证据 → 解读 → 落点**。

````markdown
We thank Reviewer {ID} for the {一两个具体的肯定点}. Below, we respond to the concerns in detail.

## A1 · {一句话主题} — W1, Q1

> **W1.** {逐字重述审稿人原话}
>
> **Q1.** {逐字重述}

**A1.** We {ran/measured/compared} {具体实验}, and {直接给结果}.

{方法与引用：术语是什么 → 输出怎么读 → 我们用哪个变体（行内引用）}

Table R1: {一句实验说明}. {符号约定，含 bold 代表什么}.

| … 表 … |

{解读段，不加标签：只写表格说不出来的那一层}

*Lands in:* {一句话，补进论文哪里}.
````

**全篇只允许两个标签：`A n.` 和 `Lands in:`。** 其他一切粗体小标题都要能通过 §4 的黑名单。

## 1 · 开场

- **两句封顶。** 第一句致谢，第二句固定 `Below, we respond to the concerns in detail.`
- 第二句**不要交代结构**（几个弱点、几个问题、什么顺序）—— 小标题里已经写着了。
- 措辞按初始分分岔：

| 审稿人 | 第一句 |
|---|---|
| 正分 / 明确表态支持 | `for the constructive suggestions and positive feedback!` — 点出**具体**肯定了什么 |
| 低分 | `for the valuable comments.` — 不虚假热情、**不道歉**、无感叹号 |

- **审稿人的原话引用不要放在开场当装饰**，留给它真正当论据的那个回答。

## 2 · 一个回答的骨架

**审稿人是三层扫读：标题 → 第一句 → 有疑问才读证据。** 前两层必须已经交付答案。

```
## A n · {可核查的结论，不是话题} — W1, Q1

> **W1.** {逐字重述}

**A n.** {第一句：大白话给出原因或结论}

**{命名短语}.** {证据：数字 + 表号}
**{命名短语}.** {证据}

{诚实限定：我们不占优的、算不出的}

*Lands in:* {一句话}
```

| 层 | 要求 | ❌ | ✅ |
|---|---|---|---|
| 标题 | 给结论 | `The performance claim` | `Accuracy is a tie by construction; the separation is in cost` |
| 第一句 | 给原因或结论 | `We ran Welch t-tests over every comparison…` | `The three realisations describe the same space, so at a well-tuned operating point they can only reach the same accuracy.` |
| 块首 | 3–5 词命名短语 | `The range of settings that train at all.` | `Method X breaks on subtraction.` |
| 结尾 | 限定放最后 | 开头就让步 | `Two qualifications. …` |

**第一句按提问类型选形式**：问"你测了吗"→ **实验 → 结果**；问"为什么 / 什么因素"→ **大白话因果**。
两者都禁止用过程或元话起手（`We collected…` / `We agree at the level of…`）。

> **同一组数字，换一个因果顺序就换了性质**：把"打平"从测出来的意外改写成
> 由某个结构性质决定的必然，tie 就从缺点变成预测被验证。

### 2.1 标题与编号

- 编号一律 `W1 W2 W3` / `Q1 Q2 Q3`，**即使审稿人自己写的是 `(i) (ii)`**。
- 标题格式：`## A1 · {一句话主题} — W1, Q1`
- **一条 W / 一条 Q 各一个独立回答。** 禁止 `(W2&W3)` 式合并标签。
  合并只在三条闸门同时过时允许：**同源**（Q 是 W 的祈使句形式）·
  **无残留**（逐分句能对回原文）· **编号干净**（无重号跳号）。
  > 反面 ⭐⭐：某篇把 6 条 weakness 压成 4 个标签、`W3` 用了两次，整帖实质只有两句。
  > 该审稿人虽涨了分，但 AC 归因在别处，**这帖一分没挣**。
- **审稿人的编号和我们自己的列举编号，永远不能共用一套记号。**
- 引用块逐字重述原话，一字不改。

### 2.2 断言 `A n.`

**句式固定：我们做了什么实验 → 得到什么结果。** 第一句就是结论。

```
**An.** We {ran / measured / compared / collected} {具体到能复现的实验}, and {直接给结果}.
```

- 实验要具体：❌ `We ran the tests` → ✅ `We ran Welch two-sample t-tests with Holm correction over the four comparisons`
- **没有实验的问题**（范围/影响面类）仍然第一句给结论，只是省掉实验从句，
  但**绝不用 `We accept the framing, with one qualification` 这种纯 meta 起手**。
- 模板：`We re-ran both sweeps over three seeds, 90 runs with no missing cells, and the result is not seed noise: …`

### 2.3 证据 · 表格

**顺序：caption → 表 → 解读。表在最前面，caption 自己把实验交代清楚。**

- **caption 要短。** 一句实验说明 + 一句符号约定，到头了。
  必须含：是什么实验 · **bold 代表什么** · 表内非通用缩写的映射。
- **格子里只放数字。** 不许出现 `sig` / `tie` / `behind` / `n.s.` / `(p=.011)`。
  显著性用 **bold**，在 caption 里定义。需要 p 值就给独立一列。
  > **bold 标的是"显著"不是"赢"**，所以显著地输的格子也要加粗，
  > caption 里补一句 `the sign gives the direction`，防止 bold 被读成"我们赢的地方"。
- 列能砍就砍（重复表达同一件事的列合并掉）。
- **小表钉死差异 → 大表证泛化** ⭐⭐⭐：
  先一张 ≤3 行同数据集对照表把"我们和前人不一样"钉死，再上跨架构大表。粗体只加自己那行。
- **定性质疑要量成一列数字** ⭐⭐⭐：遇到"你凭什么说数据有性质 P"，
  别用文字论证，找一个可测代理量把所有对象测一遍列表，**不利的数值照实留着**。
- 数字一律**绝对值 + 倍数/百分比双写**：
  `from 24.35s to about 1.5s, which is nearly a 16× improvement`

### 2.4 证据 · 方法与引用

**判定/实验类用表格；定义与机制论证用段落 + 公式，不要硬塞进表格。**

> ⭐⭐⭐ 实证：某篇拿分最重的两段（一个形式化定义、一个 margin 定理）
> 都是纯段落 + 公式，被 AC 逐一点名。

**引用四条铁律：**

1. **域外术语必引。** 判据一句话：**这个词的定义在我们论文里吗？** 在 → 不引；不在 → 必引。

   | 要引 | 不用引 |
   |---|---|
   | 统计工具（t-test、Holm、bootstrap）· 跨领域指标 · 别人表里抄来的数 | 本文自己的机器 · 通识记法（95% CI、mean±std、FP32） |

2. **解释从术语本身开始**，不能只解释它的变体。顺序：
   **术语是什么 → 它的输出怎么读 → 我们用哪个变体（引用）→ 变体解决什么**

   > ❌ 只写 "Welch's variant does not assume equal variances" —— **从没说 t-test 本身在回答什么问题**
   > ✅ `A two-sample t-test asks whether two sets of runs differ by more than their own seed-to-seed noise; the p-value it returns is the probability of seeing a gap this large if the two methods were in fact equal…`

3. **行内引用，就地写全**：`(Welch, Biometrika 1947)`。
   **不要用 `[c]` 指向底部参考表** —— OpenReview 分条发帖，参考表可能落在几条之后，
   等于强迫跨帖跳转。
4. **引到条款号**：`[b, Prop. 5]`、`[e, Tabs. 3–4]`。`as shown in prior work` 是禁用的。

**`Setup` 段的必填项** ⭐⭐：
baseline 数字**分类交代来源**（抄原文→给表号 / 官方码复现 / 自己重实现→给依据）；
"相同设置"逐项列出 optimizer / lr / batch / epochs / splits，**不写 `same settings`**。

**两个能省掉整轮实验的技巧：**

| 技巧 | 怎么用 |
|---|---|
| 用文献合法缩小比较范围 ⭐⭐⭐ | `Prior work [e] has shown Y is more stable than {族Z}. Therefore, it is sufficient to compare against Y.` |
| 用数学等价性证明"已经比过了" ⭐⭐⭐ | 双方公式并排写出，指明退化条件，结论"比过 B = 比过 X" |

前提是**等价性/缩范围的理由真成立且当场写给审稿人看**，不是嘴上说"本质一样"。

### 2.5 解读段

**表格后紧跟一段，不加标签。** 标签本身不携带信息。

- **只写表格说不出来的那一层**：结论、机制、这个数为什么是这样。
- **表里有的数字不要再念一遍。** 数字有必要才给。
  > ❌ `Method X's std stays below 0.8 in all 30 cells …` —— 表里都写着
  > ✅ `Two cells changed once we ran three seeds, and both changed against the baselines…` —— 表里看不出来
- **解读要给机制，四步链条** ⭐⭐⭐：**现象 → 机制（指到定理号）→ 数据统计量 → 结论**。
  要解释"为什么在这里赢得多"，去量**输入数据本身的统计量**，不要再跑更多数据集。
- **定理也算表格**，statement 后必接一段"这对任务意味着什么"的翻译 ⭐⭐⭐。
  定理可以在 rebuttal 期现造：开头主动缩小范围 → 一个等式 + 一个不等式 → 证明扔附录 → 翻译段。
  **一页能证完的界，比"实践中没观察到"有力得多。**

### 2.6 落点 `Lands in:`

**一句短句，说明补进论文哪里。** 不要在同一行再交代顺便替换哪张表、顺便写进哪段。

> ✅ `*Lands in:* the appendix, as an added subsection of App. E.5.`
> ❌ `*Lands in:* App. E.5 (Additional Numerical Diagnostics), with Tabs. 3–4 of §4.1 replaced by these three-seed versions and the two fragilities named in the text.`

**指向的章节号必须在修订稿里真实存在**（写之前去论文里查一遍）。

---

## 3 · 收尾与给 AC 的那一层

**收尾三句**：一句"响应期不能传修订稿，以上都会进最终版" + 一句具体致谢（点名他的意见**产出了什么**）
+ 一句按分岔的索分：

- 低分：`we sincerely hope you will reconsider our rating.`
- 已过线：只致谢不索分

**AC 是独立的读者。** ⭐⭐⭐

> 某次 AC 原话：*While not all reviewers explicitly acknowledged these updates post-rebuttal, the
> substantive technical concerns … appear to be directly resolved in the revision.*
> **审稿人不回帖也能涨分，因为 AC 自己判。**

讨论期末**单发一帖 Summary of Revisions**，让 AC 不看讨论区也能独立判定"解决了"：

- 每条粗体标题**内嵌落点号**（`… in App. E.3.`）
- 正文**必须写到结论**，不止于"我们加了 X"—— AC 才能直接抄进 meta-review
  > 标准：*Results show that most θ values already match or outperform existing metrics.*（写到结论）
  > 弱版：*We added experiments on θ.*（只描述动作）
- 修订稿改动标蓝，帖首说明
- **把所有回答的 `Lands in:` 机械拼装成这一帖** —— 那个构件就是为此存在的

---

## 4 · 黑名单（提交前 grep 一遍）

| 禁用 | 为什么 |
|---|---|
| `Verdict.` · `Setup.`（当无信息标签用时）· `One limitation.` · `The change we will make.` | 粗体标题必须携带信息。读完标题不知道下面讲什么 = 占位 |
| 自造复合名词（`the divergence boundary`） | 要审稿人自己猜是哪个边界 |
| 文学化/评价性词（`the single seed had flattered them`） | 是评价不是观测。直接说 NaN 在哪个设置、哪几个 seed 上出现 |
| `One limitation.` 式自贴标签 | **"限制"不是我们要主动引入的框架。** 说成"这里为什么和论文的数不同"是澄清；说成"一个限制"是替审稿人写好扣分理由 |
| `(W2&W3)` 合并标签 | 审稿人逐条打勾时对不上号 |
| `please see Q1 below` · `as below in Question 4` | 让审稿人跳转 = 这条视为没答 |
| `[c]` 指向底部参考表 | 分条发帖后要跨帖跳转 |
| `{X} actually {是/不是} …` + 扔附录 | 硬顶懂数学的审稿人，一分没挣 |
| `so we are trying` · `still running experiments` | 既无时间承诺也无部分结果 |
| `under the same settings` | 空话，要逐项列 |
| `as shown in prior work` | 引用必须指到条款号 |
| `We could not identify the word "…" in our manuscript.` | 纯否认 = 浪费一轮 |
| 收件人张冠李戴（标题 ID ≠ Reply to ID ≠ 正文内容） | 顶会作者也犯，且犯不止一次 |

**零跳转是总原则**：宁可把同一张表贴四次、同一段话写两遍，也不要让审稿人跳一次。

> 正面 ⭐⭐⭐：把论文已有表抄进 rebuttal 并注明 `which is copied from Tabs. 2-3 from the manuscript`。

---

## 5 · 挨刀时怎么答

| 挨的刀 | 怎么答 |
|---|---|
| **提升 marginal** ⭐⭐ | ① 承认幅度小不辩解 ② 提出替代评价标准并说明为什么它更重要 ③ **同段内指向新补的跨架构证据**。缺第三步 = 空话 |
| **靠调参赢的** ⭐⭐⭐ | 甩全网格而非最优点；baseline 数抄进同一处；结论写成"**整个区间都不差**"；崩掉的点和大方差照实留 |
| **novelty incremental** ⭐⭐⭐ | 夺过打分词自己定坐标系。两种手法：**先命名坐标轴再上 ✗/✓ 表** · **给争议词下编号条件的形式化定义 → 代入前人证明不满足 → 预判并堵住最尖锐的反问** |
| **缺 baseline** | 先查等价性（§2.4 技巧二）；确实没有就划时间边界 `to the best of our knowledge, at the time of submission (before {月})` |
| **理论弱点 / 失效模式** ⭐⭐⭐ | **四段式**：① 列出所有没问题的部分，把弱点缩到**最小且唯一** ② 引先例并**引到 Prop./Sec. 号** ③ 给一行可写进论文的补救 + 落点 ④ 说明实践触发频率 + 用已有实验证明不影响结果 |
| **必然输的指标** ⭐⭐ | 给对手真实数字 → 说明结构性原因 → 明确认账（`there is no free lunch`）→ 公平比较划在同族内 → 族外列为 future work |
| **缺某个性质** ⭐⭐ | `Although our … is not X, it admits Y` 一句话认账 + 反击，给 Y 的公式，再用读者已知的情形做一句类比 |
| **无争议的事实错误** ⭐⭐ | 1–2 句认完，**无 sorry / apologize / regret**。若被升级成对实现可信度的怀疑：**先给正确事实 → 一句切断衍生指控 → 才写"已在修订稿修正"** |

**照实写不利数字是拿分动作，不是风险：**

| 做法 | 背书 |
|---|---|
| 自己的组件没什么用 → 照实写，顺势论证主实验的简化配置有依据 | ⭐⭐ |
| 全网格里崩掉的点照实留 | ⭐⭐⭐ |
| 自己方法的崩溃阈值照实报 | ⭐⭐⭐ |
| 不利的代理量照实留在表里，不删 | ⭐⭐⭐ |

---

## 6 · 提交前 Checklist

**覆盖**

- [ ] **数一遍**：审稿人的 W 条数 + Q 条数 = 我们的 `A n.` 条数
- [ ] 编号无重号无跳号；没有 `(W2&W3)` 式合并标签
- [ ] 逐分句核对：审稿人原话的每个分句都能指到我们答案里承接它的那一句
- [ ] 逐条核对 `reviewer ID ↔ 标题 ↔ Reply to ↔ 正文 W/Q 内容` 四者一致

**结构**

- [ ] 开场两句，第二句没交代结构
- [ ] 每个 `A n.` 第一句是"实验 → 结果"，实验具体到能复现
- [ ] 每个表格组下面紧跟一个解读段，且**没有复述表格已有的数字**
- [ ] 每个回答末尾有 `*Lands in:*`，一句话，章节号真实存在
- [ ] 全篇只有 `A n.` 和 `Lands in:` 两个标签

**表格**

- [ ] caption 短，且含 bold 代表什么 + 缩写映射
- [ ] 格子里没有 `sig` / `tie` / `behind` / `n.s.` / 内嵌 `(p=…)`
- [ ] bold 定义为"显著"时，显著地输的格子也加粗了，且 caption 说明了 sign 给方向
- [ ] 涉及提交版已有表格的数，**抄进来了**并注明 `copied from Tab. X in the manuscript`

**引用**

- [ ] 域外术语首次出现即带行内引用，且**从术语本身**开始解释
- [ ] 没有底部字母引用表；没有 `as shown in prior work`
- [ ] 引先例 / 引常数 / 引抄来的数字都指到了条款号
- [ ] `Setup` 里 baseline 来源分类交代；"相同设置"逐项列出

**诚实**

- [ ] 负结果、崩溃点、大方差、自己方法的失效阈值都照实留在表里
- [ ] 承诺的补充实验真能做完；没有 `still running` 式表述
- [ ] 开场与末尾措辞按初始分分岔

**黑名单**

- [ ] §4 那张表 grep 一遍，零命中

**给 AC**

- [ ] 讨论期末发了 Summary of Revisions，每条粗体标题内嵌落点号且**写到结论**
- [ ] 所有 `Lands in:` 都拼进了那一帖

---

## 7 · 关于抄别人的模板

同行常见骨架里有些是**记名创意**（特定的标签词、特定的三列判定表结构），
逐格照抄会被认出来。做法是：**拿走通用工法**（每格可执行、判定写成 if–then、钉到论文已有图号），
**留下可识别指纹**（那几个列名、标签词、行结构），换成自己的构件。

本规则库的三个构件是这么来的：

| | 通用工法 | 我们的构件 | 理由 |
|---|---|---|---|
| 答案先行 | 结论放最前 | `**A1.**` 编号断言 | 编号让 Q/A 配对可索引 |
| 判定表 | if–then 表 | `If you observe \| Then \| Why` 症状驱动 | 挨的刀是失效模式，症状驱动对口 |
| 落点 | 钉到论文位置 | `*Lands in:*` 一行 | 位置固定，末尾能机械拼成给 AC 的清单 |
