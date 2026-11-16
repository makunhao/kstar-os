#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 L2 经验与 L3 使用记录生成 AAR 草稿（八维）。

用法：
    python3 aar.py [--since 2026-11-01] [--out aar.md]
"""
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
L2 = ROOT / "memory" / "L2_episodes" / "episodes.json"
L3 = ROOT / "memory" / "L3_skills"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="1970-01-01")
    ap.add_argument("--out")
    a = ap.parse_args()

    eps = [e for e in json.loads(L2.read_text(encoding="utf-8")) if e["date"] >= a.since] if L2.exists() else []
    skills = []
    if L3.exists():
        for d in sorted(L3.iterdir()):
            u = d / "usage.json"
            if u.exists():
                data = json.loads(u.read_text(encoding="utf-8"))
                skills.append((d.name, len(data.get("uses", [])), len(data.get("iterations", []))))

    n = len(eps)
    mean = sum(e["delta"] for e in eps) / n if n else 0
    worst = sorted(eps, key=lambda e: -abs(e["delta"]))[:3]
    text = f"""# AAR（{a.since} 起）— 自动草稿

> 这是脚本根据 L2/L3 记录生成的骨架。**判断必须人来写**，尤其第 5、6 维。

## 1. 目标（计划做什么）
（引用本周 plan 的 T 与 R̂）

## 2. 过程（实际做了什么）
- L2 经验 {n} 条，平均 ΔR {mean:+.3f}
- 技能使用：{', '.join(f'{s}×{u}' for s, u, _ in skills) or '—'}

## 3. 结果（可验证产出）
（列出文件路径 / 链接 / 截图，不写「基本完成」）

## 4. 证据
（每条结果对应的路径）

## 5. 失败与偏差
{chr(10).join(f'- {e["title"]}：ΔR {e["delta"]:+.3f}' for e in worst) or '- （本周无记录，需补）'}

## 6. 根因（不是「时间不够」）
（至少区分：前提错了 / 度量错了 / 执行错了）

## 7. 改进（下次怎么做，可执行）
（一条即可，但要能被下周的 AAR 检验）

## 8. 可迁移经验
（能写进 L3 技能的那一句）

---
生成时间：{date.today().isoformat()}
"""
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"AAR → {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
