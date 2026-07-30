# GitHub 数学建模相关项目调研报告（第二轮）

> **调研时间**: 2026-06-21
> **调研目标**: 继续寻找可优化当前系统的 GitHub 项目

---

## 一、高价值数学建模 Skill 项目

### 1. XiaoMaColtAI/math-modeling-skill ⭐338

**URL**: https://github.com/XiaoMaColtAI/math-modeling-skill

**核心价值**: 面向CUMCM/MCM/ICM的数学建模skill，支持Claude Code和Codex

**目录结构**:
```
├── SKILL.md           # 主入口
├── assets/            # 资源文件
├── imgs/              # 图片
├── references/        # 参考资料
│   └── roles/         # 角色定义
└── tools/             # 工具集
    ├── docx/          # Word文档工具
    │   └── scripts/
    ├── paper_search/  # 论文检索工具
    │   └── scripts/
    ├── pdf/           # PDF处理工具
    └── xlsx/          # Excel处理工具
```

**可借鉴的设计**:
- 工具集分离（docx/pdf/xlsx/paper_search）
- 角色定义系统
- 多格式文档处理

---

### 2. HyperCharon/mathematical-modeling ⭐1

**URL**: https://github.com/HyperCharon/mathematical-modeling

**核心价值**: Python数学建模竞赛工具包，包含AHP、TOPSIS、灰色预测、优化、图论等

**特点**:
- 即用型算法脚本
- 覆盖评价、预测、优化、图论等题型

---

### 3. Jackksonns/Mathematical-Modeling-Toolkit ⭐0

**URL**: https://github.com/Jackksonns/Mathematical-Modeling-Toolkit

**核心价值**: 综合性Python数学建模和数据分析工具包

**包含算法**:
- 评价类：AHP/TOPSIS
- 预测类：LSTM/ARIMA
- 优化类：GA/PSO

---

## 二、LaTeX 模板资源

### 4. mohuangrui/ucasthesis ⭐3881

**URL**: https://github.com/mohuangrui/ucasthesis

**核心价值**: 中国科学院大学LaTeX论文模板

**可借鉴**: 论文格式规范、LaTeX最佳实践

### 5. mengchaoheng/SCUT_thesis ⭐557

**URL**: https://github.com/mengchaoheng/SCUT_thesis

**核心价值**: 华南理工大学LaTeX论文模板

### 6. obster-y/XJTU-thesis ⭐413

**URL**: https://github.com/obster-y/XJTU-thesis

**核心价值**: 西安交通大学LaTeX学位论文模板

---

## 三、算法与优化库

### 7. szilard/benchm-ml ⭐1896

**URL**: https://github.com/szilard/benchm-ml

**核心价值**: 机器学习算法基准测试，比较R、Python scikit-learn、H2O、xgboost、Spark MLlib等

**可借鉴**: 算法性能对比方法

### 8. EpistasisLab/scikit-rebate ⭐421

**URL**: https://github.com/EpistasisLab/scikit-rebate

**核心价值**: scikit-learn兼容的Relief特征选择算法实现

**可借鉴**: 特征选择算法集成

### 9. PacktPublishing/Hands-On-Machine-Learning-with-scikit-learn-and-Scientific-Python-Toolkits ⭐151

**URL**: https://github.com/PacktPublishing/Hands-On-Machine-Learning-with-scikit-learn-and-Scientific-Python-Toolkits

**核心价值**: scikit-learn和科学Python工具包实战指南

**可借鉴**: 监督/无监督学习实现最佳实践

---

## 四、特征工程与数据预处理

### 10. FinDii/FeatureEngineering ⭐26

**URL**: https://github.com/FinDii/FeatureEngineering

**核心价值**: 清晰模块化的Python特征工程工具包

**包含功能**:
- 数据预处理
- 数据转换
- 编码
- 缩放
- 特征选择

**可借鉴**: 特征工程标准化流程

---

## 五、学术研究工具

### 11. Imbad0202/academic-research-skills ⭐33215

**URL**: https://github.com/Imbad0202/academic-research-skills

**核心价值**: 学术研究全流程skill套件

**关键模块**:
- `academic-paper` - 论文写作
- `academic-paper-reviewer` - 论文评审
- `academic-pipeline` - 研究管道
- `deep-research` - 深度研究

**可借鉴**:
- 7-mode blocking checklist（AI研究失败模式检查）
- Style Calibration（从用户过往作品学习写作风格）
- Writing Quality Check（检测机器生成痕迹）
- trust-chain frontmatter（引用来源溯源）

---

## 六、可视化库

### 12. Plotly/Plotly ⭐16000+

**特点**: 交互式图表，支持3D曲面、平行坐标、动态时间线

### 13. Bokeh/Bokeh ⭐19000+

**特点**: 交互式可视化，支持大数据集

### 14. mwaskom/seaborn ⭐12000+

**特点**: 统计图表，基于matplotlib，更美观

---

## 七、可引入的优化方向

### 优先级 P0（核心增强）

| 优化方向 | 来源 | 当前状态 | 建议 |
|---------|------|---------|------|
| **工具集分离** | XiaoMaColtAI | 工具混在skill中 | 按功能分离tools目录 |
| **论文检索工具** | XiaoMaColtAI | 无专用工具 | 引入paper_search工具 |
| **特征工程标准化** | FinDii | 无标准流程 | 创建feature-engineering skill |

### 优先级 P1（功能增强）

| 优化方向 | 来源 | 当前状态 | 建议 |
|---------|------|---------|------|
| **LaTeX模板库** | ucasthesis等 | 无专用模板 | 收集常用LaTeX模板 |
| **算法基准测试** | benchm-ml | 无基准测试 | 添加算法性能对比 |
| **交互式图表** | Plotly/Bokeh | 基础matplotlib | 增强交互式图表支持 |

### 优先级 P2（质量增强）

| 优化方向 | 来源 | 当前状态 | 建议 |
|---------|------|---------|------|
| **Style Calibration** | academic-research-skills | 无写作风格学习 | 引入风格校准 |
| **引用溯源** | academic-research-skills | 基础引用检查 | 增强引用真实性验证 |
| **AI失败模式检查** | academic-research-skills | 无此检查 | 引入7-mode checklist |

---

## 八、实施建议

### Phase 1: 工具集优化（1周）

1. 参考XiaoMaColtAI的tools目录结构
2. 分离当前系统中的工具脚本
3. 创建统一的tools入口

### Phase 2: 功能增强（2周）

1. 引入论文检索工具
2. 创建特征工程skill
3. 收集LaTeX模板

### Phase 3: 质量提升（2周）

1. 引入Style Calibration
2. 增强引用溯源
3. 添加AI失败模式检查

---

## 九、总结

**最有价值的3个新发现项目**:

1. **XiaoMaColtAI/math-modeling-skill** ⭐338 - 工具集分离设计，论文检索工具
2. **Imbad0202/academic-research-skills** ⭐33215 - Style Calibration、AI失败模式检查
3. **FinDii/FeatureEngineering** ⭐26 - 特征工程标准化流程

**核心借鉴方向**:
- 工具集按功能分离
- 论文检索工具集成
- 特征工程标准化
- 写作风格校准
- AI失败模式检查

---

**调研完成** 🎉
