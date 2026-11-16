---
name: submission-audit
description: 交付前体检一个交付包——关键文件是否齐全、有没有空壳、命名能否归属、AI 日志是否像日志。触发词：提交前 / 自查 / 体检 / 交付包。
version: 0.3
status: active
created: 2026-11-16
---

# submission-audit

## What
对一个交付目录做机械体检，输出缺件、空壳、命名与 AI 日志质量四个维度的结果。

## When to Use
- 任何交付包「写完但还没交」的时候。
- 重建旧交付物后，确认没有漏文件。
- 评审别人的包之前，先跑一遍，免得把「缺件」误判成「内容差」。

## Input
交付包目录路径。目录里应有 README、AI 日志、AAR、产物。

## Steps
1. 运行 `python3 audit.py <目录> --json report.json`。
2. 缺 CORE 任一项 → 先补文件，不要改文案。
3. 有空文件 → 打开看是「真没内容」还是「生成失败」，分别处理。
4. AI 日志 structured score < 30 → 补日期、prompt 原文、迭代轮次。
5. 体检通过后，再人工看一遍「数字是否有唯一出处」。

## Tools
Python 3 标准库。

## Output
屏幕表格 + 可选 JSON；退出码 1 表示存在缺件或空文件。

## 使用记录
见 `usage.json`。
