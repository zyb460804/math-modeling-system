---
name: ai-failure-checker
description: "AI失败模式检查：检测AI生成内容中的常见失败模式，防止编造、幻觉、逻辑错误。参考 academic-research-skills 的7-mode blocking checklist。"
---

# AI失败模式检查（AI Failure Checker）

> **版本**: v1.0 | **更新**: 2026-06-21
> **来源**: 参考 Imbad0202/academic-research-skills 的7-mode blocking checklist

---

## 设计理念

AI生成的内容可能存在多种失败模式。本skill提供7种失败模式检查，确保内容质量：
1. 编造检查
2. 幻觉检查
3. 逻辑错误检查
4. 数据一致性检查
5. 引用真实性检查
6. 方法适用性检查
7. 结论合理性检查

---

## 7种失败模式

### 1. 编造检查（Fabrication Check）

**检测内容**:
- 编造的数据
- 编造的实验结果
- 编造的引用
- 编造的方法

**检查方法**:
```python
def check_fabrication(content: str, source_data: dict) -> list:
    """
    检查编造内容

    参数:
        content: 生成的内容
        source_data: 源数据

    返回:
        编造内容列表
    """
    issues = []

    # 提取内容中的数字
    import re
    numbers = re.findall(r'\d+\.?\d*', content)

    # 检查数字是否在源数据中
    for num in numbers:
        if float(num) not in source_data.get("valid_numbers", []):
            issues.append({
                "type": "fabrication",
                "severity": "CRITICAL",
                "description": f"数字 {num} 可能是编造的",
                "suggestion": "验证数字来源"
            })

    return issues
```

### 2. 幻觉检查（Hallucination Check）

**检测内容**:
- 不存在的方法
- 不存在的理论
- 不存在的结论

**检查方法**:
```python
def check_hallucination(content: str, knowledge_base: dict) -> list:
    """
    检查幻觉内容

    参数:
        content: 生成的内容
        knowledge_base: 知识库

    返回:
        幻觉内容列表
    """
    issues = []

    # 检查方法是否存在
    import re
    methods = re.findall(r'使用(.*?)(?:方法|模型|算法)', content)
    for method in methods:
        if method not in knowledge_base.get("valid_methods", []):
            issues.append({
                "type": "hallucination",
                "severity": "CRITICAL",
                "description": f"方法 '{method}' 可能不存在",
                "suggestion": "验证方法是否存在"
            })

    return issues
```

### 3. 逻辑错误检查（Logic Error Check）

**检测内容**:
- 因果关系错误
- 推理过程错误
- 结论与前提矛盾

**检查方法**:
```python
def check_logic_errors(content: str) -> list:
    """
    检查逻辑错误

    参数:
        content: 生成的内容

    返回:
        逻辑错误列表
    """
    issues = []

    # 检查因果关系
    if "因此" in content and "因为" not in content:
        issues.append({
            "type": "logic_error",
            "severity": "HIGH",
            "description": "有结论但缺少原因说明",
            "suggestion": "补充因果关系说明"
        })

    # 检查前后矛盾
    sentences = content.split("。")
    for i in range(len(sentences) - 1):
        if "增加" in sentences[i] and "减少" in sentences[i+1]:
            if sentences[i].split("增加")[0] == sentences[i+1].split("减少")[0]:
                issues.append({
                    "type": "logic_error",
                    "severity": "HIGH",
                    "description": f"可能存在前后矛盾",
                    "suggestion": "检查前后一致性"
                })

    return issues
```

### 4. 数据一致性检查（Data Consistency Check）

**检测内容**:
- 数据前后不一致
- 单位不一致
- 格式不一致

### 5. 引用真实性检查（Citation Authenticity Check）

**检测内容**:
- 引用不存在
- 引用信息错误
- 引用与内容不符

### 6. 方法适用性检查（Method Applicability Check）

**检测内容**:
- 方法不适合问题类型
- 方法假设不满足
- 方法参数不合理

### 7. 结论合理性检查（Conclusion Reasonableness Check）

**检测内容**:
- 结论超出合理范围
- 结论与数据不符
- 结论过于绝对

---

## 完整检查流程

```python
def run_full_check(content: str, source_data: dict, knowledge_base: dict) -> dict:
    """
    运行完整检查

    参数:
        content: 生成的内容
        source_data: 源数据
        knowledge_base: 知识库

    返回:
        检查结果
    """
    all_issues = []

    # 1. 编造检查
    all_issues.extend(check_fabrication(content, source_data))

    # 2. 幻觉检查
    all_issues.extend(check_hallucination(content, knowledge_base))

    # 3. 逻辑错误检查
    all_issues.extend(check_logic_errors(content))

    # 4. 数据一致性检查
    all_issues.extend(check_data_consistency(content, source_data))

    # 5. 引用真实性检查
    all_issues.extend(check_citation_authenticity(content))

    # 6. 方法适用性检查
    all_issues.extend(check_method_applicability(content, knowledge_base))

    # 7. 结论合理性检查
    all_issues.extend(check_conclusion_reasonableness(content, source_data))

    # 统计
    critical_count = sum(1 for i in all_issues if i["severity"] == "CRITICAL")
    high_count = sum(1 for i in all_issues if i["severity"] == "HIGH")
    medium_count = sum(1 for i in all_issues if i["severity"] == "MEDIUM")

    return {
        "total_issues": len(all_issues),
        "critical": critical_count,
        "high": high_count,
        "medium": medium_count,
        "status": "FAIL" if critical_count > 0 else "WARN" if high_count > 0 else "PASS",
        "issues": all_issues
    }
```

---

## 使用方式

```bash
# 运行AI失败模式检查
python .claude/skills/ai-failure-checker/scripts/check_failures.py \
  --paper paper_output/final_paper_source.md \
  --source paper_output/results/ \
  --output paper_output/qa/ai_failure_report.json
```

### 脚本实现范围（诚实说明）

`scripts/check_failures.py` 实现的是 **7 类可离线判定的启发式扫描**，每类输出 PASS/FAIL + 证据行号：

| # | 离线模式 | 对应上方清单 |
|---|---------|-------------|
| 1 | 占位符/TODO 残留 | 编造检查（部分） |
| 2 | 可疑编造标记（"数据来源：略"、示例年份连号等） | 编造检查（部分） |
| 3 | 文内引用断链（[n] 与参考文献不匹配） | 引用真实性检查（部分） |
| 4 | 数字自相矛盾（同一主体+指标多处不同值粗检） | 数据一致性检查（部分） |
| 5 | AI 套话（读取 anti-ai-detection-guide.md 禁用词表匹配） | — |
| 6 | 空洞章节（正文 <100 字的叶子节） | — |
| 7 | 图表引用悬空（引用了无题注/图片定义的图表编号） | — |

以下检查**无法离线判定，由 agent 按本 SKILL 清单人工完成**：幻觉检查（方法是否真实存在）、
引用文献真实性核验（配合 `citation-tracer`）、方法适用性检查、结论合理性检查。
论文数字与代码结果的交叉验证由 `quality-assurance-auditor/scripts/check_number_consistency.py` 负责，
`--source` 参数仅记录证据目录存在性。

可选参数：`--guide`（禁用词表路径，默认 paper-formal-writer 的 anti-ai-detection-guide.md，
解析失败时回退内置词表）、`--banned-threshold 5`（套话超限命中达该数判 FAIL）。
退出码：0=全 PASS，1=有 FAIL，2=执行错误。

---

## 输出格式

```json
{
  "total_issues": 3,
  "critical": 1,
  "high": 1,
  "medium": 1,
  "status": "FAIL",
  "issues": [
    {
      "type": "fabrication",
      "severity": "CRITICAL",
      "description": "数字 0.85 可能是编造的",
      "location": "line 45",
      "suggestion": "验证数字来源"
    },
    {
      "type": "logic_error",
      "severity": "HIGH",
      "description": "有结论但缺少原因说明",
      "location": "line 78",
      "suggestion": "补充因果关系说明"
    },
    {
      "type": "hallucination",
      "severity": "MEDIUM",
      "description": "方法 '模糊神经网络' 可能不存在",
      "location": "line 92",
      "suggestion": "验证方法是否存在"
    }
  ]
}
```

---

## 版本历史

- v1.0.0 (2026-06-21): 初始版本，参考 Imbad0202/academic-research-skills 的7-mode blocking checklist