# 聚类与分组方法手册

覆盖：K-Means、层次聚类（R型/Q型）、DBSCAN、GMM-EM、聚类数确定、聚类评价

---

## 1. 层次聚类（R 型 + Q 型）

### R 型聚类 vs Q 型聚类

| 类型 | 聚类对象 | 作用 | 典型用法 |
|------|---------|------|---------|
| **R 型聚类** | 变量/特征 | 特征降维、去除冗余变量 | 选出代表性特征后再做 Q 型聚类 |
| **Q 型聚类** | 样本/观测 | 将样本分组 | R 型选出特征变量后对样本聚类 |

### 距离度量选择

| 数据类型 | 推荐距离 |
|---------|---------|
| 连续数值（已标准化）| 欧氏距离 |
| 成分数据（定和为1）| Aitchison 距离（需先 CLR 变换） |
| 高维稀疏数据 | 余弦距离 |
| 混合类型（数值+类别）| Gower 距离 |

### Python 实现

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist

Z = linkage(X_scaled, method='ward')
dendrogram(Z)
labels = fcluster(Z, t=3, criterion='maxclust')
```

---

## 2. K-Means 聚类

### 适用场景
- 样本量大、类别数为已知或可估计
- 簇形状近似球形
- 需要快速计算

### 肘部法则 + 轮廓系数（确定 K）

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

inertias = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, init='k-means++', random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

for k in range(2, 11):
    km = KMeans(n_clusters=k, init='k-means++', random_state=42)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}, silhouette={score:.3f}")
```

### 常见陷阱
- **忘记标准化**：量纲差异大的特征会主导聚类结果
- **K 随意定**：必须用肘部法则+轮廓系数双重验证
- **异常值敏感**：先做异常值检测（IQR/Isolation Forest）

---

## 3. DBSCAN（密度聚类）

### 适用场景
- 簇形状不规则（非球形）
- 数据中有噪声点需要自动识别
- 类别数完全未知

### 关键参数

| 参数 | 含义 | 调参方法 |
|------|------|---------|
| eps | 邻域半径 | K-距离图：对每个点计算到第 k 近邻的距离，排序后找拐点 |
| min_samples | 核心点最少邻居数 | 通常取 2×特征维度 |

```python
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=eps_val, min_samples=2*X.shape[1])
labels = db.fit_predict(X_scaled)
# label=-1 的点为噪声
```

---

## 4. 成分数据预处理（竞赛高频）

### CLR 变换（中心化对数比变换）

$$clr(x) = \left(\ln\frac{x_1}{g(x)}, \ln\frac{x_2}{g(x)}, ..., \ln\frac{x_D}{g(x)}\right)$$

其中 $g(x) = (\prod_{i=1}^D x_i)^{1/D}$ 为几何均值。

```python
def clr_transform(X):
    X = np.array(X, dtype=float)
    X = X / X.sum(axis=1, keepdims=True)
    X = np.clip(X, 1e-10, None)
    gmean = np.exp(np.mean(np.log(X), axis=1, keepdims=True))
    return np.log(X / gmean)
```

**关键**：CLR 变换后可用标准欧氏距离做聚类。论文中必须引用 Aitchison (1986) 的成分数据分析理论。

---

## 5. GMM-EM（高斯混合模型）

### 适用场景
- 数据来自多个高斯分布的混合
- 需要软聚类（每个点属于各类的概率）

```python
from sklearn.mixture import GaussianMixture

bic_scores = []
for k in range(1, 11):
    gmm = GaussianMixture(n_components=k, random_state=42)
    gmm.fit(X_scaled)
    bic_scores.append(gmm.bic(X_scaled))

gmm = GaussianMixture(n_components=best_k, random_state=42)
labels = gmm.fit_predict(X_scaled)
probs = gmm.predict_proba(X_scaled)
```

---

## 6. 聚类结果评价与验证

### 内部评价（无标签时）

| 指标 | 含义 | 越 X 越好 |
|------|------|---------|
| 轮廓系数 (Silhouette) | 簇内紧密度 vs 簇间分离度 | 越大（接近 1） |
| Davies-Bouldin Index | 簇间相似度的均值 | 越小 |
| Calinski-Harabasz | 簇间方差 / 簇内方差 | 越大 |

### 敏感性分析（竞赛必备）

对特征值在 [0.1, 0.2] 范围内随机扰动，重新聚类。若分类结果一致率 > 90%，模型敏感度良好。

---

## 7. 常见陷阱

| 陷阱 | 正确做法 |
|------|---------|
| 成分数据不转换直接聚类 | CLR 变换后聚类 |
| 只用一种方法确定类别数 | 肘部法则 + 轮廓系数 + 业务解释三重验证 |
| 聚类后不分析每类的含义 | 对每个簇做描述统计，给出业务解释 |
| 不检验聚类稳定性 | 扰动输入 ±10%，对比聚类结果一致性 |
| 高维数据直接聚类 | 先做 R 型聚类或 PCA 降维，选关键特征再聚类 |
