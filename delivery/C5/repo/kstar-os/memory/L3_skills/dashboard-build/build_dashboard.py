#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把提交数据 JSON 变成单文件交互式仪表盘（零依赖、离线可用）。

用法：
    python3 build_dashboard.py data.json --out dashboard.html --title "Elite 20 提交仪表盘"

数据格式（最小）：
[
  {"student":"张三","challenge":"C4C","submitted_at":"2026-10-05",
   "status":"complete|partial|missing","completeness":0.86,
   "files":[{"filename":"...","required":true,"present":true}],
   "missing":["验证报告"],"score":88,"notes":"..."}
]
"""
import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path

STATUS = {"complete": ("完整", "#0a7d32", "#e7f6ec"),
          "partial": ("部分", "#b26a00", "#fff4e0"),
          "missing": ("缺失", "#b3261e", "#fdecea")}


def esc(x):
    return html.escape(str(x))


def ch_key(c):
    import re
    m = re.match(r"C(\d+)([A-Z]?)", c)
    return (int(m.group(1)), m.group(2)) if m else (999, c)


def build(records, title):
    students = sorted({r["student"] for r in records})
    challenges = sorted({r["challenge"] for r in records}, key=ch_key)
    idx = {(r["student"], r["challenge"]): r for r in records}
    total_cells = len(students) * len(challenges)
    done = sum(1 for r in records if r.get("status") == "complete")
    partial = sum(1 for r in records if r.get("status") == "partial")

    # 热力图
    head = "".join(f"<th>{esc(c)}</th>" for c in challenges)
    rows = []
    for s in students:
        cells = []
        for c in challenges:
            r = idx.get((s, c))
            if not r:
                cells.append("<td class='cell none' data-s='%s' data-c='%s'>·</td>" % (esc(s), esc(c)))
            else:
                label, color, bg = STATUS.get(r.get("status", "partial"), STATUS["partial"])
                pct = int(round((r.get("completeness") or 0) * 100))
                cells.append(
                    f"<td class='cell' data-s='{esc(s)}' data-c='{esc(c)}' style='color:{color};background:{bg}'>"
                    f"{label}<span class='pct'>{pct}%</span></td>")
        rows.append(f"<tr><th class='rowh'>{esc(s)}</th>{''.join(cells)}</tr>")

    # 详情
    details = []
    for s in students:
        rs = [r for r in records if r["student"] == s]
        items = []
        for r in sorted(rs, key=lambda x: x["challenge"]):
            label, color, bg = STATUS.get(r.get("status", "partial"), STATUS["partial"])
            files = "".join(
                f"<li class='{'ok' if f.get('present') else 'no'}'>{esc(f.get('filename'))}"
                f"{' · 必填' if f.get('required') else ''}</li>" for f in r.get("files", []))
            items.append(f"""<div class='item'>
              <div class='ihead'><b>{esc(r['challenge'])}</b>
                <span class='badge' style='color:{color};background:{bg}'>{label}</span>
                <span class='meta'>{esc(r.get('submitted_at','—'))} · 完整度 {int((r.get('completeness') or 0)*100)}%
                {' · AI 初评 ' + str(r['score']) if r.get('score') else ''}</span></div>
              <ul class='files'>{files or '<li class="meta">无文件记录</li>'}</ul>
              {f"<div class='notes'>缺失：{esc('、'.join(r['missing']))}</div>" if r.get("missing") else ""}
            </div>""")
        details.append(f"<section class='student' id='s-{esc(s)}' data-name='{esc(s)}'>"
                       f"<h3>{esc(s)} <small>{len(rs)} 个挑战</small></h3>{''.join(items)}</section>")

    data_json = json.dumps(records, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html><html lang="zh"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>
:root{{--ink:#1b1b1f;--muted:#6b6b76;--line:#e7e7ec;--bg:#fbfbfd;--accent:#2f5bea}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}}
header{{padding:28px 32px 8px}} h1{{margin:0 0 6px;font-size:26px;letter-spacing:-.02em}}
.sub{{color:var(--muted);font-size:14px}}
.wrap{{padding:0 32px 48px;max-width:1280px;margin:0 auto}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:20px 0 26px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}}
.card .k{{color:var(--muted);font-size:12px;letter-spacing:.04em;text-transform:uppercase}}
.card .v{{font-size:28px;font-weight:650;margin-top:6px;font-variant-numeric:tabular-nums}}
.bar{{height:8px;background:#ececf2;border-radius:6px;overflow:hidden;margin-top:10px}}
.bar>i{{display:block;height:100%;background:linear-gradient(90deg,#2f5bea,#6f8cff)}}
section.panel{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-bottom:22px}}
h2{{font-size:16px;margin:4px 0 14px}} table.heat{{width:100%;border-collapse:collapse;font-size:13px}}
table.heat th{{font-weight:600;color:var(--muted);padding:8px 6px;text-align:center;white-space:nowrap}}
table.heat th.rowh{{text-align:left;color:var(--ink);position:sticky;left:0;background:#fff}}
.cell{{text-align:center;padding:9px 6px;border:1px solid #fff;border-radius:8px;cursor:default}}
.cell.none{{color:#c9c9d2}} .pct{{display:block;font-size:11px;opacity:.7}}
.controls{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}}
select,input{{padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;font-size:14px}}
.item{{border-top:1px solid var(--line);padding:12px 0}} .item:first-of-type{{border-top:0}}
.ihead{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
.badge{{font-size:12px;padding:2px 8px;border-radius:999px}}
.meta{{color:var(--muted);font-size:12px}}
ul.files{{margin:8px 0 0;padding-left:18px;font-size:13px;color:#333}}
ul.files li.ok::marker{{color:#0a7d32}} ul.files li.no{{color:#b3261e}}
.notes{{margin-top:6px;font-size:12px;color:#b3261e}}
.student{{display:none}} .student.show{{display:block}}
h3 small{{color:var(--muted);font-weight:400;font-size:12px;margin-left:6px}}
footer{{color:var(--muted);font-size:12px;padding:0 32px 40px}}
</style>
<header><h1>{esc(title)}</h1><div class="sub">数据源：records JSON · 状态与完整度为启发式标注（判定规则见随附 Excel「字段说明」） · 文件内自包含，可离线打开</div></header>
<div class="wrap">
<div class="cards">
  <div class="card"><div class="k">学生</div><div class="v">{len(students)}</div></div>
  <div class="card"><div class="k">挑战</div><div class="v">{len(challenges)}</div></div>
  <div class="card"><div class="k">有记录</div><div class="v">{len(records)}<span style="font-size:14px;color:#6b6b76"> / {total_cells}</span></div>
    <div class="bar"><i style="width:{len(records)/max(total_cells,1)*100:.0f}%"></i></div></div>
  <div class="card"><div class="k">完整提交</div><div class="v">{done}</div>
    <div class="bar"><i style="width:{done/max(len(records),1)*100:.0f}%"></i></div></div>
  <div class="card"><div class="k">部分提交</div><div class="v">{partial}</div></div>
</div>
<section class="panel"><h2>学生 × 挑战 热力图</h2><div style="overflow:auto"><table class="heat">
<tr><th class="rowh">学生</th>{head}</tr>{''.join(rows)}</table></div></section>
<section class="panel"><h2>提交明细</h2>
<div class="controls">
  <select id="fStudent"><option value="">全部学生</option>{''.join(f'<option>{esc(s)}</option>' for s in students)}</select>
  <select id="fStatus"><option value="">全部状态</option><option value="complete">完整</option><option value="partial">部分</option><option value="missing">缺失</option></select>
  <input id="q" placeholder="搜索挑战 / 文件名 / 备注">
</div>
<div id="list">{''.join(details)}</div></section>
</div>
<footer>KSTAR OS · dashboard-build v0.1 · 数据与模板分离，替换 JSON 即可复用</footer>
<script>
const DATA = {data_json};
const list = document.getElementById('list');
const fS = document.getElementById('fStudent'), fT = document.getElementById('fStatus'), q = document.getElementById('q');
function apply(){{
  const s = fS.value, st = fT.value, kw = q.value.trim().toLowerCase();
  document.querySelectorAll('.student').forEach(sec=>{{
    let any=false;
    sec.querySelectorAll('.item').forEach(it=>{{
      const txt = it.textContent.toLowerCase();
      let ok = (!kw || txt.includes(kw));
      if (st) ok = ok && it.querySelector('.badge') && it.querySelector('.badge').textContent.includes(
        st==='complete'?'完整':st==='partial'?'部分':'缺失');
      it.style.display = ok ? '' : 'none'; if(ok) any=true;
    }});
    sec.classList.toggle('show', (!s || sec.dataset.name===s) && any);
  }});
}}
[fS,fT,q].forEach(el=>el.addEventListener('input',apply));
document.querySelectorAll('.cell[data-s]').forEach(td=>td.addEventListener('click',()=>{{
  fS.value = td.dataset.s; apply();
  document.getElementById('s-'+td.dataset.s)?.scrollIntoView({{behavior:'smooth',block:'start'}});
}}));
apply();
</script></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--out", default="dashboard.html")
    ap.add_argument("--title", default="提交数据仪表盘")
    a = ap.parse_args()
    records = json.loads(Path(a.data).read_text(encoding="utf-8"))
    Path(a.out).write_text(build(records, a.title), encoding="utf-8")
    print(f"dashboard → {a.out}  ({len(records)} 条记录)")


if __name__ == "__main__":
    main()
