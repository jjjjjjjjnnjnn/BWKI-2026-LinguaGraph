// LinguaGraph Cognitive City V3 — Export Module
// Screenshot and data export functionality

class ExportController {
    constructor(renderer, scene, camera) {
        this.renderer = renderer;
        this.scene = scene;
        this.camera = camera;
    }

    captureScreenshot() {
        // Render one frame at high quality
        this.renderer.render(this.scene, this.camera);
        const dataURL = this.renderer.domElement.toDataURL("image/png");
        return dataURL;
    }

    downloadScreenshot(filename) {
        const dataURL = this.captureScreenshot();
        const link = document.createElement("a");
        link.href = dataURL;
        link.download = filename || `linguagraph_${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    exportJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename || `linguagraph_data_${Date.now()}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    exportCurrentView(topic) {
        const data = {
            topic: topic,
            timestamp: new Date().toISOString(),
            lds: LDS_DATA[topic] || {},
            city: CITY_DATA[topic] || {},
        };
        this.exportJSON(data, `linguagraph_${topic}_${Date.now()}.json`);
    }
}
