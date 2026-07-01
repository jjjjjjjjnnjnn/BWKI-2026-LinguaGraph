#!/usr/bin/env python3
"""
LPA — Language Production Analysis Pipeline
=============================================
Framework for analyzing cross-linguistic language production data.
Implements the coding scheme defined in docs/lpa_framework.md.

Dimensions:
  D1: Spatial Cognition (SGS: Spatial Granularity Score)
  D2: Temporal Cognition (TFP: Temporal Frame Preference)
  D3: Conceptual Flexibility (CFI: Conceptual Flexibility Index)
  D4: Lexical Creativity (LCS: Lexical Creativity Score)

Usage:
  python scripts/analyze_lpa.py --input data/survey_archive/*.xlsx
  python scripts/analyze_lpa.py --demo  # Run with pilot data
"""

import json
import re
import sys
from pathlib import Path
from typing import Any
from collections import Counter

# =============================================================================
# D1: Spatial Granularity Score (SGS)
# =============================================================================

def code_motion_event(text: str) -> dict:
    """Code Task 5: Motion event translation.

    Scoring:
    - Source (aus/von/from/从/出): 1 pt
    - Path (durch/through/穿过/经过): 1 pt
    - Goal (in/nach/zu/into/enter/进入/到): 1 pt
    - Manner verb (läuft/rennt/run/walk/rush/跑/走/冲): 1 pt
    """
    scores = {}
    scores['source'] = 1 if any(p in text.lower() for p in
        ['aus', 'von', 'from', 'out of', '出', '从']) else 0
    scores['path'] = 1 if any(p in text.lower() for p in
        ['durch', 'through', 'across', '穿过', '经过', '通过']) else 0
    scores['goal'] = 1 if any(p in text.lower() for p in
        ['in', 'nach', 'zu', 'into', 'enter', 'betritt', '到达', '进入', '到']) else 0
    scores['manner'] = 1 if any(p in text.lower() for p in
        ['läuft', 'rennt', 'run', 'walk', 'rush', 'laeuft', '走', '跑', '冲']) else 0
    return scores


def code_static_spatial(text: str) -> dict:
    """Code Task 6: Static spatial description.

    Scoring:
    - Object 1 (cup/Tasse/杯子): 1 pt
    - Object 2 (pen/Stift/笔/铅笔): 1 pt
    - Spatial relation 1 (hinter/vor/neben/behind/front/next to/后面/前面/旁边): 1 pt
    - Spatial relation 2 (second relation or additional precision): 1 pt
    - Orientation detail (Henkel/Spitze/parallel/handle/tip/指向/朝向): 1 pt
    - Multiple reference frames (intrinsic + relative): 1 pt
    """
    scores = {}
    obj1_words = ['cup', 'tasse', '杯子', '杯']
    obj2_words = ['pen', 'stift', '笔', '铅笔', '钢笔']
    rel_words = ['hinter', 'vor', 'neben', 'über', 'unter', 'hinterm',
                 'behind', 'front', 'next to', 'above', 'below', 'left of', 'right of',
                 '后面', '前面', '旁边', '上面', '下面', '左边', '右边']
    orient_words = ['henkel', 'spitze', 'schreibseite', 'parallel', 'handle', 'tip',
                    'pointing', '指向', '朝向', '平行', '把手', '笔尖']

    t = text.lower()
    scores['obj1'] = 1 if any(w in t for w in obj1_words) else 0
    scores['obj2'] = 1 if any(w in t for w in obj2_words) else 0

    rel_count = sum(1 for w in rel_words if w in t)
    scores['rel1'] = 1 if rel_count >= 1 else 0
    scores['rel2'] = 1 if rel_count >= 2 else 0

    scores['orientation'] = 1 if any(w in t for w in orient_words) else 0
    scores['ref_frame'] = 1 if rel_count >= 2 else 0  # multiple relations = multiple frames

    return scores


def compute_sgs(spatial_q: str, motion_q: str) -> dict:
    """Compute total Spatial Granularity Score (0-10)."""
    motion = code_motion_event(motion_q)
    static = code_static_spatial(spatial_q)

    detail = {}
    detail.update(motion)
    detail.update(static)

    total = sum(detail.values())
    return {
        'detail': detail,
        'total': total,
        'max': 10,
        'normalized': round(total / 10, 2)
    }


# =============================================================================
# D2: Temporal Frame Preference (TFP)
# =============================================================================

def code_temporal(text: str) -> dict:
    """Code Task 7: Temporal reference processing.

    Categories:
    - T+: Correct-unambiguous (vorverlegt, earlier, 提前)
    - T?: Ambiguous-avoidant (verschoben, shifted, 改到)
    - T~: Non-standard (vorwärts bewegt, forward, 向前移)
    - T-: Incomplete/missing
    """
    t = text.lower()

    # Check for unambiguous "earlier" markers
    unambiguous = any(w in t for w in ['vorverlegt', '提前', 'early', 'earlier',
                                        '前移', '往前'])
    ambiguous = any(w in t for w in ['verschoben', 'shifted', '推迟', '改期',
                                      'moved', 'changed'])
    non_standard = any(w in t for w in ['forward', 'vorwärts', '向前', 'ahead'])
    incomplete = len(t.strip()) < 5 or t.strip() in ['-', '.', '..', '...', '—']

    if incomplete:
        return {'code': 'T-', 'label': 'Incomplete', 'value': 0}
    if unambiguous:
        return {'code': 'T+', 'label': 'Unambiguous earlier', 'value': 3}
    if non_standard:
        return {'code': 'T~', 'label': 'Non-standard expression', 'value': 1}
    if ambiguous:
        return {'code': 'T?', 'label': 'Ambiguous avoidant', 'value': 2}
    return {'code': 'T?', 'label': 'Ambiguous (default)', 'value': 2}


# =============================================================================
# D3: Conceptual Flexibility Index (CFI)
# =============================================================================

def code_bilingual(text: str) -> dict:
    """Code Task 2: Bilingual concept explanation."""
    t = text.lower()
    has_bilingual = bool(re.search(r'[a-z]{2,}.*[a-z]{2,}', t))
    en_markers = ['the ', ' is ', ' to ', ' feeling', ' desire', ' want']
    has_en = any(m in t for m in en_markers)
    de_markers = ['das ', 'der ', 'die ', 'ist ', 'ein ', 'gefühl']
    has_de = any(m in t for m in de_markers)

    scores = {}
    scores['attempted'] = 1 if len(t) > 5 else 0
    scores['true_bilingual'] = 1 if has_en and has_de else 0
    scores['code_switch'] = 1 if has_en and has_de and len(t.split()) > 5 else 0
    scores['total'] = scores['attempted'] + scores['true_bilingual'] + scores['code_switch']
    return scores


def code_social_script(text: str) -> dict:
    """Code Task 3: Social script strategy."""
    t = text.lower()
    has_apology = any(w in t for w in ['sorry', 'leid', 'entschuldigung', 'mistake',
                                        'fehler', '对不起', '抱歉', '不好意思'])
    has_defiance = any(w in t for w in ['verarscht', 'just kidding', '玩笑', '故意的'])
    has_philosophical = any(w in t for w in ['niemand', 'perfekt', 'jeder', 'everyone',
                                              'nobody', '人人', '每个人', '完美'])
    has_command = any(w in t for w in ['sei', 'beruhigen', 'leise', 'quiet', 'calm',
                                        '安静', '别吵'])
    multi_clause = len(re.findall(r'[,.\n]', t)) >= 1

    scores = {}
    scores['response_given'] = 1 if len(t) > 3 else 0
    scores['multi_clause'] = 1 if multi_clause else 0
    scores['sophisticated'] = 1 if (has_apology or has_philosophical) else 0
    scores['total'] = scores['response_given'] + scores['multi_clause'] + scores['sophisticated']
    return scores


def code_event_construal(event_text: str, complex_text: str) -> dict:
    """Code Tasks 8-9: Event construal / perspective."""
    scores = {}

    # Check for perspective shift (agent change from default)
    default_agents = ['mother', 'mutter', '妈妈', '母亲', 'person a', 'person a']
    shifted_agents = ['girl', 'mädchen', '女孩', '女儿', 'person b']

    t = complex_text.lower()
    has_default = any(w in t for w in default_agents)
    has_shifted = any(w in t for w in shifted_agents)
    scores['perspective_shift'] = 1 if has_shifted and not has_default else 0
    has_causal = any(w in t for w in ['da', 'weil', 'denn', 'because', 'since',
                                       '因为', '由于', '所以'])
    scores['causal_subordination'] = 1 if has_causal else 0
    scores['natural_expression'] = 1 if len(t) > 20 else 0
    scores['total'] = scores['perspective_shift'] + scores['causal_subordination'] + scores['natural_expression']
    return scores


def compute_cfi(q2: str, q3: str, q8: str, q9: str) -> dict:
    """Compute total Conceptual Flexibility Index (0-8)."""
    bilingual = code_bilingual(q2)
    social = code_social_script(q3)
    event = code_event_construal(q8, q9)

    total = bilingual['total'] + social['total'] + event['total']
    return {
        'bilingual': bilingual,
        'social_script': social,
        'event_construal': event,
        'total': total,
        'max': 8,
        'normalized': round(total / 8, 2)
    }


# =============================================================================
# D4: Lexical Creativity Score (LCS)
# =============================================================================

def code_free_association(text: str) -> dict:
    """Code Task 1: Free association."""
    words = [w.strip().strip(',.') for w in text.replace('/', ',').split(',')]
    words = [w for w in words if len(w) > 1]

    scores = {}
    scores['word_count'] = len(words)
    scores['above_3'] = 1 if len(words) >= 3 else 0
    scores['non_prototype'] = 0  # needs language-specific prototype detection

    # Check for non-prototypical associates (not just clock/watch)
    t = text.lower()
    clock_words = ['uhr', 'clock', 'watch', '时间', '钟']
    non_clock = any(w.lower() not in clock_words for w in words)
    if non_clock and len(words) >= 2:
        scores['non_prototype'] = 1

    scores['total'] = scores['above_3'] + scores['non_prototype']
    return scores


def code_naming(text: str) -> dict:
    """Code Task 10: Robot naming strategy."""
    t = text.strip()
    scores = {}
    words = t.split()

    scores['multi_word'] = 1 if len(words) >= 2 else 0
    scores['functional'] = 1 if any(w in t.lower() for w in
        ['assist', 'medizin', 'kranken', 'nurse', 'help', 'helper', 'care',
         '医疗', '护理', '助手', '护士', '辅助']) else 0
    scores['creative'] = 1 if len(t) > 15 or any(c.isupper() for c in t[1:]) else 0
    bot_markers = ['bot', 'robot', 'maximus', 'aura', 'allesmacher']
    scores['bilingual'] = 1 if any(w in t.lower() for w in bot_markers) else 0
    scores['total'] = scores['multi_word'] + scores['functional'] + scores['creative'] + scores['bilingual']
    return scores


def compute_lcs(q1: str, q10: str) -> dict:
    """Compute total Lexical Creativity Score (0-6)."""
    fa = code_free_association(q1)
    naming = code_naming(q10)

    total = fa['total'] + naming['total']
    return {
        'free_association': fa,
        'naming': naming,
        'total': total,
        'max': 6,
        'normalized': round(total / 6, 2)
    }


# =============================================================================
# Full LPA Profile
# =============================================================================

def compute_lpa(
    q1: str,  # Free association
    q2: str,  # Bilingual explanation
    q3: str,  # Social script
    q5: str,  # Motion event
    q6: str,  # Static spatial
    q7: str,  # Temporal reference
    q8: str,  # Event description (give book)
    q9: str,  # Complex sentence
    q10: str, # Robot naming
    respondent_id: str = "UNKNOWN",
    language: str = "DE"
) -> dict:
    """Compute full LPA profile for one respondent."""

    d1 = compute_sgs(q6, q5)
    d2 = code_temporal(q7)
    d3 = compute_cfi(q2, q3, q8, q9)
    d4 = compute_lcs(q1, q10)

    total = d1['total'] + d2['value'] + d3['total'] + d4['total']
    max_total = d1['max'] + 3 + d3['max'] + d4['max']  # TFP max=3
    overall = round(total / max_total, 2) if max_total > 0 else 0

    return {
        'respondent_id': respondent_id,
        'language': language,
        'd1_spatial': {'score': d1['total'], 'max': d1['max'], 'normalized': d1['normalized']},
        'd2_temporal': {'code': d2['code'], 'label': d2['label'], 'score': d2['value']},
        'd3_flexibility': {'score': d3['total'], 'max': d3['max'], 'normalized': d3['normalized']},
        'd4_creativity': {'score': d4['total'], 'max': d4['max'], 'normalized': d4['normalized']},
        'overall': {'score': total, 'max': max_total, 'normalized': overall}
    }


def summarize_cohort(profiles: list) -> dict:
    """Summarize LPA across a cohort."""
    if not profiles:
        return {}

    def avg_scores(key, subkey='normalized'):
        vals = [p[key][subkey] for p in profiles if p]
        return round(sum(vals) / len(vals), 2) if vals else 0

    return {
        'n': len(profiles),
        'd1_spatial_mean': avg_scores('d1_spatial'),
        'd2_temporal_distribution': Counter(p['d2_temporal']['code'] for p in profiles if p),
        'd3_flexibility_mean': avg_scores('d3_flexibility'),
        'd4_creativity_mean': avg_scores('d4_creativity'),
        'overall_mean': avg_scores('overall'),
    }


# =============================================================================
# Demo Mode (Pilot Data)
# =============================================================================

def demo():
    """Run LPA on pilot data (6 existing DE responses)."""

    pilot_data = {
        'R1': {
            'q1': 'Uhr, Zeiger, Monat, Jahr, spät',
            'q2': 'Das Gefühl, gerne wieder verreisen zu wollen.',
            'q3': 'Das tut mir leid, mir ist ein Fehler unterlaufen.',
            'q5': 'Mike kommt aus einem Raum, geht durch das Wohnzimmer und betritt den Garten.',
            'q6': 'Die Tasse liegt hinter dem Buch und rechts neben dem Stift.',
            'q7': 'Der Test ist in 6 Tagen. Der Test wurde zwei Tage vorverlegt.',
            'q8': 'Person A gibt Person B ein Buch.',
            'q9': 'Gestern Nachmittag gab eine Mutter dem Mädchen einen Regenschirm, da es regnete.',
            'q10': 'Medizinischer Stationsassistenz-Roboter'
        },
        'R2': {
            'q1': 'Beeilen/hetzen/zu spät kommen/Uhr',
            'q2': 'In deutsch heißt es das man nach Hause will',
            'q3': 'Sei leise',
            'q5': 'Kann kein Englisch sorry',
            'q6': 'Vor dem Buch steht die Tasse',
            'q7': 'Kann kein Englisch sorry',
            'q8': 'A gibt B ein Buch',
            'q9': 'Das Mädchen nahm den Regenschirm mit',
            'q10': 'Robot 200 Maximus Aura'
        },
        'R3': {
            'q1': 'uhr zeiger schulzeit bildschirmzeit 15:40',
            'q2': '-',
            'q3': 'da hab ich euch verarscht',
            'q5': '-',
            'q6': 'die tasse steht hinterm buch und der stift liegt nebem buch',
            'q7': 'das exam ist in sechs tagen',
            'q8': 'person a gibt person b ein buch',
            'q9': '-',
            'q10': 'krankenschwester'
        },
        'R4': {
            'q1': 'Uhr Stoppuhr später',
            'q2': 'Das man sich nach anderen Orten snd',
            'q3': 'Ich meine',
            'q5': 'Mike geht in das Wohnzimmer',
            'q6': 'Die Tasse steht vor dem Buch und der Stift liegt links neben dem Buch',
            'q7': '.. .....',
            'q8': 'A gibt b das Buch',
            'q9': 'Sie gibt ihr den Regen Schirm',
            'q10': '.........'
        },
        'R5': {
            'q1': 'Uhr, Uhrzeit, Uhrzeiger, Schulzeit, Schulstunde',
            'q2': 'Fernweh ist das Gegenteil von Heimweh es ist der Wille zu reisen und zu erkunden. its a Desiree tot Go far away from Home',
            'q3': 'Alle beruhigen sich jetzt Mal das ist nicht so wichtig',
            'q5': 'Mike kommt aus einem Raum raus und geht durch das Wohnzimmer in den Gärten',
            'q6': 'Der Stift liegt parallel zum Buch, während die Tasse dahinter ist und der Henkel zeigt nach rechts',
            'q7': 'Der Test ist in sieben Tagen. Er wurde um zwei Tage vorwärts bewegt',
            'q8': 'Person a gibt Person b ein buch',
            'q9': '-',
            'q10': 'Krankenschwester bot'
        },
        'R6': {
            'q1': 'Uhr Sekunde Minute Stunde Tag',
            'q2': 'Ein Gefühl das man von seinem Zuhause weg will. The feeling that you want to leave your home.',
            'q3': 'Niemand ist perfekt, jeder kann mal Fehler machen.',
            'q5': 'Mike kommt aus einem Raum, läuft durch das Wohzimmer und betritt den Garten',
            'q6': 'Der Stift liegt mit der Schreibseite nach unten links neben dem Buch, die Tasse steht über dem Buch.',
            'q7': 'Die Prüfung ist in sechs Tagen. Die Prüfung wurde um zwei Tage verschoben.',
            'q8': 'Person A übergibt Person B ein Buch.',
            'q9': '—————————————————————————',
            'q10': 'Der (Allesmacher).'
        }
    }

    profiles = []
    print("=" * 60)
    print("LPA PILOT ANALYSIS — 6 German Respondents")
    print("=" * 60)

    for rid, data in pilot_data.items():
        profile = compute_lpa(
            q1=data['q1'], q2=data['q2'], q3=data['q3'],
            q5=data['q5'], q6=data['q6'], q7=data['q7'],
            q8=data['q8'], q9=data['q9'], q10=data['q10'],
            respondent_id=rid, language='DE'
        )
        profiles.append(profile)

        print(f"\n{rid}:")
        print(f"  D1 Spatial:     {profile['d1_spatial']['score']}/{profile['d1_spatial']['max']} ({profile['d1_spatial']['normalized']:.2f})")
        print(f"  D2 Temporal:    {profile['d2_temporal']['code']} - {profile['d2_temporal']['label']}")
        print(f"  D3 Flexibility: {profile['d3_flexibility']['score']}/{profile['d3_flexibility']['max']} ({profile['d3_flexibility']['normalized']:.2f})")
        print(f"  D4 Creativity:  {profile['d4_creativity']['score']}/{profile['d4_creativity']['max']} ({profile['d4_creativity']['normalized']:.2f})")
        print(f"  OVERALL:        {profile['overall']['score']}/{profile['overall']['max']} ({profile['overall']['normalized']:.2f})")

    summary = summarize_cohort(profiles)
    print(f"\n{'=' * 60}")
    print(f"COHORT SUMMARY (N={summary['n']})")
    print(f"{'=' * 60}")
    print(f"  D1 Spatial (SGS) mean:     {summary['d1_spatial_mean']}")
    print(f"  D2 Temporal distribution:  {dict(summary['d2_temporal_distribution'])}")
    print(f"  D3 Flexibility (CFI) mean: {summary['d3_flexibility_mean']}")
    print(f"  D4 Creativity (LCS) mean:  {summary['d4_creativity_mean']}")
    print(f"  OVERALL mean:              {summary['overall_mean']}")
    print()

    return {'profiles': profiles, 'summary': summary}


if __name__ == '__main__':
    if '--demo' in sys.argv:
        result = demo()
        with open('outputs/lpa_pilot_results.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results saved to outputs/lpa_pilot_results.json")
    else:
        print("Usage: python scripts/analyze_lpa.py --demo")
        print("       python scripts/analyze_lpa.py --input <file>")
