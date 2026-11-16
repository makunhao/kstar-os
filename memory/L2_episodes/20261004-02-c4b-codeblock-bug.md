# C4B：代码块多行被渲染成一行

- 日期：2026-10-04（导入）
- 来源：`.workbuddy/memory/2026-10-04.md`
- ΔR 说明：按当时记录事后标注

## S — Situation
给公众号 HTML 转换器做合规自检，输出看起来结构正常，<pre>/<code> 已被剥离。

## T — Task
让转换后的 HTML 在公众号编辑器里保留代码块换行。

## A — Action
定位 starter 用 p.string = code_text 且未设 white-space；改为逐行转义 + 显式 <br> + NavigableString 拼接。

## R — Result
代码块换行恢复。同一轮合规自检还在第一次运行时抓出 6 个我自己的问题：<strong> 残留、thead/tbody 不在允许列表、tr/ul/ol 无样式、7 个空 <p>。

## ΔR — 预期 vs 实际（事后标注）
- R̂：0.85
- R：0.55
- ΔR：**-0.300**

## 教训
渲染类 bug 只能靠真实输出发现；「代码看起来对」不等于「渲染出来对」。自检器要在第一次运行时就能报红。
