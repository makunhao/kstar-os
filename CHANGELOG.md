# Changelog

All notable changes to this project are documented here.
Format follows Keep a Changelog; versioning follows SemVer.

## [0.3.0] — 2026-11-16

### Added
- `recall`：跨 L1/L2/L3 的关键词检索（中文按 2-gram 切分）
- `plan`：生成 KSTAR 计划模板，强制写 R̂
- `reflect`：按时间窗聚合 ΔR、偏差最大的三条、技能调用分布
- `export-html`：单文件静态面板
- 6 个真实使用过的技能（submission-audit、dashboard-build、repo-release、github-repo-analysis、weekly-aar、content-outline）

### Changed
- `skill-use` / `skill-iter` 在技能不存在时报错退出（码 2），不再静默创建"幽灵技能"
- 仪表盘挑战列改为自然排序（C1 → C2 → C2A → C2G → C3）

### Fixed
- 扫描器遍历大目录导致超时：改为 `os.walk` + 目录剪枝

## [0.2.0] — 2026-11-16

### Added
- `episode`：写入 L2 经验并自动计算 ΔR
- `import_legacy.py`：从既有工作日志导入 5 条真实经验（带 source 字段）
- `status`：五层完整性检查

### Changed
- L2 索引从目录扫描改为 `episodes.json` 显式索引（检索更快、可排序）

## [0.1.0] — 2026-11-16

### Added
- 初始版本：`capture`、`skill-new`、`status`
- AGENT.md、identity.md、tools.md 三层配置
