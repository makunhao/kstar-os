---
name: weekly-aar
description: 从 L2 经验与技能使用记录生成八维 AAR 草稿，逼出 ΔR、根因与可检验的改进。触发词：AAR / 复盘 / 周报。
version: 0.2
status: active
created: 2026-11-16
---

# weekly-aar

## What
把一周的 KSTAR 记录汇总成八维 AAR：目标 / 过程 / 结果 / 证据 / 失败 / 根因 / 改进 / 可迁移经验。

## When to Use
- 每周结束。
- 一个交付包收尾（项目级 AAR）。
- ΔR 连续为负，需要停下来找根因。

## Input
`memory/L2_episodes/episodes.json` + 各技能 `usage.json`。

## Steps
1. `python3 aar.py --since <周一> --out aar.md`
2. 人工补第 3、4 维：只写路径与链接，不写形容词。
3. 第 6 维必须区分「前提错 / 度量错 / 执行错」，三者改法不同。
4. 第 7 维写成下周可检验的一句话，不写「加强沟通」。
5. 把第 8 维写回 L3 技能（`skill-iter`）。

## Tools
Python 3。

## Output
`aar.md`。

## 使用记录
见 `usage.json`。
