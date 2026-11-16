---
name: dashboard-build
description: 把「学生×挑战」提交数据 JSON 变成单文件、可筛选、可离线打开的仪表盘。触发词：仪表盘 / dashboard / 提交总览 / 完成率。
version: 0.2
status: active
created: 2026-11-16
---

# dashboard-build

## What
读一个 records JSON，生成自包含 HTML：总览卡片、热力图、按学生展开的明细、筛选与搜索。

## When to Use
- 需要向别人展示「谁交了什么、缺什么」。
- 数据会更新，但不想维护前端工程。
- 交付物要求「打开就能看」，而不是「装环境才能跑」。

## Input
records 数组，字段：student / challenge / submitted_at / status / completeness / files[] / missing[] / score / notes。

## Steps
1. 先把原始数据转成 records JSON（转换脚本留在数据目录，别手改 JSON）。
2. `python3 build_dashboard.py data.json --out dashboard.html --title "..."`
3. 打开 HTML 检查：热力图单元格数 = 学生数 × 挑战数；随机点 3 个学生核对明细。
4. 数据更新后重跑脚本，不编辑 HTML。

## Tools
Python 3 标准库；模板内嵌 CSS/JS，无 CDN 依赖。

## Output
单个 `.html` 文件 + 屏幕一行统计。

## 使用记录
见 `usage.json`。
