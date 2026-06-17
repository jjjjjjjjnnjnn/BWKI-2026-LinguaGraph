"""
Test: v3 Pipeline Evaluation (using inline demo data)

Tests calculate_mcl_score with a simple calculus graph.
This is a self-contained test that does not depend on external data files.
"""
import sys, json
sys.path.insert(0, 'src')
from scoring import calculate_mcl_score
import networkx as nx

# Self-contained test data (calculus domain expert graph)
expert = nx.DiGraph()
expert.add_edges_from([
    ('极限', '导数'), ('导数', '变化率'), ('积分', '导数'),
    ('积分', '面积'), ('导数', '切线斜率')
])

# Student graph (simulates what a learner might have)
student = nx.DiGraph()
student.add_edges_from([
    ('导数', '变化率'), ('积分', '面积')
])

mcl = calculate_mcl_score(student, expert)

print('=== v3 Pipeline Evaluation ===')
print('Student nodes:', student.number_of_nodes())
print('Student edges:', student.number_of_edges())
print('Expert nodes:', expert.number_of_nodes())
print('Expert edges:', expert.number_of_edges())
print('MCL Score:', f"{mcl['mcl_score']}%", f"({mcl['missing_count']}/{mcl['total_expert']} missing)")

# Assert expected results
assert mcl['missing_count'] == 3, f"Expected 3 missing edges, got {mcl['missing_count']}"
assert mcl['total_expert'] == 5, f"Expected 5 expert edges, got {mcl['total_expert']}"
print("\nAll assertions passed!")
