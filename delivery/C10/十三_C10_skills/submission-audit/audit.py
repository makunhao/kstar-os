#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付包体检器：检查一个交付目录是否具备可评审的最低条件。

用法：
    python3 audit.py <交付包目录> [--json report.json]

它不是评分器，只回答四个问题：
    1. 关键文件在不在？  2. 文件是不是空的？
    3. 命名是否可归属？  4. AI 日志是否像"日志"而不是"总结"？
"""
import argparse
import json
import re
import sys
from pathlib import Path

CORE = {
    "README": ["README.md", "readme.md"],
    "AI日志": ["AI日志", "AI_LOG", "ailog"],
    "AAR/复盘": ["AAR", "复盘"],
    "拿来说明": ["拿来说明", "ATTRIBUTION"],
}
NICE = {
    "方案/架构": ["方案设计", "architecture", "方案"],
    "验证报告": ["验证报告", "验证"],
    "教学说明": ["教学说明", "教学"],
}


def pick(files, keys):
    return [f for f in files if any(k.lower() in f.name.lower() for k in keys)]


def is_empty(p):
    try:
        return p.stat().st_size < 80
    except OSError:
        return True


def ai_log_quality(p):
    if not p:
        return "missing", 0
    text = p.read_text(encoding="utf-8", errors="ignore")
    dates = len(re.findall(r"20\d{2}-\d{2}-\d{2}", text))
    prompts = len(re.findall(r"(prompt|提示词|指令原文)", text, re.I))
    rounds = len(re.findall(r"(第\s*\d+\s*轮|迭代|Round)", text, re.I))
    score = min(100, dates * 8 + prompts * 10 + rounds * 8)
    level = "good" if score >= 60 else ("weak" if score >= 30 else "poor")
    return level, score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--json")
    a = ap.parse_args()
    root = Path(a.pack)
    if not root.is_dir():
        print(f"不是目录：{root}")
        return 2
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    top = [p for p in files if p.parent == root]
    result = {"pack": root.name, "files": len(files), "bytes": sum(p.stat().st_size for p in files),
              "checks": {}, "missing": [], "empty": [], "warnings": []}

    for label, keys in CORE.items():
        hit = pick(files, keys)
        result["checks"][label] = [str(x.relative_to(root)) for x in hit]
        if not hit:
            result["missing"].append(label)
    for label, keys in NICE.items():
        hit = pick(files, keys)
        result["checks"].setdefault(label, [str(x.relative_to(root)) for x in hit])
        if not hit:
            result["warnings"].append(f"可选：{label} 未找到")

    for p in files:
        if is_empty(p) and p.suffix.lower() in {".md", ".py", ".json", ".html", ".txt", ".tex"}:
            result["empty"].append(str(p.relative_to(root)))

    unnamed = [p.name for p in top if p.suffix == ".md" and not re.match(r"^(十三|[A-Za-z0-9_-]+)_C\d", p.name)]
    if unnamed:
        result["warnings"].append(f"顶层 md 命名不含 姓名_C编号：{', '.join(unnamed[:5])}")

    log_hit = pick(files, ["AI日志", "AI_LOG"])
    level, score = ai_log_quality(log_hit[0] if log_hit else None)
    result["ai_log"] = {"level": level, "score": score}

    print(f"\n# 交付体检 · {root.name}\n")
    print(f"- 文件 {result['files']} 个 / {result['bytes']/1024:.1f} KB")
    print(f"- AI 日志：{level}（结构化分 {score}/100）")
    for label, paths in result["checks"].items():
        mark = "OK" if paths else "MISSING"
        print(f"- {label}: {mark}" + (f" · {len(paths)} 个" if paths else ""))
    if result["empty"]:
        print(f"- 空文件：{len(result['empty'])} 个（{', '.join(result['empty'][:5])}）")
    if result["warnings"]:
        for w in result["warnings"]:
            print(f"- 提示：{w}")

    if a.json:
        Path(a.json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON → {a.json}")

    return 1 if result["missing"] or result["empty"] else 0


if __name__ == "__main__":
    sys.exit(main())
