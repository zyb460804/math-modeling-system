# Frozen Numbers Convention（冻结数字协议）

> **用途**：定义数值从代码流向论文的唯一通道，防止代码修改静默改变论文数字。
> **来源**：MathModeling-skills/CLAUDE.md
> **版本**：v1.0
> **核心原则**：数字流向 code → results → paper。没有冻结层，代码中的 bug fix 会静默改变论文数字。

---

## 1. frozen_numbers.json Schema

### 文件位置

```
results/Qx/reports/frozen_numbers.json
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FrozenNumbers",
  "description": "某子问题 Qx 的冻结数字快照",
  "type": "object",
  "required": ["question_id", "frozen_at", "frozen_by_skill", "method_decisions", "numbers"],
  "properties": {
    "question_id": {
      "type": "string",
      "description": "子问题标识，如 Q1, Q2, Q3",
      "pattern": "^Q[0-9]+$"
    },
    "frozen_at": {
      "type": "string",
      "format": "date-time",
      "description": "冻结时间戳（ISO 8601），必须晚于所有源文件的 mtime"
    },
    "frozen_by_skill": {
      "type": "string",
      "description": "执行冻结的 skill 名称",
      "const": "solution-package-builder"
    },
    "method_decisions": {
      "type": "object",
      "description": "方法选择决策溯源",
      "additionalProperties": {
        "type": "object",
        "required": ["decision_id", "status", "choice"],
        "properties": {
          "decision_id": {
            "type": "string",
            "description": "对应 decision log 中的 decision_id"
          },
          "status": {
            "type": "string",
            "enum": ["CHOSEN", "BACKUP", "REJECTED"]
          },
          "choice": {
            "type": "string",
            "description": "选定的方法 ID"
          }
        }
      }
    },
    "numbers": {
      "type": "array",
      "description": "所有被冻结的数值条目",
      "items": {
        "type": "object",
        "required": ["id", "value", "unit", "source_file", "source_line", "method", "description"],
        "properties": {
          "id": {
            "type": "string",
            "description": "数值唯一标识，如 q1_rmse_m2, q2_accuracy_best"
          },
          "value": {
            "type": ["number", "string"],
            "description": "冻结的数值（数字或数值字符串如 '95.3%'）"
          },
          "unit": {
            "type": "string",
            "description": "单位，如 %, kg, 无量纲"
          },
          "source_file": {
            "type": "string",
            "description": "数值来源的代码或报告文件路径"
          },
          "source_line": {
            "type": "integer",
            "description": "源文件中的行号（便于溯源）"
          },
          "method": {
            "type": "string",
            "description": "产出该数值的方法名称"
          },
          "description": {
            "type": "string",
            "description": "该数值的含义描述"
          },
          "round": {
            "type": "string",
            "description": "实验轮次，如 round1, round2"
          },
          "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "数值可信度"
          },
          "related_decision_id": {
            "type": "string",
            "description": "关联的决策 ID（如该数值支撑了某个方法选择）"
          }
        }
      }
    }
  }
}
```

### 完整示例

```json
{
  "question_id": "Q1",
  "frozen_at": "2026-06-21T14:30:00+08:00",
  "frozen_by_skill": "solution-package-builder",
  "method_decisions": {
    "q1_primary": {
      "decision_id": "q1_method_choice",
      "status": "CHOSEN",
      "choice": "M2_entropy_topsis"
    }
  },
  "numbers": [
    {
      "id": "q1_rmse_m2",
      "value": 0.0342,
      "unit": "无量纲",
      "source_file": "results/Q1/experiments/round3/metrics.json",
      "source_line": 15,
      "method": "M2_entropy_topsis",
      "description": "TOPSIS 方法的 RMSE 指标",
      "round": "round3",
      "confidence": "high",
      "related_decision_id": "q1_method_choice"
    },
    {
      "id": "q1_ranking_city_1",
      "value": 1,
      "unit": "排名",
      "source_file": "results/Q1/experiments/round3/tables/ranking.csv",
      "source_line": 3,
      "method": "M2_entropy_topsis",
      "description": "城市 1 的综合排名",
      "round": "round3",
      "confidence": "high"
    },
    {
      "id": "q1_sensitivity_alpha_range",
      "value": "0.3-0.5",
      "unit": "无量纲",
      "source_file": "robustness/Q1/q1_robustness_report.md",
      "source_line": 42,
      "method": "sensitivity_analysis",
      "description": "参数 alpha 的稳定区间",
      "confidence": "medium"
    }
  ]
}
```

---

## 2. 解冻-修改-重冻结三步协议（3-Step Protocol）

冻结快照是**按约定不可变的**（immutable by convention）。要修改一个已冻结的数字，必须走以下三步：

### 步骤一：解冻（Unfreeze）

**操作者**：建模手（人类）

**动作**：
1. 在 `results/Qx/reports/freeze_change_log.md` 中追加一条记录
2. 记录格式：

```markdown
## [解冻时间] 解冻记录

- **解冻原因**：[为什么需要修改这个数字]
- **影响数字**：[frozen_numbers.json 中的 id 列表]
- **当前值**：[当前冻结值]
- **预期修改**：[计划如何修改]
- **操作人**：[人类姓名]
```

**约束**：
- 不得跳过此步骤直接修改源文件
- 解冻记录不可删除，只可追加

### 步骤二：修改（Modify）

**操作者**：编程手 / 建模手

**动作**：
1. 修改规范源文件（代码或分析报告）
2. 如需要，重新运行实验
3. 确保修改后的结果已写入 `results/Qx/experiments/roundN/`

**约束**：
- 修改完成后，必须执行 Change-propagation rule P1：
  ```bash
  grep -rn '<changed_identifier>' methods/ code/ results/ paper/ planning/
  ```
- 列出所有引用了被修改数值的文件
- 更新或标记为 STALE

### 步骤三：重冻结（Refreeze）

**操作者**：solution-package-builder skill

**动作**：
1. 重新生成 `results/Qx/reports/frozen_numbers.json`
2. 新的 `frozen_at` 时间戳必须晚于所有源文件的 mtime
3. 在 `freeze_change_log.md` 中追加重冻结记录

```markdown
## [重冻结时间] 重冻结记录

- **新的 frozen_at**：[时间戳]
- **变更的数字**：
  - [id]: [旧值] → [新值]
- **关联的代码变更**：[修改了哪些文件]
- **一致性审计状态**：[待运行 / 已通过]
```

**约束**：
- 不得手工编辑 `frozen_numbers.json`，必须通过 skill 重新生成
- 重冻结后必须运行 `consistency-auditor` 增量检查

---

## 3. 与 consistency-auditor 的集成

### 陈旧检测（Staleness Detection）

`consistency-auditor` 通过文件修改时间（mtime）检测冻结快照是否过期：

```python
import os
import json
from datetime import datetime

def check_freeze_staleness(qx_dir, frozen_numbers_path):
    """
    检查 frozen_numbers.json 是否比源文件更旧。
    如果任何源文件的 mtime 晚于 frozen_at，标记为 STALE。
    """
    with open(frozen_numbers_path, 'r') as f:
        frozen = json.load(frozen(f)

    frozen_at = datetime.fromisoformat(frozen['frozen_at'])
    stale_files = []

    # 检查所有被引用的源文件
    for num in frozen['numbers']:
        source = num['source_file']
        if os.path.exists(source):
            source_mtime = datetime.fromtimestamp(os.path.getmtime(source))
            if source_mtime > frozen_at:
                stale_files.append({
                    'file': source,
                    'mtime': source_mtime.isoformat(),
                    'frozen_at': frozen_at.isoformat(),
                    'number_id': num['id']
                })

    return stale_files
```

### 一致性审计检查项

| 检查项 | 规则 | 严重度 |
|--------|------|--------|
| frozen_numbers.json 存在 | 文件必须存在 | CRITICAL |
| frozen_at 有效性 | 时间戳合法且非未来时间 | CRITICAL |
| 源文件 mtime 比较 | 所有源文件 mtime <= frozen_at | CRITICAL |
| 数值与源文件一致 | frozen value == 源文件中的实际值 | CRITICAL |
| 论文数字一致性 | paper 中的数字与 frozen_numbers 匹配 | HIGH |
| 符号一致性 | symbol_table.md 中的符号与代码一致 | HIGH |
| 文件名一致性 | 论文中引用的文件名实际存在 | MEDIUM |

### STALE 状态处理

当检测到 STALE 状态时：

1. **标记**：在 `results/Qx/reports/freeze_change_log.md` 中记录 STALE 状态
2. **阻断**：该子问题的论文写作暂停，直到重冻结完成
3. **审计**：运行 `consistency-auditor` 增量检查，确认影响范围
4. **通知**：在 `paper_output/qa/workflow_guard_report.md` 中标记为 RED

---

## 4. 使用规则

### 禁止事项

- 禁止手工编辑 `frozen_numbers.json`（必须通过 skill 生成）
- 禁止跳过解冻步骤直接修改源文件
- 禁止在 G4 之前引用 frozen_numbers 中的数值写入论文
- 禁止在重冻结后不运行 consistency-auditor

### 强制事项

- 每个子问题 Qx 必须有独立的 `frozen_numbers.json`
- 冻结时间戳必须晚于所有源文件的 mtime
- 论文中的每个数值断言必须可追溯到 frozen_numbers.json 中的一个 id
- 解冻-修改-重冻结的每一步都必须有 freeze_change_log.md 记录

### 论文写作集成

论文手在写作时：

```markdown
# 正确做法
根据实验结果，TOPSIS 方法的 RMSE 为 0.0342（见 frozen_numbers.json: q1_rmse_m2），
优于基线方法的 0.0521（见 frozen_numbers.json: q1_rmse_baseline）。

# 错误做法（直接引用代码输出）
根据代码运行结果，RMSE 为 0.0342...
```

论文手**只看材料包**（`qx_solution_package_for_writer.md`），不从零散 results 中猜。