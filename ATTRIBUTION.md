# 拿来说明（Attribution）

> 本项目的设计不是原创，是把几个已验证的方法拆开、删掉不适用的部分、再组合。
> 下面写清楚：从哪拿、拿了什么、改了什么、为什么。

## 参考系统

| 系统 / 方法 | 链接 | 拿了什么 | 改了什么 |
|---|---|---|---|
| **Obsidian / Zettelkasten** | https://obsidian.md | 文件夹 + 双向链接的组织直觉；本地文件优先 | 用 KSTAR 四层替代自由标签；链接改为显式 `[[name]]`，减少"链接很多但没用" |
| **PARA 方法** | https://fortelabs.com/blog/para/ | 按"可行动性"分层，而不是按主题分类 | PARA 的四层（Projects/Areas/Resources/Archive）改为 L1 原始 / L2 经验 / L3 技能 / L4 身份；因为 PARA 不区分"经验"与"能力" |
| **Claude Skills** | https://docs.claude.com/en/docs/claude-code/skills | `SKILL.md` 的 frontmatter + 正文结构；渐进加载 | 增加 `usage.json` 与 `iterations.md`；技能必须有调用记录，否则不算能力 |
| **KSTAR 教学框架** | 课程内部材料 | K / S / T / Â / R̂ 五段 | 把 R̂ 落成数值并计算 ΔR，作为技能迭代的触发器 |
| **Getting Things Done** | https://gettingthingsdone.com | "收集箱"（inbox）先收后处理 | 只保留 inbox，不做上下文清单；避免系统退化成待办软件 |
| **Git** | https://git-scm.com | 追加式历史、可追溯 | L1 只追加、不修改，借鉴 commit 的不可变性 |

## 代码与库

| 来源 | 拿了什么 | 说明 |
|---|---|---|
| Python `argparse` 文档 | 子命令组织方式 | 标准库，无第三方依赖 |
| Python `pathlib` 文档 | 路径处理 | 跨平台 |
| 本项目 C6A 的 `dashboard-build` | HTML 模板的卡片/热力图布局 | 同一作者，模板复用 |
| 无 | 无第三方运行时依赖 | 刻意保持零依赖，方便在任何机器上跑 |

## 明确没拿的

| 没拿 | 原因 |
|---|---|
| LangChain / LlamaIndex | 本项目不需要 agent 编排框架；Markdown + CLI 足够 |
| 向量数据库 | 数据量小；引入后会增加部署与迁移成本 |
| 现成的笔记应用模板 | 会绑定特定应用；本项目的目标是"数据属于自己" |
| 云同步服务 | 隐私与可迁移性优先；用 git 备份 |

## 引用规范

- 文档中出现的每个数字（5 条经验、6 个技能、9 个测试）都能通过 `python3 scripts/kstar.py status` 或测试命令复算。
- 外部方法与概念在首次出现处标注来源；没有来源的判断会写成"我的判断"，不伪装成引用。
