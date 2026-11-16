#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KSTAR OS — 一个零依赖的 Markdown 驱动个人 Agent 系统。

五层架构对应关系：
  Layer 1 Memory      -> memory/L1_raw, memory/L2_episodes, memory/L3_skills, config/identity.md
  Layer 2 Skill       -> memory/L3_skills/<skill>/SKILL.md
  Layer 3 Agent Loop  -> 本脚本的 plan / episode / reflect 三个命令
  Layer 4 Tool        -> config/tools.md + subprocess 可调用的本地脚本
  Layer 5 Interface   -> CLI（本脚本）+ export-html 生成的静态面板

设计原则：
  1. 纯标准库，任何机器上 `python3 kstar.py status` 就能跑；
  2. 所有数据都是人类可读的 Markdown / JSON，不锁定任何应用；
  3. 每次调用都写 logs/agent_runs.jsonl，可审计。
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / "memory"
L1 = MEM / "L1_raw"
L2 = MEM / "L2_episodes"
L3 = MEM / "L3_skills"
LOGS = ROOT / "logs"
RUNS = LOGS / "agent_runs.jsonl"
EP_INDEX = L2 / "episodes.json"
CONFIG = ROOT / "config"


def now():
    return dt.datetime.now().astimezone()


def ts():
    return now().strftime("%Y-%m-%d %H:%M:%S%z")


def ensure_dirs():
    for p in (L1, L2, L3, LOGS, CONFIG, ROOT / "inbox"):
        p.mkdir(parents=True, exist_ok=True)


def log_run(cmd, payload):
    ensure_dirs()
    rec = {"ts": ts(), "cmd": cmd, **payload}
    with RUNS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default
    return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- Layer 1
def cmd_capture(args):
    """把一条原始输入写进 L1。"""
    ensure_dirs()
    day = now().strftime("%Y-%m-%d")
    path = L1 / f"{day}.md"
    tag = f" [{args.tag}]" if args.tag else ""
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n- {now().strftime('%H:%M')}{tag} {args.text}\n")
    log_run("capture", {"file": str(path.relative_to(ROOT)), "chars": len(args.text)})
    print(f"[L1] 已写入 {path.relative_to(ROOT)}")


def cmd_inbox(args):
    """把待处理输入放进 inbox，稍后结构化。"""
    ensure_dirs()
    name = args.name or now().strftime("inbox-%Y%m%d-%H%M%S") + ".md"
    path = ROOT / "inbox" / name
    path.write_text(args.text or sys.stdin.read(), encoding="utf-8")
    log_run("inbox", {"file": str(path.relative_to(ROOT))})
    print(f"[inbox] {path.relative_to(ROOT)}")


# ---------------------------------------------------------------- Layer 2
def slugify(text):
    keep = re.sub(r"[^\w一-鿿-]+", "-", text.strip())
    return keep.strip("-")[:60] or "episode"


def cmd_episode(args):
    """写一条 KSTAR 经验（L2），并计算 ΔR。"""
    ensure_dirs()
    expected = args.expected
    actual = args.actual
    delta = round(actual - expected, 3)
    ep = {
        "id": now().strftime("%Y%m%d%H%M%S"),
        "date": now().strftime("%Y-%m-%d"),
        "title": args.title,
        "situation": args.situation,
        "task": args.task,
        "action": args.action,
        "result": args.result,
        "expected": expected,
        "actual": actual,
        "delta": delta,
        "lesson": args.lesson,
        "tags": [t for t in (args.tags or "").split(",") if t],
        "skills": [s for s in (args.skills or "").split(",") if s],
    }
    fname = f"{ep['id']}-{slugify(args.title)}.md"
    body = f"""# {args.title}

- 日期：{ep['date']}
- 标签：{', '.join(ep['tags']) or '—'}
- 调用的 Skill：{', '.join(ep['skills']) or '—'}

## S — Situation
{args.situation}

## T — Task
{args.task}

## A — Action
{args.action}

## R — Result
{args.result}

## ΔR — 预期 vs 实际
- R̂（预期达成度，0–1）：{expected}
- R（实际达成度，0–1）：{actual}
- ΔR = R − R̂：**{delta:+.3f}**

## 教训（写进 L2 的唯一目的）
{args.lesson}
"""
    (L2 / fname).write_text(body, encoding="utf-8")
    index = load_json(EP_INDEX, [])
    index.append({k: ep[k] for k in ("id", "date", "title", "expected", "actual", "delta", "tags", "skills")} | {"file": fname})
    save_json(EP_INDEX, index)
    log_run("episode", {"file": fname, "delta": delta, "skills": ep["skills"]})
    print(f"[L2] {fname}  ΔR={delta:+.3f}")


# ---------------------------------------------------------------- Layer 3
SKILL_TEMPLATE = """---
name: {name}
description: {desc}
version: {version}
status: active
created: {date}
---

# {title}

## What（做什么）
{desc}

## When to Use（什么时候用）
{when}

## Input（输入）
{inp}

## Steps（步骤）
1. 读取输入并确认边界（缺信息就先问，不猜）。
2. {step2}
3. 生成输出，并附上可核查的来源或路径。
4. 自检：输出是否满足 {check}。

## Tools（需要什么工具）
{tools}

## Output（输出）
{out}

## 使用记录
见同目录 `usage.json`；迭代记录见 `iterations.md`。
"""


def cmd_skill_new(args):
    ensure_dirs()
    d = L3 / args.name
    d.mkdir(parents=True, exist_ok=True)
    skill_md = d / "SKILL.md"
    if skill_md.exists() and not args.force:
        print(f"[L3] 已存在：{skill_md.relative_to(ROOT)}（--force 覆盖）")
        return
    skill_md.write_text(SKILL_TEMPLATE.format(
        name=args.name, desc=args.desc, version="0.1", date=now().strftime("%Y-%m-%d"),
        title=args.name, when=args.when or "（待补：触发条件）",
        inp=args.input or "（待补：输入）", step2=args.step or "（待补：核心步骤）",
        check=args.check or "输入契约", tools=args.tools or "本地脚本 / LLM",
        out=args.output or "（待补：输出）"), encoding="utf-8")
    usage = d / "usage.json"
    if not usage.exists():
        save_json(usage, {"name": args.name, "uses": [], "iterations": []})
    log_run("skill_new", {"name": args.name})
    print(f"[L3] 新建技能 {args.name}")


def _require_skill(name):
    d = L3 / name
    if not (d / "SKILL.md").exists():
        print(f"[L3] 没有这个技能：{name}（先用 skill-new 创建，避免拼写错误产生幽灵技能）")
        raise SystemExit(2)
    return d


def cmd_skill_use(args):
    d = _require_skill(args.name)
    usage = load_json(d / "usage.json", {"name": args.name, "uses": [], "iterations": []})
    rec = {"ts": ts(), "context": args.context, "outcome": args.outcome,
           "delta": args.delta, "public": args.public or ""}
    usage["uses"].append(rec)
    save_json(d / "usage.json", usage)
    log_run("skill_use", {"name": args.name, "delta": args.delta})
    print(f"[L3] {args.name} 第 {len(usage['uses'])} 次使用已记录（ΔR={args.delta:+.2f}）")


def cmd_skill_iter(args):
    d = _require_skill(args.name)
    usage = load_json(d / "usage.json", {"name": args.name, "uses": [], "iterations": []})
    it = {"ts": ts(), "from": args.frm, "to": args.to, "why": args.why, "effect": args.effect}
    usage["iterations"].append(it)
    save_json(d / "usage.json", usage)
    with (d / "iterations.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {now().strftime('%Y-%m-%d')}  v{args.frm} → v{args.to}\n"
                f"- 改动：{args.to}\n- 原因：{args.why}\n- 效果：{args.effect}\n")
    log_run("skill_iter", {"name": args.name, "from": args.frm, "to": args.to})
    print(f"[L3] {args.name} 迭代记录已写入")


# ---------------------------------------------------------------- Layer 3 loop: recall / plan
def _all_docs():
    docs = []
    for p in list(L1.glob("*.md")) + list(L2.glob("*.md")) + list(L3.glob("*/SKILL.md")):
        docs.append((p, p.read_text(encoding="utf-8", errors="ignore")))
    return docs


def _tokens(q):
    latin = re.findall(r"[A-Za-z0-9_+-]{2,}", q.lower())
    han = re.findall(r"[一-鿿]{2,}", q)
    grams = set(latin)
    for h in han:
        grams.add(h)
        grams.update(h[i:i + 2] for i in range(len(h) - 1))
    return [g for g in grams if g]


def score_doc(text, grams):
    low = text.lower()
    return sum(low.count(g) for g in grams)


def cmd_recall(args):
    grams = _tokens(args.query)
    scored = []
    for p, text in _all_docs():
        s = score_doc(text, grams)
        if s > 0:
            scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    top = scored[:args.top]
    log_run("recall", {"query": args.query, "hits": len(scored)})
    if not top:
        print("[recall] 没有命中。先 capture 一些原始输入，或换个说法。")
        return
    print(f"[recall] 「{args.query}」命中 {len(scored)} 份，前 {len(top)}：")
    for s, p in top:
        title = p.stem
        print(f"  {s:4d}  {p.relative_to(ROOT)}  {title}")


def cmd_plan(args):
    grams = _tokens(args.task)
    hits = []
    for p, text in _all_docs():
        s = score_doc(text, grams)
        if s > 0:
            hits.append((s, p))
    hits.sort(key=lambda x: -x[0])
    skills = [p.parent.name for s, p in hits if p.parent.parent == L3][:5]
    episodes = [p.stem for s, p in hits if p.parent == L2][:3]
    print(f"""# KSTAR 计划 · {args.task}

## K — 检索到的知识
- 相关 Skill：{', '.join(skills) or '（无，建议先看 L1 原始笔记）'}
- 相关经验：{', '.join(episodes) or '（无）'}

## S — 情境
{args.situation or '（待补：约束、资源、当前状态）'}

## T — 任务
{args.task}

## Â — 行动计划
1. （步骤 1）
2. （步骤 2）
3. （步骤 3）

## R̂ — 预期结果（0–1，必须写，做完才能算 ΔR）
{args.expect or '（待补：预期达成度 + 可验证的成功标准）'}
""")
    log_run("plan", {"task": args.task, "skills": skills})


# ---------------------------------------------------------------- reflect
def cmd_status(args):
    eps = load_json(EP_INDEX, [])
    skills = sorted([p.name for p in L3.iterdir() if (p / "SKILL.md").exists()]) if L3.exists() else []
    uses = 0
    for s in skills:
        u = load_json(L3 / s / "usage.json", {"uses": []})
        uses += len(u.get("uses", []))
    l1_files = len(list(L1.glob("*.md")))
    runs = 0
    if RUNS.exists():
        runs = sum(1 for _ in RUNS.open(encoding="utf-8"))
    print(f"""KSTAR OS 状态
  工作目录 : {ROOT}
  L1 原始  : {l1_files} 个日期文件
  L2 经验  : {len(eps)} 条
  L3 技能  : {len(skills)} 个（{', '.join(skills) or '空'}）
  L4 工具  : config/tools.md
  L5 界面  : CLI + export-html
  技能调用 : {uses} 次
  运行日志 : {runs} 条
  平均|ΔR| : {round(sum(abs(e['delta']) for e in eps)/len(eps), 3) if eps else 'n/a'}
""")


def cmd_reflect(args):
    eps = load_json(EP_INDEX, [])
    if args.since:
        eps = [e for e in eps if e["date"] >= args.since]
    if not eps:
        print("[reflect] 没有可复盘的 episode。")
        return
    n = len(eps)
    mean_delta = sum(e["delta"] for e in eps) / n
    abs_delta = sum(abs(e["delta"]) for e in eps) / n
    skills = {}
    for e in eps:
        for s in e.get("skills", []):
            skills[s] = skills.get(s, 0) + 1
    out = [f"# KSTAR 周复盘（{eps[0]['date']} → {eps[-1]['date']}）\n",
           f"- 经验条数：{n}",
           f"- 平均 ΔR：{mean_delta:+.3f}（|ΔR| 均值 {abs_delta:.3f}）",
           f"- 调用技能：{', '.join(f'{k}×{v}' for k, v in sorted(skills.items(), key=lambda x: -x[1])) or '—'}",
           "\n## 偏差最大的三条\n"]
    for e in sorted(eps, key=lambda x: -abs(x["delta"]))[:3]:
        out.append(f"- **{e['title']}**（{e['date']}）ΔR={e['delta']:+.3f}")
    out.append("\n## 下一步\n- 把 |ΔR| 最大的经验对应技能改一版；\n- 下周只保留真正被调用的技能。\n")
    text = "\n".join(out)
    if args.write:
        path = LOGS / f"reflect-{now().strftime('%Y%m%d-%H%M%S')}.md"
        path.write_text(text, encoding="utf-8")
        print(f"[reflect] 已写入 {path.relative_to(ROOT)}\n")
    print(text)
    log_run("reflect", {"n": n, "mean_delta": round(mean_delta, 3)})


# ---------------------------------------------------------------- export
def cmd_export(args):
    eps = load_json(EP_INDEX, [])
    skills = sorted([p for p in L3.iterdir() if (p / "SKILL.md").exists()]) if L3.exists() else []
    rows = "".join(
        f"<tr><td>{html.escape(e['date'])}</td><td>{html.escape(e['title'])}</td>"
        f"<td class='num'>{e['delta']:+.3f}</td></tr>" for e in eps)
    srows = ""
    for s in skills:
        u = load_json(s / "usage.json", {"uses": [], "iterations": []})
        srows += (f"<tr><td>{html.escape(s.name)}</td><td class='num'>{len(u.get('uses', []))}</td>"
                  f"<td class='num'>{len(u.get('iterations', []))}</td></tr>")
    doc = f"""<!doctype html><html lang="zh"><meta charset="utf-8">
<title>KSTAR OS</title>
<style>
body{{font-family:-apple-system,"Segoe UI","Noto Sans SC",sans-serif;max-width:900px;margin:40px auto;padding:0 20px;color:#1c1c1e}}
h1{{font-size:28px}} .sub{{color:#666}} table{{width:100%;border-collapse:collapse;margin:16px 0}}
td,th{{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;font-size:14px}}
.num{{font-variant-numeric:tabular-nums;text-align:right}} .pos{{color:#0a7d32}}
</style>
<h1>KSTAR OS</h1><p class="sub">第二大脑 · 生成于 {ts()}</p>
<h2>L2 经验（{len(eps)}）</h2><table><tr><th>日期</th><th>经验</th><th class="num">ΔR</th></tr>{rows}</table>
<h2>L3 技能（{len(skills)}）</h2><table><tr><th>技能</th><th class="num">使用</th><th class="num">迭代</th></tr>{srows}</table>
</body></html>"""
    path = Path(args.out) if args.out else ROOT / "logs" / "kstar-dashboard.html"
    path.write_text(doc, encoding="utf-8")
    log_run("export", {"out": str(path)})
    print(f"[export] {path}")


def build_parser():
    p = argparse.ArgumentParser(prog="kstar", description="KSTAR OS — 第二大脑 Agent 系统")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", help="写一条 L1 原始笔记")
    c.add_argument("text")
    c.add_argument("--tag")
    c.set_defaults(func=cmd_capture)

    c = sub.add_parser("inbox", help="把待处理文本放进 inbox")
    c.add_argument("--name")
    c.add_argument("--text")
    c.set_defaults(func=cmd_inbox)

    c = sub.add_parser("episode", help="写一条 L2 KSTAR 经验")
    for a in ("--title", "--situation", "--task", "--action", "--result", "--lesson"):
        c.add_argument(a, required=True)
    c.add_argument("--expected", type=float, required=True)
    c.add_argument("--actual", type=float, required=True)
    c.add_argument("--tags")
    c.add_argument("--skills")
    c.set_defaults(func=cmd_episode)

    c = sub.add_parser("skill-new", help="新建 L3 技能")
    c.add_argument("name")
    c.add_argument("--desc", required=True)
    c.add_argument("--when")
    c.add_argument("--input")
    c.add_argument("--step")
    c.add_argument("--check")
    c.add_argument("--tools")
    c.add_argument("--output")
    c.add_argument("--force", action="store_true")
    c.set_defaults(func=cmd_skill_new)

    c = sub.add_parser("skill-use", help="记录技能使用")
    c.add_argument("name")
    c.add_argument("--context", required=True)
    c.add_argument("--outcome", required=True)
    c.add_argument("--delta", type=float, default=0.0)
    c.add_argument("--public")
    c.set_defaults(func=cmd_skill_use)

    c = sub.add_parser("skill-iter", help="记录技能迭代")
    c.add_argument("name")
    c.add_argument("--frm", default="0.1")
    c.add_argument("--to", default="0.2")
    c.add_argument("--why", required=True)
    c.add_argument("--effect", required=True)
    c.set_defaults(func=cmd_skill_iter)

    c = sub.add_parser("recall", help="跨四层检索")
    c.add_argument("query")
    c.add_argument("--top", type=int, default=8)
    c.set_defaults(func=cmd_recall)

    c = sub.add_parser("plan", help="生成 KSTAR 计划")
    c.add_argument("task")
    c.add_argument("--situation")
    c.add_argument("--expect")
    c.set_defaults(func=cmd_plan)

    c = sub.add_parser("reflect", help="生成周复盘")
    c.add_argument("--since")
    c.add_argument("--write", action="store_true")
    c.set_defaults(func=cmd_reflect)

    c = sub.add_parser("export-html", help="导出静态面板")
    c.add_argument("--out")
    c.set_defaults(func=cmd_export)

    c = sub.add_parser("status", help="查看系统状态")
    c.set_defaults(func=cmd_status)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    ensure_dirs()
    args.func(args)


if __name__ == "__main__":
    main()
