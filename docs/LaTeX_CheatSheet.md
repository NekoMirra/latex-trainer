# LaTeX 数学公式 CheatSheet

> 基于 PiPeak LaTeX 训练项目的完整参考表格  
> 包含所有常用的 LaTeX 数学公式"零件"和语法

## 📋 目录

- [基础语法](#基础语法)
- [分数与根号](#分数与根号)
- [希腊字母](#希腊字母)
- [常用符号](#常用符号)
- [函数与三角函数](#函数与三角函数)
- [求和、积分与极限](#求和积分与极限)
- [矩阵与向量](#矩阵与向量)
- [方程组与不等式](#方程组与不等式)
- [集合论与逻辑符号](#集合论与逻辑符号)
- [数论与特殊运算](#数论与特殊运算)
- [高级分析与拓扑](#高级分析与拓扑)

---

## 基础语法

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 行内公式 | `$x^2$` | $x^2$ | 使用单个 $ 包围 |
| 独立公式 | `$$E = mc^2$$` | $$E = mc^2$$ | 使用双 $$ 包围 |
| 上标 | `$x^2$` | $x^2$ | 使用 ^ 符号 |
| 下标 | `$x_1$` | $x_1$ | 使用 _ 符号 |
| 上下标组合 | `$x_1^2$` | $x_1^2$ | 先下标后上标 |
| 复杂上标 | `$x^{2n+1}$` | $x^{2n+1}$ | 多字符用花括号 |
| 复杂下标 | `$x_{max}$` | $x_{max}$ | 多字符用花括号 |

## 分数与根号

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 简单分数 | `$\frac{1}{2}$` | $\frac{1}{2}$ | 基本分数格式 |
| 复杂分数 | `$\frac{a+b}{c-d}$` | $\frac{a+b}{c-d}$ | 分子分母可以是表达式 |
| 嵌套分数 | `$\frac{x^2}{y^3}$` | $\frac{x^2}{y^3}$ | 包含上标的分数 |
| 平方根 | `$\sqrt{x}$` | $\sqrt{x}$ | 基本根号 |
| n次根 | `$\sqrt[3]{x}$` | $\sqrt[3]{x}$ | 指定根次 |
| 复杂根式 | `$\sqrt{x^2 + y^2}$` | $\sqrt{x^2 + y^2}$ | 根号内的表达式 |
| 组合表达式 | `$\frac{(x+y)^2}{2}$` | $\frac{(x+y)^2}{2}$ | 分数与括号组合 |

## 希腊字母

### 小写希腊字母

| 字母 | LaTeX 代码 | 渲染效果 | 中文名 |
|------|------------|----------|--------|
| α | `$\alpha$` | $\alpha$ | 阿尔法 |
| β | `$\beta$` | $\beta$ | 贝塔 |
| γ | `$\gamma$` | $\gamma$ | 伽马 |
| δ | `$\delta$` | $\delta$ | 德尔塔 |
| ε | `$\epsilon$` | $\epsilon$ | 艾普西隆 |
| ζ | `$\zeta$` | $\zeta$ | 泽塔 |
| η | `$\eta$` | $\eta$ | 伊塔 |
| θ | `$\theta$` | $\theta$ | 西塔 |
| ι | `$\iota$` | $\iota$ | 约塔 |
| κ | `$\kappa$` | $\kappa$ | 卡帕 |
| λ | `$\lambda$` | $\lambda$ | 兰姆达 |
| μ | `$\mu$` | $\mu$ | 缪 |
| ν | `$\nu$` | $\nu$ | 纽 |
| ξ | `$\xi$` | $\xi$ | 克西 |
| π | `$\pi$` | $\pi$ | 派 |
| ρ | `$\rho$` | $\rho$ | 柔 |
| σ | `$\sigma$` | $\sigma$ | 西格马 |
| τ | `$\tau$` | $\tau$ | 陶 |
| υ | `$\upsilon$` | $\upsilon$ | 宇普西隆 |
| φ | `$\phi$` | $\phi$ | 斐 |
| χ | `$\chi$` | $\chi$ | 卡 |
| ψ | `$\psi$` | $\psi$ | 普西 |
| ω | `$\omega$` | $\omega$ | 欧米伽 |

### 大写希腊字母

| 字母 | LaTeX 代码 | 渲染效果 | 中文名 |
|------|------------|----------|--------|
| Γ | `$\Gamma$` | $\Gamma$ | 大伽马 |
| Δ | `$\Delta$` | $\Delta$ | 大德尔塔 |
| Θ | `$\Theta$` | $\Theta$ | 大西塔 |
| Λ | `$\Lambda$` | $\Lambda$ | 大兰姆达 |
| Ξ | `$\Xi$` | $\Xi$ | 大克西 |
| Π | `$\Pi$` | $\Pi$ | 大派 |
| Σ | `$\Sigma$` | $\Sigma$ | 大西格马 |
| Υ | `$\Upsilon$` | $\Upsilon$ | 大宇普西隆 |
| Φ | `$\Phi$` | $\Phi$ | 大斐 |
| Ψ | `$\Psi$` | $\Psi$ | 大普西 |
| Ω | `$\Omega$` | $\Omega$ | 大欧米伽 |

## 常用符号

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 无穷 | `$\infty$` | $\infty$ | 极限、积分 |
| 正负 | `$\pm$` | $\pm$ | 误差、解 |
| 负正 | `$\mp$` | $\mp$ | 相反符号 |
| 乘号 | `$\times$` | $\times$ | 乘法运算 |
| 除号 | `$\div$` | $\div$ | 除法运算 |
| 点乘 | `$\cdot$` | $\cdot$ | 数量积 |
| 不等于 | `$\neq$` | $\neq$ | 不等关系 |
| 小于等于 | `$\leq$` | $\leq$ | 不等关系 |
| 大于等于 | `$\geq$` | $\geq$ | 不等关系 |
| 远小于 | `$\ll$` | $\ll$ | 数量级比较 |
| 远大于 | `$\gg$` | $\gg$ | 数量级比较 |
| 约等于 | `$\approx$` | $\approx$ | 近似相等 |
| 恒等于 | `$\equiv$` | $\equiv$ | 恒等关系 |
| 正比于 | `$\propto$` | $\propto$ | 比例关系 |

## 函数与三角函数

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 函数 | `$f(x)$` | $f(x)$ | 基本函数表示 |
| 复合函数 | `$f(g(x))$` | $f(g(x))$ | 函数嵌套 |
| 反函数 | `$f^{-1}(x)$` | $f^{-1}(x)$ | 逆函数 |
| 正弦 | `$\sin x$` | $\sin x$ | 三角函数 |
| 余弦 | `$\cos x$` | $\cos x$ | 三角函数 |
| 正切 | `$\tan x$` | $\tan x$ | 三角函数 |
| 正弦平方 | `$\sin^2 x$` | $\sin^2 x$ | 函数的幂 |
| 反正弦 | `$\arcsin x$` | $\arcsin x$ | 反三角函数 |
| 反余弦 | `$\arccos x$` | $\arccos x$ | 反三角函数 |
| 反正切 | `$\arctan x$` | $\arctan x$ | 反三角函数 |
| 对数 | `$\log x$` | $\log x$ | 常用对数 |
| 自然对数 | `$\ln x$` | $\ln x$ | 自然对数 |
| 指数函数 | `$\exp x$` | $\exp x$ | e的x次方 |
| 双曲正弦 | `$\sinh x$` | $\sinh x$ | 双曲函数 |
| 双曲余弦 | `$\cosh x$` | $\cosh x$ | 双曲函数 |
| 双曲正切 | `$\tanh x$` | $\tanh x$ | 双曲函数 |

## 求和、积分与极限

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 有限求和 | `$\sum_{i=1}^{n} x_i$` | $\sum_{i=1}^{n} x_i$ | 基本求和 |
| 无穷级数 | `$\sum_{k=0}^{\infty} \frac{1}{k!}$` | $\sum_{k=0}^{\infty} \frac{1}{k!}$ | 无穷求和 |
| 连乘 | `$\prod_{i=1}^{n} a_i$` | $\prod_{i=1}^{n} a_i$ | 乘积符号 |
| 不定积分 | `$\int f(x) dx$` | $\int f(x) dx$ | 基本积分 |
| 定积分 | `$\int_0^1 x^2 dx$` | $\int_0^1 x^2 dx$ | 有界积分 |
| 二重积分 | `$\iint f(x,y) dx dy$` | $\iint f(x,y) dx dy$ | 面积分 |
| 三重积分 | `$\iiint f(x,y,z) dx dy dz$` | $\iiint f(x,y,z) dx dy dz$ | 体积分 |
| 环积分 | `$\oint f(x) dx$` | $\oint f(x) dx$ | 闭合路径积分 |
| 极限 | `$\lim_{x \to 0} f(x)$` | $\lim_{x \to 0} f(x)$ | 基本极限 |
| 数列极限 | `$\lim_{n \to \infty} a_n$` | $\lim_{n \to \infty} a_n$ | 无穷极限 |
| 右极限 | `$\lim_{x \to a^+} f(x)$` | $\lim_{x \to a^+} f(x)$ | 单侧极限 |
| 左极限 | `$\lim_{x \to a^-} f(x)$` | $\lim_{x \to a^-} f(x)$ | 单侧极限 |

## 矩阵与向量

### 矩阵类型

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 基础矩阵 | `$\begin{matrix} a & b \\ c & d \end{matrix}$` | $\begin{matrix} a & b \\ c & d \end{matrix}$ | 无边框 |
| 圆括号矩阵 | `$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$` | $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ | 常用矩阵 |
| 方括号矩阵 | `$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$` | $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ | 方括号 |
| 行列式 | `$\begin{vmatrix} a & b \\ c & d \end{vmatrix}$` | $\begin{vmatrix} a & b \\ c & d \end{vmatrix}$ | 竖线边框 |
| 大括号矩阵 | `$\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}$` | $\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}$ | 花括号 |
| 双竖线矩阵 | `$\begin{Vmatrix} a & b \\ c & d \end{Vmatrix}$` | $\begin{Vmatrix} a & b \\ c & d \end{Vmatrix}$ | 双竖线 |

### 特殊矩阵

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 3×3单位矩阵 | `$\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$` | $\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ | 对角线为1 |
| 列向量 | `$\begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}$` | $\begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}$ | 垂直排列 |
| 行向量 | `$\begin{pmatrix} x_1 & x_2 & x_3 \end{pmatrix}$` | $\begin{pmatrix} x_1 & x_2 & x_3 \end{pmatrix}$ | 水平排列 |

### 向量符号

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 向量箭头 | `$\vec{v}$` | $\vec{v}$ | 常用向量表示 |
| 粗体向量 | `$\mathbf{v}$` | $\mathbf{v}$ | 粗体表示 |
| 有向线段 | `$\overrightarrow{AB}$` | $\overrightarrow{AB}$ | 从A到B |
| 单位向量 | `$\hat{i}$` | $\hat{i}$ | 帽子符号 |
| 向量点积 | `$\vec{a} \cdot \vec{b}$` | $\vec{a} \cdot \vec{b}$ | 数量积 |
| 向量叉积 | `$\vec{a} \times \vec{b}$` | $\vec{a} \times \vec{b}$ | 向量积 |
| 向量模长 | `$\|\vec{v}\|$` | $\|\vec{v}\|$ | 向量长度 |

## 方程组与不等式

### 方程组

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 二元方程组 | `$\begin{cases} x + y = 1 \\ x - y = 0 \end{cases}$` | $\begin{cases} x + y = 1 \\ x - y = 0 \end{cases}$ | 基本方程组 |
| 对齐方程组 | `$\begin{aligned} x + y &= 1 \\ 2x - y &= 3 \end{aligned}$` | $\begin{aligned} x + y &= 1 \\ 2x - y &= 3 \end{aligned}$ | 等号对齐 |
| 条件组 | `$\left\{\begin{array}{l} x > 0 \\ y > 0 \end{array}\right.$` | $\left\{\begin{array}{l} x > 0 \\ y > 0 \end{array}\right.$ | 约束条件 |

### 分段函数

| 描述 | LaTeX 代码 | 渲染效果 | 备注 |
|------|------------|----------|------|
| 分段函数 | `$f(x) = \begin{cases} x^2 & \text{if } x \geq 0 \\ -x^2 & \text{if } x < 0 \end{cases}$` | $f(x) = \begin{cases} x^2 & \text{if } x \geq 0 \\ -x^2 & \text{if } x < 0 \end{cases}$ | 条件函数 |

### 不等式符号

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 小于 | `$<$` | $<$ | 基本不等号 |
| 大于 | `$>$` | $>$ | 基本不等号 |
| 小于等于 | `$\leq$` | $\leq$ | 不严格不等 |
| 大于等于 | `$\geq$` | $\geq$ | 不严格不等 |
| 远小于 | `$\ll$` | $\ll$ | 数量级比较 |
| 远大于 | `$\gg$` | $\gg$ | 数量级比较 |
| 连续不等式 | `$0 \leq x \leq 1$` | $0 \leq x \leq 1$ | 范围表示 |

## 集合论与逻辑符号

### 集合符号

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 属于 | `$x \in A$` | $x \in A$ | 元素关系 |
| 不属于 | `$x \notin A$` | $x \notin A$ | 否定关系 |
| 子集 | `$A \subset B$` | $A \subset B$ | 真子集 |
| 子集或等于 | `$A \subseteq B$` | $A \subseteq B$ | 包含关系 |
| 超集 | `$A \supset B$` | $A \supset B$ | 真超集 |
| 超集或等于 | `$A \supseteq B$` | $A \supseteq B$ | 包含关系 |
| 并集 | `$A \cup B$` | $A \cup B$ | 集合并 |
| 交集 | `$A \cap B$` | $A \cap B$ | 集合交 |
| 差集 | `$A \setminus B$` | $A \setminus B$ | 集合差 |
| 空集 | `$\emptyset$` | $\emptyset$ | 空集合 |
| 补集 | `$A^c$` | $A^c$ | 集合补 |

### 数集符号

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 自然数集 | `$\mathbb{N}$` | $\mathbb{N}$ | 自然数 |
| 整数集 | `$\mathbb{Z}$` | $\mathbb{Z}$ | 整数 |
| 有理数集 | `$\mathbb{Q}$` | $\mathbb{Q}$ | 有理数 |
| 实数集 | `$\mathbb{R}$` | $\mathbb{R}$ | 实数 |
| 复数集 | `$\mathbb{C}$` | $\mathbb{C}$ | 复数 |
| 四元数 | `$\mathbb{H}$` | $\mathbb{H}$ | 四元数 |
| n维实空间 | `$\mathbb{R}^n$` | $\mathbb{R}^n$ | 欧几里得空间 |
| n维球面 | `$\mathbb{S}^n$` | $\mathbb{S}^n$ | 球面 |

### 逻辑符号

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 逻辑与 | `$P \land Q$` | $P \land Q$ | 合取 |
| 逻辑或 | `$P \lor Q$` | $P \lor Q$ | 析取 |
| 逻辑非 | `$\neg P$` | $\neg P$ | 否定 |
| 蕴含 | `$P \implies Q$` | $P \implies Q$ | 条件 |
| 当且仅当 | `$P \iff Q$` | $P \iff Q$ | 双条件 |
| 全称量词 | `$\forall x \in \mathbb{R}$` | $\forall x \in \mathbb{R}$ | 对所有 |
| 存在量词 | `$\exists x \in \mathbb{R}$` | $\exists x \in \mathbb{R}$ | 存在 |
| 不存在 | `$\nexists x$` | $\nexists x$ | 不存在 |
| 唯一存在 | `$\exists! x$` | $\exists! x$ | 唯一存在 |

## 数论与特殊运算

### 数论符号

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 整除 | `$a \mid b$` | $a \mid b$ | a整除b |
| 不整除 | `$a \nmid b$` | $a \nmid b$ | a不整除b |
| 同余 | `$a \equiv b \pmod{n}$` | $a \equiv b \pmod{n}$ | 模n同余 |
| 最大公约数 | `$\gcd(a,b)$` | $\gcd(a,b)$ | 最大公因数 |
| 最小公倍数 | `$\lcm(a,b)$` | $\lcm(a,b)$ | 最小公倍数 |
| 互质 | `$a \perp b$` | $a \perp b$ | 互质关系 |
| 欧拉函数 | `$\phi(n)$` | $\phi(n)$ | 欧拉φ函数 |
| 莫比乌斯函数 | `$\mu(n)$` | $\mu(n)$ | 莫比乌斯μ函数 |

### 组合数学

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 阶乘 | `$n!$` | $n!$ | n的阶乘 |
| 双阶乘 | `$n!!$` | $n!!$ | 双阶乘 |
| 二项式系数 | `$\binom{n}{k}$` | $\binom{n}{k}$ | n选k |
| 排列数 | `$P(n,k)$` | $P(n,k)$ | 排列 |
| 组合数 | `$C(n,k)$` | $C(n,k)$ | 组合 |
| 多项式系数 | `$\binom{n}{k_1,k_2,\ldots,k_m}$` | $\binom{n}{k_1,k_2,\ldots,k_m}$ | 多项式系数 |
| 斯特林数 | `$S(n,k)$` | $S(n,k)$ | 第二类斯特林数 |
| 贝尔数 | `$B_n$` | $B_n$ | 贝尔数 |

### 高德纳箭头与超运算

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 指数运算 | `$a \uparrow b = a^b$` | $a \uparrow b = a^b$ | 三级运算 |
| 幂塔 | `$a \uparrow\uparrow b$` | $a \uparrow\uparrow b$ | 四级运算 |
| 五级运算 | `$a \uparrow\uparrow\uparrow b$` | $a \uparrow\uparrow\uparrow b$ | 五级运算 |
| 超幂 | `${}^n a$` | ${}^n a$ | 左上标记法 |
| n级运算 | `$a^{(n)} b$` | $a^{(n)} b$ | 通用记法 |
| 阿克曼函数 | `$\text{Ack}(m,n)$` | $\text{Ack}(m,n)$ | 快速增长函数 |

### 特殊函数

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 伽马函数 | `$\Gamma(n)$` | $\Gamma(n)$ | 阶乘推广 |
| 贝塔函数 | `$B(x,y)$` | $B(x,y)$ | 贝塔函数 |
| 黎曼ζ函数 | `$\zeta(s)$` | $\zeta(s)$ | 黎曼函数 |
| 狄利克雷η函数 | `$\eta(s)$` | $\eta(s)$ | 狄利克雷函数 |
| 雅可比θ函数 | `$\theta(z,\tau)$` | $\theta(z,\tau)$ | 椭圆函数 |

## 高级分析与拓扑

### 微分与积分

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 偏导数 | `$\frac{\partial f}{\partial x}$` | $\frac{\partial f}{\partial x}$ | 偏微分 |
| 二阶偏导 | `$\frac{\partial^2 f}{\partial x^2}$` | $\frac{\partial^2 f}{\partial x^2}$ | 二阶偏导 |
| 混合偏导 | `$\frac{\partial^2 f}{\partial x \partial y}$` | $\frac{\partial^2 f}{\partial x \partial y}$ | 混合偏导 |
| 梯度 | `$\nabla f$` | $\nabla f$ | 梯度算子 |
| 散度 | `$\nabla \cdot \vec{F}$` | $\nabla \cdot \vec{F}$ | 散度 |
| 旋度 | `$\nabla \times \vec{F}$` | $\nabla \times \vec{F}$ | 旋度 |
| 拉普拉斯算子 | `$\Delta f$` | $\Delta f$ | 拉普拉斯算子 |
| 达朗贝尔算子 | `$\Box f$` | $\Box f$ | 波算子 |

### 复分析

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 复积分 | `$\oint_C f(z) dz$` | $\oint_C f(z) dz$ | 复变函数积分 |
| 留数 | `$\text{Res}(f,z_0)$` | $\text{Res}(f,z_0)$ | 留数 |
| 复共轭 | `$\overline{z}$` | $\overline{z}$ | 复数共轭 |
| 实部 | `$\Re(z)$` | $\Re(z)$ | 实部 |
| 虚部 | `$\Im(z)$` | $\Im(z)$ | 虚部 |
| 模长 | `$|z|$` | $|z|$ | 复数模 |
| 幅角 | `$\arg(z)$` | $\arg(z)$ | 复数幅角 |

### 拓扑符号

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 拓扑 | `$\mathcal{T}$` | $\mathcal{T}$ | 拓扑结构 |
| 闭包 | `$\overline{A}$` | $\overline{A}$ | 集合闭包 |
| 内部 | `$A^{\circ}$` | $A^{\circ}$ | 集合内部 |
| 边界 | `$\partial A$` | $\partial A$ | 集合边界 |
| 导集 | `$A'$` | $A'$ | 聚点集 |
| 同胚 | `$X \cong Y$` | $X \cong Y$ | 拓扑等价 |
| 同伦 | `$f \simeq g$` | $f \simeq g$ | 同伦等价 |

### 泛函分析

| 描述 | LaTeX 代码 | 渲染效果 | 含义 |
|------|------------|----------|------|
| 范数 | `$\|x\|$` | $\|x\|$ | 向量范数 |
| 内积 | `$\langle x, y \rangle$` | $\langle x, y \rangle$ | 内积 |
| 算子范数 | `$\|T\|$` | $\|T\|$ | 算子范数 |
| Lp空间 | `$L^p(\Omega)$` | $L^p(\Omega)$ | Lp空间 |
| 无穷可微 | `$C^{\infty}(\mathbb{R})$` | $C^{\infty}(\mathbb{R})$ | 光滑函数 |
| 希尔伯特空间 | `$\mathcal{H}$` | $\mathcal{H}$ | 希尔伯特空间 |
| 巴拿赫空间 | `$\mathcal{B}$` | $\mathcal{B}$ | 巴拿赫空间 |
| 有界算子 | `$\mathcal{B}(X,Y)$` | $\mathcal{B}(X,Y)$ | 有界线性算子 |
| 谱 | `$\sigma(T)$` | $\sigma(T)$ | 算子谱 |
| 谱半径 | `$r(T)$` | $r(T)$ | 谱半径 |

## 特殊符号与装饰

### 装饰符号

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 帽子 | `$\hat{x}$` | $\hat{x}$ | 单位向量、估计值 |
| 波浪线 | `$\tilde{x}$` | $\tilde{x}$ | 近似值 |
| 横线 | `$\overline{x}$` | $\overline{x}$ | 平均值、闭包 |
| 下划线 | `$\underline{x}$` | $\underline{x}$ | 强调 |
| 点 | `$\dot{x}$` | $\dot{x}$ | 时间导数 |
| 双点 | `$\ddot{x}$` | $\ddot{x}$ | 二阶导数 |
| 撇号 | `$x'$` | $x'$ | 导数、导集 |
| 双撇号 | `$x''$` | $x''$ | 二阶导数 |
| 星号 | `$x^*$` | $x^*$ | 共轭、对偶 |
| 匕首 | `$x^\dagger$` | $x^\dagger$ | 厄米共轭 |

### 箭头符号

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 右箭头 | `$\rightarrow$` | $\rightarrow$ | 映射、趋向 |
| 左箭头 | `$\leftarrow$` | $\leftarrow$ | 反向映射 |
| 双向箭头 | `$\leftrightarrow$` | $\leftrightarrow$ | 等价 |
| 长右箭头 | `$\longrightarrow$` | $\longrightarrow$ | 长映射 |
| 双线箭头 | `$\Rightarrow$` | $\Rightarrow$ | 蕴含 |
| 双向双线 | `$\Leftrightarrow$` | $\Leftrightarrow$ | 当且仅当 |
| 上箭头 | `$\uparrow$` | $\uparrow$ | 增长、高德纳箭头 |
| 下箭头 | `$\downarrow$` | $\downarrow$ | 下降 |
| 东北箭头 | `$\nearrow$` | $\nearrow$ | 趋向正无穷 |
| 东南箭头 | `$\searrow$` | $\searrow$ | 趋向负无穷 |

## 常用环境与结构

### 数学环境

| 环境名 | 用途 | 示例 |
|--------|------|------|
| `equation` | 带编号的独立公式 | `\begin{equation} E = mc^2 \end{equation}` |
| `align` | 多行对齐公式 | `\begin{align} x &= 1 \\ y &= 2 \end{align}` |
| `gather` | 多行居中公式 | `\begin{gather} x = 1 \\ y = 2 \end{gather}` |
| `split` | 分割长公式 | `\begin{split} x &= a + b \\ &\quad + c \end{split}` |
| `cases` | 分段函数 | `\begin{cases} x & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}` |
| `array` | 通用数组 | `\begin{array}{cc} a & b \\ c & d \end{array}` |

### 字体样式

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 粗体 | `$\mathbf{x}$` | $\mathbf{x}$ | 向量、矩阵 |
| 斜体 | `$\mathit{text}$` | $\mathit{text}$ | 强调 |
| 罗马体 | `$\mathrm{d}x$` | $\mathrm{d}x$ | 微分符号 |
| 无衬线 | `$\mathsf{text}$` | $\mathsf{text}$ | 特殊标记 |
| 打字机 | `$\mathtt{text}$` | $\mathtt{text}$ | 代码 |
| 花体 | `$\mathcal{L}$` | $\mathcal{L}$ | 拉格朗日、拉普拉斯 |
| 空心 | `$\mathbb{R}$` | $\mathbb{R}$ | 数集 |
| 哥特体 | `$\mathfrak{g}$` | $\mathfrak{g}$ | 李代数 |

## 实用技巧

### 间距控制

| 描述 | LaTeX 代码 | 效果 | 用途 |
|------|------------|------|------|
| 细间距 | `$a\,b$` | $a\,b$ | 微调间距 |
| 中间距 | `$a\:b$` | $a\:b$ | 中等间距 |
| 大间距 | `$a\;b$` | $a\;b$ | 较大间距 |
| 四分之一空格 | `$a\!b$` | $a\!b$ | 负间距 |
| 一个空格 | `$a\ b$` | $a\ b$ | 标准空格 |
| 两个空格 | `$a\quad b$` | $a\quad b$ | 四分之一em |
| 四个空格 | `$a\qquad b$` | $a\qquad b$ | 半个em |

### 大小控制

| 描述 | LaTeX 代码 | 渲染效果 | 用途 |
|------|------------|----------|------|
| 巨大 | `$\Huge{x}$` | $\Huge{x}$ | 标题 |
| 很大 | `$\huge{x}$` | $\huge{x}$ | 强调 |
| 大 | `$\LARGE{x}$` | $\LARGE{x}$ | 重要公式 |
| 较大 | `$\Large{x}$` | $\Large{x}$ | 子标题 |
| 正常 | `$\normalsize{x}$` | $\normalsize{x}$ | 默认大小 |
| 小 | `$\small{x}$` | $\small{x}$ | 注释 |
| 很小 | `$\tiny{x}$` | $\tiny{x}$ | 下标 |

---

## 📚 练习题索引

从 PiPeak 题库中按难度选出的代表性题目：

### 简单 (Easy)
1. x 的平方: `$x^2$`
2. a 下标 1: `$a_1$`
3. 二分之一: `$\frac{1}{2}$`
4. 根号 2: `$\sqrt{2}$`
5. 希腊字母 π: `$\pi$`
6. α + β: `$\alpha + \beta$`
7. sin x: `$\sin x$`
8. f(x) = x²: `$f(x) = x^2$`
9. 向量 v: `$\vec{v}$`
10. x 属于 A: `$x \in A$`
11. A ∪ B: `$A \cup B$`
12. 0 ≤ x ≤ 1: `$0 \leq x \leq 1$`
13. 偏导数 ∂f/∂x: `$\frac{\partial f}{\partial x}$`
14. 梯度 ∇f: `$\nabla f$`
15. 范数 ‖x‖: `$\|x\|$`

### 中等 (Medium)
16. x 下标 n 的平方: `$x_n^2$`
17. (x+y)²/2: `$\frac{(x+y)^2}{2}$`
18. 三次根号下 8: `$\sqrt[3]{8}$`
19. x ≠ ∞: `$x \neq \infty$`
20. Δx ≈ 0: `$\Delta x \approx 0$`
21. sin²θ + cos²θ = 1: `$\sin^2 \theta + \cos^2 \theta = 1$`
22. ln(e^x) = x: `$\ln(e^x) = x$`
23. 求和 ∑: `$\sum_{i=1}^{n}$`
24. 定积分: `$\int_0^1$`
25. 极限: `$\lim_{x \to 0} f(x)$`
26. 向量点积: `$\vec{a} \cdot \vec{b}$`
27. ∀x ∈ ℝ: `$\forall x \in \mathbb{R}$`
28. 同余: `$a \equiv b \pmod{n}$`
29. 二项式系数: `$\binom{n}{k}$`
30. 内积: `$\langle x, y \rangle$`

### 困难 (Hard)
31. 定积分等式: `$\int_0^1 x^2 dx = \frac{1}{3}$`
32. 2×2矩阵: `$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$`
33. 3×3单位矩阵: `$\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$`
34. 二元方程组: `$\begin{cases} x + y = 1 \\ x - y = 0 \end{cases}$`
35. 分段函数: `$f(x) = \begin{cases} x^2 & \text{if } x \geq 0 \\ -x^2 & \text{if } x < 0 \end{cases}$`
36. 集合关系: `$A \subseteq B \implies A \cap B = A$`
37. 高德纳箭头: `$3 \uparrow\uparrow 4$`
38. 互质关系: `$\gcd(a,b) = 1 \implies a \perp b$`

---

## 🎯 使用建议

1. **初学者**: 从基础语法开始，重点掌握上标、下标、分数、根号
2. **进阶用户**: 熟练掌握希腊字母、函数、矩阵等常用结构
3. **高级用户**: 学习复杂的数学环境和特殊符号
4. **实际应用**: 根据具体需求查找相应的符号和语法

## 📖 参考资源

- [PiPeak LaTeX 训练项目](https://github.com/prehisle/pipeak)
- [KaTeX 支持的函数](https://katex.org/docs/supported.html)
- [LaTeX 数学模式](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

---

*本 CheatSheet 基于 PiPeak 项目的18个课程与216个练习题整理而成，涵盖了从基础到高级的所有常用 LaTeX 数学公式语法。*
