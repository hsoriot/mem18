# Agent Skills

一组帮助 AI agent 在复杂任务中更高效工作的 skill。

## Skills

### project-memory

让 AI agent 在复杂开发任务中记住关键决策和当前进度，并能将完整上下文交接给新的 agent 继续工作。

### req-decompose

帮助用户将模糊的一句话需求，通过结构化的迭代问询，逐步拆解为一份完整的、可实施的需求文档。

---

## project-memory 详细说明

## 解决什么问题

AI agent（Claude Code、Codex 等）的会话是短暂的。一旦上下文窗口用尽或开启新会话，之前积累的任务理解、技术决策、进度状态就全部丢失。在多步骤的开发任务中，这意味着：

- 新 agent 需要从头理解项目，浪费大量上下文
- 重要的技术决策没有被记录，可能被推翻或重复讨论
- 遇到阻塞切换 agent 时，任务进度无法衔接

`project-memory` 通过在本地文件系统维护一组结构化的记忆文件来解决这些问题。任何 agent 都可以读取上一个 agent 留下的记忆，快速恢复上下文并继续工作。

## 核心概念

每个项目的记忆存储在 `~/.agent-memory/project-memory/projects/<project-slug>/` 下，包含四个文件：

| 文件 | 内容 | 更新频率 |
|------|------|----------|
| `project.md` | 项目背景、目标、约束、非目标 | 很少变动 |
| `current.md` | 当前任务、进度、阻塞项、下一步 | 随任务推进频繁更新 |
| `decisions.md` | 关键技术决策及理由、被否决的备选方案 | 每次重要决策时追加 |
| `meta.yaml` | 项目元数据与时间戳 | 每次写入时自动刷新 |

全局索引 `~/.agent-memory/project-memory/registry.yaml` 记录所有项目的名称到 slug 的映射，方便快速查找。

## 典型使用场景

**场景 1：长任务中途切换 agent**
> 重构进行到一半，上下文窗口快满了。告诉 agent 保存进度，然后开一个新 agent 说"继续项目 xxx"，新 agent 立即恢复上下文。

**场景 2：记录架构决策**
> 在几个技术方案中做了选择。agent 将决策、理由和被否决的方案写入 `decisions.md`，后续 agent 不会重复讨论同样的问题。

**场景 3：多人/多 agent 协作**
> 记忆文件存储在 `~/.agent-memory/` 下，不污染项目仓库。不同工具（Claude Code、Codex 等）共享同一份记忆。

## 安装

全局安装（推荐，所有项目可用）：

```bash
npx skills add hsoriot/mem18 --skill project-memory -g
```

仅当前项目安装：

```bash
npx skills add hsoriot/mem18 --skill project-memory
```

## 使用方式

开始新项目：

```
Use project-memory for project <项目名>.
```

恢复已有项目：

```
Use project-memory to continue project <项目名>.
```

agent 会自动读取记忆文件并返回结构化摘要，然后从上次中断的地方继续工作。

## 四个操作

| 操作 | 说明 |
|------|------|
| `read_project_memory` | 读取全部记忆，返回紧凑摘要 |
| `update_current_status` | 更新当前任务、进度、阻塞项 |
| `append_decision` | 追加一条带日期的技术决策 |
| `generate_handoff_summary` | 生成 agent 间交接摘要 |

## 仓库结构

```
skills/project-memory/
  SKILL.md                        # skill 定义（agent 读取的入口）
  references/                     # 详细参考文档
    schema.md                     # 文件结构与模板定义
    actions.md                    # 操作定义与输出格式
    usage.md                      # 日常使用约定
```

---

## req-decompose 详细说明

## 解决什么问题

用户心中有一个想法或需求，但往往只能用一句话描述。直接让 AI 从这句话生成代码，结果通常偏离用户真实意图。原因在于：

- 用户自己也没有想清楚所有细节
- 一句话包含太多隐含假设，AI 无法猜对
- 需求中的歧义只有通过反复问询才能消除

`req-decompose` 通过结构化的迭代问询流程解决这个问题。agent 按维度（目标、用户、功能、流程、数据、约束等）逐步提问，每次只问 1-3 个问题，帮助用户把模糊想法变成一份完整的、可实施的需求文档。

## 核心特点

- **迭代式提问**：按 9 个维度分阶段提问，而不是一次性问一大堆问题
- **提议而非追问**：agent 主动提出具体方案让用户确认，比开放式提问更高效
- **渐进式文档**：每轮问答后可以预览当前需求草稿，看到文档逐步成型
- **可中断恢复**：会话状态持久化存储，可以跨会话继续拆解
- **标记假设**：agent 做出的假设会明确标记，用户可以在最终审查时修改

## 9 个提问维度

| 阶段 | 内容 |
|------|------|
| 1. 目标与背景 | 为什么要做？解决什么问题？ |
| 2. 用户与角色 | 谁在用？不同角色有什么差异？ |
| 3. 核心功能 | 必须有哪些能力？ |
| 4. 用户流程 | 用户怎么一步步操作？ |
| 5. 数据与状态 | 涉及什么数据？数据之间什么关系？ |
| 6. 非功能需求 | 性能、安全、兼容性目标？ |
| 7. 约束与依赖 | 技术限制、第三方集成、时间线？ |
| 8. 边界与非目标 | 什么不做？ |
| 9. 验收标准 | 怎么算做完了？ |

## 安装

全局安装（推荐）：

```bash
npx skills add hsoriot/mem18 --skill req-decompose -g
```

仅当前项目安装：

```bash
npx skills add hsoriot/mem18 --skill req-decompose
```

## 使用方式

开始拆解新需求：

```
Use req-decompose for 我想做一个用户权限管理系统.
```

继续已有的拆解：

```
Continue decomposing requirement for project user-permission.
```

查看当前草稿：

```
Show me the current draft for project user-permission.
```

agent 会按维度逐步提问，每轮展示进度和已收集的信息，最终生成结构化需求文档。

## 输出文件

需求文档存储在 `~/.agent-memory/req-decompose/projects/<project-slug>/` 下：

| 文件 | 内容 |
|------|------|
| `requirement.md` | 结构化需求文档（最终产物） |
| `session.yaml` | 问询会话状态（支持中断恢复） |
| `meta.yaml` | 项目元数据与时间戳 |

## 仓库结构

```
skills/req-decompose/
  SKILL.md                        # skill 定义（agent 读取的入口）
  references/                     # 详细参考文档
    schema.md                     # 需求文档模板与会话文件格式
    workflow.md                   # 迭代提问框架与阶段转换规则
    usage.md                      # 使用约定与触发示例
```
