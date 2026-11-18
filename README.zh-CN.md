# Agent Forge

十个体积小巧、安装在项目内的 Agent Skills，面向必须保持意图对齐并以证据收尾的编码工作。当需求含糊、代码库陌生、缺陷报告嘈杂，或变更需要评审前证据时，可以从其中一个开始。

Agent Forge 不是框架，也不是插件。每个技能都是一个简短检查清单加按需打开的本地参考。把一个技能文件夹复制进项目，在触发条件匹配时阅读主文件，并在任一阶段带着有用结果停下。

[English](README.md) | [可运行示例](examples/triage-repro-fix/README.md) | [验证说明](docs/validation.md) | [参与贡献](CONTRIBUTING.md)

## 它解决什么问题

- **需求还没澄清就开始动手。** 把观察到的事实与推测原因分开，记录假设，并在修改前定义验收检查。
- **上下文读得太多或太少。** 聚焦入口、接口、测试、日志和近期变更，而不是逐个文件通读。
- **把看似合理的原因当成证据。** 先分诊报告，捕获精确流程，写出失败回归测试，再做针对机制的最小修复。
- **只凭偏好评审。** 把“看起来没问题”变成由已执行检查、反例和明确列出的未测试区域支撑的结论。
- **该停下时强行修复。** “不是缺陷”“无法复现”“风险过高”和 `NOT RUN` 都是有用结果。

## 快速开始：安装一个技能

克隆公开仓库 [github.com/kabishou11/agent-forge](https://github.com/kabishou11/agent-forge)，然后在仓库根目录运行片段。只把需要的技能复制到项目级技能目录。保护检查会拒绝已有文件、目录或符号链接，因此不会合并或覆盖用户内容。

Codex 风格的 `.agents/skills` 示例：

```bash
set -eu
TARGET=../target-project
SKILL=forge-intent-alignment

mkdir -p "$TARGET/.agents/skills"
DEST="$TARGET/.agents/skills/$SKILL"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  printf 'Refusing to overwrite existing destination: %s\n' "$DEST" >&2
  exit 1
fi
cp -R "skills/$SKILL" "$DEST"
```

OpenCode 的 `.opencode/skills` 示例：

```bash
set -eu
TARGET=../target-project
SKILL=forge-verification-harness

mkdir -p "$TARGET/.opencode/skills"
DEST="$TARGET/.opencode/skills/$SKILL"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  printf 'Refusing to overwrite existing destination: %s\n' "$DEST" >&2
  exit 1
fi
cp -R "skills/$SKILL" "$DEST"
```

每个选中的技能运行一次片段，并替换 `SKILL`。复制后的文件夹是自包含的：相对链接、`LICENSE`、`NOTICES.md` 和参考文档都会一起保留。

正确结构应为：

```text
<target-project>/.agents/skills/forge-intent-alignment/SKILL.md
<target-project>/.agents/skills/forge-intent-alignment/LICENSE
<target-project>/.agents/skills/forge-intent-alignment/NOTICES.md
<target-project>/.agents/skills/forge-intent-alignment/references/field-guide.md
<target-project>/.agents/skills/forge-intent-alignment/references/sources.md
<target-project>/.agents/skills/forge-intent-alignment/references/smoke-case.md
```

不要把整个仓库复制到技能根目录，不要多套一层 `skills/`，也不要把 `SKILL.md` 直接放在 `.agents/skills/SKILL.md`。部分宿主还文档化了用户级目录；这些位置请遵循宿主自己的文档。Agent Forge 不会全局安装，也不会自动安装。

## 第一个工作流：从缺陷报告到评审后的修复

可运行示例会把一个合成缺陷走完分诊流程：

```bash
python3 examples/triage-repro-fix/run_demo.py --output .forge-demo-output
```

预期最后两行：

```text
status: evidence-ready
artifacts: .forge-demo-output
```

它会读取一份很小的虚构[缺陷报告](examples/triage-repro-fix/bug-report.md)，写出意图简报，让回归测试失败，应用一行修复，重跑同一个测试，并生成证据评审。查看 `intent-brief.md`、`repro-failure.txt`、`bounded-fix.diff`、`verification-pass.txt` 和 `evidence-review.md`，然后删除输出目录。路径必须是相对路径，示例会拒绝已有的文件、目录或符号链接。

结论要求修复前出现预期的断言失败、修复后同一个测试通过，并且评审检查成功。导入、语法、测试框架错误或无关失败会返回 `needs-work`，并保留在工件中。这是可执行的工件流程，不测试语言模型是否会遵循技能。完整说明见[示例 README](examples/triage-repro-fix/README.md)。

## 十个技能

| 技能 | 适用时机 | 有用产物 |
| --- | --- | --- |
| [forge-intent-alignment](skills/forge-intent-alignment/SKILL.md) | 需求含糊、把症状和原因混在一起、范围变化，或需要验收检查。 | 意图简报、假设清单、验收检查 |
| [forge-signal-first-context](skills/forge-signal-first-context/SKILL.md) | 代码库陌生或庞大，或探索正在变成逐文件通读。 | 带事实、出处和排除项的上下文包 |
| [forge-disposable-prototypes](skills/forge-disposable-prototypes/SKILL.md) | 多个方案需要比较，且一个开放问题挡住了设计决策。 | 限时原型、测量表、丢弃决策 |
| [forge-architectural-constraints](skills/forge-architectural-constraints/SKILL.md) | 同一类纠正反复出现，或快速补丁会传播坏模式。 | 结构性修复、约束执行点、迁移与回滚 |
| [forge-verification-harness](skills/forge-verification-harness/SKILL.md) | 变更需要可重复的端到端检查、驱动、隔离状态或用户功能地图。 | 可用驱动、功能地图、前后工件 |
| [forge-triage-repro-fix](skills/forge-triage-repro-fix/SKILL.md) | 缺陷报告需要分诊、精确复现、失败测试和有边界的修复。 | 判定、复现、失败测试、机制说明 |
| [forge-evidence-review](skills/forge-evidence-review/SKILL.md) | diff、修复、设计或形式化主张需要基于可执行证据的独立评审。 | 结论、反例、阻塞项、未测试区域 |
| [forge-depth-first-parallelism](skills/forge-depth-first-parallelism/SKILL.md) | 同一故障有多种假设，且存在隔离工作区。 | 假设台账与排除证据 |
| [forge-context-budget](skills/forge-context-budget/SKILL.md) | 会话过载、多个技能都可能适用，或需要消融指令。 | 上下文清单、触发说明、消融结果 |
| [forge-formal-boundaries](skills/forge-formal-boundaries/SKILL.md) | 有人把模型、证明、状态机或有界检查当作证据。 | 假设、边界、反例解释、残余风险 |

一个任务可以使用多个技能。只有触发条件匹配时才阅读主文件，只有下一步需要时才打开参考文档。

## 在会话中使用技能

1. 让宿主按名称加载技能，例如 `forge-intent-alignment`。
2. 提供需求、相关文件以及已有证据。
3. 当下一步需要审批、缺少环境或需要其他负责人时，允许技能停下。

## 文档与参与贡献

- [可运行分诊示例](examples/triage-repro-fix/README.md) — 输入、命令、工件与检查。
- [合成组合示例](docs/examples/synthetic-walkthrough.md) — 多个技能如何组合。
- [来源目录](docs/sources.md) — 影响这些主题的公开写作。
- [验证与兼容性](docs/validation.md) — 检查、宿主参考文档与未测试边界。
- [参与贡献](CONTRIBUTING.md) — 技能修改、来源、隐私、提交格式与检查。
- [变更日志](CHANGELOG.md) 与 [第三方声明](THIRD_PARTY_NOTICES.md)。

## 兼容性与验证

技能文件夹遵循 Agent Skills 结构：小写 kebab-case 名称与文件夹一致、描述说明触发时机、参考文档本地存放。文档中的复制片段已在项目内临时目录中实际执行；真实宿主发现与模型行为没有实测。宿主参考文档、检查项和确切边界见[验证与兼容性](docs/validation.md)。

## 归属与许可

Agent Forge 是独立原创工作，灵感来自 Lauren Tan（@poteto）的公开写作。它不是官方项目，与 Lauren Tan 本人及其任何雇主或公司均无隶属、赞助、审阅或背书关系。原创材料采用 MIT 许可；来源帖子的权利归各自作者所有。详见[来源目录](docs/sources.md)、[第三方声明](THIRD_PARTY_NOTICES.md)与 [LICENSE](LICENSE)。每个技能文件夹都带有自己的 `LICENSE` 与 `NOTICES.md`。
