# 机理/物理建模手册

覆盖：热传导与扩散、ODE 建模与求解、几何/运动学建模、光学/辐射建模、流体/压力系统、振动/波动系统

---

## 机理建模方法选择速查

| 问题特征 | 推荐方法 | 典型赛题 |
|---------|---------|---------|
| 温度随时间/空间变化 | 热传导 PDE + FDM | 2018A 高温作业服、2020A 回焊炉 |
| 系统状态随时间演化 | ODE 方程组 + solve_ivp | 2019A 高压油管、2022A 波浪能 |
| 运动轨迹/空间布局（无 PDE） | 几何/运动学模型 | 2024A 板凳龙、2021A FAST、2023B 测线 |
| 光能传输/反射/聚焦 | 光学模型 + 光线追迹 | 2023A 定日镜、2021A FAST |
| 流体压力/流量/密度关系 | Bernoulli + PVT + 管道流 | 2019A 高压油管 |
| 振动/波动/能量转换 | 质量-弹簧-阻尼 ODE | 2022A 波浪能 |

---

## 1. 热传导/扩散建模

### 物理背景

热传导问题在数学建模 A 题中反复出现，核心是求解温度场在时间和空间上的分布。

### 控制方程

**一维 Fourier 热传导方程**：

$$\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}$$

其中 $\alpha = \frac{k}{\rho c_p}$ 为热扩散系数（m^2/s）。

### 边界条件

| 类型 | 数学表达 | 物理意义 |
|------|---------|---------|
| Dirichlet（第一类） | $T(0, t) = T_0$ | 边界温度固定 |
| Neumann（第二类） | $-k\frac{\partial T}{\partial x}\big|_{x=0} = q_0$ | 边界热流密度固定 |
| Robin（第三类） | $-k\frac{\partial T}{\partial x}\big|_{x=0} = h(T - T_\infty)$ | 对流换热边界 |

### 有限差分法 (FDM) 离散

**显式格式 (Forward Euler)**：

$$T_i^{n+1} = T_i^n + \frac{\alpha \Delta t}{(\Delta x)^2}(T_{i+1}^n - 2T_i^n + T_{i-1}^n)$$

**CFL 稳定性条件**：$r = \frac{\alpha \Delta t}{(\Delta x)^2} \leq \frac{1}{2}$

**Crank-Nicolson 格式**（推荐）：无条件稳定且二阶精度。

### Python 实现模板

```python
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def solve_heat_1d_cn(L, T_total, Nx, Nt, alpha, T_left, T_right, T_init):
    dx = L / Nx
    dt = T_total / Nt
    r = alpha * dt / (dx * dx)
    x = np.linspace(0, L, Nx + 1)
    T = T_init.copy()
    main_diag = (1 + r) * np.ones(Nx - 1)
    off_diag = (-r / 2) * np.ones(Nx - 2)
    A = diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
    for n in range(Nt):
        b = np.zeros(Nx - 1)
        for i in range(1, Nx):
            idx = i - 1
            b[idx] = T[i] + (r / 2) * (T[i+1] - 2*T[i] + T[i-1])
        b[0] += (r / 2) * T_left
        b[-1] += (r / 2) * T_right
        T_interior = spsolve(A, b)
        T[1:Nx] = T_interior
        T[0], T[-1] = T_left, T_right
    return x, T
```

---

## 2. ODE 建模与求解

### 问题识别

当题目涉及「系统状态随时间的演化速率」时，应当建立 ODE 模型。

### 高阶 ODE 转化

将 $n$ 阶 ODE $y^{(n)} = f(t, y, y', ..., y^{(n-1)})$ 转化为一阶方程组。

### 求解器选择

| 方法 | 精度 | 稳定性 | 适用场景 | Python |
|------|------|--------|---------|--------|
| RK45（Dormand-Prince） | 五阶 (4) | 自适应步长 | **默认首选**，非刚性通用 | `solve_ivp(method='RK45')` |
| BDF（后向差分） | 变阶 | 刚性稳定 | **刚性 ODE 首选** | `solve_ivp(method='BDF')` |
| Radau | 五阶 | 刚性稳定 | 刚性 + 高精度 | `solve_ivp(method='Radau')` |

### Python 模板

```python
from scipy.integrate import solve_ivp
import numpy as np

def ode_system(t, y, params):
    a, b, c = params
    y1, y2, y3 = y
    dy1 = a * y1 - b * y2 * y3
    dy2 = -c * y2 + y1 * y3
    dy3 = b * y2 * y1 - y3
    return [dy1, dy2, dy3]

sol = solve_ivp(ode_system, [t0, tf], y0, args=(params,),
                method='RK45', rtol=1e-6, atol=1e-9)
```

### 参数拟合

```python
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp

def ode_forward(t_eval, *theta):
    sol = solve_ivp(ode_system, [t_eval[0], t_eval[-1]], y0,
                    args=(theta,), t_eval=t_eval, method='RK45',
                    rtol=1e-6, atol=1e-9)
    return sol.y[0]

popt, pcov = curve_fit(ode_forward, t_obs, y_obs, p0=theta0, bounds=(lb, ub))
perr = np.sqrt(np.diag(pcov))
```

---

## 3. 几何/运动学建模

### 曲线运动学

**阿基米德螺线**：$r = a + b\theta$

弧长公式：$s(\theta) = \int_0^\theta \sqrt{(a+bt)^2 + b^2} \, dt$

### 坐标变换：齐次变换矩阵

$$T = \begin{bmatrix} R_{3\times3} & \mathbf{p}_{3\times1} \\ \mathbf{0}_{1\times3} & 1 \end{bmatrix}$$

### 碰撞/干涉检测

二维圆形物体：$(x_i - x_j)^2 + (y_i - y_j)^2 \geq (r_i + r_j)^2$

---

## 4. 光学/辐射建模

### 太阳位置计算（NOAA 算法）

太阳赤纬角：$\delta = 23.45^\circ \times \sin\left(\frac{360^\circ}{365} \times (284 + n)\right)$

太阳高度角：$\sin \alpha_s = \sin \phi \sin \delta + \cos \phi \cos \delta \cos \omega$

### 光学效率链

$$\eta_{\text{opt}} = \eta_{\text{shadow}} \times \eta_{\text{cos}} \times \eta_{\text{ref}} \times \eta_{\text{atten}} \times \eta_{\text{spill}}$$

### 反射定律

镜面法向量：$\mathbf{n} = \frac{\mathbf{s} + \mathbf{t}}{|\mathbf{s} + \mathbf{t}|}$

---

## 5. 流体/压力系统

### Bernoulli 方程

$$P + \frac{1}{2}\rho v^2 + \rho g h = \text{const}$$

### 流量方程

通过小孔的流量：$Q = C_d A \sqrt{\frac{2\Delta P}{\rho}}$

### PVT 关系

理想气体：$PV = nRT$

---

## 6. 振动/波动系统

### 质量-弹簧-阻尼系统

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

无阻尼自振频率：$\omega_n = \sqrt{\frac{k}{m}}$

阻尼比：$\zeta = \frac{c}{2\sqrt{mk}}$

---

## 7. 求解工具速查表

| 问题类型 | Python | MATLAB |
|---------|--------|--------|
| ODE 求解（非刚性） | `scipy.integrate.solve_ivp(method='RK45')` | `ode45` |
| ODE 求解（刚性） | `scipy.integrate.solve_ivp(method='BDF')` | `ode15s` |
| 1D 热传导 PDE | 自定义 FDM / FiPy 库 | `pdepe` |
| 非线性参数拟合 | `scipy.optimize.curve_fit` | `lsqcurvefit` |
| 非线性优化 | `scipy.optimize.minimize` | `fmincon` |
| 全局优化 | `scipy.optimize.differential_evolution` | `ga` / `particleswarm` |
| 数值积分 | `scipy.integrate.quad` / `simpson` | `integral` / `trapz` |
| 太阳位置 | `pvlib.solarposition.get_solarposition` | 自定义 NOAA 公式 |
| 插值 | `scipy.interpolate.interp1d` / `CubicSpline` | `interp1` / `spline` |

---

## 常见陷阱与对策

| 陷阱 | 对策 |
|------|------|
| 显式 FDM 不检查 CFL 条件，结果发散 | 显式方案先算 $r = \alpha \Delta t / (\Delta x)^2$，确保 $r \leq 0.5$ |
| ODE 求解用错方法（刚性用 RK45，求解极慢） | 先试 RK45，步数异常大则切 BDF/Radau |
| 参数拟合陷入局部最优 | 多次从不同初值启动，或先用网格搜索粗找，再用 curve_fit 精化 |
| 高阶 ODE 忘记降阶转化 | $n$ 阶 ODE 转化为 $n$ 个一阶 ODE 再送 solve_ivp |
| 几何模型中角度单位混淆 | 始终统一使用弧度（rad），sin/cos 函数均以 rad 为单位 |
| 忘记方向向量归一化 | 光线追迹中所有方向向量使用前必须归一化 |
| 几何约束遗漏 | 多体系统中检查所有可能碰撞对，用穷举或空间哈希加速 |
| 忽略了多层介质的界面连续性条件 | 多层热传导问题中界面的温度和热流必须连续 |
