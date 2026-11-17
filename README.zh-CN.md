# **Agent Forge** — 把意图锻造成可验证的工程

Agent Forge 是一套独立的、面向发布的 Agent Skills 工具包，包含十个聚焦编码工作的技能。它的目标不是堆砌摘要，而是让工作始终对齐意图，并以证据收尾。每个技能都有一个简短的主文件用于执行，并按需打开本地参考文档。

[English](README.md) | [来源目录](docs/sources.md) | [验证说明](docs/validation.md) | [合成示例](docs/examples/synthetic-walkthrough.md)

## 为什么需要它

编码智能体常在几个固定位置出错：目标还没澄清就开始写代码，上下文读得太多或太少，把看似合理的猜测当成证据，没跑通完整流程就宣布成功。Agent Forge 把这些失效点拆成小而可停止的工作流。每个阶段都能产出有用的结果，包括“不是缺陷”“无法复现”“修复因风险停止”或 `NOT RUN`。

这些技能是结构性的说明与工件。它们不强制行为、不扩大权限、不替代评审，也不保证结果一定更好。

## 十个工作流

| 技能 | 适用时机 | 典型产物 |
| --- | --- | --- |
| [forge-intent-alignment](skills/forge-intent-alignment/SKILL.md) | 需求含糊、把症状和原因混在一起、范围变化，或需要复述与验收检查。 | 意图简报、假设清单、验收检查 |
| [forge-signal-first-context](skills/forge-signal-first-context/SKILL.md) | 代码库陌生或庞大，或探索正在变成逐文件通读。 | 带事实、出处和排除项的上下文包 |
| [forge-disposable-prototypes](skills/forge-disposable-prototypes/SKILL.md) | 多个方案需要比较，且一个开放问题挡住了设计决策。 | 限时原型、测量表、丢弃决策 |
| [forge-architectural-constraints](skills/forge-architectural-constraints/SKILL.md) | 同一类纠正反复出现，或快速补丁会传播坏模式。 | 结构性修复、约束执行点、迁移与回滚 |
| [forge-verification-harness](skills/forge-verification-harness/SKILL.md) | 变更需要可重复的端到端检查、驱动、隔离状态或用户功能地图。 | 可用驱动、功能地图、前后工件 |
| [forge-triage-repro-fix](skills/forge-triage-repro-fix/SKILL.md) | 缺陷报告需要分诊、精确复现、失败测试和有边界的修复。 | 判定、复现、失败测试、机制说明 |
| [forge-evidence-review](skills/forge-evidence-review/SKILL.md) | diff、修复、设计或形式化主张需要基于可执行证据的独立评审。 | 结论、反例、阻塞项、未测试区域 |
| [forge-depth-first-parallelism](skills/forge-depth-first-parallelism/SKILL.md) | 同一故障有多种假设，且存在隔离工作区。 | 假设台账与排除证据 |
| [forge-context-budget](skills/forge-context-budget/SKILL.md) | 会话过载、多个技能都可能适用，或需要消融指令。 | 上下文清单、触发说明、消融结果 |
| [forge-formal-boundaries](skills/forge-formal-boundaries/SKILL.md) | 有人把模型、证明、状态机或有界检查当作证据。 | 假设、边界、反例解释、残余风险 |

## 选择指南

- **不确定用户到底要什么：** 先做意图对齐。
- **新仓库或大仓库：** 先用信号优先上下文，再收敛到一个决策。
- **有多个设计但没有证据：** 使用一次性研究原型。
- **同一个错误反复出现：** 转向架构约束。
- **需要证明某条流程可用：** 先建验证基础设施，再谈就绪。
- **收到缺陷报告：** 走可停止的分诊、复现、修复循环。
- **变更准备评审：** 要求证据优先评审，而不是猜测式挑刺大会。
- **一个故障有多个解释：** 围绕一个问题做深度优先的并行尝试。
- **会话或技能集膨胀：** 使用上下文预算。
- **有人引用证明或模型：** 应用形式化验证边界。

一个任务可以使用多个技能，但只有触发条件匹配时才应阅读主文件。参考文档按需打开。

## 安装

只从 Agent Forge 的公开项目页面或发布归档获取文件。如果发布方提供克隆 URL，只能使用 Agent Forge 的 URL；其他仓库都不是这些技能文件夹的来源。

把选中的技能文件夹复制到宿主使用的技能目录，保留文件夹本身、`references/`、`LICENSE` 与 `NOTICES.md`。每个技能都是自包含的，包括自己的来源映射和声明。不要把整个仓库复制到技能根目录，不要多套一层 `skills/`，也不要覆盖或合并到已有目标。

Codex 风格的项目级示例，使用相对目标路径并带拒绝覆盖保护：

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

OpenCode 项目级示例：

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

每个选中的技能运行一次对应片段。保护检查会在复制前识别已有文件、目录或符号链接，因此检查失败时不会合并出部分目标。

正确结构应为：

```text
<target-project>/.agents/skills/forge-intent-alignment/SKILL.md
<target-project>/.agents/skills/forge-intent-alignment/LICENSE
<target-project>/.agents/skills/forge-intent-alignment/NOTICES.md
<target-project>/.agents/skills/forge-intent-alignment/references/field-guide.md
<target-project>/.agents/skills/forge-intent-alignment/references/sources.md
<target-project>/.agents/skills/forge-intent-alignment/references/smoke-case.md
```

错误结构包括 `<target-project>/.agents/skills/skills/forge-intent-alignment/`，以及把主文件直接放在 `.agents/skills/SKILL.md`。部分宿主还文档化了用户级技能目录；这些位置请遵循宿主自己的文档。本仓库不会全局安装，也不会自动安装。

宿主发现规则有公开文档，但本仓库**没有实测**任何宿主的真实安装或运行行为。目录结构在 2026-11-18 检查时与 Agent Skills 约定结构兼容：小写 kebab-case 名称与父目录一致、描述说明触发时机、通过本地参考实现渐进披露。该日期检查的公开宿主文档包括：[Agent Skills 规范](https://agentskills.io/specification)、[Codex 技能文档](https://learn.chatgpt.com/docs/build-skills.md) 与 [OpenCode 技能文档](https://opencode.ai/docs/skills/)。Agent Forge 不是插件包。

## 示例

合成示例展示了意图、上下文、验证基础设施和分诊技能如何组合。它只用于说明，不是行为评估：[docs/examples/synthetic-walkthrough.md](docs/examples/synthetic-walkthrough.md)。

智能体会话中的最小使用方式：

1. 让宿主加载 `forge-intent-alignment`，先复述目标。
2. 问题清楚后，再加载 `forge-signal-first-context`。
3. 当结论需要端到端检查时，加入验证基础设施。
4. 用分诊或证据优先评审，让结果保持可停止、可核查。

## 验证

需要 Python 3.11 或更高版本；检查本身不访问网络：

```bash
python scripts/validate.py
python scripts/smoke.py
python -m unittest discover -s tests -v
```

验证器检查受限的字符串标量前置元数据配置、名称与描述规则、章节顺序与主文件长度、示例标记、相对链接、技能内链接包含关系、独立许可证与声明、合成 smoke 用例结构、规范且双向的来源映射、重复来源 URL、发布清单、禁止的发布工件、超大文件以及基于模式的隐私卫生。测试包含负向变异用例，覆盖坏名称、缺少触发词、断链、缺失来源、重复来源 URL、错误前置元数据、缺失声明、禁止工件、超大文件、清单漂移、smoke 用例错误和合成泄漏夹具。GitHub Actions 会运行全部三条命令；工作流的 checkout 和 Python 安装步骤需要访问 GitHub，但验证逻辑本身是离线的。

隐私扫描是启发式检查，不能证明不存在任何秘密。发布清单必须与仓库文件集合完全一致，因此意外日志、缓存、会话导出或其他工件都会导致验证失败。Python 缓存文件和 `.git` 不进入发布扫描；工件与会话目录不会被静默忽略。

通过这些检查**不能**证明模型会遵循工作流、宿主会发现技能、产出质量会提高或成本会下降。确切边界见 [docs/validation.md](docs/validation.md)。

## 归属与权利

Agent Forge 是一套独立改编，灵感来自 Lauren Tan（@poteto）的公开写作。它**不是官方项目，与 Lauren Tan 本人及其任何雇主或公司均无隶属、赞助、审阅或背书关系**。它不是 pstack 代码，没有复制文章正文、仓库代码或完整帖子。这里的模板、标签、工作流措辞、验证器、测试和示例均为原创改编，不应归功于来源作者。

[docs/sources.md](docs/sources.md) 中列出的公开帖子权利归各自作者所有。URL 仅用于署名与延伸阅读；公开可读不等于获得再许可权利。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本仓库的原创材料采用 [MIT License](LICENSE)。该许可仅适用于我们的原创工作。每个技能文件夹都带有自己的 `LICENSE` 与 `NOTICES.md`，因此按文件夹安装时无需仓库根目录也能保留权利声明。

## 限制

- 这些是说明与工件，不会覆盖宿主政策、审批、沙箱规则、凭据规则或用户权限。
- 技能可以停在修复之前。“不是缺陷”“无法复现”“风险过高”和 `NOT RUN` 都是有效结果。
- 验证只覆盖实际运行过的检查。
- 形式化结果受假设和模型范围限制，不是无缺陷保证。
- 验证器证明的是结构一致性，不是行为、质量、安全性或成本影响。
- 不作出生产率或 PR 数量方面的性能声明。本工具包不以这类指标衡量效果。
- 来源公开并不意味着其内容可以超出原作者条款被复用。

## 参与贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [CHANGELOG.md](CHANGELOG.md)。
