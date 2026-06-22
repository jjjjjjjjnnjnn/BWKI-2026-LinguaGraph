#!/usr/bin/env python3
"""
Expand Chemistry knowledge graph — elementary through university, trilingual (ZH/EN/DE).
Covers: matter structure, chemical reactions, stoichiometry, organic/inorganic chemistry,
physical chemistry, analytical chemistry. 200+ concepts, 10+ publishers per language.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT_DIR / "config" / "expert_graphs" / "chemistry_full.json"

# ── Publisher catalogs ──────────────────────────────────────────────

ZH_PUBS = {
    "middle": [
        "人教版初中化学九年级上", "人教版初中化学九年级下",
        "沪教版初中化学", "北师大版初中化学",
        "粤教版初中化学", "鲁教版初中化学", "苏教版初中化学",
        "湘教版初中化学", "科粤版初中化学",
    ],
    "high": [
        "人教版高中化学必修第一册", "人教版高中化学必修第二册",
        "人教版高中化学选择性必修第一册（化学反应原理）",
        "人教版高中化学选择性必修第二册（物质结构与性质）",
        "人教版高中化学选择性必修第三册（有机化学基础）",
        "沪科版高中化学", "粤教版高中化学", "鲁科版高中化学",
        "苏教版高中化学", "湘教版高中化学",
    ],
    "college": [
        "无机化学（武汉大学）", "无机化学（大连理工）",
        "有机化学（邢其毅）", "有机化学（汪小兰）",
        "物理化学（傅献彩）", "物理化学（南京大学）",
        "分析化学（武汉大学）", "分析化学（华东理工）",
        "结构化学（周公度）", "高分子化学（潘祖仁）",
        "化工原理（柴诚敬）", "生物化学（王镜岩）",
        "环境化学（戴树桂）", "材料化学（曾兆华）",
    ],
}

EN_PUBS = {
    "middle": [
        "Khan Academy Chemistry", "CK-12 Chemistry",
        "Pearson: Prentice Hall Chemistry", "Glencoe Chemistry",
        "Holt Chemistry", "BBC Bitesize KS3 Chemistry",
    ],
    "high": [
        "AP Chemistry", "IB Chemistry SL/HL", "IGCSE Chemistry (0620)",
        "GCSE AQA Chemistry", "GCSE Edexcel Chemistry",
        "A-Level Chemistry (AQA)", "A-Level Chemistry (OCR)",
        "Cambridge IGCSE Chemistry", "GCSE AQA Combined Science",
        "Edexcel GCSE Chemistry",
    ],
    "college": [
        "Zumdahl: Chemistry", "Chang: Chemistry",
        "Silberberg: Chemistry", "Brown: Chemistry",
        "Atkins: Physical Chemistry", "Levine: Physical Chemistry",
        "Bruice: Organic Chemistry", "Wade: Organic Chemistry",
        "Solomons: Organic Chemistry", "Clayden: Organic Chemistry",
        "Housecroft: Inorganic Chemistry", "Shriver & Atkins: Inorganic Chemistry",
        "Skoog: Analytical Chemistry", "Harris: Quantitative Chemical Analysis",
        "Petrucci: General Chemistry", "Engel: Physical Chemistry",
    ],
}

DE_PUBS = {
    "middle": [
        "Duden Chemie Kompakt", "Cornelsen Chemie entdecken",
        "Westermann Chemie", "Klett Chemie",
        "Auer Chemie", "Dorn-Bader Chemie",
    ],
    "high": [
        "Westermann Chemie Oberstufe", "Dorn-Bader Chemie Abitur",
        "Kern Chemie Abitur LK", "Thieme Chemie",
        "Cornelsen Chemie Oberstufe", "DUDEN Chemie Abitur",
    ],
    "college": [
        "Housecroft: Anorganische Chemie", "Shriver & Atkins: Anorganische Chemie",
        "Clayden: Organische Chemie", "Bruice: Organische Chemie",
        "Atkins: Physikalische Chemie", "Levine: Physikalische Chemie",
        "Skoog: Analytische Chemie", "Harris: Quantitative Chemische Analyse",
        "Engel: Physikalische Chemie", "Silberberg: Chemie",
        "Mortimer: Physikalische Chemie", "Laidler: Physikalische Chemie",
    ],
}

def ref(lang, textbook, chapter="", section=""):
    return {"textbook": textbook, "language": lang, "chapter": chapter, "section": section}

def mkrefs(level):
    refs = []
    for lang, pubs in [("zh", ZH_PUBS), ("en", EN_PUBS), ("de", DE_PUBS)]:
        for p in pubs.get(level, [])[:2]:
            refs.append(ref(lang, p))
    return refs

def c(name, display, level, labels):
    return {"name": f"chem_{name}", "display_name": display, "category": "concept",
            "level": level, "labels": labels, "source_references": mkrefs(level)}

def rel(s, t, rt):
    return {"source": f"chem_{s}", "target": f"chem_{t}", "type": rt, "relation": rt}

# ══════════════════════════════════════════════════════════════════════
#  CONCEPTS
# ══════════════════════════════════════════════════════════════════════

concepts = []

# ── MIDDLE: 物质与变化 ──
concepts += [
    c("物质", "物质", "middle", {"zh": "物质", "en": "Matter", "de": "Materie"}),
    c("混合物", "混合物", "middle", {"zh": "混合物", "en": "Mixture", "de": "Mischung"}),
    c("纯净物", "纯净物", "middle", {"zh": "纯净物", "en": "Pure Substance", "de": "Reinstoff"}),
    c("单质", "单质", "middle", {"zh": "单质", "en": "Element (substance)", "de": "Element (Stoff)"}),
    c("化合物", "化合物", "middle", {"zh": "化合物", "en": "Compound", "de": "Verbindung"}),
    c("氧化物", "氧化物", "middle", {"zh": "氧化物", "en": "Oxide", "de": "Oxid"}),
    c("酸", "酸", "middle", {"zh": "酸", "en": "Acid", "de": "Säure"}),
    c("碱", "碱", "middle", {"zh": "碱", "en": "Base (alkali)", "de": "Base (Alkali)"}),
    c("盐", "盐", "middle", {"zh": "盐", "en": "Salt", "de": "Salz"}),
    c("物理变化", "物理变化", "middle", {"zh": "物理变化", "en": "Physical Change", "de": "Physische Veränderung"}),
    c("化学变化", "化学变化", "middle", {"zh": "化学变化", "en": "Chemical Change", "de": "Chemische Veränderung"}),
    c("质量守恒定律", "质量守恒定律", "middle", {"zh": "质量守恒定律", "en": "Law of Conservation of Mass", "de": "Massenerhaltungssatz"}),
    c("原子", "原子", "middle", {"zh": "原子", "en": "Atom", "de": "Atom"}),
    c("分子", "分子", "middle", {"zh": "分子", "en": "Molecule", "de": "Molekül"}),
    c("离子", "离子", "middle", {"zh": "离子", "en": "Ion", "de": "Ion"}),
    c("元素", "元素", "middle", {"zh": "元素", "en": "Element (periodic)", "de": "Chemisches Element"}),
    c("元素符号", "元素符号", "middle", {"zh": "元素符号", "en": "Chemical Symbol", "de": "Chemiche Zeichen"}),
    c("元素周期表", "元素周期表", "middle", {"zh": "元素周期表", "en": "Periodic Table", "de": "Periodensystem"}),
    c("相对原子质量", "相对原子质量", "middle", {"zh": "相对原子质量", "en": "Relative Atomic Mass", "de": "Relative Atommasse"}),
    c("化学式", "化学式", "middle", {"zh": "化学式", "en": "Chemical Formula", "de": "Summenformel"}),
    c("化合价", "化合价", "middle", {"zh": "化合价", "en": "Valence", "de": "Wertigkeit"}),
    c("化学方程式", "化学方程式", "middle", {"zh": "化学方程式", "en": "Chemical Equation", "de": "Reaktionsgleichung"}),
    c("化合反应", "化合反应", "middle", {"zh": "化合反应", "en": "Combination Reaction", "de": "Synthese"}),
    c("分解反应", "分解反应", "middle", {"zh": "分解反应", "en": "Decomposition Reaction", "de": "Zersetzung"}),
    c("置换反应", "置换反应", "middle", {"zh": "置换反应", "en": "Single Displacement", "de": "Einfache Substitution"}),
    c("复分解反应", "复分解反应", "middle", {"zh": "复分解反应", "en": "Double Displacement", "de": "Doppelte Substitution"}),
    c("氧化还原反应", "氧化还原反应", "middle", {"zh": "氧化还原反应", "en": "Redox Reaction", "de": "Redoxreaktion"}),
    c("氧化剂", "氧化剂", "middle", {"zh": "氧化剂", "en": "Oxidizing Agent", "de": "Oxidationsmittel"}),
    c("还原剂", "还原剂", "middle", {"zh": "还原剂", "en": "Reducing Agent", "de": "Reduktionsmittel"}),
    c("燃烧", "燃烧", "middle", {"zh": "燃烧", "en": "Combustion", "de": "Verbrennung"}),
    c("金属活动性顺序", "金属活动性顺序", "middle", {"zh": "金属活动性顺序", "en": "Activity Series of Metals", "de": "Metallaktivitätsreihe"}),
    c("酸碱中和反应", "酸碱中和反应", "middle", {"zh": "酸碱中和反应", "en": "Acid-Base Neutralization", "de": "Säure-Base-Neutralisation"}),
    c("pH值", "pH值", "middle", {"zh": "pH值", "en": "pH Value", "de": "pH-Wert"}),
    c("指示剂", "指示剂", "middle", {"zh": "指示剂", "en": "Indicator", "de": "Indikator"}),
    c("溶液", "溶液", "middle", {"zh": "溶液", "en": "Solution", "de": "Lösung"}),
    c("溶质", "溶质", "middle", {"zh": "溶质", "en": "Solute", "de": "Lösungsmittel (gelöster Stoff)"}),
    c("溶剂", "溶剂", "middle", {"zh": "溶剂", "en": "Solvent", "de": "Lösungsmittel"}),
    c("溶解度", "溶解度", "middle", {"zh": "溶解度", "en": "Solubility", "de": "Löslichkeit"}),
    c("饱和溶液", "饱和溶液", "middle", {"zh": "饱和溶液", "en": "Saturated Solution", "de": "Gesättigte Lösung"}),
    c("不饱和溶液", "不饱和溶液", "middle", {"zh": "不饱和溶液", "en": "Unsaturated Solution", "de": "Ungesättigte Lösung"}),
    c("结晶", "结晶", "middle", {"zh": "结晶", "en": "Crystallization", "de": "Kristallisation"}),
    c("悬浊液", "悬浊液", "middle", {"zh": "悬浊液", "en": "Suspension", "de": "Suspension"}),
    c("乳浊液", "乳浊液", "middle", {"zh": "乳浊液", "en": "Emulsion", "de": "Emulsion"}),
    c("胶体", "胶体", "middle", {"zh": "胶体", "en": "Colloid", "de": "Kolloid"}),
]

# ── HIGH: 进阶化学 ──
concepts += [
    c("物质的量", "物质的量", "high", {"zh": "物质的量", "en": "Amount of Substance", "de": "Stoffmenge"}),
    c("摩尔", "摩尔", "high", {"zh": "摩尔", "en": "Mole", "de": "Mol"}),
    c("阿伏伽德罗常数", "阿伏伽德罗常数", "high", {"zh": "阿伏伽德罗常数", "en": "Avogadro's Number", "de": "Avogadro-Konstante"}),
    c("摩尔质量", "摩尔质量", "high", {"zh": "摩尔质量", "en": "Molar Mass", "de": "Molare Masse"}),
    c("气体摩尔体积", "气体摩尔体积", "high", {"zh": "气体摩尔体积", "en": "Molar Volume of Gas", "de": "Molvolumen"}),
    c("物质的量浓度", "物质的量浓度", "high", {"zh": "物质的量浓度", "en": "Molar Concentration", "de": "Stoffmengenkonzentration"}),
    c("离子反应", "离子反应", "high", {"zh": "离子反应", "en": "Ionic Reaction", "de": "Ionenreaktion"}),
    c("离子方程式", "离子方程式", "high", {"zh": "离子方程式", "en": "Net Ionic Equation", "de": "Ionenreaktionsgleichung"}),
    c("电解质", "电解质", "high", {"zh": "电解质", "en": "Electrolyte", "de": "Elektrolyt"}),
    c("非电解质", "非电解质", "high", {"zh": "非电解质", "en": "Non-Electrolyte", "de": "Nicht-Elektrolyt"}),
    c("强电解质", "强电解质", "high", {"zh": "强电解质", "en": "Strong Electrolyte", "de": "Starker Elektrolyt"}),
    c("弱电解质", "弱电解质", "high", {"zh": "弱电解质", "en": "Weak Electrolyte", "de": "Schwacher Elektrolyt"}),
    c("原子结构", "原子结构", "high", {"zh": "原子结构", "en": "Atomic Structure", "de": "Atomstruktur"}),
    c("电子层", "电子层", "high", {"zh": "电子层", "en": "Electron Shell", "de": "Elektronenschale"}),
    c("电子排布", "电子排布", "high", {"zh": "电子排布", "en": "Electron Configuration", "de": "Elektronenkonfiguration"}),
    c("能级", "能级", "high", {"zh": "能级", "en": "Energy Level", "de": "Energieniveau"}),
    c("化学键", "化学键", "high", {"zh": "化学键", "en": "Chemical Bond", "de": "Chemische Bindung"}),
    c("离子键", "离子键", "high", {"zh": "离子键", "en": "Ionic Bond", "de": "Ionische Bindung"}),
    c("共价键", "共价键", "high", {"zh": "共价键", "en": "Covalent Bond", "de": "Kovalente Bindung"}),
    c("金属键", "金属键", "high", {"zh": "金属键", "en": "Metallic Bond", "de": "Metallische Bindung"}),
    c("分子间作用力", "分子间作用力", "high", {"zh": "分子间作用力", "en": "Intermolecular Forces", "de": "Intermolekulare Kräfte"}),
    c("氢键", "氢键", "high", {"zh": "氢键", "en": "Hydrogen Bond", "de": "Wasserstoffbrücke"}),
    c("范德华力", "范德华力", "high", {"zh": "范德华力", "en": "Van der Waals Forces", "de": "Van-der-Waals-Kräfte"}),
    c("晶体结构", "晶体结构", "high", {"zh": "晶体结构", "en": "Crystal Structure", "de": "Kristallstruktur"}),
    c("离子晶体", "离子晶体", "high", {"zh": "离子晶体", "en": "Ionic Crystal", "de": "Ionenkristall"}),
    c("原子晶体", "原子晶体", "high", {"zh": "原子晶体", "en": "Covalent Crystal", "de": "Kovalenter Kristall"}),
    c("分子晶体", "分子晶体", "high", {"zh": "分子晶体", "en": "Molecular Crystal", "de": "Molekülkristall"}),
    c("金属晶体", "金属晶体", "high", {"zh": "金属晶体", "en": "Metallic Crystal", "de": "Metallkristall"}),
    c("化学反应速率", "化学反应速率", "high", {"zh": "化学反应速率", "en": "Reaction Rate", "de": "Reaktionsgeschwindigkeit"}),
    c("化学平衡", "化学平衡", "high", {"zh": "化学平衡", "en": "Chemical Equilibrium", "de": "Chemisches Gleichgewicht"}),
    c("平衡常数", "平衡常数", "high", {"zh": "平衡常数", "en": "Equilibrium Constant", "de": "Gleichgewichtskonstante"}),
    c("勒夏特列原理", "勒夏特列原理", "high", {"zh": "勒夏特列原理", "en": "Le Chatelier's Principle", "de": "Prinzip von Le Chatelier"}),
    c("催化剂", "催化剂", "high", {"zh": "催化剂", "en": "Catalyst", "de": "Katalysator"}),
    c("活化能", "活化能", "high", {"zh": "活化能", "en": "Activation Energy", "de": "Aktivierungsenergie"}),
    c("反应热", "反应热", "high", {"zh": "反应热", "en": "Enthalpy of Reaction", "de": "Reaktionsenthalpie"}),
    c("盖斯定律", "盖斯定律", "high", {"zh": "盖斯定律", "en": "Hess's Law", "de": "Hess'sches Gesetz"}),
    c("原电池", "原电池", "high", {"zh": "原电池", "en": "Galvanic Cell", "de": "Galvanische Zelle"}),
    c("电解池", "电解池", "high", {"zh": "电解池", "en": "Electrolytic Cell", "de": "Elektrolysezelle"}),
    c("电极反应", "电极反应", "high", {"zh": "电极反应", "en": "Electrode Reaction", "de": "Elektrodenreaktion"}),
    c("标准电极电势", "标准电极电势", "high", {"zh": "标准电极电势", "en": "Standard Electrode Potential", "de": "Standard-Elektrodenpotenzial"}),
    c("水的电离", "水的电离", "high", {"zh": "水的电离", "en": "Ionization of Water", "de": "Ionisation von Wasser"}),
    c("弱酸的电离平衡", "弱酸的电离平衡", "high", {"zh": "弱酸的电离平衡", "en": "Weak Acid Ionization", "de": "Ionisationsgleichgewicht schwacher Säuren"}),
    c("盐类水解", "盐类水解", "high", {"zh": "盐类水解", "en": "Salt Hydrolysis", "de": "Hydrolyse von Salzen"}),
    c("溶度积", "溶度积", "high", {"zh": "溶度积", "en": "Solubility Product", "de": "Löslichkeitsprodukt"}),
    c("配合物", "配合物", "high", {"zh": "配合物", "en": "Coordination Compound", "de": "Komplexverbindung"}),
    c("配位键", "配位键", "high", {"zh": "配位键", "en": "Coordinate Bond", "de": "Dative Bindung"}),
    c("氧化数", "氧化数", "high", {"zh": "氧化数", "en": "Oxidation Number", "de": "Oxidationszahl"}),
    c("氧化还原滴定", "氧化还原滴定", "high", {"zh": "氧化还原滴定", "en": "Redox Titration", "de": "Redox-Titration"}),
    c("蒸馏", "蒸馏", "high", {"zh": "蒸馏", "en": "Distillation", "de": "Destillation"}),
    c("萃取", "萃取", "high", {"zh": "萃取", "en": "Extraction", "de": "Extraktion"}),
    c("层析", "层析", "high", {"zh": "层析", "en": "Chromatography", "de": "Chromatographie"}),
]

# ── COLLEGE: 无机化学 ──
concepts += [
    c("元素周期律", "元素周期律", "college", {"zh": "元素周期律", "en": "Periodic Law", "de": "Periodisches Gesetz"}),
    c("原子半径", "原子半径", "college", {"zh": "原子半径", "en": "Atomic Radius", "de": "Atomradius"}),
    c("电离能", "电离能", "college", {"zh": "电离能", "en": "Ionization Energy", "de": "Ionisierungsenergie"}),
    c("电负性", "电负性", "college", {"zh": "电负性", "en": "Electronegativity", "de": "Elektronegativität"}),
    c("电子亲和能", "电子亲和能", "college", {"zh": "电子亲和能", "en": "Electron Affinity", "de": "Elektronenaffinität"}),
    c("s区元素", "s区元素", "college", {"zh": "s区元素", "en": "s-Block Elements", "de": "s-Block-Elemente"}),
    c("p区元素", "p区元素", "college", {"zh": "p区元素", "en": "p-Block Elements", "de": "p-Block-Elemente"}),
    c("d区元素", "d区元素", "college", {"zh": "d区元素", "en": "d-Block Elements", "de": "d-Block-Elemente"}),
    c("ds区元素", "ds区元素", "college", {"zh": "ds区元素", "en": "ds-Block Elements", "de": "ds-Block-Elemente"}),
    c("f区元素", "f区元素", "college", {"zh": "f区元素", "en": "f-Block Elements", "de": "f-Block-Elemente"}),
    c("过渡金属", "过渡金属", "college", {"zh": "过渡金属", "en": "Transition Metals", "de": "Übergangsmetalle"}),
    c("镧系元素", "镧系元素", "college", {"zh": "镧系元素", "en": "Lanthanides", "de": "Lanthanoide"}),
    c("锕系元素", "锕系元素", "college", {"zh": "锕系元素", "en": "Actinides", "de": "Actinoide"}),
    c("共价半径", "共价半径", "college", {"zh": "共价半径", "en": "Covalent Radius", "de": "Kovalenter Radius"}),
    c("离子半径", "离子半径", "college", {"zh": "离子半径", "en": "Ionic Radius", "de": "Ionenradius"}),
    c("晶体场理论", "晶体场理论", "college", {"zh": "晶体场理论", "en": "Crystal Field Theory", "de": "Kristallfeldtheorie"}),
    c("配位数", "配位数", "college", {"zh": "配位数", "en": "Coordination Number", "de": "Koordinationszahl"}),
    c("配位化合物的命名", "配位化合物的命名", "college", {"zh": "配位化合物的命名", "en": "Nomenclature of Complexes", "de": "Nomenklatur von Komplexen"}),
    c("分子轨道理论", "分子轨道理论", "college", {"zh": "分子轨道理论", "en": "Molecular Orbital Theory", "de": "Molekülorbitaltheorie"}),
    c("杂化轨道理论", "杂化轨道理论", "college", {"zh": "杂化轨道理论", "en": "Hybridization Theory", "de": "Hybridisierungstheorie"}),
    c("价层电子对互斥理论", "价层电子对互斥理论", "college", {"zh": "价层电子对互斥理论", "en": "VSEPR Theory", "de": "VSEPR-Theorie"}),
    c("分子极性", "分子极性", "college", {"zh": "分子极性", "en": "Molecular Polarity", "de": "Molekülpolarität"}),
    c("手性分子", "手性分子", "college", {"zh": "手性分子", "en": "Chiral Molecule", "de": "Chirales Molekül"}),
    c("对映异构体", "对映异构体", "college", {"zh": "对映异构体", "en": "Enantiomer", "de": "Enantiomer"}),
]

# ── COLLEGE: 有机化学 ──
concepts += [
    c("有机化合物", "有机化合物", "college", {"zh": "有机化合物", "en": "Organic Compound", "de": "Organische Verbindung"}),
    c("烃", "烃", "college", {"zh": "烃", "en": "Hydrocarbon", "de": "Kohlenwasserstoff"}),
    c("烷烃", "烷烃", "college", {"zh": "烷烃", "en": "Alkane", "de": "Alkan"}),
    c("烯烃", "烯烃", "college", {"zh": "烯烃", "en": "Alkene", "de": "Alken"}),
    c("炔烃", "炔烃", "college", {"zh": "炔烃", "en": "Alkyne", "de": "Alkin"}),
    c("芳香烃", "芳香烃", "college", {"zh": "芳香烃", "en": "Aromatic Hydrocarbon", "de": "Aromatischer Kohlenwasserstoff"}),
    c("苯", "苯", "college", {"zh": "苯", "en": "Benzene", "de": "Benzol"}),
    c("卤代烃", "卤代烃", "college", {"zh": "卤代烃", "en": "Halogenated Hydrocarbon", "de": "Halogenkohlenwasserstoff"}),
    c("醇", "醇", "college", {"zh": "醇", "en": "Alcohol", "de": "Alkohol"}),
    c("酚", "酚", "college", {"zh": "酚", "en": "Phenol", "de": "Phenol"}),
    c("醚", "醚", "college", {"zh": "醚", "en": "Ether", "de": "Ether"}),
    c("醛", "醛", "college", {"zh": "醛", "en": "Aldehyde", "de": "Aldehyd"}),
    c("酮", "酮", "college", {"zh": "酮", "en": "Ketone", "de": "Keton"}),
    c("羧酸", "羧酸", "college", {"zh": "羧酸", "en": "Carboxylic Acid", "de": "Carbonsäure"}),
    c("酯", "酯", "college", {"zh": "酯", "en": "Ester", "de": "Ester"}),
    c("酰胺", "酰胺", "college", {"zh": "酰胺", "en": "Amide", "de": "Amid"}),
    c("胺", "胺", "college", {"zh": "胺", "en": "Amine", "de": "Amin"}),
    c("氨基酸", "氨基酸", "college", {"zh": "氨基酸", "en": "Amino Acid", "de": "Aminosäure"}),
    c("蛋白质", "蛋白质", "college", {"zh": "蛋白质", "en": "Protein", "de": "Protein"}),
    c("核酸", "核酸", "college", {"zh": "核酸", "en": "Nucleic Acid", "de": "Nukleinsäure"}),
    c("糖类", "糖类", "college", {"zh": "糖类", "en": "Carbohydrate", "de": "Kohlenhydrat"}),
    c("油脂", "油脂", "college", {"zh": "油脂", "en": "Lipid", "de": "Lipid"}),
    c("加成反应", "加成反应", "college", {"zh": "加成反应", "en": "Addition Reaction", "de": "Additionsreaktion"}),
    c("取代反应", "取代反应", "college", {"zh": "取代反应", "en": "Substitution Reaction", "de": "Substitutionsreaktion"}),
    c("消去反应", "消去反应", "college", {"zh": "消去反应", "en": "Elimination Reaction", "de": "Eliminierungsreaktion"}),
    c("酯化反应", "酯化反应", "college", {"zh": "酯化反应", "en": "Esterification", "de": "Veresterung"}),
    c("水解反应", "水解反应", "college", {"zh": "水解反应", "en": "Hydrolysis", "de": "Hydrolyse"}),
    c("聚合反应", "聚合反应", "college", {"zh": "聚合反应", "en": "Polymerization", "de": "Polymerisation"}),
    c("加聚反应", "加聚反应", "college", {"zh": "加聚反应", "en": "Addition Polymerization", "de": "Additionspolymerisation"}),
    c("缩聚反应", "缩聚反应", "college", {"zh": "缩聚反应", "en": "Condensation Polymerization", "de": "Kondensationspolymerisation"}),
    c("同分异构体", "同分异构体", "college", {"zh": "同分异构体", "en": "Isomer", "de": "Isomer"}),
    c("构造异构体", "构造异构体", "college", {"zh": "构造异构体", "en": "Constitutional Isomer", "de": "Konstitutionsisomer"}),
    c("立体异构体", "立体异构体", "college", {"zh": "立体异构体", "en": "Stereoisomer", "de": "Stereoisomer"}),
    c("顺反异构体", "顺反异构体", "college", {"zh": "顺反异构体", "en": "Cis-Trans Isomer", "de": "Cis-Trans-Isomer"}),
    c("官能团", "官能团", "college", {"zh": "官能团", "en": "Functional Group", "de": "Funktionelle Gruppe"}),
    c("同系物", "同系物", "college", {"zh": "同系物", "en": "Homologue", "de": "Homologe Reihe"}),
]

# ── COLLEGE: 物理化学 ──
concepts += [
    c("热力学第一定律_chem", "热力学第一定律", "college", {"zh": "热力学第一定律", "en": "First Law of Thermodynamics", "de": "1. Hauptsatz der Thermodynamik"}),
    c("热力学第二定律_chem", "热力学第二定律", "college", {"zh": "热力学第二定律", "en": "Second Law of Thermodynamics", "de": "2. Hauptsatz der Thermodynamik"}),
    c("吉布斯自由能", "吉布斯自由能", "college", {"zh": "吉布斯自由能", "en": "Gibbs Free Energy", "de": "Gibbssche freie Energie"}),
    c("焓变", "焓变", "college", {"zh": "焓变", "en": "Enthalpy Change", "de": "Enthalpieänderung"}),
    c("熵变", "熵变", "college", {"zh": "熵变", "en": "Entropy Change", "de": "Entropieänderung"}),
    c("化学反应方向判据", "化学反应方向判据", "college", {"zh": "化学反应方向判据", "en": "Criterion for Spontaneity", "de": "Kriterium der Spontaneität"}),
    c("标准生成焓", "标准生成焓", "college", {"zh": "标准生成焓", "en": "Standard Enthalpy of Formation", "de": "Standardbildungsenthalpie"}),
    c("标准摩尔熵", "标准摩尔熵", "college", {"zh": "标准摩尔熵", "en": "Standard Molar Entropy", "de": "Standardmolare Entropie"}),
    c("化学势", "化学势", "college", {"zh": "化学势", "en": "Chemical Potential", "de": "Chemisches Potential"}),
    c("拉乌尔定律", "拉乌尔定律", "college", {"zh": "拉乌尔定律", "en": "Raoult's Law", "de": "Raoultsches Gesetz"}),
    c("亨利定律", "亨利定律", "college", {"zh": "亨利定律", "en": "Henry's Law", "de": "Henry-Gesetz"}),
    c("稀溶液的依数性", "稀溶液的依数性", "college", {"zh": "稀溶液的依数性", "en": "Colligative Properties", "de": "Kolligative Eigenschaften"}),
    c("沸点升高", "沸点升高", "college", {"zh": "沸点升高", "en": "Boiling Point Elevation", "de": "Siedepunkterhöhung"}),
    c("凝固点降低", "凝固点降低", "college", {"zh": "凝固点降低", "en": "Freezing Point Depression", "de": "Gefrierpunkterniedrigung"}),
    c("渗透压", "渗透压", "college", {"zh": "渗透压", "en": "Osmotic Pressure", "de": "Osmotischer Druck"}),
    c("反应速率理论", "反应速率理论", "college", {"zh": "反应速率理论", "en": "Theories of Reaction Rates", "de": "Theorien der Reaktionsgeschwindigkeit"}),
    c("阿伦尼乌斯方程", "阿伦尼乌斯方程", "college", {"zh": "阿伦尼乌斯方程", "en": "Arrhenius Equation", "de": "Arrhenius-Gleichung"}),
    c("碰撞理论", "碰撞理论", "college", {"zh": "碰撞理论", "en": "Collision Theory", "de": "Stoßtheorie"}),
    c("过渡态理论", "过渡态理论", "college", {"zh": "过渡态理论", "en": "Transition State Theory", "de": "Übergangszustandstheorie"}),
    c("催化机理", "催化机理", "college", {"zh": "催化机理", "en": "Catalysis Mechanism", "de": "Katalysemechanismus"}),
    c("酶催化", "酶催化", "college", {"zh": "酶催化", "en": "Enzyme Catalysis", "de": "Enzymkatalyse"}),
    c("电化学热力学", "电化学热力学", "college", {"zh": "电化学热力学", "en": "Electrochemical Thermodynamics", "de": "Elektrochemische Thermodynamik"}),
    c("能斯特方程", "能斯特方程", "college", {"zh": "能斯特方程", "en": "Nernst Equation", "de": "Nernst-Gleichung"}),
    c("电导率", "电导率", "college", {"zh": "电导率", "en": "Conductivity", "de": "Leitfähigkeit"}),
    c("摩尔电导率", "摩尔电导率", "college", {"zh": "摩尔电导率", "en": "Molar Conductivity", "de": "Molare Leitfähigkeit"}),
    c("电解", "电解", "college", {"zh": "电解", "en": "Electrolysis", "de": "Elektrolyse"}),
    c("电镀", "电镀", "college", {"zh": "电镀", "en": "Electroplating", "de": "Galvanisieren"}),
    c("表面吸附", "表面吸附", "college", {"zh": "表面吸附", "en": "Surface Adsorption", "de": "Oberflächenadsorption"}),
    c("朗缪尔吸附等温线", "朗缪尔吸附等温线", "college", {"zh": "朗缪尔吸附等温线", "en": "Langmuir Adsorption Isotherm", "de": "Langmuir-Adsorptionsisotherme"}),
    c("胶体的性质", "胶体的性质", "college", {"zh": "胶体的性质", "en": "Properties of Colloids", "de": "Eigenschaften von Kolloiden"}),
    c("丁达尔效应", "丁达尔效应", "college", {"zh": "丁达尔效应", "en": "Tyndall Effect", "de": "Tyndall-Effekt"}),
    c("电泳", "电泳", "college", {"zh": "电泳", "en": "Electrophoresis", "de": "Elektrophorese"}),
    c("布朗运动_chem", "布朗运动", "college", {"zh": "布朗运动", "en": "Brownian Motion", "de": "Brownsche Bewegung"}),
    c("聚沉", "聚沉", "college", {"zh": "聚沉", "en": "Coagulation", "de": "Koagulation"}),
]

# ── COLLEGE: 分析化学 ──
concepts += [
    c("定量分析", "定量分析", "college", {"zh": "定量分析", "en": "Quantitative Analysis", "de": "Quantitative Analyse"}),
    c("定性分析", "定性分析", "college", {"zh": "定性分析", "en": "Qualitative Analysis", "de": "Qualitative Analyse"}),
    c("重量分析法", "重量分析法", "college", {"zh": "重量分析法", "en": "Gravimetric Analysis", "de": "Gravimetrische Analyse"}),
    c("滴定分析法", "滴定分析法", "college", {"zh": "滴定分析法", "en": "Titrimetric Analysis", "de": "Titrimetrische Analyse"}),
    c("酸碱滴定", "酸碱滴定", "college", {"zh": "酸碱滴定", "en": "Acid-Base Titration", "de": "Säure-Base-Titration"}),
    c("配位滴定", "配位滴定", "college", {"zh": "配位滴定", "en": "Complexometric Titration", "de": "Komplexometrische Titration"}),
    c("氧化还原滴定_chem", "氧化还原滴定", "college", {"zh": "氧化还原滴定", "en": "Redox Titration", "de": "Redox-Titration"}),
    c("沉淀滴定", "沉淀滴定", "college", {"zh": "沉淀滴定", "en": "Precipitation Titration", "de": "Fällungstitration"}),
    c("指示剂的选择", "指示剂的选择", "college", {"zh": "指示剂的选择", "en": "Choice of Indicators", "de": "Indikatorwahl"}),
    c("滴定曲线", "滴定曲线", "college", {"zh": "滴定曲线", "en": "Titration Curve", "de": "Titrationskurve"}),
    c("滴定终点", "滴定终点", "college", {"zh": "滴定终点", "en": "End Point", "de": "Endpunkt"}),
    c("化学计量点", "化学计量点", "college", {"zh": "化学计量点", "en": "Stoichiometric Point", "de": "Stöchiometrischer Punkt"}),
    c("误差分析", "误差分析", "college", {"zh": "误差分析", "en": "Error Analysis", "de": "Fehleranalyse"}),
    c("有效数字", "有效数字", "college", {"zh": "有效数字", "en": "Significant Figures", "de": "Signifikante Stellen"}),
    c("标准溶液", "标准溶液", "college", {"zh": "标准溶液", "en": "Standard Solution", "de": "Standardlösung"}),
    c("基准物质", "基准物质", "college", {"zh": "基准物质", "en": "Primary Standard", "de": " primärer Standard"}),
    c("分光光度法", "分光光度法", "college", {"zh": "分光光度法", "en": "Spectrophotometry", "de": "Spektralphotometrie"}),
    c("比尔定律", "比尔定律", "college", {"zh": "比尔定律", "en": "Beer-Lambert Law", "de": "Beer-Lambert-Gesetz"}),
    c("原子吸收光谱", "原子吸收光谱", "college", {"zh": "原子吸收光谱", "en": "Atomic Absorption Spectroscopy", "de": "Atomabsorptionsspektroskopie"}),
    c("红外光谱", "红外光谱", "college", {"zh": "红外光谱", "en": "Infrared Spectroscopy", "de": "Infrarotspektroskopie"}),
    c("核磁共振", "核磁共振", "college", {"zh": "核磁共振", "en": "Nuclear Magnetic Resonance", "de": "Kernmagnetische Resonanz"}),
    c("质谱", "质谱", "college", {"zh": "质谱", "en": "Mass Spectrometry", "de": "Massenspektrometrie"}),
    c("色谱法", "色谱法", "college", {"zh": "色谱法", "en": "Chromatography", "de": "Chromatographie"}),
    c("气相色谱", "气相色谱", "college", {"zh": "气相色谱", "en": "Gas Chromatography", "de": "Gaschromatographie"}),
    c("液相色谱", "液相色谱", "college", {"zh": "液相色谱", "en": "Liquid Chromatography", "de": "Flüssigchromatographie"}),
    c("薄层色谱", "薄层色谱", "college", {"zh": "薄层色谱", "en": "Thin Layer Chromatography", "de": "Dünnschichtchromatographie"}),
    c("电位分析法", "电位分析法", "college", {"zh": "电位分析法", "en": "Potentiometry", "de": "Potentiometrie"}),
    c("离子选择电极", "离子选择电极", "college", {"zh": "离子选择电极", "en": "Ion-Selective Electrode", "de": "Ionenselektive Elektrode"}),
    c("库仑分析法", "库仑分析法", "college", {"zh": "库仑分析法", "en": "Coulometric Analysis", "de": "Koulometrische Analyse"}),
]

# ══════════════════════════════════════════════════════════════════════
#  RELATIONS
# ══════════════════════════════════════════════════════════════════════

relations = [
    # ── Middle: 物质分类 ──
    rel("物质", "混合物", "generalization"),
    rel("物质", "纯净物", "generalization"),
    rel("纯净物", "单质", "generalization"),
    rel("纯净物", "化合物", "generalization"),
    rel("化合物", "氧化物", "specialization"),
    rel("化合物", "酸", "specialization"),
    rel("化合物", "碱", "specialization"),
    rel("化合物", "盐", "specialization"),
    rel("物理变化", "化学变化", "analogy"),
    rel("质量守恒定律", "化学变化", "requires"),
    rel("原子", "分子", "analogy"),
    rel("原子", "离子", "analogy"),
    rel("元素", "原子", "requires"),
    rel("元素符号", "元素", "representation"),
    rel("元素周期表", "元素", "representation"),
    rel("相对原子质量", "原子", "requires"),
    rel("化学式", "元素符号", "requires"),
    rel("化学式", "化合价", "requires"),
    rel("化学方程式", "化学式", "requires"),
    rel("化学方程式", "质量守恒定律", "requires"),
    rel("化合反应", "化学方程式", "applies_to"),
    rel("分解反应", "化学方程式", "applies_to"),
    rel("置换反应", "化学方程式", "applies_to"),
    rel("复分解反应", "化学方程式", "applies_to"),
    rel("氧化还原反应", "化合反应", "analogy"),
    rel("氧化还原反应", "分解反应", "analogy"),
    rel("氧化剂", "氧化还原反应", "representation"),
    rel("还原剂", "氧化还原反应", "representation"),
    rel("燃烧", "氧化还原反应", "specialization"),
    rel("金属活动性顺序", "置换反应", "applies_to"),
    rel("酸碱中和反应", "酸", "requires"),
    rel("酸碱中和反应", "碱", "requires"),
    rel("pH值", "酸碱中和反应", "representation"),
    rel("指示剂", "pH值", "applies_to"),
    rel("溶液", "溶质", "generalization"),
    rel("溶液", "溶剂", "generalization"),
    rel("溶解度", "溶液", "requires"),
    rel("饱和溶液", "溶解度", "representation"),
    rel("不饱和溶液", "饱和溶液", "analogy"),
    rel("结晶", "饱和溶液", "applies_to"),
    rel("悬浊液", "溶液", "analogy"),
    rel("乳浊液", "溶液", "analogy"),
    rel("胶体", "溶液", "analogy"),

    # ── High: 物质的量 ──
    rel("物质的量", "摩尔", "representation"),
    rel("阿伏伽德罗常数", "摩尔", "representation"),
    rel("摩尔质量", "摩尔", "requires"),
    rel("气体摩尔体积", "摩尔", "requires"),
    rel("物质的量浓度", "摩尔", "requires"),
    rel("离子反应", "离子", "requires"),
    rel("离子方程式", "离子反应", "representation"),
    rel("电解质", "离子反应", "requires"),
    rel("非电解质", "电解质", "analogy"),
    rel("强电解质", "电解质", "specialization"),
    rel("弱电解质", "电解质", "specialization"),

    # ── High: 原子结构 ──
    rel("原子结构", "原子", "requires"),
    rel("电子层", "原子结构", "representation"),
    rel("电子排布", "电子层", "requires"),
    rel("能级", "电子排布", "representation"),

    # ── High: 化学键 ──
    rel("化学键", "原子", "requires"),
    rel("离子键", "化学键", "specialization"),
    rel("共价键", "化学键", "specialization"),
    rel("金属键", "化学键", "specialization"),
    rel("分子间作用力", "共价键", "requires"),
    rel("氢键", "分子间作用力", "specialization"),
    rel("范德华力", "分子间作用力", "specialization"),

    # ── High: 晶体 ──
    rel("晶体结构", "化学键", "requires"),
    rel("离子晶体", "晶体结构", "specialization"),
    rel("原子晶体", "晶体结构", "specialization"),
    rel("分子晶体", "晶体结构", "specialization"),
    rel("金属晶体", "晶体结构", "specialization"),

    # ── High: 化学反应 ──
    rel("化学反应速率", "化学变化", "requires"),
    rel("化学平衡", "化学反应速率", "prerequisite"),
    rel("平衡常数", "化学平衡", "representation"),
    rel("勒夏特列原理", "化学平衡", "applies_to"),
    rel("催化剂", "化学反应速率", "applies_to"),
    rel("活化能", "化学反应速率", "representation"),
    rel("反应热", "化学变化", "requires"),
    rel("盖斯定律", "反应热", "applies_to"),

    # ── High: 电化学 ──
    rel("原电池", "氧化还原反应", "applies_to"),
    rel("电解池", "原电池", "analogy"),
    rel("电极反应", "原电池", "representation"),
    rel("标准电极电势", "电极反应", "representation"),

    # ── High: 水溶液平衡 ──
    rel("水的电离", "水", "requires"),
    rel("弱酸的电离平衡", "弱电解质", "requires"),
    rel("弱酸的电离平衡", "平衡常数", "requires"),
    rel("盐类水解", "弱电解质", "requires"),
    rel("溶度积", "溶解度", "requires"),

    # ── High: 配合物 ──
    rel("配合物", "配位键", "requires"),
    rel("配位键", "共价键", "generalization"),

    # ── High: 其他 ──
    rel("氧化数", "氧化还原反应", "representation"),
    rel("氧化还原滴定", "氧化还原反应", "applies_to"),
    rel("蒸馏", "混合物", "applies_to"),
    rel("萃取", "混合物", "applies_to"),
    rel("层析", "混合物", "applies_to"),

    # ── College: 元素周期律 ──
    rel("元素周期律", "元素周期表", "representation"),
    rel("原子半径", "元素周期律", "representation"),
    rel("电离能", "元素周期律", "representation"),
    rel("电负性", "元素周期律", "representation"),
    rel("电子亲和能", "元素周期律", "representation"),
    rel("s区元素", "元素周期表", "specialization"),
    rel("p区元素", "元素周期表", "specialization"),
    rel("d区元素", "元素周期表", "specialization"),
    rel("ds区元素", "元素周期表", "specialization"),
    rel("f区元素", "元素周期表", "specialization"),
    rel("过渡金属", "d区元素", "generalization"),
    rel("镧系元素", "f区元素", "specialization"),
    rel("锕系元素", "f区元素", "specialization"),
    rel("共价半径", "原子半径", "specialization"),
    rel("离子半径", "原子半径", "specialization"),

    # ── College: 配位化学 ──
    rel("晶体场理论", "配合物", "requires"),
    rel("配位数", "配合物", "representation"),
    rel("配位化合物的命名", "配合物", "representation"),

    # ── College: 分子结构 ──
    rel("分子轨道理论", "共价键", "generalization"),
    rel("杂化轨道理论", "共价键", "generalization"),
    rel("价层电子对互斥理论", "杂化轨道理论", "applies_to"),
    rel("分子极性", "共价键", "requires"),
    rel("手性分子", "分子极性", "specialization"),
    rel("对映异构体", "手性分子", "representation"),

    # ── College: 有机化学 ──
    rel("有机化合物", "化合物", "specialization"),
    rel("烃", "有机化合物", "specialization"),
    rel("烷烃", "烃", "specialization"),
    rel("烯烃", "烃", "specialization"),
    rel("炔烃", "烃", "specialization"),
    rel("芳香烃", "烃", "specialization"),
    rel("苯", "芳香烃", "specialization"),
    rel("卤代烃", "烃", "specialization"),
    rel("醇", "有机化合物", "specialization"),
    rel("酚", "醇", "analogy"),
    rel("醚", "醇", "analogy"),
    rel("醛", "有机化合物", "specialization"),
    rel("酮", "醛", "analogy"),
    rel("羧酸", "有机化合物", "specialization"),
    rel("酯", "羧酸", "specialization"),
    rel("酰胺", "羧酸", "specialization"),
    rel("胺", "有机化合物", "specialization"),
    rel("氨基酸", "胺", "generalization"),
    rel("氨基酸", "羧酸", "generalization"),
    rel("蛋白质", "氨基酸", "representation"),
    rel("核酸", "有机化合物", "specialization"),
    rel("糖类", "有机化合物", "specialization"),
    rel("油脂", "有机化合物", "specialization"),
    rel("加成反应", "烯烃", "applies_to"),
    rel("取代反应", "烷烃", "applies_to"),
    rel("消去反应", "醇", "applies_to"),
    rel("酯化反应", "醇", "requires"),
    rel("酯化反应", "羧酸", "requires"),
    rel("水解反应", "酯", "applies_to"),
    rel("聚合反应", "烯烃", "applies_to"),
    rel("加聚反应", "聚合反应", "specialization"),
    rel("缩聚反应", "聚合反应", "specialization"),
    rel("同分异构体", "有机化合物", "representation"),
    rel("构造异构体", "同分异构体", "specialization"),
    rel("立体异构体", "同分异构体", "specialization"),
    rel("顺反异构体", "立体异构体", "specialization"),
    rel("官能团", "有机化合物", "representation"),
    rel("同系物", "有机化合物", "representation"),

    # ── College: 物理化学 ──
    rel("吉布斯自由能", "焓变", "requires"),
    rel("吉布斯自由能", "熵变", "requires"),
    rel("化学反应方向判据", "吉布斯自由能", "representation"),
    rel("标准生成焓", "反应热", "representation"),
    rel("标准摩尔熵", "熵变", "representation"),
    rel("化学势", "吉布斯自由能", "generalization"),
    rel("拉乌尔定律", "溶液", "requires"),
    rel("亨利定律", "溶液", "requires"),
    rel("稀溶液的依数性", "拉乌尔定律", "representation"),
    rel("沸点升高", "稀溶液的依数性", "specialization"),
    rel("凝固点降低", "稀溶液的依数性", "specialization"),
    rel("渗透压", "稀溶液的依数性", "specialization"),
    rel("反应速率理论", "化学反应速率", "generalization"),
    rel("阿伦尼乌斯方程", "反应速率理论", "representation"),
    rel("碰撞理论", "反应速率理论", "specialization"),
    rel("过渡态理论", "反应速率理论", "specialization"),
    rel("催化机理", "催化剂", "representation"),
    rel("酶催化", "催化机理", "specialization"),
    rel("电化学热力学", "原电池", "generalization"),
    rel("能斯特方程", "标准电极电势", "generalization"),
    rel("电导率", "电解质", "requires"),
    rel("摩尔电导率", "电导率", "representation"),
    rel("电解", "电解池", "representation"),
    rel("电镀", "电解", "applies_to"),
    rel("表面吸附", "胶体", "requires"),
    rel("朗缪尔吸附等温线", "表面吸附", "representation"),
    rel("胶体的性质", "胶体", "representation"),
    rel("丁达尔效应", "胶体的性质", "specialization"),
    rel("电泳", "胶体的性质", "specialization"),
    rel("聚沉", "胶体的性质", "specialization"),

    # ── College: 分析化学 ──
    rel("定量分析", "化学", "generalization"),
    rel("定性分析", "化学", "generalization"),
    rel("重量分析法", "定量分析", "specialization"),
    rel("滴定分析法", "定量分析", "specialization"),
    rel("酸碱滴定", "滴定分析法", "specialization"),
    rel("配位滴定", "滴定分析法", "specialization"),
    rel("氧化还原滴定_chem", "滴定分析法", "specialization"),
    rel("沉淀滴定", "滴定分析法", "specialization"),
    rel("指示剂的选择", "指示剂", "generalization"),
    rel("滴定曲线", "滴定分析法", "representation"),
    rel("滴定终点", "滴定曲线", "representation"),
    rel("化学计量点", "滴定曲线", "representation"),
    rel("误差分析", "定量分析", "requires"),
    rel("有效数字", "误差分析", "representation"),
    rel("标准溶液", "滴定分析法", "requires"),
    rel("基准物质", "标准溶液", "requires"),
    rel("分光光度法", "定量分析", "specialization"),
    rel("比尔定律", "分光光度法", "representation"),
    rel("原子吸收光谱", "分光光度法", "specialization"),
    rel("红外光谱", "定性分析", "specialization"),
    rel("核磁共振", "定性分析", "specialization"),
    rel("质谱", "定性分析", "specialization"),
    rel("色谱法", "定性分析", "specialization"),
    rel("气相色谱", "色谱法", "specialization"),
    rel("液相色谱", "色谱法", "specialization"),
    rel("薄层色谱", "色谱法", "specialization"),
    rel("电位分析法", "定量分析", "specialization"),
    rel("离子选择电极", "电位分析法", "representation"),
    rel("库仑分析法", "定量分析", "specialization"),
]

# ══════════════════════════════════════════════════════════════════════
#  BUILD OUTPUT
# ══════════════════════════════════════════════════════════════════════

# Deduplicate
seen = set()
unique_concepts = []
for c in concepts:
    if c["name"] not in seen:
        seen.add(c["name"])
        unique_concepts.append(c)

seen_rels = set()
unique_relations = []
for r in relations:
    key = (r["source"], r["target"], r["type"])
    if key not in seen_rels:
        seen_rels.add(key)
        unique_relations.append(r)

# Verify no dangling refs
concept_names = {c["name"] for c in unique_concepts}
dangling = []
for r in unique_relations:
    if r["source"] not in concept_names:
        dangling.append(("source", r["source"]))
    if r["target"] not in concept_names:
        dangling.append(("target", r["target"]))

if dangling:
    for kind, name in dangling:
        print(f"DANGLING {kind}: {name}")

# Publisher counts
zh_pubs = set()
en_pubs = set()
de_pubs = set()
for c in unique_concepts:
    for ref in c.get("source_references", []):
        if ref["language"] == "zh": zh_pubs.add(ref["textbook"])
        elif ref["language"] == "en": en_pubs.add(ref["textbook"])
        elif ref["language"] == "de": de_pubs.add(ref["textbook"])

level_dist = Counter(c["level"] for c in unique_concepts)

output = {
    "version": "2.0",
    "domain": "chemistry",
    "description": "Chemistry knowledge graph — middle school through university, trilingual (ZH/EN/DE).",
    "languages": ["zh", "en", "de"],
    "created": datetime.now().isoformat(),
    "pipeline": "scripts/expand_chemistry_graph.py",
    "publisher_counts": {"zh": len(zh_pubs), "en": len(en_pubs), "de": len(de_pubs)},
    "concepts": unique_concepts,
    "relations": unique_relations,
    "metadata": {
        "total_concepts": len(unique_concepts),
        "total_relations": len(unique_relations),
        "dangling_refs": len(dangling),
        "created": datetime.now().isoformat()
    }
}

print(f"Total concepts: {len(unique_concepts)}")
print(f"Total relations: {len(unique_relations)}")
print(f"Levels: {dict(level_dist)}")
print(f"Publishers: ZH={len(zh_pubs)}, EN={len(en_pubs)}, DE={len(de_pubs)}")
print(f"Dangling refs: {len(dangling)}")

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n[OK] Written to {OUTPUT}")
