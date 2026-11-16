# C5 交付包 · GitHub Repository（kstar-os）

把 C10 的第二大脑系统打包成一个可 clone、可运行、可贡献的开源仓库。

## 文件

```
C5交付包/
├── README.md
├── 十三_C5_repo链接.md          ← 仓库地址（待推送）
├── 十三_C5_readme截图.png       ← README 本地渲染截图
├── 十三_C5_AI日志.md
├── 十三_C5_拿来说明.md
├── 十三_C5_AAR.md
└── repo/kstar-os/               ← 完整 git 仓库（12 commits）
```

## 仓库一览

| 项 | 值 |
|---|---|
| 名称 | kstar-os |
| 语言 | Python 3.9+（零第三方依赖） |
| License | MIT |
| 提交 | 12 |
| 测试 | 9/9 通过 |
| CI | GitHub Actions 3.9–3.12 |
| 社区要素 | CONTRIBUTING / CHANGELOG / issue 表单 / PR 规范 |

## 线上地址

- 仓库：https://github.com/makunhao/kstar-os
- Web：https://makunhao.github.io/kstar-os/

## 5 分钟验证

```bash
cd repo/kstar-os
python3 -m unittest discover -s tests -v
python3 scripts/kstar.py status
python3 -m http.server 8000   # http://localhost:8000/web/
```

## 诚实边界

- 已推送 GitHub 并开通 Pages；没有外部用户 star/fork，不能声称“被使用”。
- README 截图是本地渲染，不是 GitHub 页面。
- 在 Linux 工作区建仓后整体拷贝，因为 Windows 挂载盘不支持 git 的锁文件删除。
