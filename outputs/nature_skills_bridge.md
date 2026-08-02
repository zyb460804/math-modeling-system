# Nature Skills 归档公告

> **v3.0 | 2026-08-02**
> **变更**：9 个 Nature 学术 skill 全部归档到 `.claude/skills/_archive/`。方法论精华已抽取到主流程 references/，能力未丢失。
> **历史**：v2.0（2026-05-31）曾将 3 个 nature skill（figure/paper2ppt/writing）作为可选接入。v3.0 改为"全部消化进主流程"，不再保留独立 skill 入口。

---

## 一、归档清单（9 个 → 全部归档）

| 原 skill | 归档位置 | 方法论精华去向 | 是否新建文档 |
|---------|---------|--------------|------------|
| nature-polishing | `_archive/nature-polishing/` | `paper-formal-writer/references/ai-traffic-light.md` | ✅ 新建 |
| nature-writing | `_archive/nature-writing/` | `paper-formal-writer/references/english-academic-writing.md` | ✅ 新建 |
| nature-figure | `_archive/nature-figure/` | `paper-workflow-orchestrator/references/figure-evidence-layering.md` | ✅ 新建 |
| nature-paper2ppt | `_archive/nature-paper2ppt/` | **`defense-ppt-builder-zh`** skill（新建） | ✅ 新建 skill |
| nature-reader | `_archive/nature-reader/` | `award-paper-rag/references/bilingual-reader-protocol.md` | ✅ 新建 |
| nature-academic-search | `_archive/nature-academic-search/` | `authoritative-data-harvester/references/multi-source-search.md` | ✅ 新建 |
| nature-citation | `_archive/nature-citation/` | 分段-证据分级已被 `citation-tracer` 覆盖 | ❌ 无需新建 |
| nature-data | `_archive/nature-data/` | FAIR/数据可用性声明国赛无需求 | ❌ 无需新建 |
| nature-response | `_archive/nature-response/` | 仅期刊投稿审稿回复用 | ❌ 无需新建 |

---

## 二、为什么归档

### 核心问题：覆盖率天花板 + 维护内卷

v4.6 系统共 67 个 skill，但标准国赛流程只能触达约 60%。剩余 40%（含 9 个 Nature skill）**永远不进主流程**——它们是英文期刊投稿场景的产物，对国赛中文论文无价值。

保留它们导致：
1. CLAUDE.md 路由表持续膨胀
2. Agent 选 skill 时困惑（同一能力有 2-3 个入口）
3. 维护成本翻倍（9 个 skill 的 SKILL.md + scripts + references）

### 解决方案：消化而非保留

v4.8 采用"消化"策略：
1. **抽取方法论精华**到现有 skill 的 `references/`（6 份新文档）
2. **新建 1 个 skill**（`defense-ppt-builder-zh`）填补国赛答辩 PPT 空白
3. **归档原 skill**到 `_archive/`（可恢复，git mv 保留历史）
4. **更新引用文档**消灭断链

---

## 三、能力迁移对照表

| 原 Nature skill 能力 | 现在怎么获得 |
|---------------------|------------|
| Nature 风格段落润色 | `paper-polisher` skill + `ai-traffic-light.md` 参考 |
| AI 写作边界管控 | `ai-traffic-light.md`（红绿灯规则） |
| 论文写作架构重建 | `section-architecture.md` + `english-academic-writing.md` |
| 多面板科学图表 | `math-figure` skill + `figure-evidence-layering.md` 参考 |
| 答辩 PPT 生成 | **`defense-ppt-builder-zh`** skill（国赛中文版） |
| 论文中英对照精读 | `award-paper-rag` skill + `bilingual-reader-protocol.md` |
| 多源文献检索 | `authoritative-data-harvester` skill + `multi-source-search.md` |
| CNS 期刊引用 | `citation-tracer` skill（分段-证据分级） |
| 数据可用性声明 | ❌ 国赛无需求（如需英文期刊投稿，参考 `nature-skills/` 源仓库） |
| 审稿回复信 | ❌ 仅期刊投稿用（如需，参考 `nature-skills/` 源仓库） |

---

## 四、源仓库保留

`nature-skills/` 目录（源仓库）**完整保留**，不删除、不归档：

```
nature-skills/           ← 源仓库，保留完整（upstream 参考）
├── skills/
│   ├── nature-polishing/
│   ├── nature-writing/
│   └── ...（9 个完整 skill）
├── install.md
└── README.md

.claude/skills/_archive/ ← 已安装副本归档（从 .claude/skills/ git mv 来）
├── nature-polishing/
├── nature-writing/
└── ...（9 个已归档副本）
```

**用途**：
- 源仓库：英文期刊投稿场景的完整参考（保留可追溯）
- 归档副本：从 Claude Code skill 注册表移除（不再触发），但保留可恢复性

---

## 五、迁移后的调用方式

### 以前（v4.6 及之前）

```
用户："Nature 风格润色这段"
        ↓
Claude 触发 nature-polishing skill
        ↓
读取 nature-polishing/SKILL.md + references/
```

### 现在（v4.8）

```
用户："润色这段"
        ↓
Claude 触发 paper-polisher skill（统一润色入口）
        ↓
读取 paper-polisher/SKILL.md
        + paper-formal-writer/references/ai-traffic-light.md（AI 边界）
        + paper-formal-writer/references/english-academic-writing.md（美赛英文）
        ↓
输出润色结果
```

**关键变化**：不再需要用户区分"Nature 润色"vs"普通润色"——统一入口，方法论精华在底层自动应用。

---

## 六、验证

- ✅ 9 个 skill 已 git mv 到 `_archive/`（git log 可查）
- ✅ 6 份 references 文档已创建（每个都标注来源）
- ✅ `defense-ppt-builder-zh` 新 skill 已创建（SKILL.md + 目录结构）
- ✅ `settings.json` 已更新（删除 14 个注册，新增 1 个）
- ✅ `skill_applicability_matrix.json` 已更新（v1.1，含归档清单）
- ✅ `nature-skills/` 源仓库完整保留

---

## 七、回滚方案

如果需要恢复某个 Nature skill：

```bash
git mv .claude/skills/_archive/nature-XXX .claude/skills/nature-XXX
# 然后在 settings.json 的 skills 块添加注册条目
```

回滚不影响已抽取的 references 文档（它们是新增的，不冲突）。
