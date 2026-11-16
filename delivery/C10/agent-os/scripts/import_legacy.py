#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把既有工作日志里的真实经历导入 L2（冷启动用）。

不是编造历史：每条都带 source 字段，指向 D:/ai+x/.workbuddy/memory/ 的原始日志。
导入的 ΔR 是按当时记录的结果事后标注的，标记为 estimated=True。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L2 = ROOT / "memory" / "L2_episodes"
INDEX = L2 / "episodes.json"


def main(src):
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else []
    for e in data:
        delta = round(e["actual"] - e["expected"], 3)
        fname = f"{e['id']}-{e['slug']}.md"
        body = f"""# {e['title']}

- 日期：{e['date']}（导入）
- 来源：`{e['source']}`
- ΔR 说明：{e.get('delta_note', '按当时记录事后标注')}

## S — Situation
{e['situation']}

## T — Task
{e['task']}

## A — Action
{e['action']}

## R — Result
{e['result']}

## ΔR — 预期 vs 实际（事后标注）
- R̂：{e['expected']}
- R：{e['actual']}
- ΔR：**{delta:+.3f}**

## 教训
{e['lesson']}
"""
        (L2 / fname).write_text(body, encoding="utf-8")
        index.append({"id": e["id"], "date": e["date"], "title": e["title"],
                      "expected": e["expected"], "actual": e["actual"], "delta": delta,
                      "tags": e.get("tags", []), "skills": e.get("skills", []),
                      "file": fname, "imported": True, "source": e["source"]})
        print(f"导入 {fname} ΔR={delta:+.3f}")
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
