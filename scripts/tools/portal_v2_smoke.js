// Smoke-test v2 i18n wiring with stub DOM.
const fs = require("fs");
const dictSrc = fs.readFileSync("cognitive-space/portal/_v2dict.js", "utf8");
eval(dictSrc + "\nglobal.TRANSLATIONS = TRANSLATIONS;");
let jsSrc = fs.readFileSync("cognitive-space/portal/_v2js.js", "utf8");
jsSrc = jsSrc.replace(/<\/?script>/g, "");
const applied = { en: 0, de: 0, zh: 0 };
let lang = "en";
const els = [];
const html = fs.readFileSync("cognitive-space/portal/index.v2.html", "utf8");
const re = /data-i18n="([^"]+)"/g;
let m;
while ((m = re.exec(html))) els.push({ key: m[1], innerHTML: "" });
global.document = {
  title: "",
  querySelectorAll: (sel) => {
    if (sel === "[data-i18n]") return els.map((e) => ({
      getAttribute: () => e.key,
      set innerHTML(v) { e.v = v; },
    }));
    if (sel === ".lang-btn") return [];
    return [];
  },
  querySelector: () => null,
  documentElement: {},
  addEventListener: () => {},
};
global.localStorage = { setItem: () => {}, getItem: () => null };
global.navigator = { language: "en" };
global.window = {};
eval(jsSrc);
for (const L of ["en", "de", "zh"]) {
  setLanguage(L);
  const missing = els.filter((e) => !TRANSLATIONS[L][e.key]);
  console.log(L, "keys-applied:", els.length - missing.length, "/", els.length,
    "missing:", missing.map((e) => e.key).join(",") || "none");
}
