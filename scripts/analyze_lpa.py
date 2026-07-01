#!/usr/bin/env python3
"""
LPA — Exploratory Language Production Analysis Pipeline
=========================================================
Coding framework for open-ended linguistic responses.
Reports individual criteria per dimension — NO composite scores.

Usage:
  python scripts/analyze_lpa.py --demo       # Pilot analysis (6 DE)
  python scripts/analyze_lpa.py --irr        # Inter-rater reliability check
  python scripts/analyze_lpa.py --input <xlsx>  # Process survey data
"""

import json, re, sys
from collections import Counter

# =========================================================================
# D1: Spatial Granularity (Tasks 5-6) — reported as criterion flags
# =========================================================================

def code_motion(text: str) -> dict:
    """Task 5: Motion event — individual criteria (NOT a score)."""
    t = text.lower()
    return {
        'source_encoded': int(any(p in t for p in ['aus','von','from','out of','出','从'])),
        'path_encoded': int(any(p in t for p in ['durch','through','across','穿过','经过','通过'])),
        'goal_encoded': int(any(p in t for p in ['in','nach','zu','into','enter','betritt','到达','进入','到'])),
        'manner_verb': int(any(p in t for p in ['läuft','rennt','run','walk','rush','laeuft','走','跑','冲'])),
        'refused': int(len(t) < 3),
    }

def code_static(text: str) -> dict:
    """Task 6: Static spatial — individual criteria (NOT a score)."""
    obj1 = ['cup','tasse','杯子','杯']
    obj2 = ['pen','stift','笔','铅笔','钢笔']
    rel  = ['hinter','vor','neben','über','unter','hinterm','behind','front',
            'next to','above','below','left of','right of','后面','前面','旁边',
            '上面','下面','左边','右边']
    orient = ['henkel','spitze','schreibseite','parallel','handle','tip',
              'pointing','指向','朝向','平行','把手','笔尖']
    t = text.lower()
    return {
        'obj1_present': int(any(w in t for w in obj1)),
        'obj2_present': int(any(w in t for w in obj2)),
        'relation_encoded': int(any(w in t for w in rel)),
        'orientation_detail': int(any(w in t for w in orient)),
        'multi_frame': int(sum(1 for w in rel if w in t) >= 2),
        'refused': int(len(t) < 3),
    }

# =========================================================================
# D2: Temporal Framing (Task 7) — categorical, not scored
# =========================================================================

def code_temporal(text: str) -> dict:
    t = text.lower().strip()
    if len(t) < 5 or t in ['-','.','..','...','—']:
        return {'code': 'T-', 'label': 'Incomplete / refused'}
    if any(w in t for w in ['vorverlegt','提前','earlier','前移','往前']):
        return {'code': 'T+', 'label': 'Unambiguous "earlier"'}
    if any(w in t for w in ['vorwärts','forward','向前']):
        return {'code': 'T~', 'label': 'Non-standard literal translation'}
    if any(w in t for w in ['verschoben','shifted','推迟','改期','moved','changed']):
        return {'code': 'T?', 'label': 'Ambiguous / direction-neutral'}
    return {'code': 'T?', 'label': 'Ambiguous (unclassified)'}

# =========================================================================
# D3: Conceptual Flexibility (Tasks 2,3,8,9) — criterion flags
# =========================================================================

def code_bilingual(text: str) -> dict:
    t = text.lower()
    has_de = any(m in t for m in ['das ','der ','die ','ist ','ein ','gefühl'])
    en_markers = ['the ',' is ',' to ','feeling','desire','want','longing']
    has_en = any(m in t for m in en_markers)
    return {
        'attempted': int(len(t) > 5),
        'true_bilingual': int(has_de and has_en),
        'code_switching': int(has_de and has_en and len(t.split()) > 8),
    }

def code_social_script(text: str) -> dict:
    t = text.lower()
    return {
        'multi_clause': int(len(re.findall(r'[,.\n]', t)) >= 1 or len(t.split()) > 10),
        'apology': int(any(w in t for w in ['sorry','leid','entschuldigung','mistake','fehler','对不起','抱歉','不好意思'])),
        'defiance': int(any(w in t for w in ['verarscht','kidding','玩笑','故意'])),
        'philosophical': int(any(w in t for w in ['niemand','perfekt','jeder','everyone','nobody','人人','每个人','完美'])),
        'de_escalation': int(any(w in t for w in ['beruhigen','calm','quiet','wichtig','重要','安静'])),
        'hedging': int(any(w in t for w in ['ich meine','i mean','我觉得','我认为'])),
    }

def code_event_construal(event: str, complex_sentence: str) -> dict:
    shift_agents = ['girl','mädchen','女孩','女儿','person b']
    t = complex_sentence.lower()
    return {
        'perspective_shift': int(any(w in t for w in shift_agents) and
                                 not any(w in t for w in ['mother','mutter','妈妈','母亲','person a'])),
        'causal_subordination': int(any(w in t for w in ['da ','weil','denn','because','since','因为','由于','所以'])),
        'natural_expression': int(len(t) > 20),
    }

# =========================================================================
# D4: Lexical Production (Tasks 1,10) — criterion flags
# =========================================================================

def code_free_association(text: str) -> dict:
    words = [w.strip().strip(',.').strip() for w in text.replace('/',',').split(',')]
    words = [w for w in words if len(w) > 1]
    clock_words = ['uhr','clock','watch','时间','钟','time']
    non_clock = [w for w in words if w.lower() not in clock_words]
    categories = set()
    for w in words:
        wl = w.lower()
        if any(u in wl for u in ['uhr','clock','zeit','time','minute','sekunde','stunde','hour','second','minute','时','分','秒']):
            categories.add('measurement')
        if any(u in wl for u in ['schule','schul','school','学','课']):
            categories.add('institutional')
        if any(u in wl for u in ['hetzen','spät','late','hurry','beeilen','忙','迟','赶']):
            categories.add('pressure')
        if any(u in wl for u in ['monat','jahr','tag','month','year','day','年','月','日']):
            categories.add('calendar')
    return {
        'word_count': len(words),
        'categories': len(categories),
        'beyond_prototype': int(len(non_clock) >= 2),
    }

def code_naming(text: str) -> dict:
    t = text.strip()
    if len(t) < 2 or t in ['.........', '—', '-']:
        return {'refused': 1, 'multi_word': 0, 'functional': 0, 'creative': 0, 'bilingual': 0}
    words = t.split()
    return {
        'refused': 0,
        'multi_word': int(len(words) >= 2),
        'functional': int(any(w in t.lower() for w in
            ['assist','medizin','kranken','nurse','help','helper','care','医疗','护理','助手','护士','辅助'])),
        'creative': int(len(t) > 15 or any(c.isupper() for c in t[1:])),
        'bilingual': int(any(w in t.lower() for w in ['bot','robot','maximus','aura','allesmacher'])),
    }

# =========================================================================
# Full Coding Report (per respondent, per dimension — NO composite)
# =========================================================================

def code_respondent(q1, q2, q3, q5, q6, q7, q8, q9, q10,
                     respondent_id="?", language="DE") -> dict:
    motion = code_motion(q5)
    static = code_static(q6)
    temporal = code_temporal(q7)
    bilingual = code_bilingual(q2)
    social = code_social_script(q3)
    event = code_event_construal(q8, q9)
    fa = code_free_association(q1)
    naming = code_naming(q10)

    return {
        'id': respondent_id,
        'language': language,
        'd1_spatial': {
            'motion': motion,
            'static': static,
            'criteria_met': sum(v for k, v in motion.items() if k != 'refused') + sum(v for k, v in static.items() if k != 'refused'),
            'criteria_total': 4 + 5,
        },
        'd2_temporal': temporal,
        'd3_flexibility': {
            'bilingual': bilingual,
            'social_script': social,
            'event_construal': event,
            'criteria_met': sum(bilingual.values()) + sum(social.values()) + sum(event.values()),
            'criteria_total': 3 + 6 + 3,
        },
        'd4_lexical': {
            'free_association': fa,
            'naming': naming,
            'criteria_met': sum(v for k, v in fa.items() if k not in ('word_count','categories')) + sum(v for k, v in naming.items() if k != 'refused'),
            'criteria_total': 5 + 4,
        },
    }


def report_respondent(r: dict) -> str:
    d1 = r['d1_spatial']
    d2 = r['d2_temporal']
    d3 = r['d3_flexibility']
    d4 = r['d4_lexical']
    return (
        f"  D1 Spatial:  {d1['criteria_met']}/{d1['criteria_total']} criteria met\n"
        f"  D2 Temporal: {d2['code']} — {d2['label']}\n"
        f"  D3 Flex:     {d3['criteria_met']}/{d3['criteria_total']} criteria met\n"
        f"  D4 Lexical:  {d4['criteria_met']}/{d4['criteria_total']} criteria met"
    )

# =========================================================================
# Inter-Rater Reliability
# =========================================================================

def cohens_kappa(a: list, b: list, categories: list) -> float:
    """Simple Cohen's κ for two raters on nominal categories."""
    n = len(a)
    if n != len(b) or n == 0:
        return 0.0
    # Observed agreement
    observed = sum(1 for i in range(n) if a[i] == b[i]) / n
    # Expected agreement (per category)
    expected = 0.0
    for cat in categories:
        pa = a.count(cat) / n
        pb = b.count(cat) / n
        expected += pa * pb
    if expected >= 1.0:
        return 1.0
    return round((observed - expected) / (1 - expected), 3) if expected < 1 else 1.0


def compute_irr(coded_pairs: list) -> dict:
    """Compute inter-rater reliability for coded dimensions.

    Args:
        coded_pairs: list of (rater1_dict, rater2_dict) tuples
    Returns:
        dict with κ per criterion
    """
    if not coded_pairs:
        return {'error': 'No data for IRR'}

    results = {}
    # Flatten binary criteria for κ computation
    criteria_keys = []
    sample = coded_pairs[0][0]
    for dim in ['d1_spatial', 'd3_flexibility', 'd4_lexical']:
        for subdim in sample.get(dim, {}):
            if isinstance(sample[dim][subdim], dict):
                for c in sample[dim][subdim]:
                    criteria_keys.append(f"{dim}.{subdim}.{c}")
            elif isinstance(sample[dim][subdim], (int, float)):
                criteria_keys.append(f"{dim}.{subdim}")

    for key in criteria_keys:
        parts = key.split('.')
        r1_vals, r2_vals = [], []
        for r1, r2 in coded_pairs:
            try:
                v1 = r1[parts[0]][parts[1]][parts[2]] if len(parts) == 3 else r1[parts[0]][parts[1]]
                v2 = r2[parts[0]][parts[1]][parts[2]] if len(parts) == 3 else r2[parts[0]][parts[1]]
                r1_vals.append(v1)
                r2_vals.append(v2)
            except (KeyError, IndexError, TypeError):
                continue
        if r1_vals:
            results[key] = cohens_kappa(r1_vals, r2_vals, list(set(r1_vals + r2_vals)))

    # Temporal code (nominal)
    temp_pairs = [(r1['d2_temporal']['code'], r2['d2_temporal']['code']) for r1, r2 in coded_pairs]
    t_codes = list(set([p[0] for p in temp_pairs] + [p[1] for p in temp_pairs]))
    results['d2_temporal.code'] = cohens_kappa(
        [p[0] for p in temp_pairs],
        [p[1] for p in temp_pairs],
        t_codes
    )

    mean_k = sum(v for v in results.values() if isinstance(v, (int, float))) / max(len(results), 1)
    results['mean_kappa'] = round(mean_k, 3)
    return results

# =========================================================================
# DEMO: Pilot 6 DE responses
# =========================================================================

def demo():
    pilot = {
        'DE01': {'q1':'Uhr, Zeiger, Monat, Jahr, spät', 'q2':'Das Gefühl, gerne wieder verreisen zu wollen.', 'q3':'Das tut mir leid, mir ist ein Fehler unterlaufen.', 'q5':'Mike kommt aus einem Raum, geht durch das Wohnzimmer und betritt den Garten.', 'q6':'Die Tasse liegt hinter dem Buch und rechts neben dem Stift.', 'q7':'Der Test ist in 6 Tagen. Der Test wurde zwei Tage vorverlegt.', 'q8':'Person A gibt Person B ein Buch.', 'q9':'Gestern Nachmittag gab eine Mutter dem Mädchen einen Regenschirm, da es regnete.', 'q10':'Medizinischer Stationsassistenz-Roboter'},
        'DE02': {'q1':'Beeilen/hetzen/zu spät kommen/Uhr', 'q2':'In deutsch heißt es das man nach Hause will', 'q3':'Sei leise', 'q5':'Kann kein Englisch sorry', 'q6':'Vor dem Buch steht die Tasse', 'q7':'Kann kein Englisch sorry', 'q8':'A gibt B ein Buch', 'q9':'Das Mädchen nahm den Regenschirm mit', 'q10':'Robot 200 Maximus Aura'},
        'DE03': {'q1':'uhr zeiger schulzeit bildschirmzeit 15:40', 'q2':'-', 'q3':'da hab ich euch verarscht', 'q5':'-', 'q6':'die tasse steht hinterm buch und der stift liegt nebem buch', 'q7':'das exam ist in sechs tagen', 'q8':'person a gibt person b ein buch', 'q9':'-', 'q10':'krankenschwester'},
        'DE04': {'q1':'Uhr Stoppuhr später', 'q2':'Das man sich nach anderen Orten snd', 'q3':'Ich meine', 'q5':'Mike geht in das Wohnzimmer', 'q6':'Die Tasse steht vor dem Buch und der Stift liegt links neben dem Buch', 'q7':'.. .....', 'q8':'A gibt b das Buch', 'q9':'Sie gibt ihr den Regen Schirm', 'q10':'.........'},
        'DE05': {'q1':'Uhr, Uhrzeit, Uhrzeiger, Schulzeit, Schulstunde', 'q2':'Fernweh ist das Gegenteil von Heimweh es ist der Wille zu reisen und zu erkunden. its a Desiree tot Go far away from Home', 'q3':'Alle beruhigen sich jetzt Mal das ist nicht so wichtig', 'q5':'Mike kommt aus einem Raum raus und geht durch das Wohnzimmer in den Gärten', 'q6':'Der Stift liegt parallel zum Buch, während die Tasse dahinter ist und der Henkel zeigt nach rechts', 'q7':'Der Test ist in sieben Tagen. Er wurde um zwei Tage vorwärts bewegt', 'q8':'Person a gibt Person b ein buch', 'q9':'-', 'q10':'Krankenschwester bot'},
        'DE06': {'q1':'Uhr Sekunde Minute Stunde Tag', 'q2':'Ein Gefühl das man von seinem Zuhause weg will. The feeling that you want to leave your home.', 'q3':'Niemand ist perfekt, jeder kann mal Fehler machen.', 'q5':'Mike kommt aus einem Raum, läuft durch das Wohzimmer und betritt den Garten', 'q6':'Der Stift liegt mit der Schreibseite nach unten links neben dem Buch, die Tasse steht über dem Buch.', 'q7':'Die Prüfung ist in sechs Tagen. Die Prüfung wurde um zwei Tage verschoben.', 'q8':'Person A übergibt Person B ein Buch.', 'q9':'—————————————————————————', 'q10':'Der (Allesmacher).'},
    }

    print("=" * 62)
    print("LPA — EXPLORATORY PILOT ANALYSIS (N=6 DE)")
    print("=" * 62)
    print("Reporting: individual criteria per dimension. NO composite scores.\n")

    profiles = []
    for rid, d in pilot.items():
        r = code_respondent(
            q1=d['q1'], q2=d['q2'], q3=d['q3'], q5=d['q5'], q6=d['q6'],
            q7=d['q7'], q8=d['q8'], q9=d['q9'], q10=d['q10'],
            respondent_id=rid, language='DE')
        profiles.append(r)
        print(f"[{rid}]")
        print(report_respondent(r))
        print()

    # Cohort summary — distributions only, no means
    print("--- COHORT OVERVIEW (N=6) ---")
    temp_codes = [p['d2_temporal']['code'] for p in profiles]
    print(f"D2 Temporal framing: {dict(Counter(temp_codes))}")
    d1_met = [p['d1_spatial']['criteria_met'] for p in profiles]
    print(f"D1 Criteria met range: {min(d1_met)}–{max(d1_met)} (of {profiles[0]['d1_spatial']['criteria_total']})")
    d3_met = [p['d3_flexibility']['criteria_met'] for p in profiles]
    print(f"D3 Criteria met range: {min(d3_met)}–{max(d3_met)} (of {profiles[0]['d3_flexibility']['criteria_total']})")
    d4_met = [p['d4_lexical']['criteria_met'] for p in profiles]
    print(f"D4 Criteria met range: {min(d4_met)}–{max(d4_met)} (of {profiles[0]['d4_lexical']['criteria_total']})")
    print()

    # Demo IRR (artificial second coder for demonstration)
    print("--- INTER-RATER RELIABILITY (Demo) ---")
    print("Note: Second coder required for real IRR. Demo uses auto-coded × auto-coded = 1.0.")
    irr = compute_irr([(p, p) for p in profiles])  # identical copies
    print(f"Mean κ (auto × auto): {irr.get('mean_kappa', 'N/A')}")
    print()
    print(f"Results saved to outputs/lpa_pilot_coded.json")

    with open('outputs/lpa_pilot_coded.json', 'w', encoding='utf-8') as f:
        json.dump({'profiles': profiles, 'cohort': {'n': len(profiles)}}, f, ensure_ascii=False, indent=2)

    return profiles


if __name__ == '__main__':
    if '--demo' in sys.argv:
        demo()
    elif '--irr' in sys.argv:
        print("IRR mode: provide two JSON files with coded responses.")
        print("Usage: python scripts/analyze_lpa.py --irr --coder1 file1.json --coder2 file2.json")
    elif '--input' in sys.argv:
        print("Batch mode: reading survey data...")
        print("To be implemented when full dataset is available.")
    else:
        print("Usage:")
        print("  python scripts/analyze_lpa.py --demo   # Pilot analysis")
        print("  python scripts/analyze_lpa.py --irr    # IRR check")
