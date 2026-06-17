# Area 5: Knowledge Graph Visualization

## Repositories

### 3d-force-graph
- **Link**: https://github.com/vasturiano/3d-force-graph (6134 ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 5/5
- **What it does**: 3D force-directed graph component using ThreeJS/WebGL. Supports node labels, links, particles, custom geometries. De facto standard for 3D graph visualization on the web.
- **What's similar to LinguaGraph**: Both use 3D force-directed graph layout for concept visualization. Both want to make abstract knowledge structures visually intuitive.
- **What LinguaGraph does differently**: LinguaGraph uses "Cognitive City" metaphor (buildings = concepts, roads = relations); 3d-force-graph is a generic graph viz tool. LinguaGraph adds domain-specific styling.
- **Can borrow**: Core rendering engine, interaction patterns (zoom, rotate, click), performance optimization
- **Cannot borrow**: Generic layout (LinguaGraph needs custom city metaphor)
- **Cite in paper**: YES — primary visualization technology

### react-force-graph
- **Link**: https://github.com/vasturiano/react-force-graph (3184 ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: React component for 2D, 3D, VR, and AR force-directed graphs. Wraps 3d-force-graph for React apps.
- **What's similar**: Same as 3d-force-graph but React-specific
- **Can borrow**: React integration patterns
- **Cite in paper**: NO (use 3d-force-graph reference instead)

### three-forcegraph
- **Link**: https://github.com/vasturiano/three-forcegraph (298 ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Force-directed graph as a native ThreeJS object. Lower-level than 3d-force-graph, more flexible for custom scenes.
- **What's similar**: Both use ThreeJS for 3D visualization
- **Can borrow**: ThreeJS integration patterns for custom scenes
- **Cite in paper**: NO

### Knowledge-Graph-And-Visualization-Demo
- **Link**: https://github.com/xyjigsaw/Knowledge-Graph-And-Visualization-Demo (202 ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Demo of 2D search + 3D graph view for knowledge graph visualization. Interactive exploration of KG structure.
- **What's similar**: Both combine 2D and 3D views for KG exploration
- **Can borrow**: 2D/3D view switching pattern
- **Cite in paper**: NO

### chatgpt-graph-navigator
- **Link**: https://github.com/Robbings/chatgpt-graph-navigator (117 ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Transforms ChatGPT conversations into navigable knowledge graphs. Spatial graph view + timeline tree.
- **What's similar**: Both visualize text as graph structure
- **What LinguaGraph does differently**: This is about conversation history; LinguaGraph is about cognitive structures
- **Cite in paper**: NO

### Cytoscape.js
- **Link**: https://github.com/cytoscape/cytoscape.js (9600+ ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Industry-standard graph theory library for visualization and analysis. Supports many layouts, styles, and interactions.
- **What's similar**: Both are graph visualization libraries
- **What LinguaGraph does differently**: Cytoscape is 2D-focused; LinguaGraph uses 3D
- **Can borrow**: Layout algorithms, style system, analysis tools
- **Cite in paper**: NO

### Sigma.js
- **Link**: https://github.com/jacomyal/sigma.js (4500+ ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: High-performance 2D graph rendering with WebGL. Designed for large graphs.
- **What's similar**: Both are graph visualization libraries
- **Can borrow**: WebGL rendering optimization
- **Cite in paper**: NO

### D3.js
- **Link**: https://github.com/d3/d3 (109k+ ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: The foundational data visualization library. d3-force is the standard force-directed layout engine.
- **What's similar**: Both use force-directed layout for graph visualization
- **Can borrow**: Force simulation algorithms, data binding patterns
- **Cite in paper**: YES — foundational reference for visualization

## Papers

### Force-Directed Graph Drawing (Fruchterman & Reingold, 1991)
- **Title**: Graph Drawing by Force-Directed Placement
- **Link**: https://ieeexplore.ieee.org/document/2193
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Foundational algorithm for force-directed graph layout. Nodes repel each other, edges attract connected nodes.
- **What's similar**: Both use force-directed layout
- **Cite in paper**: YES — algorithmic foundation

### Graph Visualization and Navigation (Battista et al., 1999)
- **Title**: Graph Drawing: Algorithms for the Visualization of Graphs
- **Link**: https://dl.acm.org/doi/10.1145/292780.292782
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Comprehensive textbook on graph drawing algorithms including hierarchical, orthogonal, and force-directed layouts.
- **Cite in paper**: NO

### Cognitive City Metaphor
- **Note**: No single paper defines "cognitive city" as visualization metaphor. The concept appears in:
  - Information architecture literature (city-as-metaphor for knowledge spaces)
  - Urban planning visualization
  - Game design (city builders as knowledge organization)
- **Relevance to LinguaGraph**: 5/5
- **What LinguaGraph does differently**: This IS LinguaGraph's unique contribution — applying the city metaphor to cross-lingual cognitive graphs
- **Cite in paper**: YES — cite information architecture + urban planning references
