#!/usr/bin/env python3
"""
CognitiveSpace — Cross-Language Concept Alignment

Reads merged concept/relation data and aligns concepts across languages
(Chinese, English, German) using:
1. Known translation pairs from ALIAS_GROUPS (merge_extractions.py)
2. Cross-language concept mapping file (config/cross_language_mapping.json)
3. Confidence-based matching for unmatched concepts

Output: data/math_extractions/merged/aligned_data.json

Usage:
    python scripts/math_graph_pipeline/align_languages.py [--input-dir data/math_extractions]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


# ── Known Cross-Language Equivalents ─────────────────────────────────

# Core calculus and math concept equivalences across zh/en/de
# Extended from what's in merge_extractions.py's ALIAS_GROUPS
CROSS_LANG_MAP: list[dict] = [
    # ── Calculus ──
    {"zh": "导数", "en": "Derivative", "de": "Ableitung", "domain": "calculus"},
    {"zh": "极限", "en": "Limit", "de": "Grenzwert", "domain": "calculus"},
    {"zh": "积分", "en": "Integral", "de": "Integral", "domain": "calculus"},
    {"zh": "微分", "en": "Differential", "de": "Differenzial", "domain": "calculus"},
    {"zh": "不定积分", "en": "Antiderivative", "de": "Stammfunktion", "domain": "calculus"},
    {"zh": "定积分", "en": "Definite Integral", "de": "Bestimmtes Integral", "domain": "calculus"},
    {"zh": "连续性", "en": "Continuity", "de": "Stetigkeit", "domain": "calculus"},
    {"zh": "切线", "en": "Tangent", "de": "Tangente", "domain": "calculus"},
    {"zh": "变化率", "en": "Rate of Change", "de": "Änderungsrate", "domain": "calculus"},
    {"zh": "速度", "en": "Velocity", "de": "Geschwindigkeit", "domain": "calculus"},
    {"zh": "函数", "en": "Function", "de": "Funktion", "domain": "calculus"},
    {"zh": "极限定理", "en": "Limit Theorem", "de": "Grenzwertsatz", "domain": "calculus"},
    {"zh": "洛必达法则", "en": "L'Hôpital's Rule", "de": "Regel von L'Hospital", "domain": "calculus"},
    {"zh": "泰勒展开", "en": "Taylor Expansion", "de": "Taylor-Entwicklung", "domain": "calculus"},
    {"zh": "麦克劳林级数", "en": "Maclaurin Series", "de": "Maclaurin-Reihe", "domain": "calculus"},
    {"zh": "幂级数", "en": "Power Series", "de": "Potenzreihe", "domain": "calculus"},
    {"zh": "收敛", "en": "Convergence", "de": "Konvergenz", "domain": "calculus"},
    {"zh": "发散", "en": "Divergence", "de": "Divergenz", "domain": "calculus"},
    {"zh": "偏导数", "en": "Partial Derivative", "de": "Partielle Ableitung", "domain": "calculus"},
    {"zh": "方向导数", "en": "Directional Derivative", "de": "Richtungsableitung", "domain": "calculus"},
    {"zh": "梯度", "en": "Gradient", "de": "Gradient", "domain": "calculus"},
    {"zh": "散度", "en": "Divergence", "de": "Divergenz (Vektor)", "domain": "calculus"},
    {"zh": "旋度", "en": "Curl", "de": "Rotation", "domain": "calculus"},
    {"zh": "拉格朗日乘数", "en": "Lagrange Multiplier", "de": "Lagrange-Multiplikator", "domain": "calculus"},
    {"zh": "微分方程", "en": "Differential Equation", "de": "Differentialgleichung", "domain": "calculus"},
    {"zh": "常微分方程", "en": "Ordinary Differential Equation", "de": "Gewöhnliche DGL", "domain": "calculus"},
    {"zh": "偏微分方程", "en": "Partial Differential Equation", "de": "Partielle DGL", "domain": "calculus"},

    # ── Calculus (new from ch1.2-2.1, ch3, ch5) ──
    {"zh": "复合函数", "en": "Composite Function", "de": "Zusammensetzung", "domain": "calculus"},
    {"zh": "链式法则", "en": "Chain Rule", "de": "Kettenregel", "domain": "calculus"},
    {"zh": "和差法则", "en": "Sum and Difference Rules", "de": "Summenregel", "domain": "calculus"},
    {"zh": "积法则", "en": "Product Rule", "de": "Produktregel", "domain": "calculus"},
    {"zh": "商法则", "en": "Quotient Rule", "de": "Quotientenregel", "domain": "calculus"},
    {"zh": "定积分", "en": "Definite Integral", "de": "Bestimmtes Integral", "domain": "calculus"},
    {"zh": "原函数", "en": "Antiderivative", "de": "Stammfunktion", "domain": "calculus"},
    {"zh": "微积分基本定理", "en": "Fundamental Theorem of Calculus", "de": "Hauptsatz der Analysis", "domain": "calculus"},
    {"zh": "黎曼和", "en": "Riemann Sum", "de": "Riemann-Summe", "domain": "calculus"},
    {"zh": "中间变量", "en": "Intermediate Variable", "de": "Zwischenvariable", "domain": "calculus"},
    {"zh": "外层函数", "en": "Outer Function", "de": "äußere Funktion", "domain": "calculus"},
    {"zh": "内层函数", "en": "Inner Function", "de": "innere Funktion", "domain": "calculus"},

    # ── Calculus (new from ch1.4-1.5, ch3, ch4, ch6) ──
    {"zh": "洛必达法则", "en": "L'Hôpital's Rule", "de": "l'Hospitalsche Regel", "domain": "calculus"},
    {"zh": "未定式", "en": "Indeterminate Form", "de": "Unbestimmte Form", "domain": "calculus"},
    {"zh": "柯西中值定理", "en": "Cauchy Mean Value Theorem", "de": "Cauchyscher Mittelwertsatz", "domain": "calculus"},
    {"zh": "泰勒公式", "en": "Taylor's Formula", "de": "Taylorsatz", "domain": "calculus"},
    {"zh": "泰勒展开", "en": "Taylor Expansion", "de": "Taylor-Entwicklung", "domain": "calculus"},
    {"zh": "麦克劳林公式", "en": "Maclaurin Formula", "de": "Maclaurin-Formel", "domain": "calculus"},
    {"zh": "拉格朗日余项", "en": "Lagrange Remainder", "de": "Lagrange-Restglied", "domain": "calculus"},
    {"zh": "微分方程", "en": "Differential Equation", "de": "Differentialgleichung", "domain": "calculus"},
    {"zh": "常微分方程", "en": "Ordinary Differential Equation", "de": "Gewöhnliche DGL", "domain": "calculus"},
    {"zh": "通解", "en": "General Solution", "de": "Allgemeine Lösung", "domain": "calculus"},
    {"zh": "特解", "en": "Particular Solution", "de": "Partikuläre Lösung", "domain": "calculus"},
    {"zh": "初始条件", "en": "Initial Condition", "de": "Anfangsbedingung", "domain": "calculus"},
    {"zh": "可分离变量方程", "en": "Separable Equation", "de": "Separierbare Gleichung", "domain": "calculus"},

    # ── Calculus (multivariable & series) ──
    {"zh": "积分", "en": "Integral", "de": "Integral", "domain": "calculus"},
    {"zh": "微分", "en": "Differential", "de": "Differential", "domain": "calculus"},
    {"zh": "极限定理", "en": "Limit Theorem", "de": "Grenzwertsatz", "domain": "calculus"},
    {"zh": "幂级数", "en": "Power Series", "de": "Potenzreihe", "domain": "calculus"},
    {"zh": "收敛", "en": "Convergence", "de": "Konvergenz", "domain": "calculus"},
    {"zh": "发散", "en": "Divergence", "de": "Divergenz", "domain": "calculus"},
    {"zh": "偏导数", "en": "Partial Derivative", "de": "Partielle Ableitung", "domain": "calculus"},
    {"zh": "方向导数", "en": "Directional Derivative", "de": "Richtungsableitung", "domain": "calculus"},
    {"zh": "梯度", "en": "Gradient", "de": "Gradient", "domain": "calculus"},
    {"zh": "散度", "en": "Divergence (vector)", "de": "Divergenz (Vektor)", "domain": "calculus"},
    {"zh": "旋度", "en": "Curl", "de": "Rotation", "domain": "calculus"},
    {"zh": "拉格朗日乘数", "en": "Lagrange Multiplier", "de": "Lagrange-Multiplikator", "domain": "calculus"},
    {"zh": "偏微分方程", "en": "Partial Differential Equation", "de": "Partielle DGL", "domain": "calculus"},

    # ── Linear Algebra ──
    {"zh": "矩阵", "en": "Matrix", "de": "Matrix", "domain": "linear_algebra"},
    {"zh": "向量", "en": "Vector", "de": "Vektor", "domain": "linear_algebra"},
    {"zh": "行列式", "en": "Determinant", "de": "Determinante", "domain": "linear_algebra"},
    {"zh": "特征值", "en": "Eigenvalue", "de": "Eigenwert", "domain": "linear_algebra"},
    {"zh": "特征向量", "en": "Eigenvector", "de": "Eigenvektor", "domain": "linear_algebra"},
    {"zh": "线性方程组", "en": "Linear System", "de": "Lineares Gleichungssystem", "domain": "linear_algebra"},
    {"zh": "向量空间", "en": "Vector Space", "de": "Vektorraum", "domain": "linear_algebra"},
    {"zh": "线性变换", "en": "Linear Transformation", "de": "Lineare Abbildung", "domain": "linear_algebra"},
    {"zh": "方阵", "en": "Square Matrix", "de": "Quadratische Matrix", "domain": "linear_algebra"},
    {"zh": "单位矩阵", "en": "Identity Matrix", "de": "Einheitsmatrix", "domain": "linear_algebra"},
    {"zh": "对称矩阵", "en": "Symmetric Matrix", "de": "Symmetrische Matrix", "domain": "linear_algebra"},
    {"zh": "逆矩阵", "en": "Inverse Matrix", "de": "Inverse Matrix", "domain": "linear_algebra"},
    {"zh": "矩阵转置", "en": "Transpose", "de": "Transponierte", "domain": "linear_algebra"},
    {"zh": "矩阵乘法", "en": "Matrix Multiplication", "de": "Matrizenmultiplikation", "domain": "linear_algebra"},
    {"zh": "伴随矩阵", "en": "Adjugate Matrix", "de": "Adjungierte", "domain": "linear_algebra"},
    {"zh": "克莱姆法则", "en": "Cramer's Rule", "de": "Cramersche Regel", "domain": "linear_algebra"},
    {"zh": "线性组合", "en": "Linear Combination", "de": "Lineare Kombination", "domain": "linear_algebra"},
    {"zh": "线性相关", "en": "Linearly Dependent", "de": "Linear Abhängig", "domain": "linear_algebra"},
    {"zh": "线性无关", "en": "Linearly Independent", "de": "Linear Unabhängig", "domain": "linear_algebra"},
    {"zh": "极大线性无关组", "en": "Maximal Independent Set", "de": "Maximal Linear Unabhängige Teilmenge", "domain": "linear_algebra"},
    {"zh": "向量组的秩", "en": "Rank of Vector System", "de": "Rang des Vektorsystems", "domain": "linear_algebra"},
    {"zh": "矩阵的秩", "en": "Rank of Matrix", "de": "Matrixrang", "domain": "linear_algebra"},
    {"zh": "基础解系", "en": "Fundamental Solution System", "de": "Fundamentales Lösungssystem", "domain": "linear_algebra"},
    {"zh": "解空间", "en": "Solution Space", "de": "Lösungsraum", "domain": "linear_algebra"},
    {"zh": "特征方程", "en": "Characteristic Equation", "de": "Charakteristische Gleichung", "domain": "linear_algebra"},
    {"zh": "特征多项式", "en": "Characteristic Polynomial", "de": "Charakteristisches Polynom", "domain": "linear_algebra"},
    {"zh": "矩阵的迹", "en": "Trace", "de": "Spur", "domain": "linear_algebra"},
    {"zh": "对角化", "en": "Diagonalization", "de": "Diagonalisierung", "domain": "linear_algebra"},
    {"zh": "相似矩阵", "en": "Similar Matrices", "de": "Ähnliche Matrizen", "domain": "linear_algebra"},
    {"zh": "二次型", "en": "Quadratic Form", "de": "Quadratische Form", "domain": "linear_algebra"},
    {"zh": "正定矩阵", "en": "Positive Definite Matrix", "de": "Positiv Definite Matrix", "domain": "linear_algebra"},
    {"zh": "正交矩阵", "en": "Orthogonal Matrix", "de": "Orthogonale Matrix", "domain": "linear_algebra"},
    {"zh": "基", "en": "Basis", "de": "Basis", "domain": "linear_algebra"},
    {"zh": "维数", "en": "Dimension", "de": "Dimension", "domain": "linear_algebra"},
    {"zh": "列空间", "en": "Column Space", "de": "Spaltenraum", "domain": "linear_algebra"},
    {"zh": "零空间", "en": "Null Space", "de": "Nullraum", "domain": "linear_algebra"},
    {"zh": "秩", "en": "Rank", "de": "Rang", "domain": "linear_algebra"},
    {"zh": "谱定理", "en": "Spectral Theorem", "de": "Spektralsatz", "domain": "linear_algebra"},
    {"zh": "正交对角化", "en": "Orthogonal Diagonalization", "de": "Orthogonale Diagonalisierung", "domain": "linear_algebra"},

    # ── Probability & Statistics ──
    {"zh": "概率", "en": "Probability", "de": "Wahrscheinlichkeit", "domain": "statistics"},
    {"zh": "条件概率", "en": "Conditional Probability", "de": "Bedingte Wahrscheinlichkeit", "domain": "statistics"},
    {"zh": "贝叶斯公式", "en": "Bayes' Theorem", "de": "Satz von Bayes", "domain": "statistics"},
    {"zh": "随机变量", "en": "Random Variable", "de": "Zufallsgröße", "domain": "statistics"},
    {"zh": "分布函数", "en": "Distribution Function", "de": "Verteilungsfunktion", "domain": "statistics"},
    {"zh": "概率密度函数", "en": "Probability Density Function", "de": "Dichte", "domain": "statistics"},
    {"zh": "二项分布", "en": "Binomial Distribution", "de": "Binomialverteilung", "domain": "statistics"},
    {"zh": "泊松分布", "en": "Poisson Distribution", "de": "Poissonverteilung", "domain": "statistics"},
    {"zh": "正态分布", "en": "Normal Distribution", "de": "Normalverteilung", "domain": "statistics"},
    {"zh": "均匀分布", "en": "Uniform Distribution", "de": "Gleichverteilung", "domain": "statistics"},
    {"zh": "指数分布", "en": "Exponential Distribution", "de": "Exponentialverteilung", "domain": "statistics"},
    {"zh": "联合分布", "en": "Joint Distribution", "de": "Gemeinsame Verteilung", "domain": "statistics"},
    {"zh": "边缘分布", "en": "Marginal Distribution", "de": "Randverteilung", "domain": "statistics"},
    {"zh": "数学期望", "en": "Expectation", "de": "Erwartungswert", "domain": "statistics"},
    {"zh": "方差", "en": "Variance", "de": "Varianz", "domain": "statistics"},
    {"zh": "协方差", "en": "Covariance", "de": "Kovarianz", "domain": "statistics"},
    {"zh": "相关系数", "en": "Correlation Coefficient", "de": "Korrelationskoeffizient", "domain": "statistics"},
    {"zh": "大数定律", "en": "Law of Large Numbers", "de": "Gesetz der großen Zahlen", "domain": "statistics"},
    {"zh": "中心极限定理", "en": "Central Limit Theorem", "de": "Zentraler Grenzwertsatz", "domain": "statistics"},
    {"zh": "统计量", "en": "Statistic", "de": "Statistik", "domain": "statistics"},
    {"zh": "χ²分布", "en": "Chi-squared Distribution", "de": "Chi-Quadrat-Verteilung", "domain": "statistics"},
    {"zh": "t分布", "en": "t-distribution", "de": "t-Verteilung", "domain": "statistics"},
    {"zh": "F分布", "en": "F-distribution", "de": "F-Verteilung", "domain": "statistics"},
    {"zh": "参数估计", "en": "Parameter Estimation", "de": "Parameterschätzung", "domain": "statistics"},
    {"zh": "最大似然估计", "en": "Maximum Likelihood Estimation", "de": "Maximum-Likelihood-Schätzung", "domain": "statistics"},
    {"zh": "置信区间", "en": "Confidence Interval", "de": "Konfidenzintervall", "domain": "statistics"},
    {"zh": "假设检验", "en": "Hypothesis Testing", "de": "Hypothesentest", "domain": "statistics"},
    {"zh": "显著性水平", "en": "Significance Level", "de": "Signifikanzniveau", "domain": "statistics"},
    {"zh": "原假设", "en": "Null Hypothesis", "de": "Nullhypothese", "domain": "statistics"},
    {"zh": "备择假设", "en": "Alternative Hypothesis", "de": "Alternativhypothese", "domain": "statistics"},
    {"zh": "t检验", "en": "t-test", "de": "t-Test", "domain": "statistics"},
    {"zh": "F检验", "en": "F-test", "de": "F-Test", "domain": "statistics"},
    {"zh": "切比雪夫不等式", "en": "Chebyshev's Inequality", "de": "Ungleichung von Tschebyscheff", "domain": "statistics"},

    # ── ODE/PDE (advanced) ──
    {"zh": "高阶线性微分方程", "en": "Higher-order Linear ODE", "de": "Lineare DGL höherer Ordnung", "domain": "calculus"},
    {"zh": "待定系数法", "en": "Method of Undetermined Coefficients", "de": "Methode der unbestimmten Koeffizienten", "domain": "calculus"},
    {"zh": "参数变易法", "en": "Variation of Parameters", "de": "Variation der Konstanten", "domain": "calculus"},
    {"zh": "齐次方程", "en": "Homogeneous Equation", "de": "Homogene Gleichung", "domain": "calculus"},
    {"zh": "非齐次方程", "en": "Nonhomogeneous Equation", "de": "Nicht-homogene Gleichung", "domain": "calculus"},
    {"zh": "微分方程组", "en": "System of ODEs", "de": "Differentialgleichungssystem", "domain": "calculus"},
    {"zh": "矩阵指数", "en": "Matrix Exponential", "de": "Matrixexponential", "domain": "calculus"},
    {"zh": "弹簧振动", "en": "Spring Oscillation", "de": "Feder-Masse-System", "domain": "calculus"},
    {"zh": "简谐运动", "en": "Simple Harmonic Motion", "de": "Harmonische Schwingung", "domain": "calculus"},
    {"zh": "阻尼振动", "en": "Damped Oscillation", "de": "Gedämpfte Schwingung", "domain": "calculus"},
    {"zh": "共振", "en": "Resonance", "de": "Resonanz", "domain": "calculus"},
    {"zh": "逻辑斯蒂模型", "en": "Logistic Model", "de": "Logistisches Modell", "domain": "calculus"},
    {"zh": "SIR 模型", "en": "SIR Model", "de": "SIR-Modell", "domain": "calculus"},
    {"zh": "调和函数", "en": "Harmonic Function", "de": "Harmonische Funktion", "domain": "calculus"},
    {"zh": "达朗贝尔解", "en": "d'Alembert Solution", "de": "d'Alembertsche Lösung", "domain": "calculus"},
    {"zh": "特征值问题", "en": "Eigenvalue Problem", "de": "Eigenwertproblem", "domain": "calculus"},
    {"zh": "傅里叶级数", "en": "Fourier Series", "de": "Fourierreihe", "domain": "calculus"},
    {"zh": "相平面", "en": "Phase Plane", "de": "Phasenebene", "domain": "calculus"},

    # ── Elementary (小学) ──
    {"zh": "自然数", "en": "Natural Numbers", "de": "Natürliche Zahlen", "domain": "elementary"},
    {"zh": "加法", "en": "Addition", "de": "Addition", "domain": "elementary"},
    {"zh": "减法", "en": "Subtraction", "de": "Subtraktion", "domain": "elementary"},
    {"zh": "乘法", "en": "Multiplication", "de": "Multiplikation", "domain": "elementary"},
    {"zh": "除法", "en": "Division", "de": "Division", "domain": "elementary"},
    {"zh": "分数", "en": "Fraction", "de": "Bruch", "domain": "elementary"},
    {"zh": "小数", "en": "Decimal", "de": "Dezimalzahl", "domain": "elementary"},
    {"zh": "百分数", "en": "Percentage", "de": "Prozent", "domain": "elementary"},
    {"zh": "周长", "en": "Perimeter", "de": "Umfang", "domain": "elementary"},
    {"zh": "面积", "en": "Area", "de": "Fläche", "domain": "elementary"},
    {"zh": "体积", "en": "Volume", "de": "Volumen", "domain": "elementary"},
    {"zh": "角", "en": "Angle", "de": "Winkel", "domain": "elementary"},
    {"zh": "直角", "en": "Right Angle", "de": "Rechter Winkel", "domain": "elementary"},
    {"zh": "三角形", "en": "Triangle", "de": "Dreieck", "domain": "elementary"},
    {"zh": "长方形", "en": "Rectangle", "de": "Rechteck", "domain": "elementary"},
    {"zh": "正方形", "en": "Square", "de": "Quadrat", "domain": "elementary"},
    {"zh": "圆", "en": "Circle", "de": "Kreis", "domain": "elementary"},
    {"zh": "长方体", "en": "Cuboid", "de": "Quader", "domain": "elementary"},
    {"zh": "正方体", "en": "Cube", "de": "Würfel", "domain": "elementary"},
    {"zh": "圆柱", "en": "Cylinder", "de": "Zylinder", "domain": "elementary"},
    {"zh": "球", "en": "Sphere", "de": "Kugel", "domain": "elementary"},
    {"zh": "厘米", "en": "Centimeter", "de": "Zentimeter", "domain": "elementary"},
    {"zh": "米", "en": "Meter", "de": "Meter", "domain": "elementary"},
    {"zh": "千克", "en": "Kilogram", "de": "Kilogramm", "domain": "elementary"},
    {"zh": "乘法口诀", "en": "Multiplication Table", "de": "Einmaleins", "domain": "elementary"},

    # ── Middle School (初中) ──
    {"zh": "有理数", "en": "Rational Number", "de": "Rationale Zahl", "domain": "middle"},
    {"zh": "整式", "en": "Algebraic Expression", "de": "Term", "domain": "middle"},
    {"zh": "一元一次方程", "en": "Linear Equation in One Variable", "de": "Lineare Gleichung einer Unbekannten", "domain": "middle"},
    {"zh": "二元一次方程组", "en": "System of Linear Equations", "de": "Lineares Gleichungssystem", "domain": "middle"},
    {"zh": "不等式", "en": "Inequality", "de": "Ungleichung", "domain": "middle"},
    {"zh": "一次函数", "en": "Linear Function", "de": "Lineare Funktion", "domain": "middle"},
    {"zh": "勾股定理", "en": "Pythagorean Theorem", "de": "Pythagoreischer Lehrsatz", "domain": "middle"},
    {"zh": "全等三角形", "en": "Congruent Triangles", "de": "Kongruente Dreiecke", "domain": "middle"},
    {"zh": "相似三角形", "en": "Similar Triangles", "de": "Ähnliche Dreiecke", "domain": "middle"},
    {"zh": "二次函数", "en": "Quadratic Function", "de": "Quadratische Funktion", "domain": "middle"},
    {"zh": "一元二次方程", "en": "Quadratic Equation", "de": "Quadratische Gleichung", "domain": "middle"},
    {"zh": "锐角三角函数", "en": "Trigonometric Functions", "de": "Trigonometrische Funktionen", "domain": "middle"},
    {"zh": "平行四边形", "en": "Parallelogram", "de": "Parallelogramm", "domain": "middle"},
    {"zh": "矩形", "en": "Rectangle", "de": "Rechteck", "domain": "middle"},
    {"zh": "菱形", "en": "Rhombus", "de": "Raute", "domain": "middle"},
    {"zh": "扇形", "en": "Sector", "de": "Kreisabschnitt", "domain": "middle"},
    {"zh": "线性变换的核", "en": "Kernel", "de": "Kern", "domain": "linear_algebra"},
    {"zh": "线性变换的像", "en": "Image", "de": "Bild", "domain": "linear_algebra"},
    {"zh": "线性变换的矩阵表示", "en": "Matrix Representation", "de": "Matrixdarstellung", "domain": "linear_algebra"},
    {"zh": "内积", "en": "Inner Product", "de": "Skalarprodukt", "domain": "linear_algebra"},
    {"zh": "内积空间", "en": "Inner Product Space", "de": "Skalarprodukttraum", "domain": "linear_algebra"},
    {"zh": "范数", "en": "Norm", "de": "Norm", "domain": "linear_algebra"},
    {"zh": "正交", "en": "Orthogonal", "de": "Orthogonal", "domain": "linear_algebra"},
    {"zh": "标准正交基", "en": "Orthonormal Basis", "de": "Orthonormale Basis", "domain": "linear_algebra"},
    {"zh": "Gram-Schmidt 正交化", "en": "Gram-Schmidt Process", "de": "Gram-Schmidt-Verfahren", "domain": "linear_algebra"},
    {"zh": "正交投影", "en": "Orthogonal Projection", "de": "Orthogonale Projektion", "domain": "linear_algebra"},
    {"zh": "最小二乘法", "en": "Least Squares", "de": "Least Squares", "domain": "linear_algebra"},
    {"zh": "Jordan 块", "en": "Jordan Block", "de": "Jordan-Block", "domain": "linear_algebra"},
    {"zh": "Jordan 标准形", "en": "Jordan Normal Form", "de": "Jordan-Normalform", "domain": "linear_algebra"},
    {"zh": "最小多项式", "en": "Minimal Polynomial", "de": "Minimalpolynom", "domain": "linear_algebra"},
    {"zh": "Cayley-Hamilton 定理", "en": "Cayley-Hamilton Theorem", "de": "Satz von Cayley-Hamilton", "domain": "linear_algebra"},

    # ── Geometry ──
    {"zh": "三角形", "en": "Triangle", "de": "Dreieck", "domain": "geometry"},
    {"zh": "圆", "en": "Circle", "de": "Kreis", "domain": "geometry"},
    {"zh": "椭圆", "en": "Ellipse", "de": "Ellipse", "domain": "geometry"},
    {"zh": "双曲线", "en": "Hyperbola", "de": "Hyperbel", "domain": "geometry"},
    {"zh": "抛物线", "en": "Parabola", "de": "Parabel", "domain": "geometry"},
    {"zh": "面积", "en": "Area", "de": "Fläche", "domain": "geometry"},
    {"zh": "体积", "en": "Volume", "de": "Volumen", "domain": "geometry"},
    {"zh": "坐标系", "en": "Coordinate System", "de": "Koordinatensystem", "domain": "geometry"},
]


def load_merged_data(input_dir: Path) -> tuple[list[dict], list[dict]]:
    """Load merged concepts and relations."""
    concepts_file = input_dir / "merged_concepts.json"
    relations_file = input_dir / "merged_relations.json"

    if not concepts_file.exists():
        print(f"ERROR: Run merge_extractions.py first — {concepts_file} not found")
        sys.exit(1)

    with open(concepts_file, encoding="utf-8") as f:
        concepts_data = json.load(f)

    relations_data = {"relations": []}
    if relations_file.exists():
        with open(relations_file, encoding="utf-8") as f:
            relations_data = json.load(f)

    return concepts_data.get("concepts", []), relations_data.get("relations", [])


def build_name_index(concepts: list[dict]) -> dict[str, dict]:
    """Build a flat index: name → concept entry (for matching)."""
    index = {}
    for c in concepts:
        index[c["canonical_name"]] = c
        index[c["name_original"]] = c
        for alias in c.get("aliases", []):
            index[alias] = c
    return index


def align_concepts(concepts: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Group concepts by cross-language equivalence.

    Returns:
        (aligned_groups, unmatched_concepts)
    """
    name_index = build_name_index(concepts)
    matched_ids: set[int] = set()
    aligned_groups: list[dict] = []
    unmatched: list[dict] = []

    for entry in CROSS_LANG_MAP:
        zh_name = entry["zh"]
        en_name = entry["en"]
        de_name = entry["de"]
        domain = entry["domain"]

        # Find concepts matching each language name
        zh_conc = name_index.get(zh_name)
        en_conc = name_index.get(en_name)
        de_conc = name_index.get(de_name)

        # Determine canonical ID
        display_name = zh_name
        for c in [zh_conc, en_conc, de_conc]:
            if c:
                display_name = c["canonical_name"]
                break

        group = {
            "id": f"math_{domain}_{zh_name}",
            "display_name": display_name,
            "domain": domain,
            "labels": {},
            "sources": [],
            "cross_references": [],
        }

        concepts_to_index = []
        for lang_code, conc in [("zh", zh_conc), ("en", en_conc), ("de", de_conc)]:
            if conc:
                idx = concepts.index(conc)
                matched_ids.add(idx)
                group["labels"][lang_code] = conc["canonical_name"]
                group["sources"].append(conc.get("source", {}))
                for ref in conc.get("source", {}).get("cross_references", []):
                    if ref not in group["cross_references"]:
                        group["cross_references"].append(ref)
                concepts_to_index.append(conc)
            else:
                # Language not yet extracted — use the known label as placeholder
                subj = zh_name if lang_code == "zh" else en_name if lang_code == "en" else de_name
                group["labels"][lang_code] = subj

        aligned_groups.append(group)

    # Collect unmatched concepts
    for i, c in enumerate(concepts):
        if i not in matched_ids:
            unmatched.append(c)

    return aligned_groups, unmatched


def align_relations(relations: list[dict], aligned_groups: list[dict],
                     all_concepts: list[dict] | None = None) -> list[dict]:
    """Map relation source/target names to aligned group IDs where possible."""
    # Build name-to-group-id map
    name_to_group: dict[str, str] = {}
    for g in aligned_groups:
        for lang_code, label in g["labels"].items():
            name_to_group[label] = g["id"]
        if all_concepts:
            for c_data in all_concepts:
                if c_data["canonical_name"] in g["labels"].values():
                    for alias in c_data.get("aliases", []):
                        name_to_group[alias] = g["id"]

    aligned_rels = []
    for r in relations:
        new_r = dict(r)
        new_r["source_group"] = name_to_group.get(r["source"])
        new_r["target_group"] = name_to_group.get(r["target"])
        aligned_rels.append(new_r)

    return aligned_rels


# ── Main ─────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Align concepts across languages")
    parser.add_argument("--input-dir", type=str, default="data/math_extractions")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    merged_dir = (project_root / args.input_dir).resolve() / "merged"

    print(f"Input: {merged_dir}/\n")

    # Load
    global concepts, relations
    concepts, relations = load_merged_data(merged_dir)
    print(f"Loaded {len(concepts)} concepts, {len(relations)} relations")

    # Align
    aligned_groups, unmatched = align_concepts(concepts)
    print(f"Aligned groups: {len(aligned_groups)}")
    print(f"Unmatched concepts: {len(unmatched)}")

    aligned_relations = align_relations(relations, aligned_groups, concepts)
    print(f"Relations (with group IDs): {len(aligned_relations)}")

    # Write
    output = {
        "version": "2.0",
        "aligned_at": __import__('datetime').datetime.now().isoformat(),
        "total_aligned_groups": len(aligned_groups),
        "total_unmatched_concepts": len(unmatched),
        "total_relations": len(aligned_relations),
        "aligned_groups": aligned_groups,
        "unmatched_concepts": unmatched,
        "relations": aligned_relations,
    }

    output_path = merged_dir / "aligned_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nAligned data written to {output_path}")

    # Summary (avoid printing non-ASCII in Windows terminals)
    print(f"\n── Alignment Summary ({len(aligned_groups)} groups) ──")
    domain_counts = {}
    for g in aligned_groups:
        d = g.get("domain", "general")
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for d, c in sorted(domain_counts.items()):
        print(f"  {d}: {c} groups")
    if unmatched:
        print(f"\nUnmatched ({len(unmatched)} concepts — see aligned_data.json for details)")


if __name__ == "__main__":
    main()
