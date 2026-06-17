"""
LinguaGraph — ConceptNet Relation Taxonomy Reference

Based on ConceptNet5's relation hierarchy (Apache 2.0).
https://github.com/commonsense/conceptnet5

This file defines the standard relation types that LinguaGraph's
relation extraction can reference. It is NOT used by the core pipeline
— it serves as documentation and future integration reference.
"""

# ConceptNet5 Core Relation Types
# Source: ConceptNet5 paper (Havasi et al., 2017) + ConceptNet5 codebase
#
# These are the 30+ relation types ConceptNet uses to label edges
# between concepts. LinguaGraph currently uses a subset (6 types).
# This taxonomy provides theoretical grounding for future expansion.

CONCEPTNET_RELATIONS = {
    # --- Symmetric ---
    "RelatedTo": "A is related to B (most general relation)",
    "Synonym": "A and B have the same meaning",
    "Antonym": "A and B are opposites",
    "DistinctFrom": "A and B are distinct concepts",

    # --- Causal ---
    "Causes": "A causes B",
    "CausesDesire": "A causes desire for B",
    "MotivatedByGoal": "A is motivated by goal B",
    "Desires": "A desires B",

    # --- Taxonomic ---
    "IsA": "A is a type of B (hypernymy/hyponymy)",
    "InstanceOf": "A is an instance of B (instance-of)",
    "PartOf": "A is a part of B (meronymy)",
    "MemberOf": "A is a member of B",
    "SubeventOf": "A is a sub-event of B",
    "MannerOf": "A is a manner of doing B",
    "PropertyOf": "A is a property of B",
    "DefinedAs": "A is defined as B",

    # --- Functional ---
    "UsedFor": "A is used for B",
    "CapableOf": "A is capable of B",
    "HasA": "A has B (possession)",
    "HasProperty": "A has property B",
    "HasContext": "A has context B",
    "HasPrerequisite": "A has prerequisite B",
    "HasFirstSubevent": "A's first subevent is B",
    "HasLastSubevent": "A's last subevent is B",
    "ReceivesAction": "A receives action B",

    # --- Spatial / Temporal ---
    "LocatedNear": "A is located near B",
    "AtLocation": "A is located at B",
    "CreatedBy": "A is created by B",
    "UsedFor": "A is used for B",
    "SymbolOf": "A is a symbol of B",

    # --- Linguistic ---
    "DerivedFrom": "A is derived from B (etymology)",
    "EtymologicallyRelatedTo": "A is etymologically related to B",
    "EtymologicallyDerivedFrom": "A is etymologically derived from B",
    "FormOf": "A is a form of B (inflection)",
    "TranslationOf": "A is a translation of B",
}

# --- LinguaGraph Current Relation Types ---
# These 6 types are what the current extract.py produces.
# The mapping below shows which ConceptNet types they correspond to.

LINGUAGRAPH_TO_CONCEPTNET = {
    "part_of":          "PartOf",
    "cause_effect":     "Causes",
    "requires":         "HasPrerequisite",
    "equivalent":       "Synonym",
    "opposes":          "Antonym",
    "relates_to":       "RelatedTo",
    "supports":         "CausesDesire",    # LinguaGraph-specific
    "influences":       "RelatedTo",       # LinguaGraph-specific
    "conflicts_with":   "Antonym",         # LinguaGraph-specific
}

CONCEPTNET_TO_LINGUAGRAPH = {
    v: k for k, v in LINGUAGRAPH_TO_CONCEPTNET.items()
}


def get_relation_hierarchy() -> dict:
    """
    Return ConceptNet relation hierarchy grouped by category.

    Useful for future integration when extending LinguaGraph's
    relation type set.
    """
    return {
        "causal": ["Causes", "CausesDesire", "MotivatedByGoal", "Desires"],
        "taxonomic": ["IsA", "PartOf", "MemberOf", "SubeventOf", "InstanceOf",
                      "MannerOf", "PropertyOf", "DefinedAs"],
        "functional": ["UsedFor", "CapableOf", "HasA", "HasProperty",
                       "HasContext", "HasPrerequisite"],
        "symmetric": ["RelatedTo", "Synonym", "Antonym", "DistinctFrom"],
        "spatial": ["LocatedNear", "AtLocation"],
        "temporal_sequential": ["HasFirstSubevent", "HasLastSubevent"],
        "linguistic": ["DerivedFrom", "FormOf", "TranslationOf"],
    }


if __name__ == "__main__":
    print("=== ConceptNet Relation Taxonomy Reference ===\n")
    print(f"Total ConceptNet relation types: {len(CONCEPTNET_RELATIONS)}")
    print(f"LinguaGraph current types: {len(LINGUAGRAPH_TO_CONCEPTNET)}")
    print(f"Potential expansion: {len(CONCEPTNET_RELATIONS) - len(LINGUAGRAPH_TO_CONCEPTNET)} types available\n")

    print("LinguaGraph → ConceptNet mapping:")
    for lg, cn in sorted(LINGUAGRAPH_TO_CONCEPTNET.items()):
        print(f"  {lg:20s} → {cn}")

    print("\nHierarchy:")
    for category, relations in get_relation_hierarchy().items():
        print(f"  {category}:")
        for r in relations:
            print(f"    - {r}: {CONCEPTNET_RELATIONS.get(r, '?')}")
