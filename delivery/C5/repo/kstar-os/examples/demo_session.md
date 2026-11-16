# KSTAR OS 演示：一次完整循环

> 以下命令在 kstar-os 仓库根目录执行，输出为真实终端记录。

```text
$ python3 scripts/kstar.py status
KSTAR OS 状态
  工作目录 : /tmp/demo_repo
  L1 原始  : 1 个日期文件
  L2 经验  : 5 条
  L3 技能  : 6 个（content-outline, dashboard-build, github-repo-analysis, repo-release, submission-audit, weekly-aar）
  L4 工具  : config/tools.md
  L5 界面  : CLI + export-html
  技能调用 : 2 次
  运行日志 : 6 条
  平均|ΔR| : 0.39


$ python3 scripts/kstar.py recall 渲染 bug
[recall] 「渲染 bug」命中 3 份，前 3：
     4  memory/L2_episodes/20261004-02-c4b-codeblock-bug.md  20261004-02-c4b-codeblock-bug
     4  memory/L2_episodes/20261004-03-c4c-eigen-bug.md  20261004-03-c4c-eigen-bug
     2  memory/L2_episodes/20261004-05-c4a-real-bugs.md  20261004-05-c4a-real-bugs

$ python3 scripts/kstar.py plan 给交付包写一篇 C7 文章 --expect 0.7
# KSTAR 计划 · 给交付包写一篇 C7 文章

## K — 检索到的知识
- 相关 Skill：submission-audit, content-outline, weekly-aar, dashboard-build
- 相关经验：（无）

## S — 情境
（待补：约束、资源、当前状态）

## T — 任务
给交付包写一篇 C7 文章

## Â — 行动计划
1. （步骤 1）
2. （步骤 2）
3. （步骤 3）

## R̂ — 预期结果（0–1，必须写，做完才能算 ΔR）
0.7


$ python3 scripts/kstar.py capture 演示：把 C6A 的排序 bug 写进文章开头 --tag demo
[L1] 已写入 memory/L1_raw/2026-11-16.md

$ python3 scripts/kstar.py episode --title 演示：一次可校准的执行 --situation 需要在 1 小时内完成一篇文章骨架 --task 产出六段结构 + 10 个标题 --action 先跑 content-outline，再人工筛标题 --result 骨架 25 分钟完成，标题 10 个里选了 2 个 --lesson 先定读者再写标题，顺序反了会返工 --expected 0.8 --actual 0.7 --tags demo --skills content-outline
[L2] 20261116135918-演示-一次可校准的执行.md  ΔR=-0.100

$ python3 scripts/kstar.py reflect --since 2026-11-16
# KSTAR 周复盘（2026-11-16 → 2026-11-16）

- 经验条数：1
- 平均 ΔR：-0.100（|ΔR| 均值 0.100）
- 调用技能：content-outline×1

## 偏差最大的三条

- **演示：一次可校准的执行**（2026-11-16）ΔR=-0.100

## 下一步
- 把 |ΔR| 最大的经验对应技能改一版；
- 下周只保留真正被调用的技能。


$ python3 scripts/kstar.py export-html --out /tmp/demo_dashboard.html
[export] /tmp/demo_dashboard.html

```
