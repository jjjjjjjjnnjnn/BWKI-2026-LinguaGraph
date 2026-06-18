# LinguaGraph — Training Pipeline

> **Companion to** `docs/model_strategy.md`

## Overview

This document specifies the exact commands, configurations, and procedures for training, merging, and deploying the LinguaGraph local model.

---

## 0. Environment Setup

### 0.1 Python Environment

```bash
# Create conda environment
conda create -n linguagraph-training python=3.11 -y
conda activate linguagraph-training

# Install core ML dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install transformers>=4.40.0 peft>=0.10.0 bitsandbytes>=0.43.0
pip install trl>=0.8.0 datasets>=2.18.0 accelerate>=0.28.0
pip install mergekit huggingface-hub[hf_transfer]

# For GGUF conversion
pip install llama-cpp-python

# Verify GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
```

### 0.2 Directory Structure

```
BWKI-2026-备战/
├── models/                          # Model storage
│   ├── base/                        # Base (unmodified) models
│   │   └── qwen2.5-1.5b-instruct/  # Downloaded from HuggingFace
│   ├── lora/                        # LoRA adapters
│   │   ├── zh_extraction/
│   │   ├── de_extraction/
│   │   ├── en_extraction/
│   │   └── multilingual/
│   ├── merged/                      # Post-merge models
│   │   ├── merged_zh_de/
│   │   └── merged_all/
│   └── gguf/                        # Quantized models
│       └── lingua_graph_model.gguf
├── data/training/                   # Training datasets
│   ├── train.json
│   ├── val.json
│   ├── test.json
│   └── synthetic.json
├── config/training/                 # Training configs
│   ├── lora_config.yaml
│   ├── merge_config.yaml
│   └── quantize_config.yaml
├── scripts/
│   ├── prepare_training_data.py
│   ├── train_lora.py
│   ├── merge_models.py
│   └── quantize_model.py
└── evaluation/
    └── benchmark_local_model.py
```

---

## 1. Data Preparation

### 1.1 Convert Gold Labels to Alpaca Format

```bash
python scripts/prepare_training_data.py \
  --input data/gold/gold_dataset.json \
  --output data/training/train.json \
  --format alpaca \
  --split train,val,test
```

### 1.2 Generate Synthetic Data

```bash
python scripts/prepare_training_data.py \
  --generate-synthetic 500 \
  --output data/training/synthetic.json \
  --language zh,de,en \
  --topics freedom,justice,responsibility,success,family
```

### 1.3 Data Format

Each example in `data/training/train.json`:

```json
[
  {
    "instruction": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Freiheit.",
    "input": "Freiheit bedeutet, eigene Entscheidungen treffen zu können, ohne von anderen eingeschränkt zu werden.",
    "output": "{\"concepts\": [\"Freiheit\", \"Entscheidung\", \"Einschränkung\"], \"relations\": [{\"source\": \"Freiheit\", \"target\": \"Entscheidung\", \"type\": \"represents\"}, {\"source\": \"Freiheit\", \"target\": \"Einschränkung\", \"type\": \"opposite_of\"}]}"
  }
]
```

---

## 2. LoRA Training

### 2.1 Single-Language LoRA

```bash
python scripts/train_lora.py \
  --base-model models/base/qwen2.5-1.5b-instruct \
  --train-file data/training/train.json \
  --val-file data/training/val.json \
  --language zh \
  --output-dir models/lora/zh_extraction \
  --config config/training/lora_config.yaml
```

### 2.2 LoRA Training Script

`scripts/train_lora.py`:

```python
"""
LoRA fine-tuning for LinguaGraph concept extraction.
Trains a language-specific adapter on top of Qwen2.5-1.5B-Instruct.
"""

import json
import sys
from pathlib import Path

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer


def load_training_data(file_path: str, language: str = None) -> Dataset:
    """Load and filter training data by language."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    if language:
        data = [d for d in data if d.get("language", language) == language]
    return Dataset.from_list(data)


def format_alpaca(example: dict) -> dict:
    """Format example as Alpaca-style instruction."""
    text = (
        f"### Instruction:\n{example['instruction']}\n\n"
        f"### Input:\n{example['input']}\n\n"
        f"### Response:\n{example['output']}"
    )
    return {"text": text}


def create_model(base_model: str, device_map: str = "auto"):
    """Create quantized model for LoRA training."""
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        device_map=device_map,
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)
    return model


def create_lora_config(r: int = 16) -> LoraConfig:
    return LoraConfig(
        r=r,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )


def train(args):
    # Load and format data
    dataset = load_training_data(args.train_file, args.language)
    dataset = dataset.map(format_alpaca)

    val_dataset = load_training_data(args.val_file, args.language)
    val_dataset = val_dataset.map(format_alpaca)

    # Create model + tokenizer
    model = create_model(args.base_model)
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    tokenizer.pad_token = tokenizer.eos_token

    # LoRA config
    peft_config = create_lora_config(r=args.lora_r)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        num_train_epochs=5,
        logging_steps=10,
        save_steps=50,
        eval_strategy="steps",
        eval_steps=50,
        bf16=True,
        save_total_limit=2,
        remove_unused_columns=False,
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=val_dataset,
        peft_config=peft_config,
        tokenizer=tokenizer,
        max_seq_length=1024,
        dataset_text_field="text",
    )

    # Train
    trainer.train()

    # Save adapter
    trainer.save_model(args.output_dir)
    print(f"[OK] Model saved to {args.output_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--train-file", required=True)
    parser.add_argument("--val-file", required=True)
    parser.add_argument("--language", default="zh")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--config", default=None)
    args = parser.parse_args()
    train(args)
```

### 2.3 Expected Training Run

For 500 training examples, 5 epochs, batch size 4, grad accum 4:

```
Training: 500 samples × 5 epochs = 2500 steps
          2500 / (4 × 4) = ~156 optimizer steps
          At 2s/step ≈ 5 minutes on RTX 4090
          At 5s/step ≈ 13 minutes on RTX 3070
                          ≈ 18 minutes on Google Colab T4
```

---

## 3. Model Merging

### 3.1 SLERP Merge (Two Models)

```bash
python scripts/merge_models.py \
  --method slerp \
  --model-a models/lora/zh_extraction \
  --model-b models/lora/de_extraction \
  --base-model models/base/qwen2.5-1.5b-instruct \
  --output models/merged/merged_zh_de
```

### 3.2 TIES Merge (Three Models)

```bash
python scripts/merge_models.py \
  --method ties \
  --models models/lora/zh_extraction models/lora/de_extraction models/lora/en_extraction \
  --base-model models/base/qwen2.5-1.5b-instruct \
  --output models/merged/merged_all
```

### 3.3 MergeKit Configuration

`config/training/merge_config.yaml`:

```yaml
# TIES merge configuration
merge_method: ties
base_model: Qwen/Qwen2.5-1.5B-Instruct

models:
  - model: zh_extraction
    parameters:
      weight: 0.4
  - model: de_extraction
    parameters:
      weight: 0.3
  - model: en_extraction
    parameters:
      weight: 0.3

parameters:
  normalize: true
  int8_mask: true
  resize_token_embeddings: false
  
tokenizer:
  trust_remote_code: true
  
dtype: bfloat16
```

Merge command:

```bash
mergekit-yaml config/training/merge_config.yaml models/merged/merged_all \
  --copy-tokenizer \
  --trust-remote-code \
  --allow-crimes  # Allow merging differently-sized models (safe for same-base)
```

---

## 4. Quantization to GGUF

### 4.1 Using llama.cpp

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git

# Build
cd llama.cpp
make -j

# Convert merged model to GGUF FP16
python convert.py ../models/merged/merged_all/ \
  --outfile ../models/gguf/lingua_graph_model_fp16.gguf

# Quantize to Q4_K_M
./llama-quantize \
  ../models/gguf/lingua_graph_model_fp16.gguf \
  ../models/gguf/lingua_graph_model.gguf \
  q4_k_m

# Verify
./llama-cli \
  -m ../models/gguf/lingua_graph_model.gguf \
  -p "Extract concepts from: Freedom is..." \
  -n 256
```

### 4.2 MLX (Apple Silicon)

```bash
# Alternative for Mac
pip install mlx-lm

python scripts/quantize_model.py \
  --input models/merged/merged_all \
  --output models/gguf/lingua_graph_model.gguf \
  --quantization q4_k_m
```

---

## 5. Integration Tests

### 5.1 Provider Test

```bash
# Test the new LocalProvider
python -c "
from src.providers import get_provider
import yaml
from pathlib import Path

# Simulate local provider config
config = yaml.safe_load(Path('config/config.yaml').read_text())
config['llm']['provider'] = 'local'
config['llm']['local'] = {'model_path': 'models/gguf/lingua_graph_model.gguf'}

provider = get_provider(config)
result = provider.extract('Freedom means...', 'Extract concepts and relations.')
print(result[:200])
"
```

### 5.2 Full Pipeline Test

```bash
# Run full analysis with local model
python scripts/analyze_student.py --student S001 --no-mock --verbose

# Expected output:
# - Extraction uses local model
# - Graph building identical
# - LDS calculation identical
```

### 5.3 Ablation Benchmark

```bash
# Compare all configurations
python evaluation/benchmark_local_model.py \
  --gold data/gold/social_issues_gold.json \
  --models \
    gpt-4.1-mini \
    qwen3-8b \
    lingua-graph-1.5b \
    qwen2.5-1.5b-base

# Output: comparison table (concept_f1, relation_f1, latency, size)
```

---

## 6. Evaluation Benchmarks

### 6.1 Quality

```bash
# Benchmark script
python evaluation/benchmark_local_model.py \
  --gold data/gold/social_issues_gold.json \
  --test-model models/gguf/lingua_graph_model.gguf \
  --output evaluation/local_model_results.json
```

Expected report:

```
=== LinguaGraph Local Model Benchmark ===
Gold dataset: 30 samples (10 ZH, 10 DE, 10 EN)

Concept Extraction:
  ZH Concept F1:    0.82    (Precision: 0.85, Recall: 0.79)
  DE Concept F1:    0.78    (Precision: 0.81, Recall: 0.75)
  EN Concept F1:    0.85    (Precision: 0.88, Recall: 0.82)
  Weighted Avg:     0.82

Relation Extraction:
  ZH Relation F1:   0.72    (Precision: 0.76, Recall: 0.68)
  DE Relation F1:   0.68    (Precision: 0.72, Recall: 0.65)
  EN Relation F1:   0.76    (Precision: 0.80, Recall: 0.72)
  Weighted Avg:     0.72

Size:    912 MB (GGUF Q4_K_M)
Speed:   42 tok/s (RTX 4090), 8 tok/s (CPU)
RAM:     1.5 GB at peak
```

### 6.2 Performance on Mobile

```
=== Mobile Benchmark (Xiaomi 15, Snapdragon 8 Elite) ===
Model: lingua_graph_model.gguf (Q4_K_M, 912 MB)

First token latency:  180 ms
Generation speed:     4.2 tok/s
Peak RAM:             1.8 GB
Battery per query:    0.03%

Notes: Runs via llama.cpp Android NDK build.
```

---

## 7. Colab Training (No-GPU Fallback)

```python
# Google Colab notebook (file: notebooks/train_lora_colab.ipynb)
"""
1. Mount Google Drive
2. Upload training data
3. Install: pip install transformers peft bitsandbytes trl datasets accelerate
4. Download Qwen2.5-1.5B-Instruct
5. Train LoRA (T4 → ~20 min for 500 samples)
6. Save adapter to Drive
7. Download for merging
"""
```

---

*Document version: v1.0 · 2026-06-18*
