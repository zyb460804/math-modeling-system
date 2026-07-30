# 网络科学与运筹优化 Playbook（MCM D 题）

## 匹配条件
- 特征词：network flow、dynamic network、time-expanded graph、water level regulation、dam scheduling、stakeholder optimization、multi-objective、NSGA-II、linear programming、transportation network、congestion、queueing theory、traffic optimization、graph theory、accessibility、betweenness centrality
- 比赛类型：美赛 MCM/ICM
- 题目类型：D 题（网络科学 / 运筹学）
- 数学本质：动态网络流建模 + 多目标优化 + 利益相关者效用函数

## 典型题目索引
- 2025 MCM D：Baltimore 交通网络重建
- 2024 MCM D：Great Lakes 水位调控

## 解题示例（一种可行路径）

### Step 1：将物理/工程系统抽象为网络模型
将湖泊、城市、交通节点抽象为有向图 $G = (V, E)$，边权表示流量或通行时间。

**时滞互相关法确定 lag**：对各湖水位时间序列做 time-lagged cross-correlation，取相关性最大处的 lag 值。

### Step 2：建立动态网络流模型（时间展开图）
用 Ford-Fulkerson 时间展开法将动态流转化为静态流。

### Step 3：定义利益相关者效用函数
枚举所有利益相关者，为每个构建 utility function。

### Step 4：建立多目标优化模型

**LP 路径**：
- 决策变量：每个时间步的放水量
- 目标：minimize 水位偏差 + 流速偏差

**NSGA-II 路径**：
- 决策变量：水位 H 和水流 Q
- 多目标：最大化各利益相关者收益函数

### Step 5：气象/物理因素精细化修正
- 规则曲线（Rule Curves）
- 风合成模型
- 冰堵与融雪

### Step 6：利益相关者权重自适应与结果验证

## 关键陷阱
1. 忽略时滞导致模型失实
2. 利益相关者权重分配不当
3. 只建单一时间尺度模型
4. 线性回归的参数检查不足
5. 低估气象因素对网络容量的影响
