#!/usr/bin/env python3
"""Build agent-panel filled review from 6-persona majority votes (2026-09-16).

Votes: P1 strict / P2 lenient / P3 morph(abstain-semantics) / P4 DE-native /
P5 ZH-native / P6 red-team. Majority of 5 effective voters; edit = conditional
accept. Output: research/gold_review_v2/review_72_filled_agent.json
(meta.annotator documents non-human panel; human review still pending).
"""
import json
import os

SRC = os.path.join("research", "gold_review_v2", "review_72.json")
DST = os.path.join("research", "gold_review_v2", "review_72_filled_agent.json")

REJECT = {"A005", "A006", "A022", "A028", "A041", "A049", "A072"}
# panel-extracted concepts for accept/edit items (P1 primary, P4/P5 for edits)
CONCEPTS = {
    "A001": ["family"], "A002": ["担当"], "A003": ["fulfillment"],
    "A004": ["Beziehungen", "Lebensbalance"], "A007": ["Verantwortung", "Freiheit"],
    "A008": ["选择"], "A009": ["努力", "奋斗"], "A010": ["Ziel", "目标"],
    "A011": ["persönliches Glück", "berufliche Zufriedenheit", "Leidenschaft"],
    "A012": ["achieving goals", "relationships with family and friends"],
    "A013": ["persönliches Wachstum"], "A015": ["achievement"],
    "A016": ["责任", "自由", "相互依存", "放纵", "压迫", "平衡", "个人发展"],
    "A017": ["权力"], "A018": ["echter Erfolg"],
    "A019": ["Verantwortung", "Freiheit", "Chaos"],
    "A020": ["Glücklichsein", "Inspiration"], "A021": ["Erfüllung", "Selbstverwirklichung"],
    "A023": ["家庭"], "A024": ["academic success", "social balance", "emotional intelligence"],
    "A025": ["Verantwortung"], "A026": ["Glück"], "A027": ["vernachlässigte Lebensbereiche"],
    "A029": ["法律义务", "道德义务", "具体情况", "帮助别人"],
    "A030": ["Konsequenzen tragen", "Wahlfreiheit"], "A031": ["自由"],
    "A032": ["responsibility", "wise choice"], "A033": ["Ziel", "Teilerfolg"],
    "A034": ["Persönlichkeit"], "A036": ["家庭"], "A037": ["幸福"],
    "A038": ["家庭认可", "努力得到回报", "持续努力", "终点"],
    "A039": ["全面发展", "社交能力", "未来发展"],
    "A040": ["选择"], "A042": ["后果"],
    "A043": ["做自己想做的事", "为社会做贡献", "身边人过得好"],
    "A044": ["Leidenschaft", "热忱"], "A045": ["责任", "自由", "选择的权利", "选择的后果"],
    "A046": ["道德"], "A047": ["Glück"], "A048": ["义务"],
    "A050": ["生活平衡", "人际关系", "幸福生活"], "A051": ["义务"], "A052": ["贡献"],
    "A053": ["Verantwortung", "Freiheit", "Unterdrückung"], "A054": ["happiness"],
    "A055": ["Zufriedenheit", "Erfüllung"], "A056": ["无责任的自由", "混乱"],
    "A057": ["法律责任", "道德责任"], "A058": ["自由"], "A059": ["家庭"], "A060": ["成就"],
    "A061": ["实现梦想", "做善良的人"], "A062": ["梦想", "志向"],
    "A063": ["全面发展", "人际关系", "情感智慧"], "A064": ["目标"],
    "A065": ["fulfillment", "journey"], "A066": ["自由", "责任", "选择与负责"],
    "A067": ["实现目标", "充实生活"],
    "A069": ["学业成就", "牺牲社交", "生活平衡", "人际关系"],
    "A070": ["Verantwortung", "Freiheit", "Egoismus"],
    "A071": ["responsibility", "freedom", "power to choose"],
}
EDIT = {"A016", "A019", "A030", "A070"}

d = json.load(open(SRC, encoding="utf-8"))
n_acc = n_edit = n_rej = 0
for r in d["records"]:
    a = r["audit_id"]
    r["reviewer"] = "agent-panel-6persona (P1 strict/P2 lenient/P3 morph/P4 DE/P5 ZH/P6 red; majority vote)"
    if a in REJECT:
        r["decision"] = "reject"
        r["edited_concepts"] = []
        n_rej += 1
    elif a in EDIT:
        r["decision"] = "edit"
        r["edited_concepts"] = CONCEPTS[a]
        n_edit += 1
    else:
        r["decision"] = "accept"
        r["edited_concepts"] = CONCEPTS.get(a, [])
        n_acc += 1
d["meta"]["annotator"] = "6-persona-agent-panel (non-human; human blind review still pending)"
d["meta"]["vote"] = {"accept": n_acc, "edit": n_edit, "reject": n_rej}
d["meta"]["reject_ids"] = sorted(REJECT)
json.dump(d, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FILLED accept=%d edit=%d reject=%d -> %s" % (n_acc, n_edit, n_rej, DST))
