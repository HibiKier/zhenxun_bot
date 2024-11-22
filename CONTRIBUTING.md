# zhenxun_bot 贡献指南

首先，感谢你愿意为 zhenxun_bot 贡献自己的一份力量！

本指南旨在引导你更规范地向 zhenxun_bot 提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [已有的 Issues](https://github.com/HibiKier/zhenxun_bot/issues)，以防重复提交。

### 报告问题、故障与漏洞

如果你在使用过程中发现问题并确信是由 zhenxun_bot 引起的，欢迎提交 Issue。

请使用我们提供的 **Bug 反馈** 模板，并尽可能详细地描述：

- 问题描述
- 重现步骤
- 你的环境信息（如操作系统、依赖版本等）

### 建议功能

如果你有新的功能需求或改进建议，欢迎提出。

请使用 **功能建议** 模板，并详细描述你所需要的特性，可能的话可以提出你认为可行的解决方案。

### 文档相关

如果你觉得文档有误或缺乏更新，欢迎提出。

请使用 **文档改进** 模板，并详细描述问题或主题，希望我们做出的修改

## Pull Request

### 分支管理

请从 `main` 分支创建新功能分支，例如：

- 新功能：`feature/功能描述`
- 问题修复：`bugfix/问题描述`

### 代码风格

zhenxun_bot 使用 `pre-commit` 进行代码格式化和检查，请在提交前确保代码通过检查。

```bash
# 在安装项目依赖后安装 pre-commit 钩子
pre-commit install
```

> 未通过 `pre-commit` 检查的代码将无法合并。

### Commit 规范

请确保你的每一个 commit 都能清晰地描述其意图，一个 commit 尽量只有一个目的。

我们建议遵循 [gitmoji](https://gitmoji.dev/) 的 commit message 格式，在创建 commit 时请牢记这一点。

### 工作流程概述

`main` 分支为 zhenxun_bot 的主分支，在任何情况下都请不要直接修改 `main` 分支，而是创建一个目标分支为 `main` 的 Pull Request 来提交修改。Pull Request 标题请尽量清晰，以便维护者进行审核。

如果你不是 zhenxun_bot 团队的成员，可在 fork 本仓库后，向本仓库的 `main` 分支发起 Pull Request，注意遵循先前提到的 commit message 规范创建 commit。我们将在 code review 通过后合并你的贡献。

### 撰写文档

如果你对文档有改进建议，欢迎提交 Pull Request 或者 Issue。

[//]: # (我们使用 Markdown 编写文档，建议遵循以下规范：)

[//]: # ()
[//]: # (1. 中文与英文、数字、半角符号之间需要有空格。例：`zhenxun_bot 是一个高效的聊天机器人。`)

[//]: # (2. 若非英文整句，使用全角标点符号。例：`现在你可以看到机器人回复你：“Hello，世界！”。`)

[//]: # (3. 直引号`「」`和弯引号`“”`都可接受，但同一份文件里应使用同种引号。)

[//]: # (4. **不要使用斜体**，你不需要一种与粗体不同的强调。)

[//]: # (5. 文档中应以“我们”指代开发者，以“用户”指代机器人的使用者。)

[//]: # ()
[//]: # (如果你需要编辑器检查 Markdown 规范，可以在 VSCode 中安装 `markdownlint` 扩展。)

### 参与开发

zhenxun_bot 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。

> 暂未搭建测试框架，因此暂不要求添加测试代码。

## 项目沟通

如有关于贡献流程的疑问或需要进一步指导，请通过 [QQ群](https://jq.qq.com/?_wv=1027&k=u8PgBkMZ) 联系我们。

再次感谢你的贡献！