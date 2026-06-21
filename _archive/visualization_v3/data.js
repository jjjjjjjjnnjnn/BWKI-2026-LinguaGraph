// LinguaGraph Cognitive City V3 — Data Layer
// Provides data for all topics from existing LDS results + simulation baseline

const TOPICS = ["freedom", "success", "responsibility", "home", "justice"];

const TOPIC_LABELS = {
    freedom: { zh: "自由", en: "freedom", de: "Freiheit" },
    success: { zh: "成功", en: "success", de: "Erfolg" },
    responsibility: { zh: "责任", en: "responsibility", de: "Verantwortung" },
    home: { zh: "家", en: "home", de: "Heimat" },
    justice: { zh: "正义", en: "justice", de: "Gerechtigkeit" },
};

const LDS_DATA = {
    freedom: {
        zh_en: 0.215, zh_de: 0.230, en_de: 0.233,
        jaccard: 0.381,
    },
    success: {
        zh_en: 0.180, zh_de: 0.200, en_de: 0.210,
        jaccard: 0.420,
    },
    responsibility: {
        zh_en: 0.228, zh_de: 0.219, en_de: 0.233,
        jaccard: 0.395,
    },
    home: {
        zh_en: 0.250, zh_de: 0.280, en_de: 0.220,
        jaccard: 0.350,
    },
    justice: {
        zh_en: 0.201, zh_de: 0.190, en_de: 0.215,
        jaccard: 0.400,
    },
};

// Concept data per topic per language
// centrality: 0-1 (building height), freq: approximate frequency (building width)
const CITY_DATA = {
    freedom: {
        zh: {
            buildings: [
                { id: "自由", label: "自由", c: 0.95, freq: 42 },
                { id: "责任", label: "责任", c: 0.75, freq: 35 },
                { id: "权利", label: "权利", c: 0.70, freq: 30 },
                { id: "社会", label: "社会", c: 0.68, freq: 28 },
                { id: "个人", label: "个人", c: 0.60, freq: 22 },
            ],
            roads: [
                { s: "自由", t: "责任", r: "requires", w: 0.9 },
                { s: "自由", t: "权利", r: "is_a", w: 0.85 },
                { s: "责任", t: "社会", r: "part_of", w: 0.7 },
            ],
        },
        en: {
            buildings: [
                { id: "freedom", label: "freedom", c: 0.95, freq: 36 },
                { id: "rights", label: "rights", c: 0.80, freq: 30 },
                { id: "choice", label: "choice", c: 0.75, freq: 28 },
                { id: "liberty", label: "liberty", c: 0.70, freq: 25 },
                { id: "responsibility", label: "responsibility", c: 0.65, freq: 22 },
            ],
            roads: [
                { s: "freedom", t: "rights", r: "is_a", w: 0.9 },
                { s: "freedom", t: "choice", r: "enables", w: 0.85 },
            ],
        },
        de: {
            buildings: [
                { id: "Freiheit", label: "Freiheit", c: 0.95, freq: 41 },
                { id: "Selbstbestimmung", label: "Selbstbestimmung", c: 0.80, freq: 32 },
                { id: "Recht", label: "Recht", c: 0.75, freq: 28 },
                { id: "Verantwortung", label: "Verantwortung", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "Freiheit", t: "Selbstbestimmung", r: "is_a", w: 0.9 },
                { s: "Freiheit", t: "Recht", r: "requires", w: 0.85 },
            ],
        },
        bridges: [
            { s: "自由", t: "freedom" },
            { s: "责任", t: "Verantwortung" },
            { s: "权利", t: "Recht" },
        ],
    },
    success: {
        zh: {
            buildings: [
                { id: "成功", label: "成功", c: 0.95, freq: 47 },
                { id: "努力", label: "努力", c: 0.85, freq: 40 },
                { id: "家庭", label: "家庭", c: 0.75, freq: 35 },
                { id: "成就", label: "成就", c: 0.70, freq: 30 },
            ],
            roads: [
                { s: "成功", t: "努力", r: "requires", w: 0.95 },
                { s: "成功", t: "家庭", r: "for", w: 0.8 },
            ],
        },
        en: {
            buildings: [
                { id: "success", label: "success", c: 0.95, freq: 48 },
                { id: "achievement", label: "achievement", c: 0.85, freq: 38 },
                { id: "opportunity", label: "opportunity", c: 0.80, freq: 35 },
                { id: "choice", label: "choice", c: 0.75, freq: 30 },
            ],
            roads: [
                { s: "success", t: "achievement", r: "is_a", w: 0.9 },
                { s: "success", t: "opportunity", r: "enables", w: 0.85 },
            ],
        },
        de: {
            buildings: [
                { id: "Erfolg", label: "Erfolg", c: 0.95, freq: 45 },
                { id: "Leistung", label: "Leistung", c: 0.85, freq: 38 },
                { id: "Karriere", label: "Karriere", c: 0.80, freq: 35 },
                { id: "Ziel", label: "Ziel", c: 0.75, freq: 30 },
            ],
            roads: [
                { s: "Erfolg", t: "Leistung", r: "requires", w: 0.9 },
                { s: "Erfolg", t: "Karriere", r: "leads_to", w: 0.85 },
            ],
        },
        bridges: [
            { s: "成功", t: "success" },
            { s: "努力", t: "Leistung" },
            { s: "成就", t: "achievement" },
        ],
    },
    responsibility: {
        zh: {
            buildings: [
                { id: "责任", label: "责任", c: 0.95, freq: 40 },
                { id: "义务", label: "义务", c: 0.80, freq: 32 },
                { id: "道德", label: "道德", c: 0.75, freq: 28 },
                { id: "社会", label: "社会", c: 0.70, freq: 25 },
                { id: "家庭", label: "家庭", c: 0.65, freq: 22 },
            ],
            roads: [
                { s: "责任", t: "义务", r: "is_a", w: 0.9 },
                { s: "责任", t: "道德", r: "based_on", w: 0.85 },
                { s: "责任", t: "社会", r: "part_of", w: 0.7 },
            ],
        },
        en: {
            buildings: [
                { id: "responsibility", label: "responsibility", c: 0.95, freq: 38 },
                { id: "duty", label: "duty", c: 0.80, freq: 30 },
                { id: "accountability", label: "accountability", c: 0.75, freq: 28 },
                { id: "choice", label: "choice", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "responsibility", t: "duty", r: "is_a", w: 0.9 },
                { s: "responsibility", t: "accountability", r: "requires", w: 0.85 },
            ],
        },
        de: {
            buildings: [
                { id: "Verantwortung", label: "Verantwortung", c: 0.95, freq: 42 },
                { id: "Pflicht", label: "Pflicht", c: 0.80, freq: 32 },
                { id: "Haftung", label: "Haftung", c: 0.75, freq: 28 },
                { id: "Bildung", label: "Bildung", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "Verantwortung", t: "Pflicht", r: "is_a", w: 0.9 },
                { s: "Verantwortung", t: "Haftung", r: "requires", w: 0.85 },
            ],
        },
        bridges: [
            { s: "责任", t: "responsibility" },
            { s: "义务", t: "duty" },
            { s: "道德", t: "accountability" },
        ],
    },
    home: {
        zh: {
            buildings: [
                { id: "家", label: "家", c: 0.95, freq: 50 },
                { id: "家人", label: "家人", c: 0.85, freq: 40 },
                { id: "归属", label: "归属", c: 0.75, freq: 30 },
                { id: "温暖", label: "温暖", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "家", t: "家人", r: "part_of", w: 0.95 },
                { s: "家", t: "归属", r: "provides", w: 0.8 },
            ],
        },
        en: {
            buildings: [
                { id: "home", label: "home", c: 0.95, freq: 45 },
                { id: "family", label: "family", c: 0.85, freq: 38 },
                { id: "belonging", label: "belonging", c: 0.75, freq: 28 },
                { id: "safety", label: "safety", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "home", t: "family", r: "part_of", w: 0.9 },
                { s: "home", t: "belonging", r: "provides", w: 0.85 },
            ],
        },
        de: {
            buildings: [
                { id: "Heimat", label: "Heimat", c: 0.95, freq: 48 },
                { id: "Familie", label: "Familie", c: 0.85, freq: 38 },
                { id: "Zugehörigkeit", label: "Zugehörigkeit", c: 0.75, freq: 30 },
                { id: "Geborgenheit", label: "Geborgenheit", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "Heimat", t: "Familie", r: "part_of", w: 0.9 },
                { s: "Heimat", t: "Zugehörigkeit", r: "provides", w: 0.85 },
            ],
        },
        bridges: [
            { s: "家", t: "home" },
            { s: "家人", t: "family" },
            { s: "归属", t: "belonging" },
        ],
    },
    justice: {
        zh: {
            buildings: [
                { id: "正义", label: "正义", c: 0.95, freq: 38 },
                { id: "公平", label: "公平", c: 0.85, freq: 35 },
                { id: "平等", label: "平等", c: 0.75, freq: 28 },
                { id: "法律", label: "法律", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "正义", t: "公平", r: "is_a", w: 0.9 },
                { s: "正义", t: "平等", r: "requires", w: 0.85 },
            ],
        },
        en: {
            buildings: [
                { id: "justice", label: "justice", c: 0.95, freq: 40 },
                { id: "fairness", label: "fairness", c: 0.85, freq: 35 },
                { id: "equality", label: "equality", c: 0.75, freq: 30 },
                { id: "rights", label: "rights", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "justice", t: "fairness", r: "is_a", w: 0.9 },
                { s: "justice", t: "equality", r: "requires", w: 0.85 },
            ],
        },
        de: {
            buildings: [
                { id: "Gerechtigkeit", label: "Gerechtigkeit", c: 0.95, freq: 42 },
                { id: "Fairness", label: "Fairness", c: 0.85, freq: 35 },
                { id: "Gleichheit", label: "Gleichheit", c: 0.75, freq: 30 },
                { id: "Recht", label: "Recht", c: 0.70, freq: 25 },
            ],
            roads: [
                { s: "Gerechtigkeit", t: "Fairness", r: "is_a", w: 0.9 },
                { s: "Gerechtigkeit", t: "Gleichheit", r: "requires", w: 0.85 },
            ],
        },
        bridges: [
            { s: "正义", t: "justice" },
            { s: "公平", t: "fairness" },
            { s: "平等", t: "equality" },
        ],
    },
};

// Human vs Simulation comparison data (placeholder with Wikipedia LDS)
const COMPARISON_DATA = {
    human: {
        success: 0.972, responsibility: 0.831, justice: 0.822,
        freedom: 0.812, home: 0.750,
    },
    simulation: {
        success: 0.910, responsibility: 0.800, justice: 0.790,
        freedom: 0.780, home: 0.720,
    },
};
