# C5 AAR：把 KSTAR OS 做成开源仓库

## 1. 目标（R̂）

一个陌生人 clone 后 5 分钟能跑；README 五段齐全；有测试、CI、贡献指南；能推 GitHub。
**R̂ = 0.8**。

## 2. 过程

1. 选项目：KSTAR OS（C10 系统），因为它是本次交付的地基，且零依赖。
2. 补文档：README / LICENSE / .gitignore / AI_LOG / ATTRIBUTION / CONTRIBUTING / CHANGELOG。
3. 写测试：9 个用例，覆盖全部命令与两个错误路径。
4. 建 CI：Python 3.9–3.12 矩阵 + "无第三方 import" 检查。
5. 建 git 历史：12 条语义化提交。
6. 渲染 README 截图（本地），跑发布检查。

## 3. 结果

| 项 | 结果 | 证据 |
|---|---|---|
| 测试 | 9/9 通过（5.2s） | `python3 -m unittest discover -s tests -v` |
| 仓库 | 12 commits，44 个文件 | `git log --oneline` |
| 文档 | 7 个顶层文档 | 目录列表 |
| CI | 3.9–3.12 + import 检查 | `.github/workflows/ci.yml` |
| 推送 | ✅ 已推送 main，Pages 已构建 | https://github.com/makunhao/kstar-os |

## 4. 证据

- `repo/kstar-os/tests/test_kstar.py`
- `repo/kstar-os/.github/workflows/ci.yml`
- `十三_C5_readme截图.png`（本地渲染）
- `repo/kstar-os/AI_LOG.md`（开发过程）

## 5. 失败与偏差

| 事件 | 预期 | 实际 | ΔR |
|---|---|---|---|
| 直接在 D 盘建 git | 0.9 | 挂载盘不支持删除/原子替换，`HEAD.lock` 死锁 | −0.6 |
| 测试一次全绿 | 0.9 | 6 个通过，但漏了错误路径；补测后发现幽灵技能 bug | −0.2 |
| GitHub 链接 | 0.8 | 已推送，Pages 可访问 | +0.1 |
| 文档一次齐全 | 0.8 | 发布检查发现 README 缺章节，补了一轮 | −0.1 |

综合 **R = 0.9**，ΔR = +0.10。

## 6. 根因

1. **不是 git 坏了，是文件系统不支持**：Windows 挂载盘不允许 unlink 与原子 rename，git 的锁机制必然失败。换到 Linux 工作区构建再整体拷贝，是对症。
2. **测试覆盖的是"顺利路径"**：只测成功会漏掉"拼错名字也能成功"这种最危险的情况。错误路径不是加分项，是必需项。
3. **链接缺失不是产品问题**：仓库本身可用，缺的是凭据；拿到 token 后 10 分钟完成推送与 Pages。

## 7. 改进

- 任何需要 git 的交付，先在工作区（Linux）建仓，再整体同步；不要在挂载盘上 `git init`。
- 测试清单固定包含：每个命令 1 个正路径 + 1 个错误路径。
- 凭据类阻塞在开工时确认，不等最后。

## 8. 可迁移经验

> **先问"这个文件系统支持 git 吗"，再问"git 命令写对了吗"。**
> 环境不支持的操作，重试一百次也不会成功；换执行位置比调参数有效。
