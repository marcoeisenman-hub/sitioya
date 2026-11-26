// Botón "Cotiza tu página" de SitioYa en las páginas de ejemplo.
// Abre el WhatsApp de SitioYa (6919-7559) con un mensaje listo. Va abajo a la izquierda
// para no chocar con el botón de WhatsApp del negocio de ejemplo (abajo a la derecha).
(function () {
  if (document.getElementById("sy-cotiza")) return;
  var msg = "Hola, vi un ejemplo en SitioYa y quiero cotizar una página para mi negocio";
  var st = document.createElement("style");
  st.textContent =
    "#sy-cotiza{position:fixed;left:16px;bottom:20px;z-index:2147483000;display:flex;align-items:center;gap:8px;" +
    "height:46px;padding:0 16px 0 8px;border-radius:999px;background:#FF6B5B;color:#fff;text-decoration:none;" +
    "font:800 14px/1 'DM Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;letter-spacing:0;" +
    "box-shadow:0 10px 24px rgba(0,0,0,.28);mix-blend-mode:normal;white-space:nowrap}" +
    "#sy-cotiza:hover{filter:brightness(1.06)}" +
    "#sy-cotiza:focus-visible{outline:3px solid #1B2A4A;outline-offset:3px}" +
    "#sy-cotiza svg{flex:none;display:block}" +
    "@media(max-width:400px){#sy-cotiza{left:12px;gap:6px;padding:0 14px 0 7px;font-size:13px}}" +
    // en celulares muy angostos no cabe al lado del botón de WhatsApp: va encima
    "@media(max-width:359px){#sy-cotiza{bottom:84px}}" +
    "@media print{#sy-cotiza{display:none}}";
  document.head.appendChild(st);
  var a = document.createElement("a");
  a.id = "sy-cotiza";
  a.href = "https://wa.me/50769197559?text=" + encodeURIComponent(msg);
  a.target = "_blank";
  a.rel = "noopener";
  a.setAttribute("aria-label", "Cotiza tu página con SitioYa por WhatsApp");
  a.innerHTML =
    '<svg width="30" height="30" viewBox="0 0 100 100" aria-hidden="true"><rect width="100" height="100" rx="50" fill="#FFF6EC"/>' +
    '<rect x="20" y="26" width="52" height="40" rx="6" fill="#FFF6EC" stroke="#1B2A4A" stroke-width="6"/><path d="M20 37H72" stroke="#1B2A4A" stroke-width="6"/>' +
    '<path d="M52 47L52 80L60 72L66 84L71.5 81.5L65.5 69.5L77 69.5Z" fill="#1B2A4A" stroke="#FFF6EC" stroke-width="7" stroke-linejoin="round" paint-order="stroke"/></svg>' +
    "<span>Cotiza tu página</span>";
  (document.body || document.documentElement).appendChild(a);
})();
