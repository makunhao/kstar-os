# KSTAR OS

> 仓库：https://github.com/makunhao/kstar-os · 在线演示：https://makunhao.github.io/kstar-os/

一句话：输入一条经历或一个任务，输出**可检索的经验**（L2）、**可调用的技能**（L3）和**可校准的预期偏差**（ΔR）。

零第三方依赖，纯 Python 标准库 + Markdown 文件。`git clone` 后用一条命令就能看到自己的第二大脑状态。

```bash
python3 scripts/kstar.py status
```

```
KSTAR OS 状态
  L1 原始  : 1 个日期文件
  L2 经验  : 5 条
  L3 技能  : 6 个（content-outline, dashboard-build, ...）
  技能调用 : 4 次
  平均|ΔR| : 0.39
```

---

## 解决什么问题

做过的事情会留下三种东西：文件、聊天记录、以及"当时为什么那样做"的记忆。
前两种能搜索，第三种通常丢了。

通用的笔记工具解决"存"，通用 AI 对话解决"这一次"。它们都不回答三个问题：

1. 下次遇到同类任务，上次的坑在哪？
2. 同一套步骤做第三遍时，能不能变成一个可调用的技能？
3. 我做完的实际结果，和开工前的预期差多少？

KSTAR OS 用四层记忆 + 一个强制的 ΔR 字段来回答这三个问题。它不是笔记软件，是**校准系统**。

---

## 快速开始

### 安装

无需安装依赖，只要 Python ≥ 3.9 与 git。

```bash
git clone https://github.com/<your-name>/kstar-os.git
cd kstar-os
python3 scripts/kstar.py status
```

### 使用（一条完整循环）

```bash
# 1) 记录原始输入
python3 scripts/kstar.py capture "交付包里的数字和原始日志对不上" --tag 交付

# 2) 开工前生成 KSTAR 计划（必须先写 R̂）
python3 scripts/kstar.py plan "重建 C6A 仪表盘" --expect "0.75"

# 3) 做完后写经验，脚本自动算 ΔR = R − R̂
python3 scripts/kstar.py episode \
  --title "C6A：扫描器首版超时" \
  --situation "对工作区做全量扫描" --task "生成提交记录" \
  --action "改用 os.walk + 目录剪枝" --result "2 秒完成，扫出 2 条记录" \
  --lesson "先确认范围，再调超时" \
  --expected 0.9 --actual 0.5

# 4) 复盘
python3 scripts/kstar.py reflect --since 2026-10-01 --write
```

### 技能

```bash
python3 scripts/kstar.py skill-new my-skill --desc "一句话说明 + 触发条件"
python3 scripts/kstar.py skill-use my-skill --context "在什么场景" --outcome "结果如何" --delta -0.1
python3 scripts/kstar.py skill-iter my-skill --frm 0.1 --to 0.2 --why "步骤缺前提" --effect "补了输入检查"
```

### 界面

```bash
python3 scripts/kstar.py export-html      # 生成 logs/kstar-dashboard.html
```

单文件、离线可开。也可以直接用 `web/index.html`（带筛选与 AI 辅助，见 C6）。

---

## 示例

输入：

```bash
python3 scripts/kstar.py recall "渲染 bug"
```

输出：

```
[recall] 「渲染 bug」命中 4 份，前 4：
    15  memory/L3_skills/submission-audit/SKILL.md
     6  memory/L2_episodes/20261004-02-c4b-codeblock-bug.md
     3  memory/L2_episodes/20261004-03-c4c-eigen-bug.md
```

它不会给你答案，但会把你上次踩坑的记录放到面前——这通常比答案更有用。

---

## 项目结构

```
kstar-os/
├── AGENT.md                  # 主配置：启动顺序、循环规则、写入纪律
├── README.md
├── LICENSE                   # MIT
├── AI_LOG.md                 # AI 使用日志（本仓库的开发过程）
├── ATTRIBUTION.md            # 拿来说明
├── CONTRIBUTING.md
├── CHANGELOG.md
├── config/
│   ├── identity.md           # L4 身份：原则与边界
│   └── tools.md              # L4 工具：只登记跑通过的
├── scripts/
│   ├── kstar.py              # CLI：capture/episode/skill/recall/plan/reflect/export
│   └── import_legacy.py      # 把旧日志导入 L2（冷启动）
├── memory/
│   ├── L1_raw/               # 原始输入（按日期，只追加）
│   ├── L2_episodes/          # KSTAR 经验 + episodes.json
│   └── L3_skills/            # 每个技能：SKILL.md / usage.json / iterations.md
├── tests/
│   └── test_kstar.py         # 9 个回归测试（复制仓库到临时目录执行）
├── examples/
│   └── demo_session.md       # 一次完整 KSTAR 循环的终端实录
└── .github/workflows/ci.yml  # Python 3.9–3.12 矩阵 + 单元测试
```

---

## 设计原则

| 原则 | 体现 |
|---|---|
| 数据用 Markdown / JSON | 十年后还能打开，能进 git，能被人读 |
| L1 只追加 | 不改写历史，保证归因可信 |
| 没有 ΔR 不算经验 | 没有预期就无法校准 |
| 技能必须有使用记录 | 没被用过的技能是文档，不是能力 |
| 能用脚本的地方不交给模型 | 判断标准固定的步骤，脚本可回归 |

详见 [`AGENT.md`](./AGENT.md) 与 [`docs/architecture.md`](./docs/architecture.md)。

---

## 技术栈

- Python 3.9+（标准库）
- Markdown + JSON 作为存储
- 无数据库、无服务端、无前端构建
- CI：GitHub Actions（3.9 / 3.10 / 3.11 / 3.12）

---

## AI 生成说明

本项目由 AI 辅助开发，设计决策、被否掉的建议、真实 bug 都记录在 [AI_LOG.md](./AI_LOG.md)。
所有代码在提交前经过 9 个回归测试；测试失败不会被跳过。

## 借鉴来源

见 [ATTRIBUTION.md](./ATTRIBUTION.md)。核心参考：Obsidian 的文件组织、PARA 的分层思想、Claude Skills 的 SKILL.md 格式、KSTAR 教学框架。

## License

MIT
