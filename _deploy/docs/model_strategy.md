# LinguaGraph — Model Merging & Fine-Tuning Strategy

> **Status:** Future Work (Phase 2) · **Priority:** Low (for BWKI) · **Target:** Post-BWKI
>
> **⚠️ 2026-06-18 Decision:** This is deferred to after the BWKI submission. The immediate priority is
> Human Data Collection → Pilot Analysis → Results Pipeline. Model training, while technically valuable,
> does not block the competition entry. See `docs/PRIORITIES.md` for the current roadmap.

## 1. Vision

Replace the current API-dependent concept extraction (GPT-4.1-mini / Qwen3-8B via Ollama) with a **self-contained, locally-embedded, project-specific model** that:

- Runs entirely offline — no API calls, no internet dependency
- Fits on mobile devices (<2 GB RAM, <500 MB download)
- Performs concept + relation extraction from trilingual text (ZH/DE/EN)
- Is specifically fine-tuned for LinguaGraph's social issues domain
- Is reproducible and auditable for a scientific competition

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Current Architecture                          │
│                                                                  │
│  API/Ollama ──→ extract.py ──→ graph.py ──→ scoring.py          │
│  (external)       (prompt)       (NetworkX)    (LDS)            │
└─────────────────────────────────────────────────────────────────┘

                        ↓ REPLACE ↓

┌─────────────────────────────────────────────────────────────────┐
│                   Target Architecture                            │
│                                                                  │
│  ┌─────────────────────────────────┐                            │
│  │   LinguaGraph-1.5B-Instruct     │                            │
│  │   (Qwen2.5 base, LoRA adapted,  │──→ graph.py ──→ scoring.py│
│  │    GGUF Q4_K_M quantized)       │    (no change) (no change) │
│  └─────────────────────────────────┘                            │
│        ↑ Local llama.cpp runtime                                 │
│        ↑ No API, no internet                                     │
│        ↑ ~900 MB disk, ~1.5 GB RAM                               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Principle

The **only module that changes** is the LLM provider in `src/providers/`. The entire pipeline downstream (graph construction, LDS calculation, cross-language analysis) stays exactly as-is. This guarantees backward compatibility and allows A/B testing between API models and the local model.

---

## 3. Model Selection

### Candidate Matrix

| Model | Params | ZH | DE | EN | RAM | Mobile | Notes |
|-------|--------|:--:|:--:|:--:|:---:|:------:|-------|
| **Qwen2.5-1.5B-Instruct** | 1.5B | ✅ | ✅ | ✅ | ~3 GB | ✅ | **Primary choice** — strong trilingual, tiny |
| Qwen2.5-7B-Instruct | 7B | ✅ | ✅ | ✅ | ~14 GB | ❌ | Fallback if 1.5B underperforms |
| Llama-3.2-3B-Instruct | 3B | ⚠️ | ✅ | ✅ | ~6 GB | ⚠️ | Weak Chinese, good DE/EN |
| Gemma-2-2B | 2B | ⚠️ | ✅ | ✅ | ~4 GB | ⚠️ | Weak Chinese, small vocab |
| Phi-3.5-mini-Instruct | 3.8B | ⚠️ | ✅ | ✅ | ~8 GB | ❌ | Weak Chinese |
| **After merging:** | | | | | | | |
| LinguaGraph-1.5B-Merged | 1.5B | ✅+ | ✅+ | ✅+ | ~3 GB | ✅ | Qwen2.5 + multilingual expert LoRAs |

### Why Qwen2.5-1.5B as Base

| Factor | Assessment |
|--------|-----------|
| **Multilingual** | Trained on >100 languages, strong ZH/DE/EN |
| **Size** | 1.5B → GGUF Q4_K_M ~900 MB — fits on any phone |
| **Knowledge** | Already knows social concepts (freedom, justice, etc.) |
| **Instruct** | Chat format aligns with our extraction prompt |
| **Ecosystem** | Full HuggingFace + llama.cpp + MLX support |
| **License** | Apache 2.0 — compatible with BWKI requirements |

---

## 4. Model Merging Strategy

### 4.1 Why Merge?

Merging combines the strengths of multiple fine-tuned models into one without retraining:

- **Multilingual boost**: Merge a Chinese-specialized LoRA + German-specialized LoRA + English-specialized LoRA
- **Task specialization**: Merge a concept-extraction LoRA with a relation-extraction LoRA
- **No extra inference cost**: Same 1.5B parameter count at runtime

### 4.2 Merging Techniques

| Technique | When to Use | Complexity | Quality |
|-----------|-------------|:----------:|:-------:|
| **Linear (SLERP)** | Two models, similar base | Low | Good |
| **TIES-Merging** | >2 models, conflicting params | Medium | Best |
| **DARE** | >2 models, sparse diff | High | Best for sparse |

**Recommended**: SLERP for 2-model merges, TIES for 3+ model merges.

### 4.3 Merge Architecture (Tree)

```
                   Qwen2.5-1.5B-Instruct (base)
                   /         |           \
                  /          |            \
    ZH-LoRA (LoRA adapt)  DE-LoRA     EN-LoRA
         \                  |            /
          \                 |           /
           └─── TIES-Merge ────────────┘
                      |
            LinguaGraph-1.5B-Merged
                      |
              Task LoRA: concept_extraction
                      |
            LinguaGraph-1.5B-Instruct (final)
                      |
              GGUF Q4_K_M Quantization
                      |
            lingua_graph_model.gguf (~900 MB)
```

### 4.4 SLERP (Spherical Linear Interpolation)

For merging two fine-tuned models:

```python
# Conceptually:
θ_merged = slerp(θ_model_A, θ_model_B, t=0.5)
# t=0.5 gives equal weight to both
```

Best for merging:
- ZH-LoRA → DE-LoRA (multilingual)
- Extraction-LoRA → Relation-LoRA (task fusion)

### 4.5 TIES-Merging

For merging 3+ models with potential parameter conflicts:

1. **Trim**: Keep only top-k% of parameter changes (remove noise)
2. **Elect Sign**: For each parameter, majority vote on direction (+/-)
3. **Disjoint Merge**: Average only parameters that agree on sign

```python
# Using mergekit (YAML config):
merge:
  - model: zh_lora_merged
  - model: de_lora_merged
  - model: en_lora_merged
merge_method: ties
base_model: Qwen/Qwen2.5-1.5B-Instruct
parameters:
  normalize: true
  int8_mask: true
```

---

## 5. Fine-Tuning Strategy

### 5.1 Approach: LoRA (Low-Rank Adaptation)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Method | QLoRA (quantized 4-bit base) | Fits 1.5B on 8 GB GPU |
| Rank (r) | 16 | Good balance for small dataset |
| Alpha | 32 | Default scaling |
| Target modules | q_proj, v_proj, k_proj, o_proj | All attention layers |
| Dataset size | 500-2000 examples | Synthetic + gold labels |
| Epochs | 3-5 | Prevent overfitting on small data |
| Learning rate | 2e-4 | Standard LoRA LR |

### 5.2 Training Data

| Source | Count | Languages | Quality | Status |
|--------|:-----:|:---------:|:-------:|:------:|
| Gold labels (existing) | 20 | ZH/DE/EN | ★★★★★ | ✅ Existing (calculus domain) |
| Gold labels (social issues) | 30-60 | ZH/DE/EN | ★★★★★ | ❌ Needs annotation |
| Wikipedia corpus | 90 | ZH/DE/EN | ★★★★☆ | ✅ Existing, needs extraction |
| Education texts | 60 | ZH/DE/EN | ★★★★☆ | ✅ Existing |
| GPT-4.1-mini extractions | 300+ | ZH/DE/EN | ★★★☆☆ | ⚠️ Needs validation |
| Synthetic (template-based) | 500+ | ZH/DE/EN | ★★☆☆☆ | ⚠️ Needs generation |
| **Total target** | **1000+** | | | |

### 5.3 Data Format (Alpaca-style)

```json
{
  "instruction": "Extract concepts and relations from this answer about freedom.",
  "input": "Freedom means being able to make your own choices without external control.",
  "output": "{\"concepts\": [\"freedom\", \"choice\", \"autonomy\", \"control\"], \"relations\": [{\"source\": \"freedom\", \"target\": \"choice\", \"type\": \"represents\"}, {\"source\": \"freedom\", \"target\": \"autonomy\", \"type\": \"represents\"}, {\"source\": \"freedom\", \"target\": \"control\", \"type\": \"opposite_of\"}]}"
}
```

### 5.4 Training Configuration

```yaml
# LoRA config
model:
  base: Qwen/Qwen2.5-1.5B-Instruct
  load_in_4bit: true
  bnb_4bit_compute_dtype: bfloat16

lora:
  r: 16
  lora_alpha: 32
  target_modules: ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj"]
  lora_dropout: 0.05

training:
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 2e-4
  num_train_epochs: 5
  save_steps: 50
  logging_steps: 10
  eval_strategy: steps
  eval_steps: 50
```

---

## 6. Quantization Plan

### 6.1 Format Selection

| Format | Precision | Size (1.5B) | RAM | Speed | Platform |
|--------|:---------:|:-----------:|:---:|:----:|----------|
| FP16 | 16-bit | ~3.0 GB | ~4 GB | Fast | GPU only |
| Q8_0 | 8-bit | ~1.6 GB | ~2.5 GB | Fast | CPU/GPU |
| **Q4_K_M** | **4-bit** | **~900 MB** | **~1.5 GB** | **Medium** | **CPU/Mobile** |
| Q3_K_S | 3-bit | ~700 MB | ~1.2 GB | Slow | Mobile |
| IQ4_NL | 4-bit | ~850 MB | ~1.4 GB | Medium | Mobile optimized |

**Recommended: Q4_K_M** — best quality/size tradeoff for mobile deployment.

### 6.2 Quantization Pipeline

```bash
# Step 1: Convert to GGUF
python convert.py lingua_graph_model/ \
  --outfile models/lingua_graph_model.gguf \
  --outtype q4_k_m

# Step 2: Verify
llama-cli -m models/lingua_graph_model.gguf \
  -p "Extract concepts from: Freiheit bedeutet..." \
  -n 256
```

---

## 7. Integration into Project

### 7.1 New Provider: `src/providers/local.py`

```python
class LocalProvider(LLMProvider):
    """Local GGUF model via llama.cpp Python bindings."""

    def __init__(self, config: dict = None):
        config = config or {}
        model_path = config.get("model_path", "models/lingua_graph_model.gguf")
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=-1)

    def extract(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=0.1,
            max_tokens=512
        )
        return response["choices"][0]["message"]["content"]
```

### 7.2 Config Update

```yaml
# config.yaml
llm:
  provider: local           # Was: ollama / openai
  local:
    model_path: models/lingua_graph_model.gguf
    n_ctx: 2048
    n_gpu_layers: -1
    use_mlx: false          # Apple Silicon optimization
```

### 7.3 Factory Update

```python
# src/providers/__init__.py
from .local import LocalProvider

def get_provider(config: dict = None) -> LLMProvider:
    provider_name = llm_config.get("provider", "ollama")
    if provider_name == "local":
        return LocalProvider(llm_config.get("local", {}))
    elif provider_name == "ollama":
        return OllamaProvider(...)
    elif provider_name == "openai":
        return OpenAIProvider(...)
```

---

## 8. Hardware Requirements

### Training (One-time)

| Resource | Minimum | Recommended |
|----------|:-------:|:-----------:|
| GPU | 8 GB VRAM (RTX 3070) | 24 GB VRAM (RTX 4090) |
| RAM | 16 GB | 32 GB |
| Disk | 10 GB free | 20 GB free |
| Time (1 epoch 500 samples) | ~15 min (RTX 4090) | ~30 min (RTX 3070) |
| Total training time | ~2 hours | ~4 hours |

### Inference (Perpetual)

| Platform | RAM | Disk | Speed (tokens/s) |
|----------|:---:|:----:|:----------------:|
| Desktop GPU | 1.5 GB | 900 MB | 30-50 tok/s |
| Desktop CPU | 2 GB | 900 MB | 5-10 tok/s |
| Laptop CPU | 2 GB | 900 MB | 3-8 tok/s |
| Phone (Android/iOS) | 1.5 GB | 900 MB | 2-5 tok/s |

---

## 9. Roadmap & Phases

### Phase 0: Data Preparation (Week 1-2)

| Task | Output | Dependencies |
|------|--------|:------------:|
| Annotate 30 social-issues gold labels | `data/gold/social_issues_gold.json` | Human annotators |
| Convert existing responses to Alpaca format | `data/training/train.json` | None |
| Generate synthetic training data (500+) | `data/training/synthetic.json` | GPT-4.1-mini API |
| Create train/val/test split | `data/training/split.json` | Training data |

### Phase 1: Base Model Setup (Week 2-3)

| Task | Output | Dependencies |
|------|--------|:------------:|
| Download Qwen2.5-1.5B-Instruct | `models/qwen2.5-1.5b/` | Internet |
| Verify multilingual extraction baseline | Benchmark scores | Phase 0 |
| Test LoRA training infrastructure | Training script | GPU environment |
| Create QLoRA config | `config/training/lora_config.yaml` | Phase 1 |

### Phase 2: Fine-tuning (Week 3-4)

| Task | Output | Dependencies |
|------|--------|:------------:|
| Train ZH extraction LoRA | `models/lora_zh/` | Phase 0 + 1 |
| Train DE extraction LoRA | `models/lora_de/` | Phase 0 + 1 |
| Train EN extraction LoRA | `models/lora_en/` | Phase 0 + 1 |
| Cross-validation: leave-one-language-out | Evaluation report | All LoRAs |

### Phase 3: Model Merging (Week 4-5)

| Task | Output | Dependencies |
|------|--------|:------------:|
| SLERP merge ZH+DE LoRAs | `models/merged_zh_de/` | Phase 2 |
| TIES merge all 3 LoRAs | `models/merged_all/` | Phase 2 |
| Compare merged vs single vs API | Benchmark report | Phase 2 + evaluation |
| **Gate: merged model must beat single-language LoRA** | Decision: proceed or iterate | |

### Phase 4: Quantization & Deployment (Week 5-6)

| Task | Output | Dependencies |
|------|--------|:------------:|
| GGUF conversion (Q4_K_M) | `models/lingua_graph_model.gguf` | Phase 3 |
| Benchmark speed + quality | Benchmark metrics | Quantized model |
| Create `LocalProvider` | `src/providers/local.py` | None |
| Integration test: full pipeline | Test report | LocalProvider |
| Mobile test (llama.cpp Android) | Mobile benchmark | GGUF model |

### Phase 5: Documentation & Release (Week 6)

| Task | Output | Dependencies |
|------|--------|:------------:|
| Training reproducibility doc | `docs/training_pipeline.md` | All phases |
| Model card (HuggingFace) | `MODEL_CARD.md` | Phase 4 |
| Update CLAUDE.md, CHANGELOG | Updated docs | All phases |
| Release v0.2 with local model | GitHub Release v0.2 | All phases |

### Timeline Overview

```
Week 1     2     3     4     5     6
├────┤├────┤├────┤├────┤├────┤├────┤
    Phase 0                     Data Preparation
          Phase 1               Base Model Setup
                Phase 2         Fine-tuning
                      Phase 3   Model Merging
                            Phase 4  Quantization
                                  Phase 5  Docs
```

---

## 10. Evaluation Criteria

### 10.1 Quality Metrics

| Metric | Current (Qwen3-8B) | Target (Local 1.5B) | Stretch |
|--------|:------------------:|:-------------------:|:-------:|
| Concept F1 | ~0.85 | **≥0.80** | ≥0.85 |
| Relation F1 | ~0.75 | **≥0.70** | ≥0.75 |
| JSON valid rate | ~95% | **≥95%** | 99% |
| ZH Concept F1 | ~0.85 | **≥0.78** | ≥0.83 |
| DE Concept F1 | ~0.82 | **≥0.75** | ≥0.80 |
| EN Concept F1 | ~0.88 | **≥0.82** | ≥0.87 |

### 10.2 Performance Metrics

| Metric | Qwen3-8B (Ollama) | Qwen2.5-1.5B (GGUF) | Improvement |
|--------|:-----------------:|:--------------------:|:-----------:|
| Latency (first token) | ~500 ms | **~50 ms** | 10× |
| Throughput | ~30 tok/s | **~30-50 tok/s** | Similar |
| RAM usage | ~16 GB | **~1.5 GB** | 10× |
| Disk usage | ~4.5 GB | **~900 MB** | 5× |
| Internet required | No (local) | **No** | Same |
| Cost per extraction | $0 | **$0** | Same |

### 10.3 Ablation Study Design

For the BWKI paper:

| Configuration | Concept F1 | Relation F1 | Size | Notes |
|-------------|:----------:|:-----------:|:----:|-------|
| GPT-4.1-mini (API) | Baseline | Baseline | N/A | Upper bound |
| Qwen3-8B (Ollama) | T1 | T1 | 4.5 GB | Current local |
| **LinguaGraph-1.5B (final)** | **Target** | **Target** | **0.9 GB** | **Proposed** |
| Qwen2.5-1.5B (base, no FT) | Ablation | Ablation | 0.9 GB | No fine-tuning |
| Qwen2.5-1.5B + LoRA (ZH only) | Ablation | Ablation | 0.9 GB | No merging |
| TIES merge (no task LoRA) | Ablation | Ablation | 0.9 GB | No task adaptation |

This table **is the experiment** — it proves every design decision.

---

## 11. Risk Assessment

### 11.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|------------|
| 1.5B too small for extraction task | Medium | High | Benchmark early; fallback to 3B or 7B |
| Training data too small (<500) | High | High | Synthetic data generation + data augmentation |
| Multilingual degradation after merge | Medium | Medium | Per-language eval after each merge step |
| GGUF quality loss in Q4_K_M | Low | Medium | Compare Q8_0 as reference |
| Python llama.cpp bindings unavailable | Low | High | Fallback to subprocess calling llama-cli |

### 11.2 Project Risks

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|------------|
| GPU not available for training | Medium | High | Use Google Colab (free T4) or RunPod ($0.5/hr) |
| Time to train exceeds schedule | Medium | Medium | Start with smallest config; iterate |
| BWKI rules prohibit custom model | Low | High | Keep API fallback; model is supplementary |

### 11.3 Contingencies

1. **If 1.5B underperforms**: Use Qwen2.5-7B GGUF (Q3_K_M = ~3.5 GB, still feasible on desktop)
2. **If no GPU**: Use Google Colab free tier (T4 16 GB VRAM) or RunPod ($0.44/hr for RTX 4090)
3. **If merge quality is poor**: Use the best single-language LoRA without merging
4. **If time runs out**: Skip merging, just fine-tune one multilingual LoRA

---

## 12. Tools & Dependencies

### Training Stack

| Tool | Purpose | Install |
|------|---------|---------|
| `transformers` | Model loading/training | `pip install transformers` |
| `peft` | LoRA adapters | `pip install peft` |
| `bitsandbytes` | 4-bit quantization | `pip install bitsandbytes` |
| `trl` | SFT trainer | `pip install trl` |
| `datasets` | Data handling | `pip install datasets` |
| `accelerate` | Multi-GPU | `pip install accelerate` |
| `mergekit` | Model merging | `pip install mergekit` |
| `llama.cpp` | GGUF conversion | `git clone && make` |

### Inference Stack

| Tool | Purpose | Size |
|------|---------|:----:|
| `llama-cpp-python` | Python bindings | ~50 MB |
| `llama.cpp` (Android) | Mobile runtime | ~30 MB APK |
| `mlx` (Apple Silicon) | Mac optimization | ~20 MB |

---

## 13. Key Decisions Log

| # | Decision | Date | Rationale |
|---|----------|:----:|-----------|
| 1 | Qwen2.5-1.5B as primary base | — | Best trilingual support at smallest size |
| 2 | LoRA over full fine-tuning | — | 100× cheaper, equally good for narrow task |
| 3 | Q4_K_M quantization | — | Best quality/size for mobile deployment |
| 4 | TIES for 3+ model merge | — | Handles parameter conflicts across languages |
| 5 | New provider class (no pipeline change) | — | Full backward compatibility |
| 6 | Synthetic data augmentation | — | Required to reach 500+ training examples |
| 7 | Keep API providers as fallback | — | Graceful degradation if local model fails |

---

## 14. Dependencies Graph

```
Data Preparation (Phase 0)
    ↕
Base Model Setup (Phase 1)
    ↕
Fine-tuning (Phase 2)
    ↓
Model Merging (Phase 3)
    ↓
Quantization & Deployment (Phase 4)
    ↕
Documentation (Phase 5)
    ↓
Integration into Project
    ↓
BWKI Full Submission (Sept 2026)
```

Critical path: Phase 0 → 1 → 2 → 3 → 4 → BWKI submission

---

*Document version: v1.0 · 2026-06-18*
*Author: Claude (PM + QA Lead) for LinguaGraph project*
