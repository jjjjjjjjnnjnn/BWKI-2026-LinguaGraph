<script>
function setLanguage(lang) {
  var t = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.title = t.page_title;
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    var key = el.getAttribute('data-i18n');
    if (t[key]) el.innerHTML = t[key];
  });
  document.querySelectorAll('.lang-btn').forEach(function(b) { b.classList.toggle('active', b.textContent.toLowerCase() === lang); });
  try { localStorage.setItem('portal_lang', lang); } catch (e) {}
  document.documentElement.lang = lang;
}
function browserLang() {
  try {
    var n = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
    if (n.indexOf('zh') === 0) return 'zh';
    if (n.indexOf('de') === 0) return 'de';
  } catch (e) {}
  return 'en';
}
function initLang() {
  var saved = null;
  try { saved = localStorage.getItem('portal_lang'); } catch (e) {}
  setLanguage(saved || browserLang());
  document.querySelectorAll('.lang-btn').forEach(function(btn) {
    btn.addEventListener('click', function() { setLanguage(btn.textContent.toLowerCase()); });
  });
  if (window.IntersectionObserver) {
    var io = new IntersectionObserver(function(es) { es.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } }); }, { threshold: 0.08 });
    document.querySelectorAll('.fade-in').forEach(function(el) { io.observe(el); });
  } else {
    document.querySelectorAll('.fade-in').forEach(function(el) { el.classList.add('visible'); });
  }
}
document.addEventListener('DOMContentLoaded', initLang);
</script>
