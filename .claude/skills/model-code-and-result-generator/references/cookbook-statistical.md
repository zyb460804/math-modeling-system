# 统计分析手册

覆盖：假设检验、方差分析、实验设计与优化、蒙特卡洛模拟、贝叶斯推断、成分数据分析、时间序列分析、灰色关联分析

---

## 统计方法选择速查

| 问题类型 | 推荐方法 |
|---------|---------|
| 两组均值是否有显著差异 | t 检验 / Mann-Whitney U |
| 多组均值比较 | 单因素 ANOVA + Tukey HSD |
| 分类变量独立性 | 卡方检验 |
| 多因素 + 交互效应 | 双因素 ANOVA |
| 因素筛选（因素 > 5） | Plackett-Burman 设计 |
| 因素优化 + 曲面 | RSM 响应曲面法 |
| 小样本、贫信息、不确定性强 | 灰色关联分析 |
| 成分比例数据（和为 1） | 成分数据分析（CLR 变换） |
| 时序预测 | ARIMA / SARIMA / Prophet |
| 参数不确定性传播 | 蒙特卡洛模拟 |
| 先验知识 + 数据更新 | 贝叶斯推断 |

---

## 1. 假设检验

### 核心概念

| 概念 | 含义 |
|------|------|
| 原假设 $H_0$ | 默认立场（无差异、无关联），假定为真 |
| 备择假设 $H_1$ | 与原假设对立的主张 |
| 显著性水平 $\alpha$ | 犯第 I 类错误的概率上限，通常取 0.05 |
| p 值 | 在 $H_0$ 为真时，观察到当前结果（或更极端）的概率 |

**判断规则**：若 $p < \alpha$，拒绝 $H_0$，结果具有统计显著性。

### t 检验

```python
from scipy.stats import ttest_ind, ttest_rel, ttest_1samp

# 独立样本 t 检验
stat, p = ttest_ind(group_a, group_b, equal_var=False)  # Welch

# 配对 t 检验
stat, p = ttest_rel(before, after)
```

### 卡方检验

```python
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(observed_table)
```

### Mann-Whitney U 检验

```python
from scipy.stats import mannwhitneyu
stat, p = mannwhitneyu(group_a, group_b, alternative='two-sided')
```

### 多重比较校正

```python
from statsmodels.stats.multitest import multipletests
reject, p_adj, _, _ = multipletests(raw_p_values, method='bonferroni')
```

---

## 2. 方差分析 (ANOVA)

### 单因素 ANOVA

$$F = \frac{MS_B}{MS_W} = \frac{SS_B / (k-1)}{SS_W / (N-k)} \sim F(k-1, N-k)$$

```python
import pingouin as pg
result = pg.anova(data=df, dv='value', between='group', detailed=True)
```

### 双因素 ANOVA

$$SS_T = SS_A + SS_B + SS_{AB} + SS_E$$

### 前提条件检验

| 条件 | 检验方法 | Python |
|------|---------|--------|
| 正态性 | Shapiro-Wilk | `scipy.stats.shapiro(residuals)` |
| 方差齐性 | Levene | `scipy.stats.levene(*groups)` |

### 事后检验：Tukey HSD

```python
pg.pairwise_tukey(data=df, dv='value', between='group')
```

---

## 3. 实验设计与优化 (DOE/RSM)

### 响应曲面法 (RSM)

$$y = \beta_0 + \sum_{i=1}^{k} \beta_i x_i + \sum_{i=1}^{k} \beta_{ii} x_i^2 + \sum_{i<j} \beta_{ij} x_i x_j + \varepsilon$$

### Plackett-Burman 筛选设计

当备选因素较多（>5）时，先用 PB 设计筛选显著因素，再对显著因素做 RSM 优化。

---

## 4. 蒙特卡洛模拟

### 基本流程

1. 定义输入变量的概率分布
2. 从各分布独立随机抽样 N 次
3. 对每组抽样计算模型输出
4. 统计输出的分布特征

### 方差减小技术

| 技术 | 原理 | 适用场景 |
|------|------|---------|
| 对偶变量 | 成对使用 $U$ 和 $1-U$，负相关抵消方差 | 单调函数 |
| 控制变量 | 引入已知期望的相关变量校正估计 | 存在高相关辅助变量 |
| 重要性抽样 | 在重要区域多抽样，加权修正 | 稀有事件概率 |
| 拉丁超立方 | 分层抽样，每层均匀覆盖 | 多维参数空间探索 |

---

## 5. 贝叶斯推断

### 贝叶斯定理

$$P(\theta \mid D) \propto P(D \mid \theta) \times P(\theta)$$

### 共轭先验速查

| 似然 | 先验 | 后验 |
|------|------|------|
| Binomial | Beta($\alpha, \beta$) | Beta($\alpha + k, \beta + n - k$) |
| Normal(unknown $\mu$, known $\sigma^2$) | Normal($\mu_0, \tau^2$) | Normal（解析形式） |
| Poisson | Gamma($\alpha, \beta$) | Gamma($\alpha + \sum x_i, \beta + n$) |

---

## 6. 成分数据分析

### 对数比变换

| 变换 | 公式 | 特点 |
|------|------|------|
| ALR（加性对数比） | $\text{ALR}(x)_j = \ln(x_j / x_D)$ | 以最后一个成分为参考，非等距 |
| CLR（中心化对数比） | $\text{CLR}(x)_j = \ln(x_j / g(x))$ | 几何均值 $g(x)$ 为参考，等距，共线性 |
| ILR（等距对数比） | 序贯二元划分 | 正交坐标，适用于回归/分类 |

**推荐流程**：原始成分数据 $\xrightarrow{\text{CLR}}$ 变换后数据 $\to$ 聚类/分类/降维。

```python
import numpy as np

def clr_transform(X):
    X_safe = np.where(X <= 0, 1e-16, X)
    g = np.exp(np.mean(np.log(X_safe), axis=1, keepdims=True))
    return np.log(X_safe / g)
```

---

## 7. 时间序列分析

### ARIMA 建模

**建模流程**：平稳性检验 $\to$ 差分（确定 d）$\to$ ACF/PACF 定阶（确定 p, q）$\to$ 参数估计 $\to$ 残差白噪声检验

```python
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(series, order=(p, d, q))
result = model.fit()
forecast = result.forecast(steps=12)
```

### 评估指标

$$MAE = \frac{1}{n}\sum |y_i - \hat{y}_i|, \quad RMSE = \sqrt{\frac{1}{n}\sum (y_i - \hat{y}_i)^2}$$

---

## 8. 灰色关联分析 (GRA)

### 适用场景
- 样本量小（$n < 20$）
- 信息不完全、贫信息

### 关联系数

$$\xi_i(k) = \frac{\min_i \min_k |x_0(k) - x_i(k)| + \rho \cdot \max_i \max_k |x_0(k) - x_i(k)|}{|x_0(k) - x_i(k)| + \rho \cdot \max_i \max_k |x_0(k) - x_i(k)|}$$

其中 $\rho$ 为分辨系数，通常取 0.5。

---

## 9. 通用统计工具速查

| 分析类型 | Python | MATLAB |
|---------|--------|--------|
| t 检验 | `scipy.stats.ttest_ind` / `ttest_rel` | `ttest2` / `ttest` |
| 方差分析 | `statsmodels.formula.api.ols` + `anova_lm` | `anova1` / `anovan` |
| 卡方检验 | `scipy.stats.chi2_contingency` | `crosstab` |
| 正态性检验 | `scipy.stats.shapiro` | `jbtest` / `lillietest` |
| 相关分析 | `scipy.stats.pearsonr` / `spearmanr` | `corr` / `corrcoef` |
| 线性回归 | `statsmodels.api.OLS` / `sklearn.linear_model` | `fitlm` / `regress` |
| ARIMA | `statsmodels.tsa.arima.model.ARIMA` | `arima` / `estimate` |
| 多重比较 | `statsmodels.stats.multitest.multipletests` | `multcompare` |

---

## 常见陷阱与对策

| 陷阱 | 对策 |
|------|------|
| 不做正态性/方差齐性检验就直接 t 检验 | 先做 Shapiro-Wilk + Levene，不过则改用非参数检验 |
| 多次 t 检验代替 ANOVA（I 类错误膨胀） | 用 ANOVA + 事后比较 |
| 成分数据直接用普通聚类 | CLR/ILR 变换后再分析 |
| 时序不检验平稳性直接 ARIMA | 先做 ADF 检验，差分至平稳 |
| p 值不显著就声称"无差异" | 考虑检验功效是否足够（样本量是否过小） |
| 忽略多重比较校正 | 大于 3 组比较时必须用 Bonferroni/Tukey HSD |
