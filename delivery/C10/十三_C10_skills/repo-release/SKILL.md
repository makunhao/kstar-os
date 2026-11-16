---
name: repo-release
description: 把本地项目整理成别人 clone 后 5 分钟能跑起来的开源仓库——查文件、查 README 章节、查 git 历史。触发词：GitHub / 仓库 / 开源 / 发布。
version: 0.2
status: active
created: 2026-11-16
---

# repo-release

## What
发布前机械检查：必需文件、README 五个章节、依赖声明、测试、提交历史。

## When to Use
- C5 提交前。
- 把任何内部工具开源之前。

## Input
一个本地仓库目录。

## Steps
1. `python3 release_check.py <repo>`，先消掉所有「硬性缺件」。
2. README 必须能让陌生人跑通：安装 → 一条命令 → 示例输入输出。
3. `git log --oneline` 至少 5 条有意义的提交，不用 "update" 作提交信息。
4. 推送到 GitHub 后，用无痕窗口打开 README，按文档从头走一遍。
5. 记录实际耗时；超过 5 分钟就改文档，不是改预期。

## Tools
Python 3、git、GitHub token（推送时）。

## Output
检查表 + 退出码（1 = 不可发布）。

## 使用记录
见 `usage.json`。
