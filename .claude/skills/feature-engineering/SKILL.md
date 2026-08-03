---
name: feature-engineering
description: "特征工程标准化流程：数据预处理、数据转换、编码、缩放、特征选择。参考 FinDii/FeatureEngineering 设计。触发词：特征工程、feature engineering、数据预处理、特征选择、特征编码、特征缩放、特征构造。"
---

# 特征工程（Feature Engineering）

> **版本**: v1.0 | **更新**: 2026-06-21
> **来源**: 参考 FinDii/FeatureEngineering 设计

---

## 设计理念

特征工程是数据科学中最重要的环节之一。本skill提供标准化的特征工程流程，包括：
- 数据预处理
- 数据转换
- 编码
- 缩放
- 特征选择

---

## 流程图

```
原始数据
    ↓
数据预处理
    ↓
数据转换
    ↓
编码
    ↓
缩放
    ↓
特征选择
    ↓
特征工程完成
```

---

## 1. 数据预处理

### 1.1 缺失值处理

```python
import pandas as pd
import numpy as np

def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    处理缺失值

    参数:
        df: 输入数据框
        strategy: 填充策略 (mean, median, mode, drop, interpolate)

    返回:
        处理后的数据框
    """
    df_clean = df.copy()

    if strategy == "mean":
        # 数值列用均值填充
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == "median":
        # 数值列用中位数填充
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == "mode":
        # 所有列用众数填充
        for col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    elif strategy == "drop":
        # 删除含有缺失值的行
        df_clean = df_clean.dropna()
    elif strategy == "interpolate":
        # 数值列用插值填充
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].interpolate()

    return df_clean
```

### 1.2 异常值处理

```python
def handle_outliers(df: pd.DataFrame, columns: list, method: str = "iqr") -> pd.DataFrame:
    """
    处理异常值

    参数:
        df: 输入数据框
        columns: 要处理的列
        method: 处理方法 (iqr, zscore, clip)

    返回:
        处理后的数据框
    """
    df_clean = df.copy()

    for col in columns:
        if method == "iqr":
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df_clean[col] = df_clean[col].clip(lower, upper)
        elif method == "zscore":
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            df_clean[col] = df_clean[col].clip(mean - 3*std, mean + 3*std)
        elif method == "clip":
            lower = df_clean[col].quantile(0.01)
            upper = df_clean[col].quantile(0.99)
            df_clean[col] = df_clean[col].clip(lower, upper)

    return df_clean
```

---

## 2. 数据转换

### 2.1 对数转换

```python
def log_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    对数转换

    参数:
        df: 输入数据框
        columns: 要转换的列

    返回:
        转换后的数据框
    """
    df_transformed = df.copy()
    for col in columns:
        df_transformed[col] = np.log1p(df_transformed[col])
    return df_transformed
```

### 2.2 多项式特征

```python
from sklearn.preprocessing import PolynomialFeatures

def create_polynomial_features(df: pd.DataFrame, columns: list, degree: int = 2) -> pd.DataFrame:
    """
    创建多项式特征

    参数:
        df: 输入数据框
        columns: 要转换的列
        degree: 多项式度数

    返回:
        包含多项式特征的数据框
    """
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(df[columns])
    poly_df = pd.DataFrame(poly_features, columns=poly.get_feature_names_out(columns))
    return pd.concat([df, poly_df], axis=1)
```

---

## 3. 编码

### 3.1 标签编码

```python
from sklearn.preprocessing import LabelEncoder

def label_encode(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    标签编码

    参数:
        df: 输入数据框
        columns: 要编码的列

    返回:
        编码后的数据框
    """
    df_encoded = df.copy()
    le = LabelEncoder()
    for col in columns:
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
    return df_encoded
```

### 3.2 独热编码

```python
def onehot_encode(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    独热编码

    参数:
        df: 输入数据框
        columns: 要编码的列

    返回:
        编码后的数据框
    """
    return pd.get_dummies(df, columns=columns, drop_first=True)
```

---

## 4. 缩放

### 4.1 标准化

```python
from sklearn.preprocessing import StandardScaler

def standardize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    标准化 (z-score)

    参数:
        df: 输入数据框
        columns: 要标准化的列

    返回:
        标准化后的数据框
    """
    df_scaled = df.copy()
    scaler = StandardScaler()
    df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
    return df_scaled
```

### 4.2 归一化

```python
from sklearn.preprocessing import MinMaxScaler

def normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    归一化 (0-1)

    参数:
        df: 输入数据框
        columns: 要归一化的列

    返回:
        归一化后的数据框
    """
    df_scaled = df.copy()
    scaler = MinMaxScaler()
    df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
    return df_scaled
```

---

## 5. 特征选择

### 5.1 相关性分析

```python
def correlation_analysis(df: pd.DataFrame, target: str, threshold: float = 0.8) -> list:
    """
    相关性分析

    参数:
        df: 输入数据框
        target: 目标变量
        threshold: 相关性阈值

    返回:
        高相关性特征列表
    """
    corr_matrix = df.corr()
    target_corr = corr_matrix[target].abs().sort_values(ascending=False)
    high_corr_features = target_corr[target_corr > threshold].index.tolist()
    return high_corr_features
```

### 5.2 特征重要性

```python
from sklearn.ensemble import RandomForestRegressor

def feature_importance(df: pd.DataFrame, target: str, n_features: int = 10) -> list:
    """
    特征重要性

    参数:
        df: 输入数据框
        target: 目标变量
        n_features: 选择的特征数量

    返回:
        重要特征列表
    """
    X = df.drop(columns=[target])
    y = df[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    importance = pd.Series(model.feature_importances_, index=X.columns)
    top_features = importance.nlargest(n_features).index.tolist()

    return top_features
```

---

## 完整流程

```python
def full_feature_engineering(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    完整特征工程流程

    参数:
        df: 原始数据框
        target: 目标变量

    返回:
        特征工程后的数据框
    """
    # 1. 处理缺失值
    df = handle_missing_values(df, strategy="mean")

    # 2. 处理异常值
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df = handle_outliers(df, numeric_cols, method="iqr")

    # 3. 编码分类变量
    categorical_cols = df.select_dtypes(include=["object"]).columns
    if len(categorical_cols) > 0:
        df = label_encode(df, categorical_cols)

    # 4. 标准化数值变量
    df = standardize(df, numeric_cols)

    # 5. 特征选择
    top_features = feature_importance(df, target, n_features=10)
    df = df[top_features + [target]]

    return df
```

---

## 使用方式

```bash
# 运行标准预处理（缺失值 -> IQR 异常裁剪(可选) -> 类别编码 -> 缩放）
python .claude/skills/feature-engineering/scripts/preprocess.py \
  --input paper_output/data_cleaned/raw_data.csv \
  --output paper_output/data_cleaned/engineered_data.csv \
  --target target_column \
  --missing median --encode onehot --scale standard --outlier-iqr
```

选项说明：
- `--missing mean|median|drop`（默认 median；数值列填充均值/中位数，类别列填众数，drop 删整行）
- `--encode onehot|label`（默认 onehot，drop_first；label 为整数编码并在报告中记录映射）
- `--scale standard|minmax|none`（默认 none；只缩放原始数值列，不动编码列与目标列）
- `--outlier-iqr`（开关；Q1-1.5IQR ~ Q3+1.5IQR 裁剪）
- `--report xxx.json`（处理报告，默认 `<output>.report.json`，记录每列填充/裁剪/编码明细）
- `--target` 列不参与裁剪/编码/缩放；目标缺失的行直接删除

特征选择（相关性/重要性筛选）见上方参考实现，按赛题需要写进 `paper_output/code/`。

---

## 版本历史

- v1.0.0 (2026-06-21): 初始版本，参考 FinDii/FeatureEngineering 设计

## 新增脚本（v4.3）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/shap_explain.py` | SHAP 模型可解释性：特征重要性条形图 + 蜂群图 + 依赖图 + 单样本 waterfall | "模型可解释性" / "特征重要性" / "SHAP" |

ML 题（C 题预测/分类）必备——评委最看重"为啥这个预测"。`pip install shap`，产出进 `paper_output/figures/shap/`。