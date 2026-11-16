#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""开源仓库发布前检查：C5 的「5 分钟能跑起来」硬指标。

用法：
    python3 release_check.py <repo目录>
退出码 1 = 有硬性缺件。
"""
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = ["README.md", "LICENSE", ".gitignore", "AI_LOG.md", "ATTRIBUTION.md"]
README_SECTIONS = ["解决什么问题", "快速开始", "项目结构", "License"]


def git(root, *args):
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        return ""


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems, notes = [], []

    for f in REQUIRED:
        p = root / f
        if not p.exists():
            problems.append(f"缺 {f}")
        elif p.stat().st_size < 30:
            problems.append(f"{f} 内容过少（{p.stat().st_size} B）")

    readme = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").exists() else ""
    for s in README_SECTIONS:
        if s not in readme:
            problems.append(f"README 缺「{s}」章节")
    if len(readme) < 1500:
        notes.append(f"README 只有 {len(readme)} 字符，可能不足以让别人复现")

    tests = list(root.rglob("test*.py")) + list(root.rglob("*_test.py"))
    if not tests:
        notes.append("没有测试文件（非硬性，但会拉低技术质量）")

    has_req = any((root / f).exists() for f in ("requirements.txt", "pyproject.toml", "package.json"))
    if not has_req:
        notes.append("没有依赖声明文件（零依赖项目可在 README 注明）")

    commits = git(root, "rev-list", "--count", "HEAD")
    branch = git(root, "branch", "--show-current")
    dirty = git(root, "status", "--porcelain")

    print(f"\n# 发布检查 · {root.name}\n")
    print(f"- git 提交：{commits or '（不是 git 仓库）'}  当前分支：{branch or '—'}")
    if dirty:
        print(f"- 未提交改动：{len(dirty.splitlines())} 个文件")
    print(f"- 文件总数：{len([p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts])}")
    if problems:
        print("\n## 硬性缺件")
        for p in problems:
            print(f"- {p}")
    if notes:
        print("\n## 提示")
        for n in notes:
            print(f"- {n}")
    if not problems:
        print("\n✅ 硬性检查通过")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
