// LinguaGraph Cognitive City V3 — Three.js Core
// Opening animation, city switching, LDS heatmap, demo mode, export

let scene, camera, renderer;
let cityGroups = {};
let buildings = [];
let bridges = [];
let currentTopic = "freedom";
let currentLang = "all";
let hoveredBuilding = null;
let openingAnimDone = false;

const LANG_COLORS = { zh: 0xff6b6b, en: 0x4a7dff, de: 0xffd93d };
const CITY_X = { zh: -130, en: 0, de: 130 };

// ===== INIT =====

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0e1a);
    scene.fog = new THREE.Fog(0x0a0e1a, 300, 600);

    camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 2000);
    camera.position.set(0, 350, 500);

    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById("canvas"),
        antialias: true,
        preserveDrawingBuffer: true,
    });
    renderer.setSize(innerWidth, innerHeight);
    renderer.setPixelRatio(devicePixelRatio);

    scene.add(new THREE.AmbientLight(0x404060, 0.5));
    const dl = new THREE.DirectionalLight(0xffffff, 0.7);
    dl.position.set(100, 200, 100);
    scene.add(dl);

    const ground = new THREE.Mesh(
        new THREE.PlaneGeometry(800, 500),
        new THREE.MeshPhongMaterial({ color: 0x0d1117, transparent: true, opacity: 0.8 })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -2;
    scene.add(ground);

    initControls();
    setupUI();
    setupKeyboard();

    // Start with opening animation
    runOpeningAnimation(() => {
        loadTopic("freedom");
        openingAnimDone = true;
        // Hide loading overlay
        const overlay = document.getElementById("loading-overlay");
        if (overlay) setTimeout(() => overlay.classList.add("hidden"), 300);
    });

    animate();
}

// ===== OPENING ANIMATION =====

function runOpeningAnimation(onComplete) {
    const topTitle = document.getElementById("topTitle");
    const topSub = document.getElementById("topSub");
    if (topTitle) topTitle.textContent = "LinguaGraph";
    if (topSub) topSub.textContent = "Loading...";

    // Camera fly-in from above
    const startPos = { x: 0, y: 400, z: 600 };
    const endPos = { x: 0, y: 220, z: 320 };
    let t = 0;

    const step = () => {
        t += 0.008;
        if (t >= 1) {
            camera.position.set(endPos.x, endPos.y, endPos.z);
            camera.lookAt(0, 15, 0);
            if (onComplete) onComplete();
            return;
        }
        const ease = 1 - Math.pow(1 - t, 3);
        camera.position.set(
            startPos.x + (endPos.x - startPos.x) * ease,
            startPos.y + (endPos.y - startPos.y) * ease,
            startPos.z + (endPos.z - startPos.z) * ease
        );
        camera.lookAt(0, 15, 0);
        requestAnimationFrame(step);
    };
    step();
}

// ===== CONTROLS =====

function initControls() {
    let drag = false, prev = { x: 0, y: 0 };
    let sph = { r: 380, theta: Math.PI / 6, phi: Math.PI / 4 };

    const upd = () => {
        camera.position.set(
            sph.r * Math.sin(sph.phi) * Math.cos(sph.theta),
            sph.r * Math.cos(sph.phi),
            sph.r * Math.sin(sph.phi) * Math.sin(sph.theta)
        );
        camera.lookAt(0, 15, 0);
    };

    const onDown = (x, y) => { drag = true; prev = { x, y }; };
    const onMove = (x, y) => {
        if (!drag) return;
        sph.theta -= (x - prev.x) * 0.005;
        sph.phi = Math.max(0.3, Math.min(1.4, sph.phi + (y - prev.y) * 0.005));
        prev = { x, y };
        upd();
    };
    const onUp = () => (drag = false);

    const c = renderer.domElement;
    // Mouse
    c.addEventListener("mousedown", (e) => onDown(e.clientX, e.clientY));
    c.addEventListener("mousemove", (e) => onMove(e.clientX, e.clientY));
    c.addEventListener("mouseup", onUp);
    c.addEventListener("mouseleave", onUp);
    // Touch
    c.addEventListener("touchstart", (e) => { const t = e.touches[0]; onDown(t.clientX, t.clientY); });
    c.addEventListener("touchmove", (e) => { const t = e.touches[0]; onMove(t.clientX, t.clientY); });
    c.addEventListener("touchend", onUp);
    c.addEventListener("wheel", (e) => {
        sph.r = Math.max(150, Math.min(600, sph.r + e.deltaY * 0.5));
        upd();
    });
    upd();
}

// ===== KEYBOARD SHORTCUTS =====

function setupKeyboard() {
    window.addEventListener("keydown", (e) => {
        if (e.key === "1") animateCamera(0, 340, 480, 0, 15, 0);    // Panorama
        if (e.key === "2") animateCamera(0, 150, 200, 0, 15, 0);    // Close-up
        if (e.key === "3") animateCamera(0, 500, 10, 0, 15, 0);     // Top-down
    });
}

// ===== TOPIC LOADING =====

function loadTopic(topic) {
    // Remove old cities
    Object.values(cityGroups).forEach((g) => scene.remove(g));
    cityGroups = {};
    buildings = [];
    bridges = [];
    currentTopic = topic;

    const td = CITY_DATA[topic];
    if (!td) return;

    const lds = LDS_DATA[topic] || {};
    const topicLabel = TOPIC_LABELS[topic] || {};

    // Update HUD
    document.getElementById("topTitle").textContent =
        `${topicLabel.zh || topic} / ${topicLabel.en || topic} / ${topicLabel.de || topic}`;

    // Build cities with entrance animation
    ["zh", "en", "de"].forEach((lang, langIdx) => {
        const g = new THREE.Group();
        g.position.x = CITY_X[lang];
        const ld = td[lang];
        if (!ld) return;

        const pos = {};
        ld.buildings.forEach((b, i) => {
            const h = b.c * 30;
            const w = Math.min(4 + b.freq * 0.04, 8);
            const geo = new THREE.BoxGeometry(w, h, w);
            const col = LANG_COLORS[lang];
            const mat = new THREE.MeshPhongMaterial({
                color: col,
                transparent: true,
                opacity: 0,
                emissive: col,
                emissiveIntensity: 0.15,
            });
            const mesh = new THREE.Mesh(geo, mat);

            // Start below ground for entrance animation
            mesh.position.set((i % 3 - 1) * 38, -10, (Math.floor(i / 3) - 1) * 38);
            mesh.userData = { label: b.label, centrality: b.c, lang: lang, targetH: h / 2 };
            g.add(mesh);
            buildings.push(mesh);
            pos[b.id] = mesh.position.clone();

            // Edge lines
            const eg = new THREE.EdgesGeometry(geo);
            const edgeMat = new THREE.LineBasicMaterial({ color: 0x333355, transparent: true, opacity: 0 });
            const edges = new THREE.LineSegments(eg, edgeMat);
            edges.position.copy(mesh.position);
            edges.userData = { isEdge: true, targetOpacity: 0.3 };
            g.add(edges);
        });

        // Roads
        ld.roads.forEach((r) => {
            const s = pos[r.s], t = pos[r.t];
            if (!s || !t) return;
            const mid = s.clone().add(t).multiplyScalar(0.5);
            const len = s.distanceTo(t);
            const rg = new THREE.CylinderGeometry(0.3 + r.w * 0.5, 0.3 + r.w * 0.5, len, 6);
            const rm = new THREE.MeshPhongMaterial({ color: 0x555577, transparent: true, opacity: 0 });
            const road = new THREE.Mesh(rg, rm);
            road.position.copy(mid);
            road.lookAt(t);
            road.rotateX(Math.PI / 2);
            road.userData = { isRoad: true, targetOpacity: 0.5 };
            g.add(road);
        });

        scene.add(g);
        cityGroups[lang] = g;
    });

    // Bridges
    if (td.bridges) {
        td.bridges.forEach((b) => {
            const sLang = findLang(b.s, td);
            const tLang = findLang(b.t, td);
            if (!sLang || !tLang) return;
            const sp = findPos(b.s, sLang);
            const tp = findPos(b.t, tLang);
            if (!sp || !tp) return;
            const mid = sp.clone().add(tp).multiplyScalar(0.5);
            const len = sp.distanceTo(tp);
            const bg = new THREE.CylinderGeometry(0.2, 0.2, len, 6);
            const bm = new THREE.MeshPhongMaterial({
                color: 0xff4444,
                transparent: true,
                opacity: 0,
                emissive: 0xff4444,
                emissiveIntensity: 0.3,
            });
            const bridge = new THREE.Mesh(bg, bm);
            bridge.position.copy(mid);
            bridge.lookAt(tp);
            bridge.rotateX(Math.PI / 2);
            bridge.userData = { bridge: true, source: b.s, target: b.t, targetOpacity: 0.4 };
            scene.add(bridge);
            bridges.push(bridge);
        });
    }

    // Animate entrance
    animateEntrance();

    // Update LDS bars
    setLDSBars(lds);
    updateStats(td);
}

function animateEntrance() {
    let delay = 0;
    buildings.forEach((b, i) => {
        const targetY = b.userData.targetH;
        const mat = b.material;
        const startOpacity = 0;

        // Stagger animation
        setTimeout(() => {
            let t = 0;
            const anim = () => {
                t += 0.03;
                if (t >= 1) {
                    b.position.y = targetY;
                    mat.opacity = 0.8;
                    return;
                }
                const ease = 1 - Math.pow(1 - t, 3);
                b.position.y = -10 + (targetY + 10) * ease;
                mat.opacity = startOpacity + (0.8 - startOpacity) * ease;
                requestAnimationFrame(anim);
            };
            anim();
        }, delay);
        delay += 60;
    });

    // Fade in roads and bridges
    setTimeout(() => {
        buildings.forEach((b) => {
            const parent = b.parent;
            if (parent) {
                parent.children.forEach((child) => {
                    if (child.userData && child.userData.isRoad) {
                        let t = 0;
                        const anim = () => {
                            t += 0.03;
                            if (t >= 1) { child.material.opacity = 0.5; return; }
                            child.material.opacity = 0.5 * (1 - Math.pow(1 - t, 3));
                            requestAnimationFrame(anim);
                        };
                        anim();
                    }
                    if (child.userData && child.userData.isEdge) {
                        let t = 0;
                        const anim = () => {
                            t += 0.03;
                            if (t >= 1) { child.material.opacity = 0.3; return; }
                            child.material.opacity = 0.3 * (1 - Math.pow(1 - t, 3));
                            requestAnimationFrame(anim);
                        };
                        anim();
                    }
                });
            }
        });
    }, delay + 200);

    // Fade in bridges
    bridges.forEach((b, i) => {
        setTimeout(() => {
            let t = 0;
            const anim = () => {
                t += 0.03;
                if (t >= 1) { b.material.opacity = 0.4; return; }
                b.material.opacity = 0.4 * (1 - Math.pow(1 - t, 3));
                requestAnimationFrame(anim);
            };
            anim();
        }, delay + 500 + i * 100);
    });
}

// ===== HELPERS =====

function findLang(id, td) {
    for (const l of ["zh", "en", "de"])
        if (td[l] && td[l].buildings.some((b) => b.id === id)) return l;
    return null;
}

function findPos(id, lang) {
    const g = cityGroups[lang];
    if (!g) return null;
    const m = g.children.find((c) => c.isMesh && c.userData && c.userData.label === id);
    return m ? m.position.clone() : null;
}

// ===== LDS BARS =====

function setLDSBars(lds) {
    const set = (barId, valId, v) => {
        document.getElementById(barId).style.width = v * 100 + "%";
        document.getElementById(valId).textContent = (v * 100).toFixed(1) + "%";
    };
    set("b1", "l1v", lds.zh_en || 0);
    set("b2", "l2v", lds.zh_de || 0);
    set("b3", "l3v", lds.en_de || 0);

    // Update bar labels with topic-specific LDS
    document.getElementById("l1n").textContent = "ZH \u2194 EN";
    document.getElementById("l2n").textContent = "ZH \u2194 DE";
    document.getElementById("l3n").textContent = "EN \u2194 DE";

    // Color intensity based on LDS (higher = more saturated)
    const colors = [
        { id: "b1", base: [255, 107, 107], lds: lds.zh_en || 0 },
        { id: "b2", base: [255, 217, 61], lds: lds.zh_de || 0 },
        { id: "b3", base: [74, 125, 255], lds: lds.en_de || 0 },
    ];
    colors.forEach(({ id, base, lds: v }) => {
        const intensity = 0.5 + v * 0.5;
        const el = document.getElementById(id);
        el.style.background = `rgba(${base[0]},${base[1]},${base[2]},${intensity})`;
    });
}

function updateStats(td) {
    document.getElementById("sC").textContent = buildings.length;
    document.getElementById("sR").textContent = Math.floor(buildings.length * 1.5);
    const lds = LDS_DATA[currentTopic] || {};
    const vals = Object.values(lds).filter((v) => typeof v === "number" && v <= 1);
    const avg = vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
    document.getElementById("sL").textContent = avg.toFixed(3);
    document.getElementById("sJ").textContent = (lds.jaccard || 0.38).toFixed(3);
}

// ===== UI SETUP =====

function setupUI() {
    // Topic selector
    document.getElementById("topicSelect").addEventListener("change", (e) => {
        if (demoCtrl && demoCtrl.running) demoCtrl.stop();
        loadTopic(e.target.value);
    });

    // Language tabs
    document.querySelectorAll(".lt").forEach((tab) => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".lt").forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            currentLang = tab.dataset.lang;
            Object.entries(cityGroups).forEach(([l, g]) => (g.visible = currentLang === "all" || currentLang === l));
            bridges.forEach((b) => (b.visible = currentLang === "all"));
        });
    });

    // Raycaster for hover
    const rc = new THREE.Raycaster();
    const ms = new THREE.Vector2();

    renderer.domElement.addEventListener("mousemove", (e) => {
        ms.x = (e.clientX / innerWidth) * 2 - 1;
        ms.y = -(e.clientY / innerHeight) * 2 + 1;
        rc.setFromCamera(ms, camera);
        const hits = rc.intersectObjects(buildings);
        if (hits.length > 0) {
            const obj = hits[0].object;
            if (hoveredBuilding !== obj) {
                if (hoveredBuilding) hoveredBuilding.material.emissiveIntensity = 0.15;
                hoveredBuilding = obj;
                hoveredBuilding.material.emissiveIntensity = 0.5;
            }
            document.getElementById("dTitle").textContent = obj.userData.label;
            document.getElementById("dBody").textContent =
                `Centrality: ${obj.userData.centrality.toFixed(2)} | Language: ${obj.userData.lang.toUpperCase()}`;
            document.getElementById("detail").style.display = "block";
        } else {
            if (hoveredBuilding) hoveredBuilding.material.emissiveIntensity = 0.15;
            hoveredBuilding = null;
            document.getElementById("detail").style.display = "none";
        }
    });

    // Click to zoom
    renderer.domElement.addEventListener("click", (e) => {
        ms.x = (e.clientX / innerWidth) * 2 - 1;
        ms.y = -(e.clientY / innerHeight) * 2 + 1;
        rc.setFromCamera(ms, camera);
        const hits = rc.intersectObjects(buildings);
        if (hits.length > 0) {
            const obj = hits[0].object;
            const gp = obj.parent.position;
            animateCamera(gp.x + 60, 80, gp.z + 60, gp.x, 15, gp.z);
        }
    });

    // Resize
    window.addEventListener("resize", () => {
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
    });

    // Compare button
    document.getElementById("btnCompare").addEventListener("click", showComparison);

    // Demo button
    document.getElementById("btnDemo").addEventListener("click", () => {
        if (demoCtrl) demoCtrl.toggle();
    });

    // Export button
    document.getElementById("btnExport").addEventListener("click", () => {
        if (exportCtrl) exportCtrl.downloadScreenshot(`linguagraph_${currentTopic}.png`);
    });
}

// ===== COMPARISON VIEW =====

function showComparison() {
    const detail = document.getElementById("detail");
    detail.style.display = "block";
    detail.style.borderLeftColor = "#4ecdc4";

    const comp = COMPARISON_DATA;
    const topic = currentTopic;
    const humanVal = comp.human[topic] || "N/A";
    const simVal = comp.simulation[topic] || "N/A";

    document.getElementById("dTitle").textContent = "Human vs Model Comparison";
    document.getElementById("dBody").innerHTML =
        `<b>Human LDS:</b> ${typeof humanVal === "number" ? humanVal.toFixed(3) : humanVal}<br>` +
        `<b>Simulation LDS:</b> ${typeof simVal === "number" ? simVal.toFixed(3) : simVal}<br>` +
        `<b>Topic:</b> ${topic}`;
}

// ===== CAMERA ANIMATION =====

function animateCamera(tx, ty, tz, lx, ly, lz) {
    const sp = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
    const tp = { x: tx, y: ty, z: tz };
    let t = 0;
    const step = () => {
        t += 0.02;
        if (t >= 1) return;
        const ease = 1 - Math.pow(1 - t, 3);
        camera.position.set(
            sp.x + (tp.x - sp.x) * ease,
            sp.y + (tp.y - sp.y) * ease,
            sp.z + (tp.z - sp.z) * ease
        );
        camera.lookAt(lx, ly, lz);
        requestAnimationFrame(step);
    };
    step();
}

// ===== RENDER LOOP =====

function animate() {
    requestAnimationFrame(animate);
    const time = Date.now() * 0.001;

    // Bridge pulse
    bridges.forEach((b, i) => {
        if (b.material.opacity > 0) {
            b.material.opacity = 0.2 + Math.sin(time * 2 + i) * 0.15;
        }
    });

    // Building float
    buildings.forEach((b, i) => {
        if (b.position.y > 0) {
            b.position.y += Math.sin(time * 1.5 + i * 0.5) * 0.015;
        }
    });

    renderer.render(scene, camera);
}

// ===== GLOBALS =====

let demoCtrl = null;
let exportCtrl = null;

// ===== STARTUP =====

window.addEventListener("DOMContentLoaded", () => {
    init();
    demoCtrl = new DemoController(loadTopic, animateCamera);
    exportCtrl = new ExportController(renderer, scene, camera);
});
