# Cognitive City — Three.js Visualization Spec

**Version:** 2.0
**Date:** 2026-06-17
**Based on:** Method Validation (813 texts, 4 topics, 3 languages)

---

## 1. Data Structure

### Node (Building)

```json
{
  "id": "success_zh",
  "label": "成功",
  "language": "zh",
  "topic": "success",
  "centrality": 0.95,
  "community": "achievement",
  "frequency": 47,
  "mapped_concept": "success"
}
```

| Field | Mapping | Three.js |
|-------|---------|----------|
| `centrality` | 0-1 | Building height: `centrality * 30` |
| `community` | Cluster ID | District color |
| `language` | zh/en/de | Building material color |
| `frequency` | Text count | Building width: `4 + frequency * 0.05` |

### Link (Road)

```json
{
  "source": "success_zh",
  "target": "effort_zh",
  "relation": "requires",
  "strength": 0.85,
  "language": "zh"
}
```

| Field | Mapping | Three.js |
|-------|---------|----------|
| `strength` | 0-1 | Road width: `strength * 3` |
| `relation` | Type | Road color |
| `language` | Source lang | Road opacity |

### LDS (City Comparison)

```json
{
  "zh_vs_en": {"lds": 0.230, "jaccard": 0.400},
  "zh_vs_de": {"lds": 0.305, "jaccard": 0.357},
  "en_vs_de": {"lds": 0.272, "jaccard": 0.385}
}
```

LDS controls:
- City separation distance
- Bridge opacity (lower LDS = more bridges)
- Color shift intensity

---

## 2. Three.js Architecture

### Scene Graph

```
Scene
├── AmbientLight (intensity: 0.3)
├── DirectionalLight (position: 50, 80, 50)
├── CityGroup_ZH (position: -120, 0, 0)
│   ├── Building (自由) — height: 28
│   ├── Building (责任) — height: 22
│   ├── Building (成功) — height: 25
│   ├── Road (自由→责任)
│   └── Road (成功→努力)
├── CityGroup_EN (position: 0, 0, 0)
│   ├── Building (freedom) — height: 26
│   ├── Building (responsibility) — height: 20
│   ├── Building (success) — height: 28
│   ├── Road (freedom→choice)
│   └── Road (success→achievement)
├── CityGroup_DE (position: 120, 0, 0)
│   ├── Building (Freiheit) — height: 27
│   ├── Building (Verantwortung) — height: 23
│   ├── Building (Erfolg) — height: 24
│   ├── Road (Freiheit→Selbstbestimmung)
│   └── Road (Erfolg→Leistung)
├── BridgeGroup (between cities)
│   ├── Bridge (成功↔success↔Erfolg)
│   ├── Bridge (自由↔freedom↔Freiheit)
│   └── Bridge (责任↔responsibility↔Verantwortung)
└── Ground (PlaneGeometry, size: 600x300)
```

### Camera

- **Default:** PerspectiveCamera, position (0, 200, 300), looking at (0, 0, 0)
- **OrbitControls:** Orbit around city center
- **Auto-rotate:** Slow rotation when idle
- **Language focus:** Double-click building → camera flies to that city

### Lighting

- **Ambient:** Soft blue (#1a1a2e), intensity 0.3
- **Directional:** Warm white (#ffffff), intensity 0.8, position (50, 80, 50)
- **Point lights:** One per city, color = language color, intensity 0.4

---

## 3. Building Design

### Geometry

```
BoxGeometry(width, height, depth)
width = 4 + (frequency * 0.05), clamped to [4, 8]
height = centrality * 30
depth = 4 + (frequency * 0.05), clamped to [4, 8]
```

### Material (MeshPhongMaterial)

| Language | Color | Emissive | Opacity |
|----------|-------|----------|---------|
| zh | #ff6b6b | #ff6b6b * 0.2 | 0.75 |
| en | #4a7dff | #4a7dff * 0.2 | 0.75 |
| de | #ffd93d | #ffd93d * 0.2 | 0.75 |

### Top Cap

```
BoxGeometry(width + 0.5, 0.3, depth + 0.5)
Position: y = height
Color: same as building, emissiveIntensity: 0.5
```

### Edge Lines

```
EdgesGeometry(building_geo)
LineBasicMaterial(color, opacity: 0.4)
```

---

## 4. Road Design

### Geometry

```
CylinderGeometry(roadWidth, roadWidth, roadLength, 8)
Position: midpoint between source and target
Rotation: lookAt target
```

### Material

| Relation | Color |
|----------|-------|
| requires | #ff6b6b (red) |
| is_a | #4a7dff (blue) |
| equivalent | #ffd93d (gold) |
| causes | #4ecdc4 (teal) |
| co_occurs | rgba(255,255,255,0.15) (white) |

Road width = `strength * 3`, clamped to [0.5, 3]

---

## 5. Bridge Design (Cross-City Connections)

### Geometry

```
TubeGeometry(curve, tubularSegments=20, radius=0.3)
Curve: QuadraticBezierCurve3 between two cities
```

### Material

```
MeshPhongMaterial({
  color: #ff4444,
  transparent: true,
  opacity: 0.3 + (1 - lds) * 0.5,
  emissive: #ff4444,
  emissiveIntensity: 0.3
})
```

### Animation

- Directional particles flowing along bridge
- Color intensity = 1 - LDS (higher overlap = brighter bridge)

---

## 6. Camera Controls

### OrbitControls

```javascript
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 100;
controls.maxDistance = 500;
controls.maxPolarAngle = Math.PI / 2.5;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;
```

### Language Focus

```javascript
function focusLanguage(lang) {
  const cityGroup = cityGroups[lang];
  const target = cityGroup.position;
  gsap.to(camera.position, {
    x: target.x + 80,
    y: 100,
    z: target.z + 80,
    duration: 1.5,
    ease: "power2.inOut"
  });
  controls.target.copy(target);
}
```

### Reset View

```javascript
function resetView() {
  gsap.to(camera.position, {
    x: 0, y: 200, z: 300,
    duration: 1.5,
    ease: "power2.inOut"
  });
  controls.target.set(0, 0, 0);
}
```

---

## 7. Animation Design

### Building Entrance

Buildings rise from ground on load:

```javascript
buildings.forEach((b, i) => {
  const startY = 0;
  const endY = b.height / 2;
  gsap.from(b.mesh.position, {
    y: -10,
    duration: 0.8,
    delay: i * 0.05,
    ease: "back.out(1.7)"
  });
  gsap.from(b.mesh.scale, {
    y: 0,
    duration: 0.8,
    delay: i * 0.05,
    ease: "back.out(1.7)"
  });
});
```

### Language Switch Morph

When switching language focus:

```javascript
function morphCity(fromLang, toLang, duration = 2) {
  // 1. Fade out non-focused buildings
  cityGroups[fromLang].children.forEach(child => {
    gsap.to(child.material, { opacity: 0.2, duration: duration/2 });
  });
  // 2. Fade in focused buildings
  cityGroups[toLang].children.forEach(child => {
    gsap.to(child.material, { opacity: 0.8, duration: duration/2, delay: duration/2 });
  });
  // 3. Animate camera
  focusLanguage(toLang);
}
```

### Bridge Particles

```javascript
function createBridgeParticles(bridge) {
  const particleCount = 20;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  // ...沿桥路径分布粒子
  const material = new THREE.PointsMaterial({
    color: 0xff4444,
    size: 0.5,
    transparent: true,
    opacity: 0.6
  });
  return new THREE.Points(geometry, material);
}
```

---

## 8. HUD (Head-Up Display)

### Left Panel — City Info

```
┌─────────────────────────┐
│ LinguaGraph             │
│ Cognitive City          │
│                         │
│ Topic: [dropdown]       │
│ Language: [tabs]        │
│                         │
│ Concepts: 12            │
│ Relations: 8            │
│ LDS: 0.269              │
│ Jaccard: 0.381          │
└─────────────────────────┘
```

### Bottom Panel — LDS Comparison

```
┌─────────────────────────────────────┐
│ Language Drift Score                │
│ zh↔en: ████████░░░░ 0.230          │
│ zh↔de: ██████████░░ 0.305          │
│ en↔de: █████████░░░ 0.272          │
└─────────────────────────────────────┘
```

### Right Controls

```
┌──────────┐
│ Reset    │
│ Labels   │
│ Bridges  │
│ Rotate   │
└──────────┘
```

---

## 9. BWKI Demo Script

### 30-Second Demo Flow

```
0:00  Camera starts at overview (all 3 cities visible)
0:05  HUD shows "What is Success?"
0:08  Chinese city highlights (buildings glow)
0:12  Camera zooms to Chinese city
0:15  Show: 努力, 家庭, 成就, 责任 (top concepts)
0:18  Morph to English city
0:21  Show: achievement, choice, opportunity, competition
0:24  Morph to German city
0:27  Show: Leistung, Karriere, Selbstständigkeit
0:30  Pull back to overview, show LDS bars
```

### Key Visual Moment

When switching languages:
1. Current city fades to 30% opacity
2. New city rises from ground
3. Bridge connections pulse
4. LDS bar updates with animation

### Narration Points

- "Each city represents one language's conceptual structure"
- "Buildings are concepts — taller = more central"
- "Roads are relationships — wider = stronger"
- "Bridges connect equivalent concepts across languages"
- "LDS measures how different the cities are"

---

## 10. Technical Stack

| Component | Library |
|-----------|---------|
| 3D Rendering | Three.js r160 |
| Animation | GSAP 3.12 |
| Graph Layout | d3-force-3d |
| UI | HTML/CSS overlay |
| Data | JSON from pipeline |

## 11. Files

| File | Purpose |
|------|---------|
| `visualization/cognitive_cities_v2.html` | Main visualization |
| `visualization/cognitive_cities_v2.js` | Three.js logic |
| `visualization/data.json` | Pre-built city data |
| `visualization/style.css` | HUD styling |
