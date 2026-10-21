# 贡献指南

感谢参与「桌面效率助手」项目开发！本文档说明协作流程与规范。

## 开发环境

- Python 3.10+
- 依赖安装：`pip install -r requirements.txt`
- 建议使用虚拟环境：`python -m venv .venv`

## 分支策略

- `main`：稳定分支，保护分支，需通过 PR 合并
- 功能开发：从 `main` 拉出 `feature/xxx` 分支
- 缺陷修复：`fix/xxx` 分支

## 提交规范

采用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>

<body>

<footer>
```

常用 type：
- `feat`：新功能
- `fix`：修复缺陷
- `docs`：文档变更
- `refactor`：重构
- `test`：测试相关
- `chore`：构建/配置/工具变更

示例：
```
feat(clipboard): 实现剪贴板历史记录的搜索功能
fix(todo): 修复任务截止时间提醒不触发的问题
```

## 代码规范

- Python 遵循 PEP 8，缩进 4 空格
- 使用类型注解
- 模块间低耦合，共享数据通过 SQLite 数据库交互
- 所有用户数据本地存储，禁止联网上传

## 提交流程

1. Fork / 克隆仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交变更：`git commit -m "feat: ..."`
4. 推送分支：`git push origin feature/xxx`
5. 在 GitHub 发起 Pull Request

## 里程碑

阶段成果通过打 tag 存档：
- `v0.1-plan`：项目计划
- `v0.2-feasibility`：可行性分析
- `v0.3-srs`：需求规格说明
- `v0.4-design`：总体与详细设计
- `v0.5-impl`：五大模块实现
- `v0.6-test`：系统测试
- `v0.7-final`：项目总结
