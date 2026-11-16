# 工具层（L4 Tool / Access）

> 只登记**实际跑通过**的工具。装了但没冒烟测试的，写在「待验证」，不能算行动半径。

| 类别 | 工具 | 版本 / 位置 | 用途 | 最近验证 |
|---|---|---|---|---|
| 运行时 | Python | 3.10.12（Linux）/ 3.13（Windows venv） | 全部脚本 | 2026-11-16 ✅ |
| 运行时 | Node.js | v22.23.4 | 前端构建、本地服务 | 2026-11-16 ✅ |
| 版本控制 | git | 2.34.1 / 2.55.0（Windows） | 仓库、提交历史 | 2026-11-16 ✅ |
| 文档 | MiKTeX 便携版 | `D:/ai+x/work/miktex-portable` | LaTeX → PDF | 2026-11-16 ✅ |
| 表格 | openpyxl | 3.1.5 | 生成 xlsx | 2026-11-16 ✅ |
| 图像 | Pillow | 12.3.0 | 终端实录转截图 / 视频帧 | 2026-11-16 ✅ |
| 视频 | ffmpeg | 系统自带 | demo.mp4 | 2026-11-16 ✅ |
| 浏览器 | Chrome（Windows） | `/c/Program Files/Google/Chrome/Application/chrome.exe` | 无头截图 | 2026-11-16 ✅ |
| 大模型 | Claude（本会话） | mythos-magpie-8067699270 | 推理、生成、审校 | 2026-11-16 ✅ |
| 大模型 | Ollama | 0.31.1，模型已清空 | 本地推理（需重新 pull） | 2026-11-16 ⚠️ 无模型 |
| 代码托管 | GitHub | github.com 可达（沙箱 200） | C5/C5A | 2026-11-16 ✅ 无 token |
| 连接器 | 飞书 | auth-required | C3 证据 | 2026-11-16 ❌ 过期 |

## 调用规则

- 任何外部写入（push / 发布 / 删除）前，先在本地生成并自检，再执行一次可回滚的操作。
- 长任务必须留日志：`logs/` 下写文件，而不是只打屏。
- 代理环境：本地请求用 `build_opener(ProxyHandler({}))` 绕过代理（踩过 3 次）。

## 待验证

| 工具 | 状态 |
|---|---|
| `gh` CLI | 未安装（可直接用 git + token 替代） |
| Playwright | 未安装；Web App 截图先用 Chrome 无头 / 文件预览 |
| 公众号发布 API | 个人号无 API，只能人工粘贴 |
