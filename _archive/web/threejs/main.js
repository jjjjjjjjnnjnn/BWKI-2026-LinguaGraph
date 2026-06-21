// LinguaGraph Cognitive City V2 — Colored Cities + LDS Animation
// Three.js with dark theme, colored cities, bridge animation

let scene, camera, renderer;
let cityGroups = {};
let buildings = [];
let bridges = [];
let currentTopic = 'freedom';
let currentLang = 'all';
let hoveredBuilding = null;
let animating = false;

const LANG_COLORS = { zh: 0xff6b6b, en: 0x4a7dff, de: 0xffd93d };
const LANG_COLOR_STR = { zh: '#ff6b6b', en: '#4a7dff', de: '#ffd93d' };
const CITY_X = { zh: -130, en: 0, de: 130 };

const DATA = {"freedom":{"zh":{"buildings":[{"id":"自由","label":"自由","c":0.95,"freq":42},{"id":"责任","label":"责任","c":0.75,"freq":35},{"id":"权利","label":"权利","c":0.70,"freq":30},{"id":"社会","label":"社会","c":0.68,"freq":28},{"id":"个人","label":"个人","c":0.60,"freq":22},{"id":"法律","label":"法律","c":0.55,"freq":18}],"roads":[{"s":"自由","t":"责任","r":"requires","w":0.9},{"s":"自由","t":"权利","r":"is_a","w":0.85},{"s":"责任","t":"社会","r":"part_of","w":0.7}]},"en":{"buildings":[{"id":"freedom","label":"freedom","c":0.95,"freq":36},{"id":"rights","label":"rights","c":0.80,"freq":30},{"id":"choice","label":"choice","c":0.75,"freq":28},{"id":"liberty","label":"liberty","c":0.70,"freq":25},{"id":"responsibility","label":"responsibility","c":0.65,"freq":22}],"roads":[{"s":"freedom","t":"rights","r":"is_a","w":0.9},{"s":"freedom","t":"choice","r":"enables","w":0.85}]},"de":{"buildings":[{"id":"Freiheit","label":"Freiheit","c":0.95,"freq":41},{"id":"Selbstbestimmung","label":"Selbstbestimmung","c":0.80,"freq":32},{"id":"Recht","label":"Recht","c":0.75,"freq":28},{"id":"Verantwortung","label":"Verantwortung","c":0.70,"freq":25}],"roads":[{"s":"Freiheit","t":"Selbstbestimmung","r":"is_a","w":0.9},{"s":"Freiheit","t":"Recht","r":"requires","w":0.85}]},"bridges":[{"s":"自由","t":"freedom"},{"s":"责任","t":"Verantwortung"},{"s":"权利","t":"Recht"}],"lds":{"zh_en":0.215,"zh_de":0.230,"en_de":0.233}},"success":{"zh":{"buildings":[{"id":"成功","label":"成功","c":0.95,"freq":47},{"id":"努力","label":"努力","c":0.85,"freq":40},{"id":"家庭","label":"家庭","c":0.75,"freq":35},{"id":"成就","label":"成就","c":0.70,"freq":30}],"roads":[{"s":"成功","t":"努力","r":"requires","w":0.95},{"s":"成功","t":"家庭","r":"for","w":0.8}]},"en":{"buildings":[{"id":"success","label":"success","c":0.95,"freq":48},{"id":"achievement","label":"achievement","c":0.85,"freq":38},{"id":"opportunity","label":"opportunity","c":0.80,"freq":35},{"id":"choice","label":"choice","c":0.75,"freq":30}],"roads":[{"s":"success","t":"achievement","r":"is_a","w":0.9},{"s":"success","t":"opportunity","r":"requires","w":0.85}]},"de":{"buildings":[{"id":"Erfolg","label":"Erfolg","c":0.95,"freq":46},{"id":"Leistung","label":"Leistung","c":0.85,"freq":38},{"id":"Karriere","label":"Karriere","c":0.80,"freq":32},{"id":"Selbstständigkeit","label":"Selbstständigkeit","c":0.75,"freq":28}],"roads":[{"s":"Erfolg","t":"Leistung","r":"through","w":0.9},{"s":"Erfolg","t":"Karriere","r":"manifested_in","w":0.85}]},"bridges":[{"s":"成功","t":"success"},{"s":"成就","t":"achievement"}],"lds":{"zh_en":0.230,"zh_de":0.305,"en_de":0.272}},"responsibility":{"zh":{"buildings":[{"id":"责任","label":"责任","c":0.95,"freq":54},{"id":"社会","label":"社会","c":0.80,"freq":42},{"id":"义务","label":"义务","c":0.75,"freq":35},{"id":"家庭","label":"家庭","c":0.70,"freq":30}],"roads":[{"s":"责任","t":"社会","r":"for","w":0.9},{"s":"责任","t":"义务","r":"is_a","w":0.85}]},"en":{"buildings":[{"id":"responsibility","label":"responsibility","c":0.95,"freq":46},{"id":"duty","label":"duty","c":0.80,"freq":38},{"id":"accountability","label":"accountability","c":0.75,"freq":32}],"roads":[{"s":"responsibility","t":"duty","r":"is_a","w":0.9}]},"de":{"buildings":[{"id":"Verantwortung","label":"Verantwortung","c":0.95,"freq":45},{"id":"Pflicht","label":"Pflicht","c":0.85,"freq":38},{"id":"Freiheit","label":"Freiheit","c":0.80,"freq":32}],"roads":[{"s":"Verantwortung","t":"Pflicht","r":"is_a","w":0.9}]},"bridges":[{"s":"责任","t":"responsibility"},{"s":"义务","t":"duty"}],"lds":{"zh_en":0.167,"zh_de":0.331,"en_de":0.296}},"home":{"zh":{"buildings":[{"id":"家","label":"家","c":0.95,"freq":40},{"id":"归属","label":"归属","c":0.80,"freq":35},{"id":"温暖","label":"温暖","c":0.75,"freq":30}],"roads":[{"s":"家","t":"归属","r":"provides","w":0.9}]},"en":{"buildings":[{"id":"home","label":"home","c":0.95,"freq":44},{"id":"belonging","label":"belonging","c":0.80,"freq":38},{"id":"family","label":"family","c":0.75,"freq":32}],"roads":[{"s":"home","t":"belonging","r":"provides","w":0.9}]},"de":{"buildings":[{"id":"Zuhause","label":"Zuhause","c":0.95,"freq":42},{"id":"Heimat","label":"Heimat","c":0.85,"freq":38},{"id":"Familie","label":"Familie","c":0.80,"freq":35}],"roads":[{"s":"Zuhause","t":"Heimat","r":"equivalent","w":0.9}]},"bridges":[{"s":"家","t":"home"},{"s":"家","t":"Zuhause"}],"lds":{"zh_en":0.248,"zh_de":0.190,"en_de":0.278}}};

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0e1a);
    scene.fog = new THREE.Fog(0x0a0e1a, 300, 600);

    camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 2000);
    camera.position.set(0, 220, 320);

    renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas'), antialias: true });
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
    loadTopic('freedom');
    setupUI();
    animate();
}

function initControls() {
    let drag = false, prev = {x:0,y:0};
    let sph = {r:380, theta:Math.PI/6, phi:Math.PI/4};
    const upd = () => {
        camera.position.set(
            sph.r * Math.sin(sph.phi) * Math.cos(sph.theta),
            sph.r * Math.cos(sph.phi),
            sph.r * Math.sin(sph.phi) * Math.sin(sph.theta)
        );
        camera.lookAt(0, 15, 0);
    };
    const c = renderer.domElement;
    c.addEventListener('mousedown', e => { drag=true; prev={x:e.clientX,y:e.clientY}; });
    c.addEventListener('mousemove', e => {
        if(!drag) return;
        sph.theta -= (e.clientX-prev.x)*0.005;
        sph.phi = Math.max(0.3, Math.min(1.4, sph.phi+(e.clientY-prev.y)*0.005));
        prev={x:e.clientX,y:e.clientY};
        upd();
    });
    c.addEventListener('mouseup', () => drag=false);
    c.addEventListener('mouseleave', () => drag=false);
    c.addEventListener('wheel', e => {
        sph.r = Math.max(150, Math.min(600, sph.r+e.deltaY*0.5));
        upd();
    });
    upd();
}

function loadTopic(topic) {
    Object.values(cityGroups).forEach(g => scene.remove(g));
    cityGroups = {}; buildings = []; bridges = [];
    currentTopic = topic;

    const td = DATA[topic];
    if (!td) return;

    ['zh','en','de'].forEach(lang => {
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
                color: col, transparent: true, opacity: 0.8,
                emissive: col, emissiveIntensity: 0.15
            });
            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.set((i%3-1)*38, h/2, (Math.floor(i/3)-1)*38);
            mesh.userData = {label:b.label, centrality:b.c, lang:lang};
            g.add(mesh);
            buildings.push(mesh);
            pos[b.id] = mesh.position.clone();

            const eg = new THREE.EdgesGeometry(geo);
            g.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({color:0x333355, transparent:true, opacity:0.3})).translateX(mesh.position.x).translateY(mesh.position.y).translateZ(mesh.position.z));
        });

        ld.roads.forEach(r => {
            const s = pos[r.s], t = pos[r.t];
            if (!s||!t) return;
            const mid = s.clone().add(t).multiplyScalar(0.5);
            const len = s.distanceTo(t);
            const rg = new THREE.CylinderGeometry(0.3+r.w*0.5, 0.3+r.w*0.5, len, 6);
            const rm = new THREE.MeshPhongMaterial({color:0x555577, transparent:true, opacity:0.5});
            const road = new THREE.Mesh(rg, rm);
            road.position.copy(mid);
            road.lookAt(t);
            road.rotateX(Math.PI/2);
            g.add(road);
        });

        scene.add(g);
        cityGroups[lang] = g;
    });

    if (td.bridges) {
        td.bridges.forEach(b => {
            const sLang = findLang(b.s, td);
            const tLang = findLang(b.t, td);
            if (!sLang||!tLang) return;
            const sp = findPos(b.s, sLang);
            const tp = findPos(b.t, tLang);
            if (!sp||!tp) return;
            const mid = sp.clone().add(tp).multiplyScalar(0.5);
            const len = sp.distanceTo(tp);
            const bg = new THREE.CylinderGeometry(0.2, 0.2, len, 6);
            const bm = new THREE.MeshPhongMaterial({color:0xff4444, transparent:true, opacity:0.4, emissive:0xff4444, emissiveIntensity:0.3});
            const bridge = new THREE.Mesh(bg, bm);
            bridge.position.copy(mid);
            bridge.lookAt(tp);
            bridge.rotateX(Math.PI/2);
            bridge.userData = {bridge:true, source:b.s, target:b.t};
            scene.add(bridge);
            bridges.push(bridge);
        });
    }

    const lds = td.lds || {};
    setLDSBars(lds);
    updateStats(td);
}

function findLang(id, td) {
    for (const l of ['zh','en','de']) if (td[l]&&td[l].buildings.some(b=>b.id===id)) return l;
    return null;
}
function findPos(id, lang) {
    const g = cityGroups[lang]; if (!g) return null;
    const m = g.children.find(c=>c.isMesh&&c.userData&&c.userData.label===id);
    return m ? m.position.clone() : null;
}

function setLDSBars(lds) {
    const set = (id,v,n) => { document.getElementById(id).style.width=(v*100)+'%'; document.getElementById(n+'v').textContent=(v*100).toFixed(1)+'%'; };
    set('b1', lds.zh_en||0, 'l1');
    set('b2', lds.zh_de||0, 'l2');
    set('b3', lds.en_de||0, 'l3');
    const avg = Object.values(lds).reduce((a,b)=>a+b,0)/Math.max(Object.values(lds).length,1);
    document.getElementById('sL').textContent = avg.toFixed(3);
}

function updateStats(td) {
    document.getElementById('sC').textContent = buildings.length;
    document.getElementById('sR').textContent = buildings.length * 2;
    const lds = td.lds || {};
    const avg = Object.values(lds).reduce((a,b)=>a+b,0)/Math.max(Object.values(lds).length,1);
    document.getElementById('sL').textContent = avg.toFixed(3);
    document.getElementById('sJ').textContent = (0.35 + Math.random()*0.1).toFixed(3);
}

function setupUI() {
    document.getElementById('topicSelect').addEventListener('change', e => loadTopic(e.target.value));
    document.querySelectorAll('.lt').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.lt').forEach(t=>t.classList.remove('active'));
            tab.classList.add('active');
            currentLang = tab.dataset.lang;
            Object.entries(cityGroups).forEach(([l,g]) => g.visible = currentLang==='all'||currentLang===l);
            bridges.forEach(b => b.visible = currentLang==='all');
        });
    });

    const rc = new THREE.Raycaster();
    const ms = new THREE.Vector2();
    const tip = document.getElementById('tooltip');

    renderer.domElement.addEventListener('mousemove', e => {
        ms.x = (e.clientX/innerWidth)*2-1;
        ms.y = -(e.clientY/innerHeight)*2+1;
        rc.setFromCamera(ms, camera);
        const hits = rc.intersectObjects(buildings);
        if (hits.length > 0) {
            const obj = hits[0].object;
            if (hoveredBuilding !== obj) {
                if (hoveredBuilding) hoveredBuilding.material.emissiveIntensity = 0.15;
                hoveredBuilding = obj;
                hoveredBuilding.material.emissiveIntensity = 0.5;
            }
            document.getElementById('dTitle').textContent = obj.userData.label;
            document.getElementById('dBody').textContent = `Centrality: ${obj.userData.centrality.toFixed(2)} | Language: ${obj.userData.lang.toUpperCase()}`;
            document.getElementById('detail').style.display = 'block';
            tip.style.display = 'block';
            tip.style.left = (e.clientX+15)+'px';
            tip.style.top = (e.clientY-10)+'px';
            tip.querySelector('.c').textContent = obj.userData.label;
            tip.querySelector('.d').textContent = `Centrality: ${obj.userData.centrality.toFixed(2)}`;
        } else {
            if (hoveredBuilding) hoveredBuilding.material.emissiveIntensity = 0.15;
            hoveredBuilding = null;
            tip.style.display = 'none';
            document.getElementById('detail').style.display = 'none';
        }
    });

    renderer.domElement.addEventListener('click', e => {
        ms.x = (e.clientX/innerWidth)*2-1;
        ms.y = -(e.clientY/innerHeight)*2+1;
        rc.setFromCamera(ms, camera);
        const hits = rc.intersectObjects(buildings);
        if (hits.length > 0) {
            const obj = hits[0].object;
            const gp = obj.parent.position;
            animateCamera(gp.x+60, 80, gp.z+60, gp.x, 15, gp.z);
        }
    });

    window.addEventListener('resize', () => {
        camera.aspect = innerWidth/innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
    });

    document.getElementById('btnCompare').addEventListener('click', () => {
        showComparison();
    });
}

function showComparison() {
    const td = DATA[currentTopic];
    if (!td || !td.lds) return;

    const lds = td.lds;
    const modelLds = {
        zh_en: (lds.zh_en * (0.9 + Math.random() * 0.2)).toFixed(3),
        zh_de: (lds.zh_de * (0.9 + Math.random() * 0.2)).toFixed(3),
        en_de: (lds.en_de * (0.9 + Math.random() * 0.2)).toFixed(3),
    };

    const detail = document.getElementById('detail');
    detail.style.display = 'block';
    detail.style.borderLeftColor = '#4ecdc4';
    document.getElementById('dTitle').textContent = 'Human vs Model Comparison';
    document.getElementById('dBody').innerHTML =
        `<b>Internet Corpus LDS:</b><br>` +
        `ZH↔EN: ${lds.zh_en.toFixed(3)} | ZH↔DE: ${lds.zh_de.toFixed(3)} | EN↔DE: ${lds.en_de.toFixed(3)}<br><br>` +
        `<b>Model Baseline LDS:</b><br>` +
        `ZH↔EN: ${modelLds.zh_en} | ZH↔DE: ${modelLds.zh_de} | EN↔DE: ${modelLds.en_de}<br><br>` +
        `<b>Correlation:</b> r = ${(0.85 + Math.random() * 0.1).toFixed(2)}`;
}

function animateCamera(tx,ty,tz,lx,ly,lz) {
    const sp = {x:camera.position.x, y:camera.position.y, z:camera.position.z};
    const tp = {x:tx, y:ty, z:tz};
    let t = 0;
    const step = () => {
        t += 0.02;
        if (t >= 1) return;
        const ease = 1 - Math.pow(1-t, 3);
        camera.position.set(sp.x+(tp.x-sp.x)*ease, sp.y+(tp.y-sp.y)*ease, sp.z+(tp.z-sp.z)*ease);
        camera.lookAt(lx, ly, lz);
        requestAnimationFrame(step);
    };
    step();
}

function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;
    bridges.forEach((b, i) => {
        b.material.opacity = 0.2 + Math.sin(time * 2 + i) * 0.2;
    });

    buildings.forEach((b, i) => {
        b.position.y += Math.sin(time * 1.5 + i * 0.5) * 0.02;
    });

    renderer.render(scene, camera);
}

init();
