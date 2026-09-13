/**
 * CognitiveSpace node detail extension — grounding badges + evidence (W0 panel logic).
 * Requires (load order): grounding_lookup.js -> i18n.js -> node-detail-ext.js
 * Exposes: window.nodeExtraHTML(name) -> HTML string (all external text HTML-escaped).
 */
(function (global) {
'use strict';

function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
}

function tr(key, vars) {
    try {
        var I = global.i18n;
        if (I && typeof I.tr === 'function') return I.tr(key, vars);
    } catch (e) {}
    return key;
}

function lookupOf(name) {
    try {
        var L = global.GROUNDING_LOOKUP || {};
        return L[name] || null;
    } catch (e) { return null; }
}

function zhTotal(zh) {
    var n = 0;
    for (var i = 0; i < zh.length; i++) n += (+zh[i].c || 0);
    return n;
}

function uniqFiles(zh) {
    var seen = {}, out = [];
    for (var i = 0; i < zh.length; i++) {
        var f = String(zh[i].f || '');
        if (!seen[f]) { seen[f] = 1; out.push({ f: f, c: (+zh[i].c || 0) }); }
        else {
            for (var j = 0; j < out.length; j++) {
                if (out[j].f === f) { out[j].c += (+zh[i].c || 0); break; }
            }
        }
    }
    return out;
}

function nodeExtraHTML(name) {
    var entry = lookupOf(name);
    // Math / ungrounded nodes: neutral note (grounding covers physics & chemistry only).
    if (!entry) {
        return '<div class="ground-row ground-na">' + esc(tr('detail.ground_na')) + '</div>';
    }
    var zh = entry.zh || [];
    var en = entry.en || { hit: false, ev: null };
    var cn = entry.cn || [];
    var total = zhTotal(zh);

    var badges = '';
    if (total > 0) {
        badges += '<span class="ground-badge ground-zh" style="background:#1a7f37;color:#fff;border-radius:4px;padding:1px 6px;margin-right:4px;">'
            + esc(tr('detail.ground_zh', { n: total })) + '</span>';
    }
    if (en && en.hit) {
        badges += '<span class="ground-badge ground-en" style="background:#0969da;color:#fff;border-radius:4px;padding:1px 6px;margin-right:4px;">'
            + esc(tr('detail.ground_en')) + '</span>';
    }
    if (total <= 0 && !(en && en.hit)) {
        badges += '<span class="ground-badge ground-none" style="background:#6e7781;color:#fff;border-radius:4px;padding:1px 6px;margin-right:4px;">'
            + esc(tr('detail.ground_none')) + '</span>';
    }

    var html = '<div class="ground-row">' + badges + '</div>';
    html += '<details class="ground-details"><summary>' + esc(tr('detail.src_list')) + '</summary>';

    // Source-textbook file list (deduplicated; aggregated counts).
    var files = uniqFiles(zh);
    if (files.length) {
        html += '<ul class="ground-src">';
        for (var i = 0; i < files.length; i++) {
            html += '<li>' + esc(files[i].f) + ' ×' + esc(String(files[i].c)) + '</li>';
        }
        html += '</ul>';
    }
    // EN semantic evidence line.
    if (en && en.hit && en.ev) {
        html += '<p class="ground-en-ev">EN: ' + esc(en.ev.f || '')
            + (en.ev.s ? ' — ' + esc(en.ev.s) : '') + '</p>';
    }
    // Up to 2 snippet excerpts.
    var shown = Math.min(2, zh.length);
    for (var k = 0; k < shown; k++) {
        html += '<p class="ground-snip">[' + esc(zh[k].f) + '] ' + esc(zh[k].s) + '</p>';
    }
    if (zh.length > shown) {
        html += '<div class="ground-more">' + esc(tr('detail.src_more', { n: zh.length - shown })) + '</div>';
    }
    // CN textbook mapping.
    if (cn.length) {
        html += '<div class="ground-cn-title">' + esc(tr('detail.cn_map')) + '</div><ul class="ground-cn">';
        for (var m = 0; m < cn.length; m++) {
            html += '<li>' + esc(cn[m].b) + ' — ' + esc(cn[m].ch) + ' — ' + esc(cn[m].s) + '</li>';
        }
        html += '</ul>';
    }
    html += '</details>';
    return html;
}

global.nodeExtraHTML = nodeExtraHTML;

})(typeof window !== 'undefined' ? window : this);
