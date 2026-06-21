// LinguaGraph Cognitive City V3 — Demo Mode Controller
// Auto-plays through topics with camera transitions

class DemoController {
    constructor(loadTopicFn, animateCameraFn) {
        this.loadTopic = loadTopicFn;
        this.animateCamera = animateCameraFn;
        this.running = false;
        this.currentIdx = 0;
        this.topics = TOPICS;
        this.interval = 6000; // 6 seconds per topic
        this.timer = null;
    }

    start() {
        if (this.running) return;
        this.running = true;
        this.currentIdx = 0;
        this._play();
        this._updateUI(true);
    }

    stop() {
        this.running = false;
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this._updateUI(false);
    }

    toggle() {
        if (this.running) this.stop();
        else this.start();
    }

    _play() {
        if (!this.running) return;

        const topic = this.topics[this.currentIdx];
        this.loadTopic(topic);

        // Update select
        const sel = document.getElementById("topicSelect");
        if (sel) sel.value = topic;

        // Camera sweep per language
        const positions = [
            { x: -130, y: 80, z: 100, lx: -130, ly: 15, lz: 0 },
            { x: 0, y: 80, z: 100, lx: 0, ly: 15, lz: 0 },
            { x: 130, y: 80, z: 100, lx: 130, ly: 15, lz: 0 },
        ];

        let step = 0;
        const sweepInterval = setInterval(() => {
            if (!this.running || step >= positions.length) {
                clearInterval(sweepInterval);
                return;
            }
            const p = positions[step];
            this.animateCamera(p.x, p.y, p.z, p.lx, p.ly, p.lz);
            step++;
        }, 1800);

        // Next topic
        this.timer = setTimeout(() => {
            this.currentIdx = (this.currentIdx + 1) % this.topics.length;
            this._play();
        }, this.interval);
    }

    _updateUI(active) {
        const btn = document.getElementById("btnDemo");
        if (btn) {
            btn.textContent = active ? "Stop Demo" : "Demo Mode";
            btn.style.background = active
                ? "rgba(255,107,107,0.2)"
                : "rgba(74,125,255,0.15)";
            btn.style.color = active ? "#ff6b6b" : "#4a7dff";
        }

        const topSub = document.getElementById("topSub");
        if (topSub) {
            topSub.textContent = active
                ? `Demo: ${this.topics[this.currentIdx]} (${this.currentIdx + 1}/${this.topics.length})`
                : "Each city represents one language's conceptual structure";
        }
    }
}
