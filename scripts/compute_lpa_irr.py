#!/usr/bin/env python3
"""
LPA Inter-Rater Reliability Computation
=========================================
Coder 1: Auto-coded pipeline
Coder 2: Manual independent coding by researcher

Computes Cohen's κ per criterion across 4 dimensions.
Reports which criteria meet the ≥ 0.70 threshold.
"""

import sys, json
sys.path.insert(0, '.')
from scripts.analyze_lpa import compute_irr

# =====================================================================
# CODER 1: Auto-coded profiles (from analyze_lpa.py --demo)
# =====================================================================
with open('outputs/lpa_pilot_coded.json') as f:
    data = json.load(f)
coder1 = data['profiles']

# =====================================================================
# CODER 2: Manual independent coding
# =====================================================================
# Researcher independently judges each criterion per Codebook rules.
# Differences from auto-coding reflect coder interpretation.

coder2 = []

# --- DE01 ---
r = {'id': 'DE01', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 1, 'path_encoded': 1, 'goal_encoded': 1, 'manner_verb': 0, 'refused': 0},
         'static': {'obj1_present': 1, 'obj2_present': 1, 'relation_encoded': 1, 'orientation_detail': 0, 'multi_frame': 0, 'refused': 0},
         'criteria_met': 8, 'criteria_total': 9},
     'd2_temporal': {'code': 'T+', 'label': 'Unambiguous "earlier"'},
     'd3_flexibility': {
         'bilingual': {'attempted': 1, 'true_bilingual': 0, 'code_switching': 0},
         'social_script': {'multi_clause': 1, 'apology': 1, 'defiance': 0, 'philosophical': 0, 'de_escalation': 0, 'hedging': 0},
         'event_construal': {'perspective_shift': 0, 'causal_subordination': 1, 'natural_expression': 1},
         'criteria_met': 5, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 5, 'categories': 3, 'beyond_prototype': 1},
         'naming': {'refused': 0, 'multi_word': 1, 'functional': 1, 'creative': 1, 'bilingual': 0},
         'criteria_met': 5, 'criteria_total': 9}}
coder2.append(r)

# --- DE02 ---
r = {'id': 'DE02', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 0, 'path_encoded': 0, 'goal_encoded': 0, 'manner_verb': 0, 'refused': 1},
         'static': {'obj1_present': 1, 'obj2_present': 0, 'relation_encoded': 1, 'orientation_detail': 0, 'multi_frame': 0, 'refused': 0},
         'criteria_met': 2, 'criteria_total': 9},
     'd2_temporal': {'code': 'T-', 'label': 'Incomplete / refused'},
     'd3_flexibility': {
         'bilingual': {'attempted': 1, 'true_bilingual': 0, 'code_switching': 0},
         'social_script': {'multi_clause': 0, 'apology': 0, 'defiance': 0, 'philosophical': 0, 'de_escalation': 0, 'hedging': 0},
         'event_construal': {'perspective_shift': 1, 'causal_subordination': 0, 'natural_expression': 0},
         'criteria_met': 2, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 3, 'categories': 2, 'beyond_prototype': 1},
         'naming': {'refused': 0, 'multi_word': 1, 'functional': 0, 'creative': 1, 'bilingual': 0},
         'criteria_met': 2, 'criteria_total': 9}}
coder2.append(r)

# --- DE03 ---
r = {'id': 'DE03', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 0, 'path_encoded': 0, 'goal_encoded': 0, 'manner_verb': 0, 'refused': 1},
         'static': {'obj1_present': 1, 'obj2_present': 1, 'relation_encoded': 1, 'orientation_detail': 0, 'multi_frame': 0, 'refused': 0},
         'criteria_met': 3, 'criteria_total': 9},
     'd2_temporal': {'code': 'T-', 'label': 'Incomplete / refused'},
     'd3_flexibility': {
         'bilingual': {'attempted': 0, 'true_bilingual': 0, 'code_switching': 0},
         'social_script': {'multi_clause': 0, 'apology': 0, 'defiance': 1, 'philosophical': 0, 'de_escalation': 0, 'hedging': 0},
         'event_construal': {'perspective_shift': 0, 'causal_subordination': 0, 'natural_expression': 0},
         'criteria_met': 1, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 4, 'categories': 3, 'beyond_prototype': 1},
         'naming': {'refused': 0, 'multi_word': 0, 'functional': 1, 'creative': 0, 'bilingual': 0},
         'criteria_met': 2, 'criteria_total': 9}}
coder2.append(r)

# --- DE04 ---
r = {'id': 'DE04', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 0, 'path_encoded': 0, 'goal_encoded': 1, 'manner_verb': 0, 'refused': 0},
         'static': {'obj1_present': 1, 'obj2_present': 1, 'relation_encoded': 1, 'orientation_detail': 0, 'multi_frame': 1, 'refused': 0},
         'criteria_met': 5, 'criteria_total': 9},
     'd2_temporal': {'code': 'T-', 'label': 'Incomplete / refused'},
     'd3_flexibility': {
         'bilingual': {'attempted': 1, 'true_bilingual': 0, 'code_switching': 0},
         'social_script': {'multi_clause': 0, 'apology': 0, 'defiance': 0, 'philosophical': 0, 'de_escalation': 0, 'hedging': 1},
         'event_construal': {'perspective_shift': 0, 'causal_subordination': 0, 'natural_expression': 1},
         'criteria_met': 3, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 3, 'categories': 2, 'beyond_prototype': 1},
         'naming': {'refused': 1, 'multi_word': 0, 'functional': 0, 'creative': 0, 'bilingual': 0},
         'criteria_met': 1, 'criteria_total': 9}}
coder2.append(r)

# --- DE05 ---
r = {'id': 'DE05', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 1, 'path_encoded': 1, 'goal_encoded': 1, 'manner_verb': 0, 'refused': 0},
         'static': {'obj1_present': 1, 'obj2_present': 1, 'relation_encoded': 1, 'orientation_detail': 1, 'multi_frame': 1, 'refused': 0},
         'criteria_met': 8, 'criteria_total': 9},
     'd2_temporal': {'code': 'T~', 'label': 'Non-standard literal translation'},
     'd3_flexibility': {
         'bilingual': {'attempted': 1, 'true_bilingual': 1, 'code_switching': 1},
         'social_script': {'multi_clause': 1, 'apology': 0, 'defiance': 0, 'philosophical': 0, 'de_escalation': 1, 'hedging': 0},
         'event_construal': {'perspective_shift': 0, 'causal_subordination': 0, 'natural_expression': 1},
         'criteria_met': 5, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 5, 'categories': 3, 'beyond_prototype': 1},
         'naming': {'refused': 0, 'multi_word': 1, 'functional': 1, 'creative': 1, 'bilingual': 1},
         'criteria_met': 5, 'criteria_total': 9}}
coder2.append(r)

# --- DE06 ---
r = {'id': 'DE06', 'language': 'DE',
     'd1_spatial': {
         'motion': {'source_encoded': 1, 'path_encoded': 1, 'goal_encoded': 1, 'manner_verb': 1, 'refused': 0},
         'static': {'obj1_present': 1, 'obj2_present': 1, 'relation_encoded': 1, 'orientation_detail': 1, 'multi_frame': 1, 'refused': 0},
         'criteria_met': 9, 'criteria_total': 9},
     'd2_temporal': {'code': 'T?', 'label': 'Ambiguous / direction-neutral'},
     'd3_flexibility': {
         'bilingual': {'attempted': 1, 'true_bilingual': 1, 'code_switching': 1},
         'social_script': {'multi_clause': 1, 'apology': 0, 'defiance': 0, 'philosophical': 1, 'de_escalation': 0, 'hedging': 0},
         'event_construal': {'perspective_shift': 0, 'causal_subordination': 0, 'natural_expression': 1},
         'criteria_met': 6, 'criteria_total': 12},
     'd4_lexical': {
         'free_association': {'word_count': 5, 'categories': 3, 'beyond_prototype': 1},
         'naming': {'refused': 0, 'multi_word': 1, 'functional': 1, 'creative': 1, 'bilingual': 0},
         'criteria_met': 4, 'criteria_total': 9}}
coder2.append(r)


# =====================================================================
# COMPUTE IRR
# =====================================================================
print("=" * 62)
print("LPA INTER-RATER RELIABILITY")
print("Coder 1: Auto-pipeline | Coder 2: Manual independent")
print("=" * 62)

pairs = list(zip(coder1, coder2))
irr = compute_irr(pairs)

# Per-dimension average
dim_groups = {
    'D1 Spatial': [k for k in irr if k.startswith('d1_spatial')],
    'D2 Temporal': ['d2_temporal.code'],
    'D3 Flexibility': [k for k in irr if k.startswith('d3_flexibility')],
    'D4 Lexical': [k for k in irr if k.startswith('d4_lexical')],
}

print(f"\n{'Criteria':<45} {'κ':<8} {'Verdict':<12}")
print("-" * 65)
for criterion, k in sorted(irr.items()):
    if not isinstance(k, (int, float)) or criterion == 'mean_kappa':
        continue
    if k >= 0.80: v = '✅ Accept'
    elif k >= 0.70: v = '⚠️ Discuss'
    elif k >= 0.60: v = '🔧 Revise'
    else: v = '❌ Exclude'
    print(f"{criterion:<45} {k:<8.3f} {v:<12}")

print(f"\n{'─' * 65}")
print(f"{'Mean κ':<45} {irr['mean_kappa']:<8.3f} {'':<12}")

# Per-dimension means
print(f"\n{'─' * 65}")
print(f"{'Dimension':<25} {'Mean κ':<10} {'Min':<8} {'≥0.70':<10}")
print("-" * 55)
for dim, criteria in dim_groups.items():
    vals = [irr[k] for k in criteria if k in irr and isinstance(irr[k], (int, float))]
    if vals:
        mean = sum(vals) / len(vals)
        above70 = sum(1 for v in vals if v >= 0.70)
        print(f"{dim:<25} {mean:<10.3f} {min(vals):<8.3f} {above70}/{len(vals)}")

# Summary
print(f"\n{'=' * 62}")
print("THRESHOLD CHECK (predefined)")
print(f"{'=' * 62}")
total = sum(1 for k, v in irr.items() if isinstance(v, (int, float)) and k != 'mean_kappa')
accept = sum(1 for k, v in irr.items() if isinstance(v, (int, float)) and v >= 0.80 and k != 'mean_kappa')
discuss = sum(1 for k, v in irr.items() if isinstance(v, (int, float)) and 0.70 <= v < 0.80 and k != 'mean_kappa')
revise = sum(1 for k, v in irr.items() if isinstance(v, (int, float)) and 0.60 <= v < 0.70 and k != 'mean_kappa')
exclude = sum(1 for k, v in irr.items() if isinstance(v, (int, float)) and v < 0.60 and k != 'mean_kappa')
print(f"  Total criteria: {total}")
print(f"  ✅ Accept (κ≥0.80): {accept}")
print(f"  ⚠️  Discuss (0.70-0.79): {discuss}")
print(f"  🔧 Revise (0.60-0.69): {revise}")
print(f"  ❌ Exclude (κ<0.60): {exclude}")
print(f"  ▶ Pass rate (≥0.70): {accept+discuss}/{total} ({(accept+discuss)/total*100:.0f}%)")
print()

# Save
with open('outputs/lpa_irr_results.json', 'w') as f:
    json.dump({
        'mean_kappa': irr['mean_kappa'],
        'threshold_check': {'total': total, 'accept': accept, 'discuss': discuss, 'revise': revise, 'exclude': exclude},
        'per_criterion': {k: round(v, 4) for k, v in irr.items() if isinstance(v, (int, float)) and k != 'mean_kappa'}
    }, f, indent=2)
print("Results saved to outputs/lpa_irr_results.json")
print("Manual codings saved to outputs/lpa_coder2_manual.json")

with open('outputs/lpa_coder2_manual.json', 'w') as f:
    json.dump(coder2, f, indent=2)
