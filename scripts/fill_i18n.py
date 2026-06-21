"""
Fill missing i18n labels for CognitiveSpace knowledge graph.

Strategy:
1. Read existing data from data.js
2. For each node, check missing EN/DE labels
3. Fill using comprehensive math translation dictionary
4. If translation not in dictionary, leave empty (better than wrong)
5. Write updated data back

Run: python scripts/fill_i18n.py
"""

import json, re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

# ── Comprehensive ZH↔EN↔DE math dictionary ──────────────────────────
# Format: { "chinese_term": {"en": "english", "de": "german"} }
ZH_DICT = {
    # Elementary (小学)
    "自然数": {"en": "Natural Number", "de": "Natürliche Zahl"},
    "整数": {"en": "Integer", "de": "Ganze Zahl"},
    "加法": {"en": "Addition", "de": "Addition"},
    "减法": {"en": "Subtraction", "de": "Subtraktion"},
    "乘法": {"en": "Multiplication", "de": "Multiplikation"},
    "除法": {"en": "Division", "de": "Division"},
    "分数": {"en": "Fraction", "de": "Bruch"},
    "小数": {"en": "Decimal", "de": "Dezimalzahl"},
    "百分数": {"en": "Percentage", "de": "Prozent"},
    "周长": {"en": "Perimeter", "de": "Umfang"},
    "面积": {"en": "Area", "de": "Fläche"},
    "体积": {"en": "Volume", "de": "Volumen"},
    "图形": {"en": "Shape", "de": "Form"},
    "三角形": {"en": "Triangle", "de": "Dreieck"},
    "长方形": {"en": "Rectangle", "de": "Rechteck"},
    "正方形": {"en": "Square", "de": "Quadrat"},
    "圆": {"en": "Circle", "de": "Kreis"},
    "数轴": {"en": "Number Line", "de": "Zahlenstrahl"},
    "平均数": {"en": "Average", "de": "Durchschnitt"},
    "单位": {"en": "Unit", "de": "Einheit"},
    "近似": {"en": "Approximation", "de": "Näherung"},
    "对称": {"en": "Symmetry", "de": "Symmetrie"},
    "估算": {"en": "Estimation", "de": "Schätzung"},

    # Middle (初中)
    "有理数": {"en": "Rational Number", "de": "Rationale Zahl"},
    "实数": {"en": "Real Number", "de": "Reelle Zahl"},
    "整式": {"en": "Polynomial", "de": "Polynom"},
    "方程": {"en": "Equation", "de": "Gleichung"},
    "不等式": {"en": "Inequality", "de": "Ungleichung"},
    "函数": {"en": "Function", "de": "Funktion"},
    "一次函数": {"en": "Linear Function", "de": "Lineare Funktion"},
    "二次函数": {"en": "Quadratic Function", "de": "Quadratische Funktion"},
    "反比例函数": {"en": "Inverse Function", "de": "Umkehrfunktion"},
    "集合": {"en": "Set", "de": "Menge"},
    "数列": {"en": "Sequence", "de": "Folge"},
    "几何": {"en": "Geometry", "de": "Geometrie"},
    "代数": {"en": "Algebra", "de": "Algebra"},
    "四边形": {"en": "Quadrilateral", "de": "Viereck"},
    "平行四边形": {"en": "Parallelogram", "de": "Parallelogramm"},
    "勾股定理": {"en": "Pythagorean Theorem", "de": "Satz des Pythagoras"},
    "相似": {"en": "Similarity", "de": "Ähnlichkeit"},
    "全等": {"en": "Congruence", "de": "Kongruenz"},
    "三角函数": {"en": "Trigonometry", "de": "Trigonometrie"},
    "正弦": {"en": "Sine", "de": "Sinus"},
    "余弦": {"en": "Cosine", "de": "Kosinus"},
    "正切": {"en": "Tangent", "de": "Tangens"},
    "概率": {"en": "Probability", "de": "Wahrscheinlichkeit"},
    "统计": {"en": "Statistics", "de": "Statistik"},
    "向量": {"en": "Vector", "de": "Vektor"},
    "坐标系": {"en": "Coordinate System", "de": "Koordinatensystem"},
    "命题": {"en": "Proposition", "de": "Aussage"},
    "定理": {"en": "Theorem", "de": "Satz"},
    "证明": {"en": "Proof", "de": "Beweis"},

    # High (高中)
    "导数": {"en": "Derivative", "de": "Ableitung"},
    "极限": {"en": "Limit", "de": "Grenzwert"},
    "积分": {"en": "Integral", "de": "Integral"},
    "微分": {"en": "Differential", "de": "Differential"},
    "不定积分": {"en": "Indefinite Integral", "de": "Unbestimmtes Integral"},
    "定积分": {"en": "Definite Integral", "de": "Bestimmtes Integral"},
    "指数": {"en": "Exponent", "de": "Exponent"},
    "指数函数": {"en": "Exponential Function", "de": "Exponentialfunktion"},
    "对数": {"en": "Logarithm", "de": "Logarithmus"},
    "对数函数": {"en": "Logarithmic Function", "de": "Logarithmusfunktion"},
    "幂函数": {"en": "Power Function", "de": "Potenzfunktion"},
    "圆锥曲线": {"en": "Conic Section", "de": "Kegelschnitt"},
    "椭圆": {"en": "Ellipse", "de": "Ellipse"},
    "双曲线": {"en": "Hyperbola", "de": "Hyperbel"},
    "抛物线": {"en": "Parabola", "de": "Parabel"},
    "排列": {"en": "Permutation", "de": "Permutation"},
    "组合": {"en": "Combination", "de": "Kombination"},
    "二项式": {"en": "Binomial", "de": "Binom"},
    "复数": {"en": "Complex Number", "de": "Komplexe Zahl"},
    "矩阵": {"en": "Matrix", "de": "Matrix"},
    "行列式": {"en": "Determinant", "de": "Determinante"},
    "级数": {"en": "Series", "de": "Reihe"},
    "等差数列": {"en": "Arithmetic Sequence", "de": "Arithmetische Folge"},
    "等比数列": {"en": "Geometric Sequence", "de": "Geometrische Folge"},
    "数学归纳法": {"en": "Mathematical Induction", "de": "Vollständige Induktion"},
    "参数方程": {"en": "Parametric Equation", "de": "Parametergleichung"},
    "极坐标": {"en": "Polar Coordinates", "de": "Polarkoordinaten"},

    # College (大学)
    "微分方程": {"en": "Differential Equation", "de": "Differentialgleichung"},
    "偏微分方程": {"en": "Partial Differential Equation", "de": "Partielle Differentialgleichung"},
    "常微分方程": {"en": "Ordinary Differential Equation", "de": "Gewöhnliche Differentialgleichung"},
    "傅里叶": {"en": "Fourier", "de": "Fourier"},
    "傅里叶变换": {"en": "Fourier Transform", "de": "Fourier-Transformation"},
    "拉普拉斯": {"en": "Laplace", "de": "Laplace"},
    "拉普拉斯变换": {"en": "Laplace Transform", "de": "Laplace-Transformation"},
    "特征值": {"en": "Eigenvalue", "de": "Eigenwert"},
    "特征向量": {"en": "Eigenvector", "de": "Eigenvektor"},
    "线性空间": {"en": "Vector Space", "de": "Vektorraum"},
    "线性变换": {"en": "Linear Transformation", "de": "Lineare Abbildung"},
    "正交": {"en": "Orthogonal", "de": "Orthogonal"},
    "内积": {"en": "Inner Product", "de": "Inneres Produkt"},
    "范数": {"en": "Norm", "de": "Norm"},
    "极限理论": {"en": "Limit Theory", "de": "Grenzwerttheorie"},
    "中值定理": {"en": "Mean Value Theorem", "de": "Mittelwertsatz"},
    "泰勒公式": {"en": "Taylor Series", "de": "Taylor-Reihe"},
    "多元函数": {"en": "Multivariable Function", "de": "Mehrdimensionale Funktion"},
    "重积分": {"en": "Multiple Integral", "de": "Mehrfachintegral"},
    "曲线积分": {"en": "Line Integral", "de": "Kurvenintegral"},
    "曲面积分": {"en": "Surface Integral", "de": "Oberflächenintegral"},
    "梯度": {"en": "Gradient", "de": "Gradient"},
    "散度": {"en": "Divergence", "de": "Divergenz"},
    "旋度": {"en": "Curl", "de": "Rotation"},
    "线性代数": {"en": "Linear Algebra", "de": "Lineare Algebra"},
    "概率论": {"en": "Probability Theory", "de": "Wahrscheinlichkeitstheorie"},
    "数理统计": {"en": "Mathematical Statistics", "de": "Mathematische Statistik"},
    "随机变量": {"en": "Random Variable", "de": "Zufallsvariable"},
    "分布": {"en": "Distribution", "de": "Verteilung"},
    "期望": {"en": "Expected Value", "de": "Erwartungswert"},
    "方差": {"en": "Variance", "de": "Varianz"},
    "标准差": {"en": "Standard Deviation", "de": "Standardabweichung"},
    "中心极限定理": {"en": "Central Limit Theorem", "de": "Zentraler Grenzwertsatz"},
    "假设检验": {"en": "Hypothesis Testing", "de": "Hypothesentest"},
    "置信区间": {"en": "Confidence Interval", "de": "Konfidenzintervall"},
    "回归分析": {"en": "Regression Analysis", "de": "Regressionsanalyse"},
    "数值分析": {"en": "Numerical Analysis", "de": "Numerische Analysis"},
    "优化": {"en": "Optimization", "de": "Optimierung"},
    "凸优化": {"en": "Convex Optimization", "de": "Konvexe Optimierung"},
    "图论": {"en": "Graph Theory", "de": "Graphentheorie"},
    "拓扑": {"en": "Topology", "de": "Topologie"},
    "流形": {"en": "Manifold", "de": "Mannigfaltigkeit"},
    "李群": {"en": "Lie Group", "de": "Lie-Gruppe"},
    "泛函分析": {"en": "Functional Analysis", "de": "Funktionalanalysis"},
    "变分法": {"en": "Calculus of Variations", "de": "Variationsrechnung"},
    "复变函数": {"en": "Complex Analysis", "de": "Komplexe Analysis"},
    "实变函数": {"en": "Real Analysis", "de": "Reelle Analysis"},
    "测度论": {"en": "Measure Theory", "de": "Maßtheorie"},
    "微分几何": {"en": "Differential Geometry", "de": "Differentialgeometrie"},
    "代数拓扑": {"en": "Algebraic Topology", "de": "Algebraische Topologie"},
    "抽象代数": {"en": "Abstract Algebra", "de": "Abstrakte Algebra"},
    "群论": {"en": "Group Theory", "de": "Gruppentheorie"},
    "环论": {"en": "Ring Theory", "de": "Ringtheorie"},
    "域论": {"en": "Field Theory", "de": "Körpertheorie"},
    "数论": {"en": "Number Theory", "de": "Zahlentheorie"},
    "组合数学": {"en": "Combinatorics", "de": "Kombinatorik"},
    "混沌理论": {"en": "Chaos Theory", "de": "Chaostheorie"},
    "动力系统": {"en": "Dynamical System", "de": "Dynamisches System"},
    "控制理论": {"en": "Control Theory", "de": "Kontrolltheorie"},
    "信息论": {"en": "Information Theory", "de": "Informationstheorie"},
    "博弈论": {"en": "Game Theory", "de": "Spieltheorie"},
    "模糊逻辑": {"en": "Fuzzy Logic", "de": "Fuzzy-Logik"},
    "离散数学": {"en": "Discrete Mathematics", "de": "Diskrete Mathematik"},
    "线性规划": {"en": "Linear Programming", "de": "Lineare Optimierung"},
    "整数规划": {"en": "Integer Programming", "de": "Ganzzahlige Optimierung"},

    # Additional terms from data gaps
    "相反数": {"en": "Opposite Number", "de": "Gegenzahl"},
    "绝对值": {"en": "Absolute Value", "de": "Absolutbetrag"},
    "平方根": {"en": "Square Root", "de": "Quadratwurzel"},
    "立方根": {"en": "Cube Root", "de": "Kubikwurzel"},
    "因式分解": {"en": "Factorization", "de": "Faktorisierung"},
    "平移": {"en": "Translation", "de": "Translation"},
    "旋转": {"en": "Rotation", "de": "Rotation"},
    "轴对称": {"en": "Axial Symmetry", "de": "Achsensymmetrie"},
    "中心对称": {"en": "Central Symmetry", "de": "Zentralsymmetrie"},
    "全等判定": {"en": "Congruence Criterion", "de": "Kongruenzkriterium"},
    "等腰三角形": {"en": "Isosceles Triangle", "de": "Gleichschenkliges Dreieck"},
    "直角三角形": {"en": "Right Triangle", "de": "Rechtwinkliges Dreieck"},
    "三角形内角和": {"en": "Triangle Angle Sum", "de": "Dreieckswinkelsumme"},
    "圆周角": {"en": "Inscribed Angle", "de": "Umfangswinkel"},
    "勾股定理逆定理": {"en": "Converse of Pythagoras", "de": "Umkehrung des Satzes des Pythagoras"},
    "判别式": {"en": "Discriminant", "de": "Diskriminante"},
    "求根公式": {"en": "Quadratic Formula", "de": "Quadratische Lösungsformel"},
    "消元法": {"en": "Elimination Method", "de": "Eliminationsverfahren"},
    "分式": {"en": "Rational Expression", "de": "Bruchterm"},
    "比大小": {"en": "Comparison", "de": "Vergleich"},
    "平均分": {"en": "Equal Division", "de": "Gleichmäßige Teilung"},
    "凑十法": {"en": "Make-Ten Method", "de": "Zehnerergänzung"},
    "数位": {"en": "Digit Place", "de": "Ziffernstelle"},
    "近似": {"en": "Approximation", "de": "Näherung"},
    "锐角": {"en": "Acute Angle", "de": "Spitzer Winkel"},
    "钝角": {"en": "Obtuse Angle", "de": "Stumpfer Winkel"},
    "顶点": {"en": "Vertex", "de": "Scheitelpunkt"},
    "分类": {"en": "Classification", "de": "Klassifikation"},
    "混合运算": {"en": "Mixed Operations", "de": "Gemischte Rechenoperationen"},
    "向量积": {"en": "Cross Product", "de": "Kreuzprodukt"},
    "向量的模": {"en": "Vector Magnitude", "de": "Vektorbetrag"},
    "数乘向量": {"en": "Scalar Multiplication", "de": "Skalarmultiplikation"},
    "混合积": {"en": "Scalar Triple Product", "de": "Spatprodukt"},
    "二阶行列式": {"en": "Second-Order Determinant", "de": "Determinante 2. Ordnung"},
    "三阶行列式": {"en": "Third-Order Determinant", "de": "Determinante 3. Ordnung"},
    "逆序数": {"en": "Inversion Number", "de": "Inversionszahl"},
    "对换": {"en": "Transposition", "de": "Transposition"},
    "合同变换": {"en": "Congruent Transformation", "de": "Kongruenztransformation"},
    "标准形": {"en": "Canonical Form", "de": "Kanonische Form"},
    "正定二次型": {"en": "Positive Definite Quadratic Form", "de": "Positiv definite quadratische Form"},
    "线性变换的复合": {"en": "Composition of Linear Maps", "de": "Komposition linearer Abbildungen"},
    "矩阵的幂": {"en": "Matrix Power", "de": "Matrixpotenz"},
    "基": {"en": "Basis", "de": "Basis"},
    "维数": {"en": "Dimension", "de": "Dimension"},
    "逆矩阵": {"en": "Inverse Matrix", "de": "Inverse Matrix"},
    "克莱姆法则": {"en": "Cramer's Rule", "de": "Cramersche Regel"},
    "线性性质": {"en": "Linearity", "de": "Linearität"},
    "可微": {"en": "Differentiable", "de": "Differenzierbar"},
    "微分的几何意义": {"en": "Geometric Meaning of Differential", "de": "Geometrische Bedeutung des Differentials"},
    "高阶偏导数": {"en": "Higher-Order Partial Derivative", "de": "Partielle Ableitung höherer Ordnung"},
    "常数函数的导数": {"en": "Derivative of Constant", "de": "Ableitung einer Konstanten"},
    "幂函数的导数": {"en": "Derivative of Power Function", "de": "Ableitung der Potenzfunktion"},
    "和差法则": {"en": "Sum and Difference Rule", "de": "Summen- und Differenzregel"},
    "积法则": {"en": "Product Rule", "de": "Produktregel"},
    "商法则": {"en": "Quotient Rule", "de": "Quotientenregel"},
    "洛必达法则": {"en": "L'Hôpital's Rule", "de": "Regel von L'Hôpital"},
    "切线": {"en": "Tangent Line", "de": "Tangente"},
    "曲边梯形": {"en": "Curvilinear Trapezoid", "de": "Krummliniges Trapez"},
    "积分上限": {"en": "Upper Limit of Integration", "de": "Obere Integrationsgrenze"},
    "积分下限": {"en": "Lower Limit of Integration", "de": "Untere Integrationsgrenze"},
    "被积函数": {"en": "Integrand", "de": "Integrand"},
    "微积分基本定理": {"en": "Fundamental Theorem of Calculus", "de": "Fundamentalsatz der Analysis"},
    "收敛半径": {"en": "Radius of Convergence", "de": "Konvergenzradius"},
    "无穷级数": {"en": "Infinite Series", "de": "Unendliche Reihe"},
    "柯西中值定理": {"en": "Cauchy's Mean Value Theorem", "de": "Cauchyscher Mittelwertsatz"},
    "估值定理": {"en": "Estimation Theorem", "de": "Abschätzungssatz"},
    "区间可加性": {"en": "Interval Additivity", "de": "Intervalladditivität"},
    "条件分布": {"en": "Conditional Distribution", "de": "Bedingte Verteilung"},
    "概率分布": {"en": "Probability Distribution", "de": "Wahrscheinlichkeitsverteilung"},
    "古典概型": {"en": "Classical Probability", "de": "Klassische Wahrscheinlichkeit"},
    "随机试验": {"en": "Random Experiment", "de": "Zufallsexperiment"},
    "随机事件": {"en": "Random Event", "de": "Zufallsereignis"},
    "事件的独立性": {"en": "Independence of Events", "de": "Unabhängigkeit von Ereignissen"},
    "频率的稳定性": {"en": "Stability of Frequency", "de": "Stabilität der Häufigkeit"},
    "大数定律": {"en": "Law of Large Numbers", "de": "Gesetz der großen Zahlen"},
    "中心极限定理": {"en": "Central Limit Theorem", "de": "Zentraler Grenzwertsatz"},
    "样本空间": {"en": "Sample Space", "de": "Stichprobenraum"},
    "样本": {"en": "Sample", "de": "Stichprobe"},
    "样本均值": {"en": "Sample Mean", "de": "Stichprobenmittel"},
    "样本方差": {"en": "Sample Variance", "de": "Stichprobenvarianz"},
    "总体": {"en": "Population", "de": "Grundgesamtheit"},
    "点估计": {"en": "Point Estimation", "de": "Punktschätzung"},
    "矩估计": {"en": "Method of Moments", "de": "Momentenmethode"},
    "矩": {"en": "Moment", "de": "Moment"},
    "似然函数": {"en": "Likelihood Function", "de": "Likelihood-Funktion"},
    "无偏性": {"en": "Unbiasedness", "de": "Erwartungstreue"},
    "有效性": {"en": "Efficiency", "de": "Effizienz"},
    "置信区间": {"en": "Confidence Interval", "de": "Konfidenzintervall"},
    "假设检验": {"en": "Hypothesis Test", "de": "Hypothesentest"},
    "拒绝域": {"en": "Rejection Region", "de": "Ablehnungsbereich"},
    "第一类错误": {"en": "Type I Error", "de": "Fehler 1. Art"},
    "第二类错误": {"en": "Type II Error", "de": "Fehler 2. Art"},
    "Z检验": {"en": "Z-Test", "de": "Z-Test"},
    "t检验": {"en": "t-Test", "de": "t-Test"},
    "t分布": {"en": "t-Distribution", "de": "t-Verteilung"},
    "F检验": {"en": "F-Test", "de": "F-Test"},
    "F分布": {"en": "F-Distribution", "de": "F-Verteilung"},
    "χ²检验": {"en": "Chi-Square Test", "de": "Chi-Quadrat-Test"},
    "最小二乘法": {"en": "Least Squares Method", "de": "Methode der kleinsten Quadrate"},
    "回归分析": {"en": "Regression Analysis", "de": "Regressionsanalyse"},
    "卷积公式": {"en": "Convolution Formula", "de": "Faltungsformel"},
    "向量场": {"en": "Vector Field", "de": "Vektorfeld"},
    "保守场": {"en": "Conservative Field", "de": "Konservatives Feld"},
    "边界条件": {"en": "Boundary Condition", "de": "Randbedingung"},
    "一致连续性": {"en": "Uniform Continuity", "de": "Gleichmäßige Stetigkeit"},
    "有效数字": {"en": "Significant Figures", "de": "Gültige Ziffern"},
    "科学计数法": {"en": "Scientific Notation", "de": "Wissenschaftliche Notation"},
    "最大值": {"en": "Maximum", "de": "Maximum"},
    "最小值": {"en": "Minimum", "de": "Minimum"},
    "极值": {"en": "Extremum", "de": "Extremum"},
    "拐点": {"en": "Inflection Point", "de": "Wendepunkt"},
    "渐近线": {"en": "Asymptote", "de": "Asymptote"},
    "反函数": {"en": "Inverse Function", "de": "Umkehrfunktion"},
    "复合函数": {"en": "Composite Function", "de": "Verkettete Funktion"},
    "初等函数": {"en": "Elementary Function", "de": "Elementare Funktion"},
    "分段函数": {"en": "Piecewise Function", "de": "Abschnittsweise definierte Funktion"},
    "单调性": {"en": "Monotonicity", "de": "Monotonie"},
    "奇偶性": {"en": "Parity", "de": "Parität"},
    "周期性": {"en": "Periodicity", "de": "Periodizität"},
    "有界性": {"en": "Boundedness", "de": "Beschränktheit"},
    "连续性": {"en": "Continuity", "de": "Stetigkeit"},
    "一致收敛": {"en": "Uniform Convergence", "de": "Gleichmäßige Konvergenz"},
}

# Build reverse dictionary for EN→ZH and DE→ZH
EN_DICT = {v["en"]: {"zh": k, "de": v["de"]} for k, v in ZH_DICT.items()}
DE_DICT = {v["de"]: {"zh": k, "en": v["en"]} for k, v in ZH_DICT.items()}


def fill_labels(nodes):
    """Fill missing EN/DE labels using the translation dictionary."""
    filled_en = 0
    filled_de = 0
    fixed_same = 0

    for nd in nodes:
        lbs = nd.get("labels", {})
        if not lbs:
            lbs = {}
            nd["labels"] = lbs

        zh = lbs.get("zh", "")
        en = lbs.get("en", "")
        de = lbs.get("de", "")
        name = nd.get("name", "")

        # Detect "fake" trilingual: all three same Chinese text
        if zh and en and de and zh == en == de:
            # Check if ZH is a known Chinese math term
            if zh in ZH_DICT:
                lbs["en"] = ZH_DICT[zh]["en"]
                lbs["de"] = ZH_DICT[zh]["de"]
                fixed_same += 1
                continue

        # Fill missing EN from ZH
        if zh and not en:
            if zh in ZH_DICT:
                lbs["en"] = ZH_DICT[zh]["en"]
                filled_en += 1

        # Fill missing DE from ZH
        if zh and not de:
            if zh in ZH_DICT:
                lbs["de"] = ZH_DICT[zh]["de"]
                filled_de += 1

        # Also try to fill ZH from EN (for EN-only nodes)
        if not zh and en:
            if en in EN_DICT:
                lbs["zh"] = EN_DICT[en]["zh"]
                if not lbs.get("de"):
                    lbs["de"] = EN_DICT[en]["de"]

        # Fill ZH from DE
        if not zh and de:
            if de in DE_DICT:
                lbs["zh"] = DE_DICT[de]["zh"]
                if not lbs.get("en"):
                    lbs["en"] = DE_DICT[de]["en"]

    return filled_en, filled_de, fixed_same


if __name__ == "__main__":
    # Read data
    data_path = PROJECT_DIR / "cognitive-space" / "web" / "data.js"
    original = data_path.read_text("utf-8", errors="replace")

    json_str = original.split("const COGNITIVE_DATA = ")[1].rsplit(";", 1)[0]
    data = json.loads(json_str)
    nodes = data["nodes"]

    # Count before
    before = {
        "trilingual": sum(1 for nd in nodes if all(nd.get("labels",{}).get(l) for l in ["zh","en","de"])),
        "zh": sum(1 for nd in nodes if nd.get("labels",{}).get("zh")),
        "en": sum(1 for nd in nodes if nd.get("labels",{}).get("en")),
        "de": sum(1 for nd in nodes if nd.get("labels",{}).get("de")),
    }

    # Fill
    filled_en, filled_de, fixed_same = fill_labels(nodes)

    # Count after
    after = {
        "trilingual": sum(1 for nd in nodes if all(nd.get("labels",{}).get(l) for l in ["zh","en","de"])),
        "zh": sum(1 for nd in nodes if nd.get("labels",{}).get("zh")),
        "en": sum(1 for nd in nodes if nd.get("labels",{}).get("en")),
        "de": sum(1 for nd in nodes if nd.get("labels",{}).get("de")),
        "same": sum(1 for nd in nodes if nd.get("labels",{}).get("zh") and nd.get("labels",{}).get("en") and nd.get("labels",{}).get("de") and nd["labels"]["zh"] == nd["labels"]["en"] == nd["labels"]["de"])
    }

    print("=== i18n Fill Results ===")
    print(f"Filled EN: {filled_en}")
    print(f"Filled DE: {filled_de}")
    print(f"Fixed 'fake trilingual': {fixed_same}")
    print()
    print(f"Before → After:")
    print(f"  Trilingual: {before['trilingual']} → {after['trilingual']}")
    print(f"  Has ZH:     {before['zh']} → {after['zh']}")
    print(f"  Has EN:     {before['en']} → {after['en']}")
    print(f"  Has DE:     {before['de']} → {after['de']}")
    print(f"  False tri:  {after['same']}")

    # Write updated data back
    new_json = json.dumps(data, ensure_ascii=False, indent=2)
    new_block = f"// CognitiveSpace — Embedded visualization data\n// 574 concepts, 3538 links\n// 68 textbooks: 45 ZH + 20 EN + 10 DE\nconst COGNITIVE_DATA = {new_json};"

    data_path.write_text(new_block, encoding="utf-8")
    print(f"\nWritten to: {data_path}")
    print("Done!")
