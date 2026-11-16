# C5 GitHub Repository · 仓库链接

**https://github.com/makunhao/kstar-os**

**一句话**：KSTAR OS —— 输入一条经历，输出可检索的经验、可调用的技能和可校准的 ΔR。

## 仓库信息

| 项 | 值 |
|---|---|
| 项目名 | kstar-os |
| 语言 | Python 3.9+（标准库） |
| License | MIT |
| 提交数 | 12 |
| 文件数 | 44（不含 `.git`） |
| 测试 | 9 个，全部通过 |
| CI | GitHub Actions，Python 3.9–3.12 |
| Web | https://makunhao.github.io/kstar-os/ |
| 状态 | `main` 已推送；Pages 已构建 |

## 目录

```
kstar-os/
├── README.md / LICENSE / AI_LOG.md / ATTRIBUTION.md
├── CONTRIBUTING.md / CHANGELOG.md
├── AGENT.md
├── config/            identity.md / tools.md
├── scripts/           kstar.py / import_legacy.py
├── memory/            L1_raw / L2_episodes / L3_skills
├── tests/             test_kstar.py（9 个）
├── web/               index.html（C6 源）
├── docs/              index.html（Pages 入口）+ architecture.md
├── examples/          demo_session.md
└── .github/           workflows/ci.yml + ISSUE_TEMPLATE
```

## 本地复现

```bash
cd C5交付包/repo/kstar-os
python3 -m unittest discover -s tests -v   # 9 tests OK
python3 scripts/kstar.py status
python3 -m http.server 8000                # http://localhost:8000/web/
```

## 验证线上仓库

```bash
git clone https://github.com/makunhao/kstar-os.git
cd kstar-os && python3 -m unittest discover -s tests -v
```

## 诚实边界

- 仓库已公开；**没有外部用户 star/fork/issue**，不能声称"被使用"。
- CI 配置已推送，但 GitHub Actions 的首次运行结果未在本机验证（沙箱无法执行 Actions）。
- README 截图是本地 Markdown 渲染，不是 GitHub 页面截图（浏览器无外网）。
