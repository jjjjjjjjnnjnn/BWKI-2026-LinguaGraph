/**
 * CognitiveSpace i18n — Trilingual EN/DE/ZH support for 3D viewer
 *
 * Usage:
 *   1. Include this script before main viewer code
 *   2. Add data-i18n="key" to static HTML elements
 *   3. Call i18n.apply() after page load to translate static elements
 *   4. For dynamic JS text, call i18n.tr('key') or i18n.tr('key', {count: N})
 *
 * Language persistence: localStorage 'preferredLang'
 */

(function(global) {
'use strict';

const TRANSLATIONS = {
    en: {
        // HUD
        'title': 'CognitiveSpace',
        'stats.concepts': 'Concepts',
        'stats.relations': 'Relations',
        'stats.levels': 'Levels',
        'hud.subtitle': '{concepts} concepts · {relations} relations',

        // View modes
        'mode.universe': 'Universe',
        'mode.spacefill': 'Space-Fill',
        'mode.compare': 'Compare',

        // Language filter
        'lang.all': 'All',

        // Controls
        'auto.rotate': '⟳ Auto Rotate',
        'clear': '← Clear',

        // Legend
        'level.elementary': 'Elementary',
        'level.middle': 'Middle',
        'level.high': 'High',
        'level.college': 'College',

        // Links
        'research.portal': '📖 Research Portal',

        // Controls hint
        'ctrl.hint': 'DRAG · SCROLL · WASD',

        // Loading
        'loading': 'CognitiveSpace',
        'error.load': '3d-force-graph failed to load. Check network.',
        'error.data': 'Knowledge graph data not found.',

        // Detail panel headers
        'detail.node.profile': 'NODE PROFILE',
        'detail.graph.profile': 'GRAPH PROFILE (full dataset: {count} nodes)',
        'detail.about': 'ABOUT',
        'detail.degree': 'Degree:',
        'detail.role': 'Role:',
        'detail.hds_depth': 'HDS depth:',
        'detail.sources': 'Sources:',
        'detail.cds': 'CDS:',
        'detail.avg_degree': 'Avg degree:',
        'detail.lds_zhen': 'LDS ZH-EN:',
        'detail.lds_zhde': 'LDS ZH-DE:',
        'detail.lds_ende': 'LDS EN-DE:',
        'detail.connected_to': 'Connected to:',

        // Detail values
        'connections': 'connections',
        'levels': 'levels',
        'textbooks': 'textbooks',
        'sources': 'sources',

        // Node roles
        'role.intermediate': 'Intermediate',
        'role.prerequisite_chain': 'Prerequisite Chain',
        'role.hub': 'Hub Concept',
        'role.peripheral': 'Peripheral',

        // Role insights
        'insight.hub': 'This concept connects to many others, acting as a structural hub. Understanding it unlocks multiple advanced topics.',
        'insight.chain': 'This concept sits in a deep dependency chain (depth={depth}), serving as a building block for higher concepts.',
        'insight.peripheral': 'This concept has few direct connections — a specialized topic with narrow dependencies.',
        'insight.balanced': 'This concept holds a balanced position in the knowledge network with moderate connectivity.',

        // Level descriptions
        'desc.elementary': 'Foundational: basic arithmetic and early geometry concepts',
        'desc.middle': 'Intermediate: algebra, equations, and function concepts',
        'desc.high': 'Advanced: calculus, probability, and vector concepts',
        'desc.college': 'Specialized: higher mathematics with formal proofs and theory',

        // Metric definitions
        'def.cds': 'CDS = 2|E|/(|V|·(|V|-1)) — concept interconnectedness (full graph).',
        'def.hds': 'HDS = longest prerequisite chain from this concept.',
        'def.lds': 'LDS = 1 − |A∩B|/|A∪B| — cross-language structural divergence.',
    },

    de: {
        'title': 'CognitiveSpace',
        'stats.concepts': 'Konzepte',
        'stats.relations': 'Beziehungen',
        'stats.levels': 'Stufen',
        'hud.subtitle': '{concepts} Konzepte · {relations} Beziehungen',

        'mode.universe': 'Universum',
        'mode.spacefill': 'Raumfüllung',
        'mode.compare': 'Vergleich',

        'lang.all': 'Alle',

        'auto.rotate': '⟳ Auto-Rotation',
        'clear': '← Zurücksetzen',

        'level.elementary': 'Grundschule',
        'level.middle': 'Mittelstufe',
        'level.high': 'Oberstufe',
        'level.college': 'Hochschule',

        'research.portal': '📖 Forschungsportal',

        'ctrl.hint': 'ZIEHEN · SKALIEREN · WASD',

        'loading': 'CognitiveSpace',
        'error.load': '3d-force-graph konnte nicht geladen werden. Netzwerk prüfen.',
        'error.data': 'Wissensgraph-Daten nicht gefunden.',

        'detail.node.profile': 'KNOTENPROFIL',
        'detail.graph.profile': 'GRAPHPROFIL (vollständiger Datensatz: {count} Knoten)',
        'detail.about': 'INFORMATIONEN',
        'detail.degree': 'Grad:',
        'detail.role': 'Rolle:',
        'detail.hds_depth': 'HDS-Tiefe:',
        'detail.sources': 'Quellen:',
        'detail.cds': 'CDS:',
        'detail.avg_degree': 'Mittl. Grad:',
        'detail.lds_zhen': 'LDS ZH-EN:',
        'detail.lds_zhde': 'LDS ZH-DE:',
        'detail.lds_ende': 'LDS EN-DE:',
        'detail.connected_to': 'Verbunden mit:',

        'connections': 'Verbindungen',
        'levels': 'Ebenen',
        'textbooks': 'Lehrbücher',
        'sources': 'Quellen',

        'role.intermediate': 'Mittelstufe',
        'role.prerequisite_chain': 'Voraussetzungskette',
        'role.hub': 'Hub-Konzept',
        'role.peripheral': 'Peripher',

        'insight.hub': 'Dieses Konzept ist mit vielen anderen verbunden und fungiert als struktureller Knotenpunkt. Sein Verständnis erschließt mehrere fortgeschrittene Themen.',
        'insight.chain': 'Dieses Konzept liegt in einer tiefen Abhängigkeitskette (Tiefe={depth}) und dient als Baustein für höhere Konzepte.',
        'insight.peripheral': 'Dieses Konzept hat wenige direkte Verbindungen — ein spezialisiertes Thema mit engen Abhängigkeiten.',
        'insight.balanced': 'Dieses Konzept hat eine ausgewogene Position im Wissensnetzwerk mit moderater Vernetzung.',

        'desc.elementary': 'Grundlegend: einfache Arithmetik und frühe Geometriekonzepte',
        'desc.middle': 'Mittelstufe: Algebra, Gleichungen und Funktionen',
        'desc.high': 'Fortgeschritten: Analysis, Wahrscheinlichkeit und Vektoren',
        'desc.college': 'Spezialisiert: höhere Mathematik mit formalen Beweisen und Theorie',

        'def.cds': 'CDS = 2|E|/(|V|·(|V|-1)) — Konzeptvernetzung (vollständiger Graph).',
        'def.hds': 'HDS = längste Voraussetzungskette ab diesem Konzept.',
        'def.lds': 'LDS = 1 − |A∩B|/|A∪B| — sprachübergreifende strukturelle Divergenz.',
    },

    zh: {
        'title': 'CognitiveSpace',
        'stats.concepts': '概念',
        'stats.relations': '关系',
        'stats.levels': '学段',
        'hud.subtitle': '{concepts} 个概念 · {relations} 条关系',

        'mode.universe': '宇宙模式',
        'mode.spacefill': '空间填充',
        'mode.compare': '比较模式',

        'lang.all': '全部',

        'auto.rotate': '⟳ 自动旋转',
        'clear': '← 清除',

        'level.elementary': '小学',
        'level.middle': '初中',
        'level.high': '高中',
        'level.college': '大学',

        'research.portal': '📖 研究门户',

        'ctrl.hint': '拖拽 · 滚轮 · WASD',

        'loading': 'CognitiveSpace',
        'error.load': '3d-force-graph 加载失败，请检查网络。',
        'error.data': '未找到知识图谱数据。',

        'detail.node.profile': '节点信息',
        'detail.graph.profile': '图谱信息（完整数据集：{count} 个节点）',
        'detail.about': '关于',
        'detail.degree': '度：',
        'detail.role': '角色：',
        'detail.hds_depth': 'HDS 深度：',
        'detail.sources': '来源：',
        'detail.cds': 'CDS：',
        'detail.avg_degree': '平均度：',
        'detail.lds_zhen': 'LDS 中-英：',
        'detail.lds_zhde': 'LDS 中-德：',
        'detail.lds_ende': 'LDS 英-德：',
        'detail.connected_to': '连接至：',

        'connections': '条连接',
        'levels': '层',
        'textbooks': '本教材',
        'sources': '个来源',

        'role.intermediate': '中间节点',
        'role.prerequisite_chain': '前提链',
        'role.hub': '枢纽概念',
        'role.peripheral': '外围节点',

        'insight.hub': '该概念连接众多其他节点，起到结构枢纽的作用。理解它有助于掌握多个高级主题。',
        'insight.chain': '该概念位于深层依赖链中（深度={depth}），是更高层概念的基石。',
        'insight.peripheral': '该概念直接连接较少——一个依赖范围狭窄的专业化主题。',
        'insight.balanced': '该概念在知识网络中处于平衡位置，具有适中的连通性。',

        'desc.elementary': '基础：基本算术和早期几何概念',
        'desc.middle': '中等：代数、方程和函数概念',
        'desc.high': '高级：微积分、概率和向量概念',
        'desc.college': '专业化：形式化证明和理论的高等数学',

        'def.cds': 'CDS = 2|E|/(|V|·(|V|-1)) — 概念互联度（完整图谱）。',
        'def.hds': 'HDS = 从此概念出发的最长前提链。',
        'def.lds': 'LDS = 1 − |A∩B|/|A∪B| — 跨语言结构差异度。',
    }
};

// ─── Core i18n module ────────────────────────────────────────────────
const i18n = {
    lang: 'en',
    translations: TRANSLATIONS,

    /**
     * Detect user's preferred language.
     * Priority: localStorage → browser language → 'en'
     */
    detect() {
        try {
            const stored = localStorage.getItem('preferredLang');
            if (stored && this.translations[stored]) return stored;
        } catch(e) {}
        const browser = (navigator.language || '').slice(0, 2);
        if (this.translations[browser]) return browser;
        return 'en';
    },

    /**
     * Set language and persist to localStorage.
     */
    setLanguage(lang) {
        if (!this.translations[lang]) lang = 'en';
        this.lang = lang;
        try { localStorage.setItem('preferredLang', lang); } catch(e) {}
        return this;
    },

    /**
     * Translate a key with optional interpolation.
     * @param {string} key - Translation key
     * @param {object} vars - Optional {key: value} for template strings
     * @returns {string}
     */
    tr(key, vars) {
        const langObj = this.translations[this.lang] || this.translations.en;
        let t = langObj[key];
        if (!t) {
            // Fallback to English
            t = this.translations.en[key];
            if (!t) return `[${key}]`;
        }
        if (vars) {
            for (const [k, v] of Object.entries(vars)) {
                t = t.replace(`{${k}}`, v);
            }
        }
        return t;
    },

    /**
     * Apply translations to all elements with data-i18n attribute.
     */
    apply() {
        // Static data-i18n elements
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = this.tr(key);
        });

        // Elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.tr(key);
        });
    }
};

// Bootstrap
i18n.setLanguage(i18n.detect());

// Export
global.i18n = i18n;
global.TRANSLATIONS = TRANSLATIONS;

})(typeof window !== 'undefined' ? window : this);
