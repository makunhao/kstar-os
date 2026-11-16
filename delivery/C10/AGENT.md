> **位置说明**：本文件是 `agent-os/AGENT.md` 在包根目录的入口副本。
> 规范正文的唯一出处是 `agent-os/AGENT.md`；本副本与其内容一致，仅为满足评审按根目录 `AGENT.md` 检索。
> 若两者不一致，以 `agent-os/AGENT.md` 为准。

---

# AGENT.md — KSTAR OS 主配置

> 这是系统的「操作系统内核」：定义我是谁、记忆怎么用、每类任务走哪条循环、什么情况下改技能。
> 任何 AI 会话开始时，先读本文件 + `config/identity.md` + 相关 `memory/L3_skills/*/SKILL.md`。

## 0. 启动顺序（每次会话固定 4 步）

1. 读 `config/identity.md`：我是谁、当前角色、当前项目。
2. 读 `memory/L2_episodes/episodes.json` 最近 5 条：上次踩过什么坑。
3. 按任务关键词执行 `python3 scripts/kstar.py recall "<任务关键词>"`，拿到相关 Skill 与经验。
4. 若任务超过 30 分钟，先 `kstar.py plan` 生成 KSTAR 计划并写死 R̂。

## 1. 五层架构

| 层 | 位置 | 约束 |
|---|---|---|
| L1 原始输入 | `memory/L1_raw/YYYY-MM-DD.md` | 只追加，不修改；原话优先 |
| L2 KSTAR 经验 | `memory/L2_episodes/*.md` + `episodes.json` | 必须有 R̂ / R / ΔR / 教训，缺一不算 |
| L3 技能 | `memory/L3_skills/<name>/SKILL.md` | 必须有 When / Input / Steps / Output / 使用记录 |
| L4 工具 | `config/tools.md` | 只登记「实际能用」的工具；装了不等于能用 |
| L5 界面 | `scripts/kstar.py` + `logs/kstar-dashboard.html` | CLI 优先，界面后置 |

## 2. Agent Loop（KSTAR）

```
K  recall  → 从 L2/L3 检索同类经验
S  情境     → 写清约束（时间/环境/权限）
T  任务     → 一句话 + 可验证的成功标准
Â  计划     → 步骤 + R̂（0–1 的达成度预估）
A  执行     → 调 Skill / 跑脚本 / 写文件
R  结果     → 记录真实产出与证据路径
ΔR = R − R̂  → 写进 L2，作为下次的检索依据
```

**硬规则：没有 R̂ 的执行不算一次 Agent Loop，只是干活。**

## 3. 技能生命周期

- 同类事情做到第 3 次 → 提炼为 Skill（`skill-new`）。
- 一个 Skill 连续 3 次使用 ΔR 都为负 → 必须改步骤或工具（`skill-iter`）。
- 连续 4 周零调用 → 标记 `status: deprecated`，从默认检索中排除。
- 两个 Skill 经常同时出现 → 合并为 macro-skill。
- 技能不是文档：`Steps` 必须是可执行动作，不能写「认真分析」。

## 4. 写入纪律

1. **一份数据只有一个出处。** 数字写在产物文件里，文档引用路径，不复制第二份。
2. **失败必须留在 L2。** 只记成功经验的系统会越来越自信、越来越错。
3. **AI 生成的内容必须有出处。** 外部事实要能指回原始链接或本地文件；不能指回的，标 `未核实`。
4. **不改历史。** L1 只追加；L2 要修正就新写一条并注明「修正自 <id>」。

## 5. 当前入口

```bash
cd agent-os
python3 scripts/kstar.py status
python3 scripts/kstar.py recall "交付包 自检"
python3 scripts/kstar.py plan "给 C6A 做数据仪表盘"
```

## 6. 与 Elite20 的映射

| 挑战 | 沉淀到本系统的位置 |
|---|---|
| C1 翻译 | L2 经验 `c1-*` + L3 `translation-check` |
| C2 论文 | L2 `c2-*` + 技能 `paper-build` |
| C3 群内参与 | L2 `c3-*` + 技能 `engagement-check` |
| C4 技能 | L3 全部技能 |
| C5 GitHub | L4 工具层 `repo-release` |
| C6 Web App | L4 `deploy-check` + L3 `webapp-ship` |
| C6A 仪表盘 | L3 `dashboard-build` |
| C7 内容 | L3 `content-outline` |
| C8/C9 | L2 项目经验 + 每周 AAR 模板 |
