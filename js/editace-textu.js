/* Rezim rucni editace textu primo na strance (stejny princip jako u webu Solatube).
   Zapnete tlacitkem vpravo dole, klikate do textu a prepisujete. Zmeny se prubezne
   ukladaji do localStorage tohoto prohlizece, takze po obnoveni stranky zustanou.
   Az budete hotovi, tlacitkem "Stahnout seznam zmen" si stahnete soubor se seznamem
   PUVODNE/NOVE - ten pak staci poslat, at zmeny prepisu natrvalo do zdrojovych souboru. */
(function(){
  "use strict";

  var STRANKA = location.pathname.split("/").pop() || "index.html";
  var KLIC = "gf-edit:" + STRANKA;
  var VYBER = "h1,h2,h3,h4,h5,p,li,figcaption,button,label,dd,dt,td,th,a,span";
  var BLOKOVE = ["DIV","SECTION","UL","OL","TABLE","THEAD","TBODY","TR","FIGURE","HEADER","FOOTER","NAV","FORM","DIALOG","ARTICLE","PICTURE"];

  var editMode = false;
  var polozky = [];

  function jeListovy(el){
    if (el.closest("script,style,svg")) return false;
    if (el.getAttribute("aria-hidden") === "true") return false;
    for (var i=0;i<el.children.length;i++){
      if (BLOKOVE.indexOf(el.children[i].tagName) !== -1) return false;
    }
    return el.textContent.trim().length > 0;
  }

  function sesbirej(){
    var kandidati = Array.prototype.slice.call(document.querySelectorAll(VYBER)).filter(jeListovy);
    // vyradit ty, co jsou uvnitr jineho kandidata (napr. span uvnitr uz vybraneho p)
    polozky = kandidati.filter(function(el){
      return !kandidati.some(function(jiny){ return jiny !== el && jiny.contains(el); });
    });
    polozky.forEach(function(el, i){
      if (!el.dataset.eid) el.dataset.eid = "e" + i;
      if (el.dataset.orig === undefined) el.dataset.orig = el.innerHTML;
    });
  }

  function nacistUlozene(){
    var data = ctiUlozene();
    if (!data) return;
    polozky.forEach(function(el){
      var ulozeno = data[el.dataset.eid];
      if (ulozeno && ulozeno.curr !== undefined) el.innerHTML = ulozeno.curr;
    });
    oznacitZmenene();
  }

  function ctiUlozene(){
    try { return JSON.parse(localStorage.getItem(KLIC) || "null"); } catch(e){ return null; }
  }

  function ulozit(){
    var data = {};
    polozky.forEach(function(el){
      if (el.innerHTML !== el.dataset.orig){
        data[el.dataset.eid] = { curr: el.innerHTML };
      }
    });
    localStorage.setItem(KLIC, JSON.stringify(data));
    oznacitZmenene();
    zobrazPocet();
  }

  function oznacitZmenene(){
    polozky.forEach(function(el){
      el.classList.toggle("gf-edit-zmeneno", el.innerHTML !== el.dataset.orig);
    });
  }

  function popisMista(el){
    var sekce = el.closest("[id]");
    var idSekce = sekce ? "#" + sekce.id : "(bez sekce)";
    return "[" + STRANKA + " › " + idSekce + " › " + el.tagName + " › " + el.dataset.eid + "]";
  }

  function textZHtml(html){
    var d = document.createElement("div");
    d.innerHTML = html;
    return d.textContent.replace(/\s+/g," ").trim();
  }

  function exportZmen(){
    var radky = [];
    var pocet = 0;
    polozky.forEach(function(el){
      if (el.innerHTML !== el.dataset.orig){
        pocet++;
        radky.push(popisMista(el));
        radky.push("PUVODNE: " + textZHtml(el.dataset.orig));
        radky.push("NOVE: " + textZHtml(el.innerHTML));
        radky.push("");
      }
    });
    if (!pocet){
      alert("Zatím tu není žádná úprava k odeslání.");
      return;
    }
    var obsah = "ZMENY TEXTU - " + STRANKA + "\nCelkem " + pocet + " upravenych mist.\n\n" + radky.join("\n");
    var blob = new Blob([obsah], {type:"text/plain;charset=utf-8"});
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    var datum = new Date().toISOString().slice(0,10);
    a.href = url;
    a.download = "zmeny-" + STRANKA.replace(".html","") + "-" + datum + ".txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function(){ URL.revokeObjectURL(url); }, 2000);
    try { navigator.clipboard.writeText(obsah); } catch(e){}
  }

  function smazatZmeny(){
    if (!confirm("Smazat všechny úpravy textu na téhle stránce a vrátit původní znění?")) return;
    localStorage.removeItem(KLIC);
    location.reload();
  }

  function zapnoutEdit(zapnout){
    editMode = zapnout;
    polozky.forEach(function(el){ el.contentEditable = zapnout ? "true" : "false"; });
    document.body.classList.toggle("gf-edit-mode", zapnout);
    var btn = document.getElementById("gf-edit-toggle");
    if (btn) btn.textContent = zapnout ? "Ukončit úpravy" : "Upravit text";
  }

  function zobrazPocet(){
    var pocet = polozky.filter(function(el){ return el.innerHTML !== el.dataset.orig; }).length;
    var el = document.getElementById("gf-edit-pocet");
    if (el) el.textContent = pocet ? (pocet + " upraveno") : "beze změn";
  }

  function vytvoritPanel(){
    var panel = document.createElement("div");
    panel.id = "gf-edit-panel";
    panel.innerHTML =
      '<button id="gf-edit-toggle" type="button">Upravit text</button>' +
      '<button id="gf-edit-export" type="button">Stáhnout seznam změn</button>' +
      '<button id="gf-edit-reset" type="button">Vrátit původní</button>' +
      '<span id="gf-edit-pocet">beze změn</span>';
    document.body.appendChild(panel);

    document.getElementById("gf-edit-toggle").addEventListener("click", function(){
      zapnoutEdit(!editMode);
    });
    document.getElementById("gf-edit-export").addEventListener("click", exportZmen);
    document.getElementById("gf-edit-reset").addEventListener("click", smazatZmeny);
  }

  // v rezimu uprav nesmi klik na odkaz/tlacitko vyvolat navigaci ani modal
  document.addEventListener("click", function(e){
    if (!editMode) return;
    var cil = e.target.closest("a,button");
    if (cil && cil.id !== "gf-edit-toggle" && cil.id !== "gf-edit-export" && cil.id !== "gf-edit-reset"){
      e.preventDefault();
      e.stopPropagation();
    }
  }, true);

  var casovac;
  document.addEventListener("input", function(e){
    if (!editMode) return;
    clearTimeout(casovac);
    casovac = setTimeout(ulozit, 400);
  });

  document.addEventListener("DOMContentLoaded", function(){
    sesbirej();
    nacistUlozene();
    vytvoritPanel();
    zobrazPocet();
  });

  var styl = document.createElement("style");
  styl.textContent =
    "#gf-edit-panel{position:fixed;left:16px;bottom:16px;z-index:99999;display:flex;gap:8px;align-items:center;" +
    "background:#12181c;border:1px solid rgba(255,255,255,.18);border-radius:10px;padding:8px 10px;" +
    "font:13px/1.3 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.35)}" +
    "#gf-edit-panel button{background:#232c31;color:#eef3f4;border:1px solid rgba(255,255,255,.2);" +
    "border-radius:6px;padding:6px 10px;cursor:pointer;font:inherit}" +
    "#gf-edit-panel button:hover{background:#2c3841}" +
    "#gf-edit-pocet{color:#bcd;opacity:.8;padding-left:4px}" +
    "body.gf-edit-mode [contenteditable=true]{outline:1px dashed rgba(120,190,255,.55);outline-offset:2px;cursor:text}" +
    "body.gf-edit-mode [contenteditable=true]:hover{outline-color:#7ec8ff}" +
    ".gf-edit-zmeneno{background:rgba(255,214,102,.16)}";
  document.head.appendChild(styl);
})();
