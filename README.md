# Project Memory

让 AI agent 在复杂开发任务中记住关键决策和当前进度，并能将完整上下文交接给新的 agent 继续工作。

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
