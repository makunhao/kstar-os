# C10 交付包 · 构建长期智能体（KSTAR OS）

一个 Markdown 驱动的第二大脑：四层记忆 + 可调用技能 + KSTAR 认知循环 + ΔR 校准。

## 文件

```
C10交付包/
├── README.md
├── 十三_C10_architecture.md      ← 五层架构与三个关键设计决策
├── 十三_C10_usage_log.md         ← 7 次真实调用记录（含 ΔR）
├── 十三_C10_AAR.md               ← 系统级复盘
├── 十三_C10_AI日志.md            ← 8 轮构建过程 + 3 个真实 bug
├── 十三_C10_拿来说明.md
├── 十三_C10_skills/              ← 6 个技能副本（SKILL.md / usage.json / 脚本）
├── agent-os/                     ← 可运行系统
│   ├── AGENT.md                  ← 主配置
│   ├── config/                   ← identity.md / tools.md
│   ├── memory/                   ← L1 / L2 / L3
│   ├── scripts/kstar.py          ← CLI（10 个命令）
│   ├── scripts/import_legacy.py  ← 历史经验导入
│   └── logs/                     ← agent_runs.jsonl + 静态面板
└── demo/                         ← 终端实录与演示视频
```

## 五层映射

| 层 | 位置 | 状态 |
|---|---|---|
| L1 记忆 | `agent-os/memory/L1_raw` | 1 个日期文件 |
| L2 经验 | `memory/L2_episodes` | 7 条（5 导入 + 2 本次） |
| L3 技能 | `memory/L3_skills` | 6 个，7 次调用，1 次迭代 |
| L4 工具/身份 | `config/tools.md`、`identity.md` | 跑通过的工具才登记 |
| L5 界面 | CLI + `export-html` | 可用 |

## 快速开始

```bash
cd agent-os
python3 scripts/kstar.py status
python3 scripts/kstar.py recall "渲染 bug"
python3 scripts/kstar.py plan "下周的 C7 文章" --expect 0.7
python3 scripts/kstar.py reflect --since 2026-10-01
```

零第三方依赖，Python 3.9+。

## 关键数字

- L2 经验 7 条，平均 |ΔR| **0.319**
- 5 条历史经验中 **4 条 ΔR 为负**，平均 **−0.27**（系统性高估）
- 6 个技能全部至少使用 1 次；`dashboard-build` 已迭代到 v0.2

## 诚实边界

- 系统建立于 2026-11-16，**只有一天的真实使用**；历史经验是导入整理，不等于用了两个月。
- L1→L2 半自动、同义词检索、技能淘汰提醒未实现。
- 演示视频由真实终端输出合成（30 秒），不是屏幕录制。
