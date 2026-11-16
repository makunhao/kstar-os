#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仓库理解报告生成器：给一个本地 clone，输出结构/技能/git 三类客观事实。

用法：
    python3 repo_report.py <repo目录> [--out report.md]
"""
import argparse
import re
import subprocess
from collections import Counter
from pathlib import Path


def sh(root, *args):
    try:
        return subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        return ""


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def tree(root, max_depth=2):
    lines = []
    base = len(root.parts)

    def walk(d, depth):
        if depth > max_depth:
            return
        entries = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for e in entries:
            if e.name in {".git", "node_modules", "__pycache__"}:
                continue
            rel = e.relative_to(root)
            indent = "  " * (len(rel.parts) - 1)
            lines.append(f"{indent}{e.name}{'/' if e.is_dir() else ''}")
            if e.is_dir() and depth < max_depth:
                walk(e, depth + 1)

    walk(root, 1)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = Path(a.repo).resolve()
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    ext = Counter(p.suffix.lower() for p in files)

    readme = next((p for p in [root / "README.md", root / "readme.md"] if p.exists()), None)
    readme_text = readme.read_text(encoding="utf-8", errors="ignore") if readme else ""
    headings = re.findall(r"^#{1,3} (.+)$", readme_text, re.M)[:15]

    skills = []
    for p in files:
        if p.name.lower() == "skill.md":
            fm = frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
            skills.append({"path": str(p.relative_to(root)),
                           "name": fm.get("name", p.parent.name),
                           "desc": fm.get("description", "")})

    out = [f"# 仓库客观事实 · {root.name}\n",
           f"- 文件数：{len(files)}",
           f"- README：{'有' if readme else '无'}（{len(readme_text)} 字符）",
           f"- git 提交：{sh(root, 'rev-list', '--count', 'HEAD') or '非 git 仓库'}",
           f"- 最近提交：{sh(root, 'log', '-1', '--pretty=%h %ad %s', '--date=short') or '—'}",
           "\n## 文件类型 Top 10\n"]
    for e, n in ext.most_common(10):
        out.append(f"- `{e or '(无扩展名)'}`：{n}")
    out.append("\n## 目录结构（两层层级）\n```")
    out.extend(tree(root))
    out.append("```\n## README 章节\n")
    out.extend([f"- {h}" for h in headings] or ["（未提取到标题）"])
    out.append(f"\n## Skill 清单（{len(skills)}）\n")
    for s in skills:
        out.append(f"- **{s['name']}** — {s['desc'][:120] or '（无描述）'}  \n  `{s['path']}`")
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"report → {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
