# 贡献指南

## 这个项目接受什么

- 新的 KSTAR 循环命令（必须带测试）
- 新的技能模板（必须附一条真实使用记录）
- 检索质量改进（同义词、分词、排序）
- 文档修正（尤其是与代码不一致的描述）

## 不接受什么

- 引入运行时第三方依赖（除非有充分理由并默认可选）
- 把 Markdown 存储换成数据库（除非有基准数据证明当前方案不可用）
- 自动生成 R̂ / ΔR 的功能（会破坏校准的意义）

## 开发流程

```bash
git clone https://github.com/<your-name>/kstar-os.git
cd kstar-os

# 跑测试（零依赖）
python3 -m unittest discover -s tests -v

# 冒烟测试
python3 scripts/kstar.py status
```

## 提交规范

提交信息用「动词 + 对象 + 原因」：

```
fix: skill-use 拒绝拼写错误的技能名

原先会在 L3_skills/<typo>/ 下创建 usage.json，导致幽灵技能。
现在检查 SKILL.md 是否存在，不存在退出码 2。
```

不要用 `update`、`fix bug`、`修改` 这类无信息量的信息。

## 新增技能

1. `python3 scripts/kstar.py skill-new <name> --desc "..."`
2. 补全 `SKILL.md` 的 When / Input / Steps / Output；Steps 必须是动作。
3. 真实用一次，记录 `skill-use`。
4. 如果改了步骤，记录 `skill-iter`。

## 测试要求

- 新命令必须有至少一个正路径用例 + 一个错误路径用例。
- 测试不得依赖网络、不得依赖真实 `~/.neoskills` 或用户主目录。
- PR 前本地跑一遍全量测试；CI 会在 Python 3.9–3.12 上重跑。

## 代码风格

- 标准库优先；能用 20 行标准库解决的，不引入 200 行的库。
- 函数名说动作，变量名说内容；避免单字母变量（`l` 尤其）。
- 错误要打印人能看懂的原因，并给出下一步。
