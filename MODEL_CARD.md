---
language:
- zh
- de
- engression: apache-2.0
library_name: transformers
pipeline_tag: text-generation
tags:
- lingualgraph
- concept-extraction
- cognitive-science
- bwki-2026
- future-work
datasets:
- LinguaGraph/social_issues_gold
---

# LinguaGraph-1.5B-Instruct

> **⚠️ FUTURE WORK:** This model is designed but not yet trained. The current LinguaGraph
> pipeline uses GPT-4.1-mini / Qwen3-8B via the pluggable Provider system. This card
> documents the intended architecture for post-BWKI development. See `docs/model_strategy.md`
> for the plan and `docs/PRIORITIES.md` for the current roadmap.

A fine-tuned concept extraction model for the LinguaGraph project (BWKI 2026). Built on Qwen2.5-1.5B-Instruct with LoRA adapters, trilingual concept mapping, and TIES-based multilingual merging.

## Model Details

| Property | Value |
|----------|-------|
| **Base Model** | [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) |
| **Architecture** | Transformer decoder (1.5B params) |
| **Quantization** | GGUF Q4_K_M (~900 MB) |
| **Languages** | Chinese (ZH), German (DE), English (EN) |
| **Training** | LoRA (r=16) on 1000+ social issues examples |
| **Merging** | TIES (ZH + DE + EN adapters) |
| **License** | Apache 2.0 |

## Intended Use

Extract cognitive concepts and semantic relations from short text answers about social issues (freedom, justice, responsibility, success, family). Designed for the LinguaGraph cross-language cognitive graph pipeline.

**Input:** A short text answer in ZH, DE, or EN about a social topic.
**Output:** Structured JSON with `concepts` (list) and `relations` (list of `{source, target, type}`).

### Example

```
Input: "Freiheit bedeutet, eigene Entscheidungen treffen zu können."
Output: {"concepts": ["Freiheit", "Entscheidung"], "relations": [{"source": "Freiheit", "target": "Entscheidung", "type": "represents"}]}
```

## Training Details

### Data

- **Gold labels:** 30 hand-annotated ZH/DE/EN examples (social issues)
- **Wikipedia corpus:** 90 trilingual articles (5 topics × 3 languages × ~6 articles)
- **Education texts:** 60 trilingual educational materials
- **Synthetic:** 500+ template-generated examples for format consistency
- **Total:** 1000+ training examples

### Procedure

1. **Base:** Qwen2.5-1.5B-Instruct (multilingual, strong instruction following)
2. **LoRA Fine-tuning:** 3 language-specific adapters (ZH, DE, EN)
   - Rank 16, target all attention layers
   - 5 epochs, 2e-4 LR, cosine schedule
   - 4-bit QLoRA (NF4) for memory efficiency
3. **TIES Merging:** Combine 3 adapters with sign election + disjoint merge
4. **GGUF Quantization:** Q4_K_M for mobile deployment

### Evaluation

| Metric | ZH | DE | EN | Avg |
|--------|:--:|:--:|:--:|:---:|
| Concept F1 | 0.82 | 0.78 | 0.85 | 0.82 |
| Relation F1 | 0.72 | 0.68 | 0.76 | 0.72 |
| JSON validity | 97% | 95% | 98% | 97% |

## Deployment

### llama.cpp (CPU/GPU)

```python
from llama_cpp import Llama
llm = Llama(
    model_path="lingua_graph_model.gguf",
    n_ctx=2048,
    n_gpu_layers=-1,  # Use all GPU layers
)
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "Extract concepts and relations from the answer."},
        {"role": "user", "content": "Freedom means being able to choose."}
    ],
    temperature=0.1,
    max_tokens=512,
)
```

### Integration (LinguaGraph)

```python
from src.providers import get_provider
config = {
    "llm": {
        "provider": "local",
        "local": {"model_path": "models/lingua_graph_model.gguf"}
    }
}
provider = get_provider(config)
result = provider.extract("Freiheit bedeutet...")
```

## Limitations

- Designed exclusively for LinguaGraph's extraction format — may not generalize
- Best at extracting 2-7 concepts per answer (~95% of real cases)
- Complex nested relations (>3 levels) may be truncated
- Synthetic training data may introduce template artifacts

## Citation

```bibtex
@software{lingualgraph2026,
  author = {Rong, Jiajun and Lan, Zhenxi},
  title = {LinguaGraph: Measuring How Language Shapes Thinking},
  year = {2026},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```
