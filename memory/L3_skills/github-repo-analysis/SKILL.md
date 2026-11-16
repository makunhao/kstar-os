---
name: github-repo-analysis
description: 读一个陌生仓库：先出客观事实（结构/技能清单/git 历史），再写判断。触发词：仓库分析 / neoskills / fork / C5A。
version: 0.2
status: active
created: 2026-11-16
---

# github-repo-analysis

## What
把「读仓库」拆成可核查的两段：脚本出事实，人写判断。避免通篇形容词。

## When to Use
- C5A 仓库分析。
- Fork 别人项目前的尽调。

## Input
本地 clone 路径（先 `git clone`）。

## Steps
1. `git clone <url> && cd <repo>`。
2. `python3 repo_report.py . --out facts.md` 生成客观事实。
3. 读 facts.md + README，回答四个问题：做什么 / 结构 / 有哪些技能 / 哪个最有意思。
4. 每个判断后面挂一条事实依据（文件路径、行数、提交数）。
5. 提改进建议时，先确认建议在仓库里确实没有，而不是「没看到」。

## Tools
git、Python 3。

## Output
`facts.md` + 人写的分析文档。

## 使用记录
见 `usage.json`。
