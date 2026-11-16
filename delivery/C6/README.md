# C6 交付包 · KSTAR 助手（Web Application）

输入任务 → 检索经验 → 生成带 R̂ 的 KSTAR 计划 → 导出 Markdown。

## 文件

```
C6交付包/
├── README.md
├── 十三_C6_app链接.md          ← 线上地址（待部署）
├── 十三_C6_repo链接.md         ← 源码仓库（待推送）
├── 十三_C6_AI日志.md
├── 十三_C6_拿来说明.md
├── 十三_C6_AAR.md
├── 十三_C6_demo.mp4            ← 30 秒演示（截图合成，非录屏）
├── 01_home.png
├── 02_plan.png
└── 03_mobile.png
```

源码：`../C5交付包/repo/kstar-os/web/index.html`（单文件，零依赖）

## 核心流程

1. 写任务与情境（R̂ 必填）
2. 点「检索相似经验」→ 本机匹配 5 条经验 / 6 个技能
3. 点「生成 KSTAR 计划」→ 无 Key 用模板；有 Key 调用模型
4. 复制或下载 `.md`

## AI 集成说明

| 项 | 状态 |
|---|---|
| 集成方式 | 用户自带 Key（OpenAI 兼容接口），只存页面内存 |
| 无 Key 时 | 模板模式，页面明确显示，不伪装 |
| 有 Key 时 | 任务 + 情境 + 检索结果 → 模型 → 计划 |
| 假按钮 | 无 |

## 诚实边界

- 已部署：https://makunhao.github.io/kstar-os/ 。
- 没有可用 API Key，因此没有"AI 模式"的真实调用截图。
- demo.mp4 是三张真实界面截图合成的 30 秒视频，不是录屏。
