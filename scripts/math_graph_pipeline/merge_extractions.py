#!/usr/bin/env python3
"""
CognitiveSpace — Merge Extractions

Reads all raw extraction JSON files from data/math_extractions/ (produced by mimo),
merges concepts by normalized name, deduplicates relations, and handles aliases.

Usage:
    python scripts/math_graph_pipeline/merge_extractions.py [--input-dir data/math_extractions] [--output-dir data/math_extractions/merged]

Output:
    - data/math_extractions/merged/merged_concepts.json
    - data/math_extractions/merged/merged_relations.json
    - data/math_extractions/merged/merge_report.txt
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict


# ── Normalization ────────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    """Normalize a concept name for dedup matching."""
    n = name.strip().lower()
    # Remove punctuation
    n = re.sub(r"[\(\)\[\]\{\}\（\）\【\】『』「」,;:，；：、\s\-_]+", "", n)
    # Remove spaces
    n = n.replace(" ", "")
    return n


# Known alias groups (domain-specific synonyms)
# IMPORTANT: Order matters — first Chinese entry = canonical name
ALIAS_GROUPS = [
    # ── Calculus ──
    ["导数", "导函数", "微商", "derivative", "ableitung", "differentialquotient"],
    ["极限", "limit", "grenzwert", "limes"],
    ["积分", "integral", "integralrechnung"],
    ["不定积分", "stammfunktion", "antiderivative", "unbestimmtes integral"],
    ["定积分", "bestimmtes integral", "definite integral", "riemann integral"],
    ["微分", "differential", "differenzial"],
    ["连续性", "continuity", "stetigkeit", "stetig"],
    ["切线", "tangent", "tangente", "tangent line", "tangentensteigung", "切线斜率"],
    ["函数", "function", "funktion"],
    ["变化率", "rate of change", "änderungsrate"],
    ["速度", "velocity", "geschwindigkeit", "instantaneous velocity"],

    # ── Linear Algebra ──
    ["矩阵", "matrix", "matrizen"],
    ["向量", "vector", "vektor"],
    ["行列式", "determinant", "determinante"],
    ["特征值", "eigenvalue", "eigenwert"],
    ["特征向量", "eigenvector", "eigenvektor"],
    ["线性方程组", "linear system", "lineares gleichungssystem", "linear equations"],
    ["向量空间", "vector space", "vektorraum"],
    ["线性变换", "linear transformation", "lineare abbildung"],

    # ── Geometry ──
    ["三角形", "triangle", "dreieck"],
    ["圆", "circle", "kreis"],
    ["椭圆", "ellipse", "ellipse（椭圆）"],
    ["双曲线", "hyperbola", "hyperbel"],
    ["抛物线", "parabola", "parabel"],
    ["面积", "area", "fläche"],
    ["体积", "volume", "volumen"],
    ["坐标系", "coordinate system", "koordinatensystem"],

    # ── Statistics ──
    ["概率", "probability", "wahrscheinlichkeit"],
    ["统计", "statistics", "statistik"],
    ["期望", "expected value", "erwartungswert"],
    ["方差", "variance", "varianz"],
    ["标准差", "standard deviation", "standardabweichung"],
    ["分布", "distribution", "verteilung"],
    ["假设检验", "hypothesis test", "hypothesentest"],

    # ── Calculus (new rules) ──
    ["复合函数", "composite function", "zusammensetzung"],
    ["链式法则", "chain rule", "kettenregel"],
    ["和差法则", "sum and difference rules", "summenregel"],
    ["积法则", "product rule", "produktregel"],
    ["商法则", "quotient rule", "quotientenregel"],
    ["原函数", "antiderivative", "stammfunktion"],
    ["黎曼和", "riemann sum", "riemann-summe"],
    ["中间变量", "intermediate variable", "zwischenvariable"],
    ["微积分基本定理", "fundamental theorem of calculus", "hauptsatz der analysis"],
    ["被积函数", "integrand", "integrand"],
    ["积分下限", "lower limit", "untere grenze"],
    ["积分上限", "upper limit", "obere grenze"],
    ["曲边梯形", "curvilinear trapezoid"],
    ["线性性质", "linearity", "linearität"],
    ["区间可加性", "additivity", "additivität"],
    ["估值定理", "estimation theorem"],
    ["高阶导数", "higher-order derivatives", "höhere ableitungen"],
    ["二阶导数", "second derivative", "zweite ableitung"],
    ["加速度", "acceleration", "beschleunigung"],
    ["加加速度", "jerk", "ruck"],
    ["变化率", "rate of change", "änderungsrate"],
    ["切线近似", "tangent line approximation", "tangentenapproximation"],
    ["数e", "number e", "euler-zahl"],
    ["常数法则", "constant rule", "konstantenregel"],
    ["幂法则", "power rule", "potenzregel"],
    ["指数法则", "exponential rule", "exponentialregel"],
    ["对数法则", "logarithmic rule", "logarithmusregel"],
    ["正弦法则", "sine rule", "sinusregel"],
    ["余弦法则", "cosine rule", "kosinusregel"],
    ["导数运算法则", "differentiation rules", "ableitungsregeln"],

    # ── Calculus (advanced) ──
    ["洛必达法则", "l'hôpital's rule", "l'hospitalsche regel"],
    ["未定式", "indeterminate form", "unbestimmte form"],
    ["柯西中值定理", "cauchy mean value theorem", "cauchyscher mittelwertsatz"],
    ["泰勒公式", "taylor's formula", "taylorsatz"],
    ["泰勒展开", "taylor expansion", "taylor-entwicklung"],
    ["麦克劳林公式", "maclaurin formula", "maclaurin-formel"],
    ["拉格朗日余项", "lagrange remainder", "lagrange-restglied"],
    ["微分方程", "differential equation", "differentialgleichung"],
    ["常微分方程", "ordinary differential equation", "gewöhnliche dgl"],
    ["通解", "general solution", "allgemeine lösung"],
    ["特解", "particular solution", "partikuläre lösung"],
    ["初始条件", "initial condition", "anfangsbedingung"],
    ["可分离变量方程", "separable equation", "separierbare gleichung"],

    # ── Linear Algebra (new) ──
    ["方阵", "square matrix", "quadratische matrix"],
    ["单位矩阵", "identity matrix", "einheitsmatrix"],
    ["对称矩阵", "symmetric matrix", "symmetrische matrix"],
    ["逆矩阵", "inverse matrix", "inverse matrix"],
    ["矩阵转置", "transpose", "transponierte"],
    ["矩阵乘法", "matrix multiplication", "matrizenmultiplikation"],
    ["伴随矩阵", "adjugate matrix", "adjungierte"],

    # ── Linear Algebra (vector spaces, eigen) ──
    ["线性组合", "linear combination", "lineare kombination"],
    ["线性相关", "linearly dependent", "linear abhängig"],
    ["线性无关", "linearly independent", "linear unabhängig"],
    ["极大线性无关组", "maximal independent set", "maximal linear unabhängige teilmenge"],
    ["向量组的秩", "rank of vector system", "rang des vektorsystems"],
    ["矩阵的秩", "rank of matrix", "matrixrang"],
    ["基础解系", "fundamental solution system", "fundamentales lösungssystem"],
    ["解空间", "solution space", "lösungsraum"],
    ["特征方程", "characteristic equation", "charakteristische gleichung"],
    ["特征多项式", "characteristic polynomial", "charakteristisches polynom"],
    ["矩阵的迹", "trace", "spur"],
    ["对角化", "diagonalization", "diagonalisierung"],
    ["相似矩阵", "similar matrices", "ähnliche matrizen"],
    ["二次型", "quadratic form", "quadratische form"],
    ["正定矩阵", "positive definite matrix", "positiv definite matrix"],
    ["正交矩阵", "orthogonal matrix", "orthogonale matrix"],
    ["基", "basis"],
    ["维数", "dimension"],
    ["列空间", "column space", "spaltenraum"],
    ["零空间", "null space", "nullraum"],
    ["秩", "rank", "rang"],
    ["谱定理", "spectral theorem", "spektralsatz"],
    ["正交对角化", "orthogonal diagonalization", "orthogonale diagonalisierung"],

    # ── Linear Algebra (transforms, inner product) ──
    ["线性变换", "linear transformation", "lineare abbildung", "linear mapping"],
    ["线性变换的核", "kernel", "kern"],
    ["线性变换的像", "image", "bild"],
    ["线性变换的矩阵表示", "matrix representation", "matrixdarstellung"],
    ["内积", "inner product", "skalarprodukt"],
    ["内积空间", "inner product space", "skalarprodukttraum", "euclidean space"],
    ["范数", "norm"],
    ["正交", "orthogonal"],
    ["标准正交基", "orthonormal basis", "orthonormale basis"],
    ["Gram-Schmidt 正交化", "gram-schmidt process", "gram-schmidt-verfahren"],
    ["正交投影", "orthogonal projection", "orthogonale projektion"],
    ["最小二乘法", "least squares", "methode der kleinsten quadrate"],
    ["Jordan 块", "jordan block", "jordan-block"],
    ["Jordan 标准形", "jordan normal form", "jordan-normalform"],
    ["最小多项式", "minimal polynomial", "minimalpolynom"],
    ["Cayley-Hamilton 定理", "cayley-hamilton theorem", "satz von cayley-hamilton"],

    # ── Probability & Statistics ──
    ["概率", "probability", "wahrscheinlichkeit"],
    ["条件概率", "conditional probability", "bedingte wahrscheinlichkeit"],
    ["贝叶斯公式", "bayes' theorem", "satz von bayes"],
    ["随机变量", "random variable", "zufallsgröße"],
    ["分布函数", "distribution function", "verteilungsfunktion"],
    ["概率密度函数", "probability density function", "dichte"],
    ["二项分布", "binomial distribution", "binomialverteilung"],
    ["泊松分布", "poisson distribution", "poissonverteilung"],
    ["正态分布", "normal distribution", "normalverteilung"],
    ["均匀分布", "uniform distribution", "gleichverteilung"],
    ["指数分布", "exponential distribution", "exponentialverteilung"],
    ["联合分布", "joint distribution", "gemeinsame verteilung"],
    ["边缘分布", "marginal distribution", "randverteilung"],
    ["数学期望", "expectation", "erwartungswert"],
    ["方差", "variance", "varianz"],
    ["协方差", "covariance", "kovarianz"],
    ["相关系数", "correlation coefficient", "korrelationskoeffizient"],
    ["大数定律", "law of large numbers", "gesetz der großen zahlen"],
    ["中心极限定理", "central limit theorem", "zentraler grenzwertsatz"],
    ["统计量", "statistic", "statistik"],
    ["χ²分布", "chi-squared distribution", "chi-quadrat-verteilung"],
    ["t分布", "t-distribution", "t-verteilung"],
    ["F分布", "F-distribution", "F-verteilung"],
    ["参数估计", "parameter estimation", "parameterschätzung"],
    ["最大似然估计", "maximum likelihood estimation", "maximum-likelihood-schätzung"],
    ["置信区间", "confidence interval", "konfidenzintervall"],
    ["假设检验", "hypothesis testing", "hypothesentest"],
    ["显著性水平", "significance level", "signifikanzniveau"],
    ["原假设", "null hypothesis", "nullhypothese"],
    ["备择假设", "alternative hypothesis", "alternativhypothese"],
    ["t检验", "t-test", "t-test"],
    ["F检验", "F-test", "F-test"],
    ["切比雪夫不等式", "chebyshev's inequality", "ungleichung von tschebyscheff"],

    # ── ODE/PDE (advanced) ──
    ["高阶线性微分方程", "higher-order linear ode", "lineare dgl höherer ordnung"],
    ["待定系数法", "method of undetermined coefficients", "methode der unbestimmten koeffizienten"],
    ["参数变易法", "variation of parameters", "variation der konstanten"],
    ["齐次方程", "homogeneous equation", "homogene gleichung"],
    ["非齐次方程", "nonhomogeneous equation", "nicht-homogene gleichung"],
    ["微分方程组", "system of odes", "differentialgleichungssystem"],
    ["矩阵指数", "matrix exponential", "matrixexponential"],
    ["弹簧振动", "spring oscillation", "feder-masse-system"],
    ["简谐运动", "simple harmonic motion", "harmonische schwingung"],
    ["阻尼振动", "damped oscillation", "gedämpfte schwingung"],
    ["共振", "resonance", "resonanz"],
    ["逻辑斯蒂模型", "logistic model", "logistisches modell"],
    ["SIR模型", "sir model", "sir-modell"],
    ["调和函数", "harmonic function", "harmonische funktion"],
    ["达朗贝尔解", "d'alembert solution", "d'alembertsche lösung"],
    ["特征值问题", "eigenvalue problem", "eigenwertproblem"],
    ["傅里叶级数", "fourier series", "fourierreihe"],
    ["相平面", "phase plane", "phasenebene"],

    # ── Elementary (小学) ──
    ["自然数", "natural numbers", "natürliche zahlen"],
    ["加法", "addition"],
    ["减法", "subtraction", "subtraktion"],
    ["乘法", "multiplication", "multiplikation"],
    ["除法", "division"],
    ["分数", "fraction", "bruch"],
    ["小数", "decimal", "dezimalzahl"],
    ["百分数", "percentage", "prozent"],
    ["周长", "perimeter", "umfang"],
    ["面积", "area", "fläche"],
    ["体积", "volume", "volumen"],
    ["角", "angle", "winkel"],
    ["直角", "right angle", "rechter winkel"],
    ["三角形", "triangle", "dreieck"],
    ["长方形", "rectangle", "rechteck"],
    ["正方形", "square", "quadrat"],
    ["圆", "circle", "kreis"],
    ["长方体", "cuboid", "quader"],
    ["正方体", "cube", "würfel"],
    ["圆柱", "cylinder", "zylinder"],
    ["球", "sphere", "kugel"],
    ["厘米", "centimeter", "zentimeter"],
    ["米", "meter"],
    ["千克", "kilogram", "kilogramm"],
    ["乘法口诀", "multiplication table", "einmaleins"],

    # ── Middle School (初中) ──
    ["有理数", "rational number", "rationale zahl"],
    ["整式", "algebraic expression", "term"],
    ["一元一次方程", "linear equation in one variable", "lineare gleichung einer unbekannten"],
    ["二元一次方程组", "system of linear equations", "lineares gleichungssystem"],
    ["不等式", "inequality", "ungleichung"],
    ["一次函数", "linear function", "lineare funktion"],
    ["勾股定理", "pythagorean theorem", "pythagoreischer lehrsatz"],
    ["全等三角形", "congruent triangles", "kongruente dreiecke"],
    ["相似三角形", "similar triangles", "ähnliche dreiecke"],
    ["二次函数", "quadratic function", "quadratische funktion"],
    ["一元二次方程", "quadratic equation", "quadratische gleichung"],
    ["锐角三角函数", "trigonometric functions", "trigonometrische funktionen"],
    ["平行四边形", "parallelogram", "parallelogramm"],
    ["扇形", "sector", "kreisabschnitt"],
]


# ── Education Level Inference ─────────────────────────────────────────

# Keywords to infer education level from textbook names
LEVEL_RULES = [
    ("小学数学", "elementary", 1),
    ("小学", "elementary", 1),
    ("初中数学", "middle", 2),
    ("初中", "middle", 2),
    ("高中数学", "high", 3),
    ("选修", "high", 3),
    ("高中", "high", 3),
    ("linear algebra", "college", 4),
    ("线性代数", "college", 4),
    ("高等数学", "college", 4),
    ("微积分", "college", 4),
    ("calculus", "college", 4),
    ("probability", "college", 4),
    ("statistics", "college", 4),
    ("概率论", "college", 4),
    ("数理统计", "college", 4),
    ("stewart", "college", 4),
    ("strang", "college", 4),
    ("forster", "college", 4),
    ("fischer", "college", 4),
    ("analysis", "college", 4),
    ("lambacher", "high", 3),
    ("khan academy", "high", 3),
]


def infer_level(textbook_name: str):
    """Infer education level from textbook name. Returns (level, order)."""
    name_lower = textbook_name.lower()
    for keyword, level, order in LEVEL_RULES:
        if keyword.lower() in name_lower:
            return level, order
    if re.search(r"[一-龿]", textbook_name) and "小学" in textbook_name:
        return "elementary", 1
    if re.search(r"[一-龿]", textbook_name) and ("初中" in textbook_name or "七年" in textbook_name):
        return "middle", 2
    return "college", 4


def infer_level_from_textbook(textbook: dict):
    """Get level from source_textbook metadata dict."""
    tname = textbook.get('name', '') or ''
    return infer_level(tname)


def find_alias_group(name: str) -> int | None:
    """Find which alias group a name belongs to."""
    n = normalize_name(name)
    for i, group in enumerate(ALIAS_GROUPS):
        for member in group:
            if normalize_name(member) == n:
                return i
    return None


def get_canonical_name(name: str, alias_group: list | None = None) -> str:
    """Get the canonical (preferred) name from an alias group."""
    if alias_group is None:
        idx = find_alias_group(name)
        if idx is None:
            return name
        alias_group = ALIAS_GROUPS[idx]
    # Return the first Chinese name if available, else first in group
    for member in alias_group:
        if re.search(r'[一-鿿]', member):  # has Chinese characters
            return member
    return alias_group[0]


# ── Loading ──────────────────────────────────────────────────────────

def load_extractions(input_dir: Path) -> list[dict]:
    """Load all JSON extraction files from input directory."""
    extractions = []
    files_loaded = []

    for json_file in sorted(input_dir.glob("*.json")):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if "extracted_concepts" in data or "source_textbook" in data:
                extractions.append(data)
                files_loaded.append(json_file.name)
            else:
                print(f"  [SKIP] {json_file.name}: missing required fields")
        except json.JSONDecodeError as e:
            print(f"  [ERROR] {json_file.name}: invalid JSON — {e}")

    return extractions, files_loaded


# ── Merging ──────────────────────────────────────────────────────────

def merge_concepts(extractions: list[dict]) -> tuple[dict, list[str]]:
    """
    Merge concepts across extraction files.

    Returns:
        (merged_concepts_map, conflicts)
    """
    concepts: dict[str, dict] = {}  # canonical_name → concept data
    conflicts: list[str] = []

    for data in extractions:
        textbook = data.get("source_textbook", {})
        textbook_name = textbook.get("name", "unknown")
        textbook_lang = textbook.get("language", "unknown")
        chapter = textbook.get("chapter", "")
        section = textbook.get("section", "")
        license_str = textbook.get("license", "unknown")

        for c in data.get("extracted_concepts", []):
            name = c.get("name", "").strip()
            if not name:
                continue

            canonical = name
            alias_idx = find_alias_group(name)

            if alias_idx is not None:
                canonical = get_canonical_name(name, ALIAS_GROUPS[alias_idx])

            if canonical in concepts:
                existing = concepts[canonical]
                # Append cross-reference if not duplicate
                refs = existing.setdefault("source", {}).setdefault("cross_references", [])
                new_ref = {
                    "textbook": textbook_name,
                    "language": textbook_lang,
                    "chapter": chapter,
                    "section": section,
                }
                if new_ref not in refs:
                    refs.append(new_ref)

                # Merge aliases
                existing_aliases = set(existing.get("aliases", []))
                new_aliases = set(c.get("aliases", []))
                merged_aliases = existing_aliases | new_aliases
                # Add the current extraction's name as an alias if different from canonical
                if name != canonical:
                    merged_aliases.add(name)
                if canonical in merged_aliases:
                    merged_aliases.discard(canonical)
                existing["aliases"] = sorted(merged_aliases)

                # Check for conflicting categories
                if c.get("category") and existing.get("category") and c["category"] != existing["category"]:
                    conflicts.append(
                        f"Category conflict: '{canonical}' — "
                        f"'{existing['category']}' vs '{c['category']}' "
                        f"(from {textbook_name})"
                    )
            else:
                # New concept — create entry
                refs = [{
                    "textbook": textbook_name,
                    "language": textbook_lang,
                    "chapter": chapter,
                    "section": section,
                }]
                source_info = {
                    "primary": textbook_name,
                    "cross_references": refs,
                    "license": license_str,
                }
                aliases = c.get("aliases", [])
                # Remove canonical name from aliases if present
                if canonical in aliases:
                    aliases.remove(canonical)

                # Infer education level
                level, level_order = infer_level_from_textbook(textbook)

                entry = {
                    "canonical_name": canonical,
                    "name_original": name,
                    "language": textbook_lang,
                    "level": level,
                    "level_order": level_order,
                    "aliases": sorted(aliases),
                    "category": c.get("category", "concept"),
                    "definition_snippet": c.get("definition_snippet", ""),
                    "source": source_info,
                }
                concepts[canonical] = entry

    # Post-process: for alias-group members, set canonical for all
    for idx, group in enumerate(ALIAS_GROUPS):
        members_in_concepts = [c for c in concepts if normalize_name(c) in [normalize_name(m) for m in group]]
        if len(members_in_concepts) > 1:
            canonical = get_canonical_name(members_in_concepts[0], group)
            for member in members_in_concepts:
                if member != canonical:
                    # Merge member into canonical
                    if canonical in concepts:
                        concepts[canonical]["aliases"] = sorted(
                            set(concepts[canonical].get("aliases", [])) | {member}
                        )
                        # Merge cross-references
                        member_refs = concepts[member].get("source", {}).get("cross_references", [])
                        existing_refs = concepts[canonical].setdefault("source", {}).setdefault("cross_references", [])
                        for ref in member_refs:
                            if ref not in existing_refs:
                                existing_refs.append(ref)
                        if concepts[member].get("definition_snippet") and not concepts[canonical].get("definition_snippet"):
                            concepts[canonical]["definition_snippet"] = concepts[member]["definition_snippet"]
                    del concepts[member]
                    conflicts.append(f"  Merged alias '{member}' → '{canonical}'")

    return concepts, conflicts


def build_alias_map(concepts: dict) -> dict[str, str]:
    """Build a flat map: any known name → canonical name."""
    alias_map = {}
    for canonical, entry in concepts.items():
        alias_map[canonical] = canonical
        alias_map[entry.get("name_original", "")] = canonical
        for alias in entry.get("aliases", []):
            alias_map[alias] = canonical
    return alias_map


def merge_relations(extractions: list[dict],
                    concepts: dict | None = None) -> tuple[list[dict], list[str]]:
    """
    Merge relations across extraction files, deduplicating.

    Args:
        extractions: Raw extraction data from mimo
        concepts: Merged concept map (for alias resolution)

    Returns:
        (merged_relations, conflicts)
    """
    alias_map = build_alias_map(concepts) if concepts else {}

    seen: set[tuple[str, str, str]] = set()
    relations: list[dict] = []
    conflicts: list[str] = []

    for data in extractions:
        textbook = data.get("source_textbook", {})
        textbook_name = textbook.get("name", "unknown")

        for r in data.get("extracted_relations", []):
            raw_source = r.get("source", "").strip()
            raw_target = r.get("target", "").strip()
            rel_type = r.get("type", "related_to")

            if not raw_source or not raw_target:
                continue

            # Map to canonical names if possible
            source = alias_map.get(raw_source, raw_source)
            target = alias_map.get(raw_target, raw_target)

            key = (source, target, rel_type)
            if key in seen:
                continue
            seen.add(key)

            entry = {
                "source": source,
                "target": target,
                "type": rel_type,
                "importance": r.get("importance", 0.5),
                "evidence": r.get("evidence", ""),
                "source_textbooks": [textbook_name],
            }
            relations.append(entry)

    return relations, conflicts


def detect_conflicts(concepts: dict, relations: list[dict]) -> list[str]:
    """Detect structural conflicts in the merged data."""
    conflicts = []
    concept_names = set(concepts.keys())

    for r in relations:
        src = r["source"]
        tgt = r["target"]
        if src not in concept_names:
            conflicts.append(f"  Relation source '{src}' not found in concepts")
        if tgt not in concept_names:
            conflicts.append(f"  Relation target '{tgt}' not found in concepts")

    return conflicts


# ── Output ────────────────────────────────────────────────────────────

def write_report(report_path: Path, files_loaded: list[str],
                 concepts: dict, relations: list[dict],
                 all_conflicts: list[str]):
    """Write a human-readable merge report."""
    lines = [
        "=" * 60,
        "CognitiveSpace — Merge Report",
        "=" * 60,
        f"Generated: {__import__('datetime').datetime.now().isoformat()}",
        "",
        f"Files loaded: {len(files_loaded)}",
        *[f"  - {f}" for f in files_loaded],
        "",
        f"Concepts merged: {len(concepts)}",
        f"Relations merged: {len(relations)}",
        "",
    ]

    if all_conflicts:
        lines.extend(["Conflicts:", *all_conflicts])
    else:
        lines.append("No conflicts detected.")

    # Domain breakdown
    domains = defaultdict(int)
    CALCULUS_KEYWORDS = {
        "导数", "极限", "积分", "微分", "连续", "切线", "函数", "变化率",
        "derivative", "limit", "integral", "differential", "continuity",
        "tangent", "function", "rate of change", "ableitung", "grenzwert",
        "integralrechnung", "stetigkeit", "tangente", "funktion",
    }
    LINEAR_ALGEBRA_KEYWORDS = {
        "矩阵", "向量", "行列式", "特征", "线性",
        "matrix", "vector", "determinant", "eigen", "linear",
        "matrizen", "vektor", "determinante",
    }
    GEOMETRY_KEYWORDS = {
        "三角", "圆", "椭圆", "双曲线", "抛物线", "面积", "体积", "坐标",
        "triangle", "circle", "ellipse", "hyperbola", "parabola",
        "area", "volume", "coordinate",
        "dreieck", "kreis", "hyperbel", "parabel", "fläche", "volumen",
    }
    for c in concepts.values():
        name_lower = c["canonical_name"].lower()
        if any(kw in name_lower for kw in CALCULUS_KEYWORDS):
            domains["calculus"] += 1
        elif any(kw in name_lower for kw in LINEAR_ALGEBRA_KEYWORDS):
            domains["linear_algebra"] += 1
        elif any(kw in name_lower for kw in GEOMETRY_KEYWORDS):
            domains["geometry"] += 1
        else:
            domains["general"] += 1

    lines.extend([
        "",
        "Domain breakdown:",
        *[f"  {k}: {v}" for k, v in sorted(domains.items())],
        "",
        f"Cross-language concepts: {sum(1 for c in concepts.values() if c['language'] != 'unknown')}",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_path}")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Merge Mimo extraction outputs into consolidated data")
    parser.add_argument("--input-dir", type=str, default="data/math_extractions",
                        help="Directory containing raw extraction JSON files")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory for merged data (default: input-dir/merged)")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    input_dir = (project_root / args.input_dir).resolve()

    if args.output_dir:
        output_dir = (project_root / args.output_dir).resolve()
    else:
        output_dir = input_dir / "merged"

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print()

    # Load
    print("Loading extraction files...")
    extractions, files_loaded = load_extractions(input_dir)
    print(f"  Loaded {len(extractions)} valid extraction files\n")

    if not extractions:
        print("No extraction files found. Run mimo first to produce them.")
        sys.exit(0)

    # Merge concepts
    print("Merging concepts...")
    concepts, concept_conflicts = merge_concepts(extractions)
    print(f"  → {len(concepts)} unique concepts")

    # Merge relations
    print("Merging relations...")
    relations, relation_conflicts = merge_relations(extractions, concepts)
    print(f"  → {len(relations)} unique relations")

    # Detect structural conflicts
    print("Detecting structural conflicts...")
    struct_conflicts = detect_conflicts(concepts, relations)
    all_conflicts = concept_conflicts + relation_conflicts + struct_conflicts

    if all_conflicts:
        print(f"  Warning: {len(all_conflicts)} conflict(s) found")
        for c in all_conflicts:
            print(f"    {c}")
    else:
        print("  No conflicts detected")

    # Write output
    concepts_path = output_dir / "merged_concepts.json"
    relations_path = output_dir / "merged_relations.json"
    report_path = output_dir / "merge_report.txt"

    with open(concepts_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "2.0",
            "merged_at": __import__('datetime').datetime.now().isoformat(),
            "total_concepts": len(concepts),
            "concepts": list(concepts.values()),
        }, f, ensure_ascii=False, indent=2)
    print(f"\nConcepts written to {concepts_path}")

    with open(relations_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "2.0",
            "merged_at": __import__('datetime').datetime.now().isoformat(),
            "total_relations": len(relations),
            "relations": relations,
        }, f, ensure_ascii=False, indent=2)
    print(f"Relations written to {relations_path}")

    write_report(report_path, files_loaded, concepts, relations, all_conflicts)
    print("\nMerge complete.")


if __name__ == "__main__":
    main()
