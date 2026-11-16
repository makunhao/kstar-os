# C5 AI 日志：把能力打包成仓库

> 完整开发日志在仓库内 `AI_LOG.md`；这里记录"为 C5 做包装"的过程与判断。

## Round 1 · 选项目

**prompt 要点**：
> 「C5 的最高权重是实用性与可复现性。下面三个候选里选一个：A 提问诊断器、B 交付体检器、C KSTAR 记忆系统。给出选择依据，不要按代码量选。」

**它的建议**：B 或 C。
**我的判断**：选 C。理由：它是本次九个交付包的地基（C6 的界面、C8/C9 的 demo 都依赖它），而且零依赖、9 个测试可验证"clone 后能跑"。

## Round 2 · 仓库结构

**prompt 要点**：
> 「按 C5 检查清单生成仓库骨架：README / LICENSE / .gitignore / AI_LOG / ATTRIBUTION / CONTRIBUTING / CHANGELOG / tests / CI / issue 模板。README 必须能在 5 分钟内让陌生人跑起来。」

**产出**：8 个顶层文档 + `tests/` + `.github/`。
**我补的**：`examples/demo_session.md`（真实终端记录）、`docs/architecture.md`（设计决策与代价）。

## Round 3 · 测试（真实失败过一次）

首版测试只有 6 个，全部通过。但跑 `skill-use` 拼错名字时发现：**不报错，会创建幽灵技能**。
补了错误路径用例后，先红后绿：

```
FAIL: test_skill_use_rejects_unknown_skill
AssertionError: 0 != 2
```

修 `kstar.py`：加 `_require_skill()`。再跑 9 个全绿。

## Round 4 · 提交历史

要求：每条提交信息能独立说明"改了什么、为什么"。
实际 12 条：

```
chore: 初始化 KSTAR OS 骨架与 L4 身份/工具配置
feat: KSTAR CLI 与四层记忆
feat: 导入 5 条历史经验与 6 个可调用技能
feat: 旧日志导入器（L2 冷启动）
test: 9 个回归测试覆盖全部命令
docs: README、架构说明、贡献指南与 AI 日志
ci: GitHub Actions（3.9–3.12）+ issue/PR 模板
feat(web): 单文件 KSTAR 助手（检索 + 计划 + 可选 AI）
chore: 补入历史经验数据源（import_legacy 的输入）
chore: repo-release 增加一条真实使用记录（发布检查）
chore(pages): 提供 docs/ 入口，适配 GitHub Pages 的目录限制
docs: 补充线上地址、Pages 入口与 token 使用说明
```

**它建议过**：「先 `git init` 再一次性 `git add . && git commit`，省事。」
**我否掉**：一条 "init" 提交无法让别人看懂演进，也会让 CHANGELOG 与实际不符。

## Round 5 · 包装与截图

- 用 `repo-release` 技能跑发布检查：缺 `README` 章节 → 补；缺依赖声明 → 在 README 说明"零依赖"。
- README 用 Python-Markdown 渲染成本地 HTML，再截图。**没有说成"GitHub 页面截图"**。

## 真实阻塞

| # | 阻塞 | 影响 | 处理 |
|---|---|---|---|
| 1 | 无 GitHub token | 无法 push、无法给仓库链接 | 保留完整本地仓库 + 推送命令，不预填 URL |
| 2 | 挂载盘不支持 git 的删除/原子替换 | 在 D 盘直接 `git init` 会产生 `HEAD.lock` 死锁 | 在 Linux 工作区构建仓库，再整体拷贝 |
| 3 | github.com 时通时断 | 无法截 GitHub 页面 | 用本地 README 渲染截图并注明 |

## 被否掉的建议

| 建议 | 理由 |
|---|---|
| 一次性提交全部文件 | 提交历史不可读 |
| 把 `.git` 手动改写成"漂亮历史" | 伪造协作痕迹，不做 |
| 在 README 写"已被 N 人使用" | 没有真实用户，不能编 |
| 用 GitHub 页面截图占位 | 拿不到就不放，改本地渲染并注明 |
