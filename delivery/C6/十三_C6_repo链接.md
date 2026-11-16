# C6 源码仓库链接

**https://github.com/makunhao/kstar-os**

## 部署信息

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/makunhao/kstar-os |
| 分支 | `main` |
| Web 入口 | `docs/index.html`（GitHub Pages 只支持 `/` 或 `/docs`） |
| 本地入口 | `web/index.html`（与 docs 同源） |
| Pages | https://makunhao.github.io/kstar-os/ |
| Page 状态 | `built`，HTTP 200，13,031 字节 |

## 仓库说明

- 源码目录：`C5交付包/repo/kstar-os/`（与线上仓库一致，11 commits）
- Web 应用：`web/index.html`（单文件，无构建步骤）
- 本地运行：直接双击 `web/index.html`，或 `python3 -m http.server` 后访问

## 与 C5 的关系

C6 的源码就是 C5 的仓库，没有第二份代码：

| 层 | 文件 | 对应挑战 |
|---|---|---|
| CLI 与记忆系统 | `scripts/kstar.py` | C10 |
| Web 界面 | `web/index.html` / `docs/index.html` | C6 |
| 技能库 | `memory/L3_skills/` | C4/C10 |
| 仓库文档与社区要素 | `README / LICENSE / CONTRIBUTING / AI_LOG / ATTRIBUTION / .github` | C5 |
| 测试 | `tests/test_kstar.py`（9 个） | C5 |

## 部署步骤（已完成）

```bash
git push -u origin main
# Settings → Pages → Deploy from a branch → main / docs
```

API 方式：

```bash
POST /repos/makunhao/kstar-os/pages
{"source":{"branch":"main","path":"/docs"}}
```

不需要构建、不需要环境变量。API Key 由用户在页面内输入，不写入代码。
