# 架构说明：KSTAR OS

> 输入：一条经历、一个任务、一次失败。
> 输出：可检索的经验（L2）、可调用的技能（L3）、可对比的预期偏差（ΔR）。
> 系统的唯一硬指标：**同一类事情做第二次时，比第一次快，且错得更少。**

---

## 一、为什么做这个系统

我做过的事情散在三个地方：飞书群里的讨论、`D:/ai+x` 的交付包、以及 `.workbuddy/memory/` 的日志。
2026-10 的旧交付包丢失之后，我发现一个尴尬的事实：**文件可以重建，但我当时为什么那样决策，只在日志里。**

通用的笔记软件解决"存"，不解决"用"。通用 AI 对话解决"这一次"，不解决"下一次"。

所以这个系统的设计起点不是"知识管理"，而是三个具体问题：

1. 下次遇到同类任务，我能不能先看到上次的坑？（检索）
2. 同一套步骤做第三遍时，它能不能变成一个可调用的技能？（抽象）
3. 我做完之后的实际结果，和我开工前的预期差多少？（校准）

这三个问题分别对应 KSTAR 四层记忆里的 L2、L3，以及 Agent Loop 里的 ΔR。

---

## 二、五层架构

```
kstar-os/
├── AGENT.md                    ← 主配置：启动顺序、循环规则、写入纪律
├── agent-os/
│   ├── config/
│   │   ├── identity.md         ← L4 Identity：我是谁、原则、角色边界
│   │   └── tools.md            ← L4 Tool：只登记跑通过的工具
│   ├── memory/
│   │   ├── L1_raw/             ← 原始输入，按日期，只追加
│   │   ├── L2_episodes/        ← KSTAR 经验 + episodes.json 索引
│   │   └── L3_skills/          ← 每个技能一个目录：SKILL.md / usage.json / 脚本
│   ├── inbox/                  ← 未结构化输入
│   ├── logs/
│   │   ├── agent_runs.jsonl    ← 每次调用都留痕
│   │   └── kstar-dashboard.html← 静态面板（export-html 生成）
│   └── scripts/
│       ├── kstar.py            ← CLI：capture/episode/skill/recall/plan/reflect/status/export
│       └── import_legacy.py    ← 把既有日志导入 L2（冷启动）
└── examples/                   ← 可运行的演示与终端实录
```

### Layer 1 · Memory

| 层 | 存什么 | 实现 | 硬约束 |
|---|---|---|---|
| L1 原始 | 原话、链接、当时的状态 | `L1_raw/YYYY-MM-DD.md`，追加写 | 不改写历史 |
| L2 经验 | S/T/A/R + R̂/R/ΔR + 教训 | `L2_episodes/<id>-<slug>.md` | 没有 ΔR 不算经验 |
| L3 技能 | 可执行步骤 | `L3_skills/<name>/SKILL.md` | Steps 必须是动作，不是形容词 |
| L4 身份 | 角色、原则、工具边界 | `config/identity.md`、`tools.md` | 工具必须冒烟测试过 |

L1→L2 的关键不是"总结"，是**标注预期**。没有 R̂ 的记录只是日记，无法校准。

L2→L3 的晋升规则：同类经验出现 ≥3 次，或单次经验被复用 ≥2 次，才允许写成技能。
这个门槛是故意的——过早抽象会得到一个看起来很专业、但没人用的技能库。

### Layer 2 · Skill System

每个技能目录包含：

```
L3_skills/<name>/
├── SKILL.md        ← frontmatter(name/description/version/status) + What/When/Input/Steps/Tools/Output
├── usage.json      ← 每次调用：时间、上下文、结果、ΔR
├── iterations.md   ← 版本改动、原因、效果
└── *.py            ← 可选：确定性脚本（能用脚本的，不交给模型）
```

技能有两种：**脚本型**（submission-audit、dashboard-build、repo-release、github-repo-analysis、weekly-aar）和**流程型**（content-outline）。
脚本型的判断标准固定、可回归；流程型依赖判断，只给骨架，避免把写作变成填空。

### Layer 3 · Agent Loop

`kstar.py plan` 先做检索，再输出 K/S/T/Â/R̂ 模板。执行后 `episode` 写入真实 R 与 ΔR。
`reflect` 按时间窗聚合：平均 ΔR、|ΔR| 最大的三条、技能调用分布。

ΔR 的用法不是"打分"，而是分诊：

| 现象 | 判断 | 动作 |
|---|---|---|
| ΔR ≈ 0 | 预期准确，技能有效 | 继续用，不改 |
| ΔR < 0 且集中在同一技能 | 技能步骤有隐藏前提 | 改步骤（skill-iter） |
| ΔR > 0 且稳定 | 预期过于保守 | 校准 R̂，不是改技能 |
| 连续 3 次 ΔR < -0.3 | 前提可能错了 | 停下来验证前提，不是修参数 |

### Layer 4 · Tool / Access

工具清单在 `config/tools.md`，只写跑通过的。当前核心：Python 3.10、git、Node 22、MiKTeX、openpyxl、Pillow、ffmpeg、Chrome、Claude。
没有装 `gh`，所以 GitHub 操作走 `git` + token，而不是假装有 CLI。

### Layer 5 · Interface

- 主界面：CLI（`kstar.py status / recall / plan / episode / reflect`）
- 次界面：`export-html` 生成单文件面板，手机也能打开
- 不做 Chat UI：当前阶段，聊天界面会增加维护成本，不增加记忆质量

---

## 三、三个关键设计决策（含代价）

### 决策 1：用 Markdown + JSON，不用数据库

**理由**：数据要能在任何编辑器里读、能进 git、能在十年后打开。SQLite 也能做到，但迁移成本更高。
**代价**：跨文件检索是线性扫描。当前 5 条经验、6 个技能，扫描耗时 <50ms；超过约 2000 条时需要建倒排索引。
**触发条件**：`recall` 单次超过 300ms 就换 SQLite FTS，不提前优化。

### 决策 2：L1 只追加，不允许编辑

**理由**：事后修改的"原始记录"会破坏归因。C3 那次抽样误判之所以能被发现，是因为原始拉取结果还在。
**代价**：错误笔记会一直留着，需要 L2 里写"修正自 <id>"。
**取舍**：宁可保留噪声，也不让历史被美化。

### 决策 3：ΔR 必须由人写，不让模型自动打分

**理由**：模型倾向于给"完成度 0.8"这种没有信息量的分数。R̂ 的价值在于事前承诺，事后再让模型补写就失去校准意义。
**代价**：每次记录多花 30 秒。
**验证**：导入的 5 条历史经验里，ΔR 为负的 4 条都对应真实返工；模型自动打分时这些都会被记成"基本完成"。

---

## 四、自进化机制

| 能力 | 规则 | 当前状态 |
|---|---|---|
| 从经验生成技能 | 同类 ≥3 次 或 复用 ≥2 次 | 已用：repo-release 来自 C5 的重复打包动作 |
| 优化技能 | 连续 3 次 ΔR < 0 必须改 | submission-audit 已从 0.1 迭代到 0.3 |
| 淘汰技能 | 连续 4 周零调用 → deprecated | 待观察（系统 2026-11-16 建立） |
| 技能组合 | 两个技能同时出现 ≥3 次 → macro | dashboard-build + submission-audit 候选 |

**淘汰不是删除**：标 `status: deprecated`，保留历史，避免"去年那个方法叫什么来着"。

---

## 五、拿来主义（简版，详见《十三_C10_拿来说明.md》）

| 来源 | 拿了什么 | 改了什么 |
|---|---|---|
| Obsidian / Zettelkasten | 文件夹 + 双向链接的组织直觉 | 用 KSTAR 四层替代自由标签，链接改为显式 `[[name]]` |
| PARA | 按可行动性分层 | 四层改为"原始→经验→技能→身份"，因为 PARA 不区分"经验"和"能力" |
| Claude Skills | SKILL.md 的 frontmatter + 渐进加载 | 增加 usage.json 与版本淘汰机制；技能必须带使用记录 |
| KSTAR 教学框架 | K/S/T/Â/R̂ 五段 | 把 R̂ 变成可计算的 ΔR，并作为技能迭代的触发器 |
| Getting Things Done | 收集箱（inbox） | 只保留 inbox，不做上下文清单，避免系统变成待办软件 |

---

## 六、复现步骤（别人拿到这个目录）

```bash
cd agent-os
python3 scripts/kstar.py status          # 应显示 5 条经验、6 个技能
python3 scripts/kstar.py recall "渲染 自检"
python3 scripts/kstar.py plan "下周的 C7 文章"
python3 scripts/kstar.py reflect --since 2026-10-01
```

零第三方依赖，Python ≥3.9。Windows / macOS / Linux 均可。
数据目录结构固定，换机器只拷贝 `agent-os/` 即可。

---

## 七、当前实测规模（2026-11-16）

- L2 经验：5 条导入（2026-10-02 / 10-04，来源 `.workbuddy/memory/`）+ 本次新增 2 条
- L3 技能：6 个，均有 SKILL.md；其中 5 个有真实调用记录
- 运行日志：见 `agent-os/logs/agent_runs.jsonl`
- 平均 |ΔR|：0.39（历史导入样本，偏大——说明当时的事前预期普遍过于乐观）

---

## 八、边界与未完成（如实写）

1. **系统建立于 2026-11-16**，"连续使用两周"的要求尚在积累。已导入 2026-09/10 的真实项目经验做冷启动，但这不是"用该系统用了两个月"。
2. **L1→L2 仍是半自动**：capture 是手动的，没有做"从 git log / 聊天记录自动生成候选经验"。
3. **检索是关键词匹配**，没有向量检索；同义表达会漏。当前用"多写几个说法"绕过。
4. **没有多设备同步**：数据在本地文件夹，靠 git 备份。
5. **技能质量参差**：6 个里 5 个有脚本，content-outline 只有骨架，靠人执行。
