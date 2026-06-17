# LinguaGraph

**Mapping How Language Shapes Thinking**

LinguaGraph is a research project that quantifies how different languages organize conceptual space. It proposes the **Language Drift Score (LDS)**, a novel metric that measures structural differences in cognitive graphs across languages.

## Research Question

> **Does language shape the structure of thought?**

## Key Innovation

- **Language Drift Score (LDS)**: First metric to quantify cross-lingual cognitive differences at the graph-structure level (not just vocabulary)
- **Cognitive City**: 3D visualization metaphor where concepts are buildings and relations are roads
- **Cross-lingual comparison**: Chinese, German, and English cognitive graph analysis

## Installation

```bash
# Clone the repository
cd C:\Users\rongj\Desktop\linguagraph

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python pipeline.py

# Start the visualization
python web/server.py
# Open http://localhost:8080
```

## Project Structure

```
linguagraph/
├── src/
│   ├── compare.py          # Graph comparison metrics (GED, Jaccard, LDS)
│   ├── cross_language.py   # Cross-lingual concept alignment
│   └── extract_v2.py       # Concept extraction (LLM + fallback)
├── web/
│   ├── index.html          # Cognitive City 3D visualization
│   └── server.py           # Flask backend
├── data/
│   └── gold/               # Annotated gold dataset (21 samples)
├── tests/
│   └── test_compare.py     # Unit tests (30 tests)
├── docs/
│   ├── methodology.md      # LDS mathematical definition
│   ├── limitations.md      # Method limitations
│   ├── error_analysis.md   # Error taxonomy
│   └── experiment-design.md # Experimental protocol
├── pipeline.py             # End-to-end pipeline
└── requirements.txt        # Dependencies
```

## Usage

### Run Pipeline

```bash
python pipeline.py
```

### Run Tests

```bash
python -m pytest tests/ -v
```

### Start Visualization

```bash
python web/server.py
# Open http://localhost:8080
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| networkx | >=3.2 | Graph operations |
| numpy | >=1.24 | Numerical computation |
| flask | >=3.0 | Web server |
| requests | >=2.31 | HTTP client |
| pytest | >=7.0 | Testing |

## Citation

```bibtex
@software{linguagraph2026,
  title = {LinguaGraph: Mapping How Language Shapes Thinking},
  year = {2026},
  url = {https://github.com/linguagraph/linguagraph}
}
```

## License

MIT
