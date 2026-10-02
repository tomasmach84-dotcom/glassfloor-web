# -*- coding: utf-8 -*-
"""Jednorázová přestavba struktury webu GLASSFLOOR (2. 10. 2026).

Čte původní stránky ze zálohy _STARE/pred-restrukturalizaci-2026-10-02 a skládá z nich
nové podstránky se společnou hlavičkou, patičkou a formulářem. Spuštění: python tools/build-stranky.py
(zdrojem je vždy záloha, takže skript lze pouštět opakovaně).
"""
import re, json, pathlib, os
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_STARE" / "pred-restrukturalizaci-2026-10-02"
BASE = "https://www.glassfloor.cz"   # DOČASNÁ doména (canonical, og:url, sitemap, JSON-LD) - před spuštěním ověřit a přegenerovat
DATE = "2026-10-02"


def rd(name):
    return (SRC / name).read_text(encoding="utf-8")


def sections(txt):
    return re.findall(r"<section\b[^>]*>.*?</section>", txt, re.S)


def pick(txt, needle):
    for s in sections(txt):
        if needle in s:
            return s
    raise KeyError(needle)


BARVA = rd("barva-CMYK.html")
PROD = rd("produkty.html")
KST = rd("ke-stazeni.html")
ONAS = rd("o-nas.html")
KONT = rd("kontakty.html")

DIALOG = re.search(r"<dialog id=\"dlg\">.*?</dialog>", BARVA, re.S).group(0).replace('<h3 class="h3"', '<p class="h3"').replace("</h3>", "</p>")

# ---------------------------------------------------------------- společné části
MENU = [
    ("produkty", "produkty.html", "Produkty"),
    ("architekti", "pro-architekty.html", "Pro architekty"),
    ("reference", "reference.html", "Reference"),
    ("stazeni", "ke-stazeni.html", "Ke stažení"),
    ("onas", "o-nas.html", "O nás"),
    ("kontakty", "kontakty.html", "Kontakty"),
]

FOOT_LINKS = [
    ("produkty.html", "Produkty"), ("chrome.html", "chrome"), ("pure.html", "pure"), ("circle.html", "circle"),
    ("firestop.html", "FIRESTOP"), ("airflow-rwa.html", "AIRFLOW a RWA"), ("na-miru.html", "Na míru a výbava"),
    ("pro-architekty.html", "Pro architekty"), ("reference.html", "Reference"), ("ke-stazeni.html", "Ke stažení"),
    ("o-nas.html", "O nás"), ("kontakty.html", "Kontakty"),
]


def menu_items(active):
    out = []
    for key, href, label in MENU:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


def header(active):
    items = menu_items(active)
    return f"""<header id="hd">
  <div class="nav">
    <a class="lockup" href="index.html">
      <img class="gflogo" src="img/logo-glassfloor-negativ.svg" alt="GLASSFLOOR by Heliobus AG · St. Gallen, Switzerland">
    </a>
    <ul>
{items}
    </ul>
    <button class="cta" onclick="document.getElementById('dlg').showModal()">Představit projekt</button>
    <button class="menu-btn" id="mbtn" type="button" aria-expanded="false" aria-controls="mmenu" aria-label="Menu">
      <i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i>
    </button>
  </div>
  <nav class="mmenu" id="mmenu" aria-label="Hlavní nabídka">
    <ul>
{items}
    </ul>
    <button class="cta" type="button" onclick="document.getElementById('dlg').showModal()">Představit projekt</button>
  </nav>
</header>"""


FOOTER = """<footer>
  <div class="lockup">
    <img class="gflogo" src="img/logo-glassfloor-negativ.svg" alt="GLASSFLOOR">
    <span>by Heliobus AG · Engineered and manufactured in St. Gallen, Switzerland</span>
  </div>
  <div class="foot-right">
    <span class="note">Náhled webu · interní prototyp 2026 · formulář neodesílá data</span>
    <a class="wt-badge" href="https://tomasmach84-dotcom.github.io/wt-web/" target="_blank" rel="noopener" aria-label="WT - WINDOWS TOMORROW - přejít na web skupiny">
      <span class="k">Součást skupiny</span>
      <img class="wt-logo" src="img/wt-logo-bila.png" alt="WT - WINDOWS TOMORROW s.r.o.">
      <span class="wt-slogan">Tam, kde <b>světlo</b> potřebuje cestu.</span>
    </a>
  </div>
  <nav class="foot-nav" aria-label="Mapa webu">
""" + "\n".join(f'    <a href="{h}">{t}</a>' for h, t in FOOT_LINKS) + """
  </nav>
</footer>"""


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def faq_ld(items):
    return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in items]})


def product_ld(name, desc):
    return ld({"@context": "https://schema.org", "@type": "Product", "name": name,
               "brand": {"@type": "Brand", "name": "GLASSFLOOR"},
               "manufacturer": {"@type": "Organization", "name": "Heliobus AG",
                                "address": {"@type": "PostalAddress", "addressLocality": "St. Gallen", "addressCountry": "CH"}},
               "countryOfOrigin": "CH", "description": desc})


META = {
    "index.html": ("GLASSFLOOR® pochozí světlíky a prosklené podlahy na míru",
                   "GLASSFLOOR®: pochozí světlíky a prosklené podlahy ve standardních formátech i na míru. Čisté linie, bezprahové osazení, výroba ve St. Gallen, Švýcarsko."),
    "produkty.html": ("Pochozí světlíky GLASSFLOOR® · chrome, pure, circle",
                      "Přehled pochozích světlíků GLASSFLOOR: chrome s přiznaným rámem, pure s minimálním rámem, kruhový circle, požární FIRESTOP, větrání a výroba na míru."),
    "chrome.html": ("GLASSFLOOR chrome · pochozí světlík, nerezový rám 4 cm",
                    "GLASSFLOOR chrome: pochozí světlík s přiznaným nerezovým rámem 4 cm. Šest standardních rozměrů, výroba na míru od 40 cm. Heliobus AG, Švýcarsko."),
    "pure.html": ("GLASSFLOOR pure · pochozí světlík s rámem 0,5 cm", None),
    "circle.html": ("GLASSFLOOR circle · kruhový pochozí světlík 60 až 120 cm", None),
    "firestop.html": ("GLASSFLOOR FIRESTOP · požárně odolný pochozí světlík", None),
    "airflow-rwa.html": ("GLASSFLOOR AIRFLOW a RWA · pochozí světlík s větráním", None),
    "na-miru.html": ("Pochozí světlík na míru · GLASSFLOOR od 40 cm", None),
    "pro-architekty.html": ("Pochozí světlíky pro architekty · GLASSFLOOR® podklady", None),
    "reference.html": ("Reference pochozích světlíků GLASSFLOOR®", None),
    "ke-stazeni.html": ("Ke stažení · detaily pochozích světlíků GLASSFLOOR®",
                        "Technické detaily napojení pochozích světlíků GLASSFLOOR v PDF: vnější i vnitřní zateplení, fasáda, dělení skla. Produktové listy a zkušební doklady bez registrace."),
    "o-nas.html": ("O nás · GLASSFLOOR® a WT - WINDOWS TOMORROW", None),
    "kontakty.html": ("Kontakt · GLASSFLOOR® pro Českou republiku", None),
}
PTYPE = {"produkty.html": "CollectionPage", "o-nas.html": "AboutPage", "kontakty.html": "ContactPage"}
NAMES = {"index.html": "Úvod", "produkty.html": "Produkty", "chrome.html": "chrome", "pure.html": "pure", "circle.html": "circle",
         "firestop.html": "FIRESTOP", "airflow-rwa.html": "AIRFLOW a RWA", "na-miru.html": "Na míru a výbava",
         "pro-architekty.html": "Pro architekty", "reference.html": "Reference", "ke-stazeni.html": "Ke stažení",
         "o-nas.html": "O nás", "kontakty.html": "Kontakty"}
TRAIL = {f: ["index.html", "produkty.html"] for f in ("chrome.html", "pure.html", "circle.html", "firestop.html", "airflow-rwa.html", "na-miru.html")}
for _f in ("produkty.html", "pro-architekty.html", "reference.html", "ke-stazeni.html", "o-nas.html", "kontakty.html"):
    TRAIL[_f] = ["index.html"]

ORG_WT = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#wt",
          "name": "WT - WINDOWS TOMORROW s.r.o.", "alternateName": "WT WINDOWS TOMORROW",
          "description": "Oficiální zastoupení GLASSFLOOR pro Českou republiku, specialista na denní světlo v interiéru.",
          "telephone": "+420608918484", "email": "info@glassfloor.cz", "areaServed": "CZ",
          "address": {"@type": "PostalAddress", "addressLocality": "Horoměřice", "addressRegion": "Středočeský kraj", "addressCountry": "CZ"},
          "brand": {"@type": "Brand", "name": "GLASSFLOOR"}}
ORG_HELIOBUS = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#heliobus",
                "name": "Heliobus AG", "description": "Švýcarský výrobce systému GLASSFLOOR, vývoj a výroba ve St. Gallen.",
                "address": {"@type": "PostalAddress", "addressLocality": "St. Gallen", "addressCountry": "CH"},
                "brand": {"@type": "Brand", "name": "GLASSFLOOR"}}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#web", "name": "GLASSFLOOR",
           "url": BASE + "/", "inLanguage": "cs", "publisher": {"@id": BASE + "/#wt"}}

_opt_done = {}


def opt(path):
    """Velké JPG/PNG (nad 350 kB) nahradí webp kopií v img/opt (max. šířka 2000 px); originál zůstává."""
    if path in _opt_done:
        return _opt_done[path]
    res = path
    src = ROOT / path
    if path.startswith("img/") and path.lower().endswith((".jpg", ".jpeg", ".png")) and src.exists() and src.stat().st_size > 350000:
        out = ROOT / "img" / "opt" / (src.stem + ".webp")
        if not out.exists():
            out.parent.mkdir(exist_ok=True)
            im = Image.open(src)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            if im.width > 2000:
                im = im.resize((2000, round(im.height * 2000 / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=82, method=6)
        res = "img/opt/" + out.name
    _opt_done[path] = res
    return res


def process_images(html):
    html = re.sub(r'(srcset|src)="(img/[^"]+)"', lambda m: f'{m.group(1)}="{opt(m.group(2))}"', html)

    def fix(m):
        tag = m.group(0)
        sm = re.search(r'\ssrc="(img/[^"]+)"', tag)
        if not sm or sm.group(1).lower().endswith(".svg"):
            return tag
        f = ROOT / sm.group(1)
        extra = ""
        if " width=" not in tag and f.exists():
            w, h = Image.open(f).size
            extra += f' width="{w}" height="{h}"'
        if "decoding=" not in tag:
            extra += ' decoding="async"'
        if "loading=" not in tag and "hero-zumikon" not in tag:
            extra += ' loading="lazy"'
        if "hero-zumikon-169" in tag and "fetchpriority" not in tag:
            extra += ' fetchpriority="high"'
        return tag[:-1].rstrip("/").rstrip() + extra + ">"
    return re.sub(r"<img\b[^>]*>", fix, html)


def label_links(html):
    """Generické odkazy ('Stáhnout detail', 'Rozměry a provedení') dostanou popisný aria-label."""
    def art(m):
        a = m.group(0)
        h3 = re.search(r"<h3>(.*?)</h3>", a, re.S)
        if not h3:
            return a
        name = re.sub(r"<[^>]+>", "", h3.group(1)).replace("&ndash;", "-").strip()
        return re.sub(r'<a class="lnk"([^>]*)>(Stáhnout[^<]*)</a>', lambda k: f'<a class="lnk"{k.group(1)} aria-label="{k.group(2)}: {name}">{k.group(2)}</a>', a)
    html = re.sub(r'<article class="dl rv">.*?</article>', art, html, flags=re.S)
    for s in ("chrome", "pure", "circle"):
        html = html.replace(f'href="{s}.html">Rozměry a provedení</a>', f'href="{s}.html" aria-label="Rozměry a provedení řady {s}">Rozměry a provedení</a>')
    return html


def crumbs_html(fname):
    trail = TRAIL.get(fname)
    if not trail:
        return ""
    lis = "".join(f'<li><a href="{h}">{NAMES[h]}</a></li>' for h in trail)
    return f'<nav class="crumbs k" aria-label="Drobečková navigace"><ol>{lis}<li aria-current="page">{NAMES[fname]}</li></ol></nav>'


def breadcrumb_ld(fname):
    trail = TRAIL.get(fname)
    if not trail:
        return ""
    items = [(NAMES[h], h) for h in trail] + [(NAMES[fname], fname)]
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + ("" if h == "index.html" else h)}
        for i, (n, h) in enumerate(items)]})


def page(fname, title, desc, active, body, jsonld="", extra_style="", og_title=None, head_extra=""):
    mt, md = META.get(fname, (None, None))
    title = mt or title
    desc = md or desc
    og_title = og_title or title
    url = BASE + "/" + ("" if fname == "index.html" else fname)
    ogimg = BASE + "/img/hero-zumikon-169.jpg"
    body = body.replace("%%CRUMBS%%", crumbs_html(fname))
    web = ld({"@context": "https://schema.org", "@type": PTYPE.get(fname, "WebPage"), "name": title, "description": desc,
              "url": url, "inLanguage": "cs", "dateModified": DATE,
              "isPartOf": {"@id": BASE + "/#web"}, "primaryImageOfPage": {"@type": "ImageObject", "url": ogimg}})
    extra_ld = ""
    if fname == "index.html":
        extra_ld = "\n".join(ld(o) for o in (WEBSITE, ORG_WT, ORG_HELIOBUS))
    elif fname in ("kontakty.html", "o-nas.html"):
        extra_ld = ld(ORG_WT) + "\n" + ld(ORG_HELIOBUS)
    style = f"<style>\n{extra_style}\n</style>\n" if extra_style.strip() else ""
    html = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1a242c">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="cs" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="GLASSFLOOR">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="cs_CZ">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:alt" content="Pochozí světlíky GLASSFLOOR zapuštěné v rovině terasy u vily v Zumikonu, Švýcarsko">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimg}">
{head_extra}
{web}
{breadcrumb_ld(fname)}
{extra_ld}
{jsonld}
<link rel="stylesheet" href="css/glassfloor.css">
{style}</head>
<body>
<a class="skip" href="#obsah">Přeskočit na obsah</a>

{header(active)}

<main id="obsah">
{body}
</main>

{FOOTER}

{DIALOG}

<script src="js/glassfloor.js"></script>
<script src="js/editace-textu.js"></script>
</body>
</html>
"""
    html = label_links(process_images(html))
    (ROOT / fname).write_text(html, encoding="utf-8", newline="\n")
    print("zapsáno", fname, round(len(html) / 1024, 1), "kB")


def subnav(current):
    items = [("chrome.html", "chrome"), ("pure.html", "pure"), ("circle.html", "circle"), ("firestop.html", "FIRESTOP"),
             ("airflow-rwa.html", "AIRFLOW a RWA"), ("na-miru.html", "Na míru a výbava")]
    lis = []
    for h, t in items:
        cur = ' aria-current="page"' if h == current else ""
        lis.append(f'<li><a href="{h}"{cur}>{t}</a></li>')
    return '<nav class="subnav" aria-label="Produktové řady a varianty"><ul>' + "".join(lis) + "</ul></nav>"


def page_head(crumb_href, crumb_text, kicker, h1, lead, nav=""):
    return f"""<section class="page-head">
  <div class="wrap rv">
    %%CRUMBS%%
    <span class="k kicker">{kicker}</span>
    <h1 class="h1">{h1}</h1>
    <p class="lead">{lead}</p>
    {nav}
  </div>
</section>"""


def faq_section(h2, items):
    qs = "\n".join(f'      <div class="q"><h3>{q}</h3><p>{a}</p></div>' for q, a in items)
    return f"""<section class="prod faq">
  <div class="wrap g">
    <div class="c4 rv">
      <span class="meta-l">Časté otázky</span>
      <h2 class="h2" style="margin-top:10px">{h2}</h2>
    </div>
    <div class="c8 faq-list rv">
{qs}
    </div>
  </div>
</section>"""


def final_cta(h2, p):
    return f"""<section class="final tint" id="kontakt">
  <div class="wrap rv">
    <span class="k kicker">Začátek spolupráce</span>
    <h2 class="h2">{h2}</h2>
    <p>{p}</p>
    <button class="cta" onclick="document.getElementById('dlg').showModal()">Zahájit konzultaci</button>
    <p class="assess">Údaje o rozměrech, doplňcích a požární odolnosti vycházejí z podkladů výrobce Heliobus AG platných k 1. 9. 2026. Závazné jsou vždy podklady ke konkrétní zakázce.</p>
  </div>
</section>"""


PRICE_Q = ("Kolik GLASSFLOOR stojí?",
           "GLASSFLOOR je zakázkové řešení bez ceníku, cena vychází z technického návrhu konkrétního kusu. U menších standardních formátů začíná kolem 100 000 Kč.")

# ---------------------------------------------------------------- ÚVODNÍ STRÁNKA
hero = pick(BARVA, 'class="hero"').replace('<a class="lnk" href="#projekty">Vybrané projekty</a>',
                                           '<a class="lnk" href="reference.html">Vybrané projekty</a>')
manifest = pick(BARVA, 'class="manifesto"')
principle = pick(BARVA, 'id="system"')
rady = pick(BARVA, 'id="rady"')
for s in ("chrome", "pure", "circle"):
    rady = rady.replace(f"produkty.html#{s}", f"{s}.html")
rady = rady.replace(
    "Každá řada existuje i v požárně odolném provedení FIRESTOP a ve variantách s větráním (AIRFLOW) nebo odvodem kouře (RWA). Mimo standardní řadu vyrábíme na míru od 40 cm.",
    'Každá řada existuje i v požárně odolném provedení <a class="lnk" href="firestop.html">FIRESTOP</a> a ve variantách s větráním (<a class="lnk" href="airflow-rwa.html">AIRFLOW</a>) nebo odvodem kouře (<a class="lnk" href="airflow-rwa.html">RWA</a>). Mimo standardní řadu <a class="lnk" href="na-miru.html">vyrábíme na míru</a> od 40 cm.')
projekt1 = pick(BARVA, 'id="projekty"').replace(
    '    </div>\n  </div>\n</section>',
    '    </div>\n    <p class="tm-note rv">Další stavby a celou galerii najdete na stránce <a class="lnk" href="reference.html">Reference</a>.</p>\n  </div>\n</section>')
brk = pick(BARVA, 'class="break"')
final_home = pick(BARVA, 'id="kontakt"')

hub = """<section class="xl hub-sec">
  <div class="wrap">
    <div class="sec-head g rv">
      <div class="c7">
        <span class="k kicker">Kam dál</span>
        <h2 class="h2">Podle toho, co potřebujete.</h2>
      </div>
      <p class="lead c5">Web je rozdělený podle otázek, které si u pochozího prosklení kladou architekti, projektanti i investoři.</p>
    </div>
    <div class="hub-grid g rv">
      <a class="hub" href="pro-architekty.html">
        <span class="meta-l">01</span>
        <h3>Pro architekty a projektanty</h3>
        <p>Technická data, výrobní detaily, podklady k projektu a otevřeně o tom, kdy GLASSFLOOR doporučit nebudeme.</p>
        <span class="lnk">Otevřít</span>
      </a>
      <a class="hub" href="reference.html">
        <span class="meta-l">02</span>
        <h3>Reference</h3>
        <p>Vila v Zumikonu, bazén u Tegernsee, administrativní budova a další realizace ze Švýcarska.</p>
        <span class="lnk">Zobrazit realizace</span>
      </a>
      <a class="hub" href="o-nas.html">
        <span class="meta-l">03</span>
        <h3>Výroba a lidé</h3>
        <p>Kdo GLASSFLOOR vyvíjí ve St. Gallen, kdo ho dodává v České republice a jak vzniká každý kus.</p>
        <span class="lnk">O nás</span>
      </a>
    </div>
  </div>
</section>"""

idx_style = """  .hero-photo img{object-position:center 45%}
  .hero .eyebrow .e-rule{margin-top:0}
  @media(max-width:900px){.hero-photo img{object-position:center center}}
  .hero-copy{padding-top:clamp(96px,8vw,140px) !important}
  @media(max-width:900px){.hero-copy{padding-top:clamp(88px,14vw,112px) !important}}"""

HOME_FAQ = [
    ("Co je GLASSFLOOR?", "GLASSFLOOR je zakázkově vyráběný pochozí světlík švýcarského výrobce Heliobus AG. Nosné prosklení slouží jako běžně pochozí část terasy, střechy nebo podlahy a přivádí denní světlo do podlaží pod ní."),
    ("Kdo GLASSFLOOR vyrábí a kdo ho dodává v České republice?", "Vývoj, konstrukce a kompletace každého kusu probíhají ve výrobě Heliobus AG ve švýcarském St. Gallen. V České republice systém GLASSFLOOR dodává společnost WT - WINDOWS TOMORROW s.r.o., specialista na denní světlo v interiéru."),
    ("Jaké rozměry se vyrábějí?", "Řady chrome a pure standardně v šesti formátech otvoru od 80 × 80 do 250 × 80 cm, řada circle ve čtyřech průměrech 60 až 120 cm. Na míru se vyrábí od 40 cm bez horní hranice."),
    ("Jaké zatížení pochozí zasklení snese?", "Užitné zatížení je 5,0 kN/m², třída odolnosti P8B. Vyšší únosnost včetně pojezdu se navrhuje zakázkově."),
    ("Hodí se GLASSFLOOR i do interiéru nebo jako požární strop?", "Ano. Řada pure se používá i v podlahách obytných prostor a varianta FIRESTOP plní funkci požárně dělicí konstrukce s odolností REI 30 až REI 120."),
    PRICE_Q,
    ("Jak dlouho trvá dodání?", "Každý kus jde do výroby až po odsouhlaseném návrhu a vyrábí se ve Švýcarsku. Mezi zadáním a osazením počítejte s několika týdny."),
    ("Jak spolupráce začíná?", "Pošlete základní výkres, řez nebo popis záměru. Nejprve posoudíme, zda je GLASSFLOOR pro danou konstrukci a architektonický záměr vhodným řešením, a navrhneme další technický postup."),
]
home_ld = re.findall(r'<script type="application/ld\+json">.*?</script>', BARVA, re.S)[0] + "\n" + faq_ld(HOME_FAQ)

vkostce = """<section class="xl vkostce" id="v-kostce">
  <div class="wrap g">
    <div class="c5 rv">
      <span class="k kicker">GLASSFLOOR v kostce</span>
      <h2 class="h2">Co je pochozí světlík GLASSFLOOR.</h2>
      <p class="lead">GLASSFLOOR je pochozí světlík a prosklená podlaha švýcarského výrobce Heliobus AG ze St. Gallen. Nosné zasklení v nerezovém rámu slouží jako běžně pochozí plocha terasy, střechy nebo podlahy a přivádí denní světlo do podlaží pod ní. V České republice ho dodává WT - WINDOWS TOMORROW s.r.o.</p>
    </div>
    <dl class="meta c7 rv">
      <div class="r"><span class="meta-l">Řady</span><b>chrome (rám 4 cm), pure (rám 0,5 cm), circle (kruh, rám 0,3 cm)</b></div>
      <div class="r"><span class="meta-l">Varianty</span><b>FIRESTOP REI 30 až 120, AIRFLOW (větrání), RWA (odvod kouře)</b></div>
      <div class="r"><span class="meta-l">Rozměry</span><b>standardní formáty, na míru od 40 cm bez horní hranice</b></div>
      <div class="r"><span class="meta-l">Zasklení</span><b>vrstvené bezpečnostní sklo, U<sub>g</sub> 1,1 až 0,5 W/m²K, propustnost světla 73 až 88 %</b></div>
      <div class="r"><span class="meta-l">Zatížení</span><b>5,0 kN/m², třída odolnosti P8B</b></div>
      <div class="r"><span class="meta-l">Původ</span><b>Swiss made, Heliobus AG, St. Gallen</b></div>
      <div class="r"><span class="meta-l">Cena a dodání</span><b>bez ceníku, menší standardní formáty od cca 100 000 Kč, dodání v řádu týdnů</b></div>
    </dl>
  </div>
</section>"""
page("index.html",
     "GLASSFLOOR® pochozí světlíky a prosklené podlahy na míru",
     "GLASSFLOOR® by Heliobus AG: pochozí světlíky a prosklené podlahy ve standardních formátech i na míru. Čisté linie, bezprahové osazení, výroba ve St. Gallen ve Švýcarsku.",
     None,
     "\n\n".join([hero, manifest, vkostce, principle, rady, projekt1, brk, hub, faq_section("Nejčastější otázky o pochozích světlících.", HOME_FAQ), final_home]),
     jsonld=home_ld, extra_style=idx_style,
     head_extra=f'<link rel="preload" as="image" href="{opt("img/hero-zumikon-169.jpg")}" media="(min-width:901px)" fetchpriority="high">\n<link rel="preload" as="image" href="{opt("img/hero-zumikon-mobil.jpg")}" media="(max-width:900px)">',
     og_title="GLASSFLOOR® · pochozí prosklení na míru · by Heliobus AG")

# ---------------------------------------------------------------- PRODUKTY: rozcestník
rady_grid = re.search(r'<div class="rady-grid g rv">.*?</div>\s*</div>\s*<p class="tm-note', rady, re.S)
# jednodušší a spolehlivější: vezmeme celý blok od rady-grid po konec posledního .rada
start = rady.index('<div class="rady-grid g rv">')
end = rady.index('<p class="tm-note')
rady_grid_html = rady[start:end].rstrip()

varianty = """<div class="rady-grid g rv">

      <div class="c4 rada">
        <figure><img src="img/firestop-pozarni-test.jpg" alt="Kruhový světlík FIRESTOP při požární zkoušce, pod sklem hoří oheň" loading="lazy" style="object-position:50% 100%"></figure>
        <span class="meta-l rada-n">Požární varianta</span>
        <h3>GLASSFLOOR <em>FIRESTOP</em></h3>
        <p>Pochozí světlík, který zároveň plní funkci požárně dělicí konstrukce. Ve školách, nemocnicích a komerčních budovách.</p>
        <ul class="rada-fakta">
          <li><span>Odolnost</span>REI 30 až REI 120</li>
          <li><span>Provedení</span>chrome, pure, circle</li>
        </ul>
        <a class="lnk" href="firestop.html">Požární odolnost a podklady</a>
      </div>

      <div class="c4 rada">
        <figure><img src="img/varianta-airflow.webp" alt="Vizualizace GLASSFLOOR AIRFLOW: rám s vodorovnými klapkami a znázorněným prouděním vzduchu" loading="lazy"></figure>
        <span class="meta-l rada-n">Větrání a odvod kouře</span>
        <h3>GLASSFLOOR <em>AIRFLOW</em> a <em>RWA</em></h3>
        <p>Světlík, který kromě světla přivádí čerstvý vzduch, nebo se otevře pro odvod kouře a tepla při požáru.</p>
        <ul class="rada-fakta">
          <li><span>AIRFLOW</span>větrání klapkami</li>
          <li><span>RWA</span>otevření až o 60 °</li>
        </ul>
        <a class="lnk" href="airflow-rwa.html">Obě varianty podrobně</a>
      </div>

      <div class="c4 rada">
        <figure><img src="img/zahrada-svetliky-chodnik.jpg" alt="Osazení světlíků na míru v rovině kamene mezi buxusy" loading="lazy"></figure>
        <span class="meta-l rada-n">Mimo standardní řadu</span>
        <h3>Na míru a <em>výbava</em></h3>
        <p>Vlastní rozměr, tvar i únosnost. K tomu výbava podle situace na stavbě: vyhřívání, soukromí, osvětlení, protiskluz.</p>
        <ul class="rada-fakta">
          <li><span>Rozměr</span>od 40 cm bez horní hranice</li>
          <li><span>Výbava</span>devět situací z praxe</li>
        </ul>
        <a class="lnk" href="na-miru.html">Co se dá změnit</a>
      </div>

    </div>"""

spolecne = pick(PROD, "Liší se rám, ne konstrukce").replace(
    '<a href="#vybava">Co se k čemu hodí</a>', '<a href="na-miru.html#vybava">Co se k čemu hodí</a>')

prod_body = page_head("index.html", "Zpět na úvod", "Produkty", "Pochozí světlíky: tři řady, jedna konstrukce.",
                      "Každý GLASSFLOOR je nosné izolační zasklení v nerezovém rámu, osazené v jedné rovině s okolním povrchem. Řady se liší tvarem a tím, kolik rámu po dokončení zůstane vidět. Konstrukce, nosnost i způsob osazení jsou u všech tří stejné.")
prod_body += f"""

<section class="prod">
  <div class="wrap">
    <span class="meta-l rv">Tři základní řady</span>
    <h2 class="h2 rv" style="margin:10px 0 clamp(24px,3vw,40px)">Vyberte podle tvaru a rámu.</h2>
    {rady_grid_html}
  </div>
</section>

{spolecne}

<section class="prod">
  <div class="wrap">
    <span class="meta-l rv">Varianty a výbava</span>
    <h2 class="h2 rv" style="margin:10px 0 clamp(24px,3vw,40px)">Když stavba potřebuje víc.</h2>
    {varianty}
  </div>
</section>

{final_cta("Nevíte, která řada se hodí?", "Napište nám, co stavíte. Podle konstrukce a záměru doporučíme řadu, rozměr i způsob osazení.")}"""
page("produkty.html",
     "Pochozí světlíky GLASSFLOOR® · řady chrome, pure, circle a varianty",
     "Přehled produktů GLASSFLOOR: chrome s přiznaným nerezovým rámem, pure s minimálním rámem a kruhový circle. Požární FIRESTOP, větrací AIRFLOW, RWA a výroba na míru.",
     "produkty", prod_body)

# ---------------------------------------------------------------- ŘADY: chrome, pure, circle
def dl_articles(prefix):
    arts = re.findall(r'<article class="dl rv">.*?</article>', KST, re.S)
    return [a for a in arts if f"<h3>{prefix} &ndash;" in a]


COMMON_TECH = [
    ("Nosné sklo", "vrstvené bezpečnostní (VSG), extra čiré"),
    ("Tepelná izolace", "U<sub>g</sub> 1,1 W/m²K, s trojsklem Super ISO 0,5 W/m²K"),
    ("Propustnost světla", "73 až 88 % podle zasklení"),
    ("Zvuková izolace", "R<sub>w</sub> ≥ 40 dB"),
    ("Užitné zatížení", "5,0 kN/m², třída odolnosti P8B"),
    ("Výška rámu", "12 cm"),
    ("Osazení", "bezprahové, v rovině okolního povrchu, doporučený spád min. 1,5 %"),
    ("Původ", "Swiss made, Heliobus AG, St. Gallen"),
]

SIZES_RECT = ["80 × 80", "100 × 100", "120 × 80", "120 × 120", "200 × 50", "250 × 80"]
TAB_CHROME = [("80 × 80", "72 × 72", "96 × 96"), ("100 × 100", "92 × 92", "116 × 116"), ("120 × 80", "112 × 72", "136 × 96"),
              ("120 × 120", "112 × 112", "136 × 136"), ("200 × 50", "192 × 42", "216 × 66"), ("250 × 80", "242 × 72", "266 × 96")]
TAB_PURE = [("80 × 80", "72 × 72", "89 × 89"), ("100 × 100", "92 × 92", "109 × 109"), ("120 × 80", "112 × 72", "129 × 89"),
            ("120 × 120", "112 × 112", "129 × 129"), ("200 × 50", "192 × 42", "209 × 59"), ("250 × 80", "242 × 72", "259 × 89")]
TAB_CIRCLE = [("⌀ 60", "⌀ 52", "⌀ 68"), ("⌀ 80", "⌀ 72", "⌀ 88"), ("⌀ 100", "⌀ 92", "⌀ 108"), ("⌀ 120", "⌀ 112", "⌀ 128")]

RADY = {
    "chrome": dict(
        num="01", title="GLASSFLOOR chrome · pochozí světlík s nerezovým rámem 4 cm",
        desc="GLASSFLOOR chrome: pochozí světlík a prosklená podlaha s přiznaným nerezovým rámem 4 cm. Šest standardních rozměrů, výroba na míru od 40 cm. Heliobus AG, Švýcarsko.",
        h1='GLASSFLOOR <em>chrome</em>',
        lead="Nerezový rám široký 4 cm zůstává po osazení přiznaný. Působí masivně, dobře drží tvar i u větších formátů a snese pravidelný provoz na terase i ve veřejné budově.",
        photo="img/terasa-drevo-ctverec.jpg", alt="Čtvercový pochozí světlík s přiznaným nerezovým rámem v dřevěné terase", cap="Čtvercový formát v dřevěné terase", pos="",
        facts=[("Tvar", "čtverec a obdélník"), ("Rám", "nerez, šířka 4 cm")],
        chips=SIZES_RECT, mimo="Jiný rozměr vyrobíme na zakázku, od 40 cm bez horní hranice.",
        tab=TAB_CHROME, rame="nerez 1.4301, tepelně oddělený, viditelná šířka 4 cm",
        tab_intro="Tři čísla ke každému formátu: otvor, který se vynechá v konstrukci, výsledná prosklená plocha a vnější rozměr rámu.",
        faq=[("Jak široký je rám řady chrome?", "Nerezový rám je po osazení viditelný v šířce 4 cm, jeho výška je 12 cm. Rám zůstává přiznaný a dává světlíku výrazný obrys."),
             ("Jaké rozměry řada chrome nabízí?", "Standardně šest formátů otvoru: 80 × 80, 100 × 100, 120 × 80, 120 × 120, 200 × 50 a 250 × 80 cm. Jiný rozměr se vyrábí na zakázku od 40 cm bez horní hranice."),
             ("Kam se chrome hodí?", "Na terasy, střechy i do podlah uvnitř budov, kde nevadí přiznaný rám a kde se počítá s pravidelným provozem, včetně veřejných staveb. Užitné zatížení je 5,0 kN/m², třída odolnosti P8B."),
             ("Dá se chrome osadit těsně u fasády?", "Ano. Pro řadu chrome je zpracovaný samostatný detail napojení na fasádu včetně klempířského detailu, k dispozici ke stažení."),
             PRICE_Q]),
    "pure": dict(
        num="02", title="GLASSFLOOR pure · pochozí světlík s minimálním rámem 0,5 cm",
        desc="GLASSFLOOR pure: pochozí světlík s velmi úzkým nerezovým rámem 0,5 cm, téměř jen skleněná plocha v podlaze. Šest standardních rozměrů, výroba na míru od 40 cm.",
        h1='GLASSFLOOR <em>pure</em>',
        lead="Velmi úzký obvodový rám. Ze světlíku zůstane po dokončení hlavně skleněná plocha, přechod do dlažby nebo dřeva je nenápadný. Volba pro místa, kde má architektura zůstat klidná.",
        photo="img/interier-pure-jidelna.jpg", alt="Interiér se světlíkem GLASSFLOOR pure v podlaze", cap="Pure v podlaze obytného prostoru", pos="object-position:center 78%",
        facts=[("Tvar", "čtverec a obdélník"), ("Rám", "nerez, šířka 0,5 cm")],
        chips=SIZES_RECT, mimo="Stejné pravidlo jako u chrome: na zakázku od 40 cm.",
        tab=TAB_PURE, rame="nerez 1.4301, viditelná šířka 0,5 cm",
        tab_intro="Tři čísla ke každému formátu: otvor, který se vynechá v konstrukci, výsledná prosklená plocha a vnější rozměr rámu.",
        faq=[("Čím se pure liší od chrome?", "Konstrukce, zasklení i nosnost jsou stejné. Liší se šířkou viditelného rámu: u pure je to 0,5 cm, u chrome 4 cm. Pure působí jako čistá skleněná plocha v podlaze."),
             ("Jaké rozměry řada pure nabízí?", "Standardně šest formátů otvoru: 80 × 80, 100 × 100, 120 × 80, 120 × 120, 200 × 50 a 250 × 80 cm. Jiný rozměr se vyrábí na zakázku od 40 cm bez horní hranice."),
             ("Hodí se pure i do interiéru?", "Ano. Řada se používá na terasách i v podlahách obytných prostor, kde má denní světlo pokračovat o podlaží níž a rám nemá rušit architekturu."),
             PRICE_Q]),
    "circle": dict(
        num="03", title="GLASSFLOOR circle · kruhový pochozí světlík, průměr 60 až 120 cm",
        desc="GLASSFLOOR circle: kruhový pochozí světlík s rámem 0,3 cm. Čtyři standardní průměry 60 až 120 cm, výroba na míru od průměru 40 cm. Heliobus AG, Švýcarsko.",
        h1='GLASSFLOOR <em>circle</em>',
        lead="Kruh tvoří protiváhu pravoúhlé stavbě, nebo naopak doplňuje organickou architekturu. Používá se i tam, kde má světlo dopadnout do jednoho konkrétního místa pod terénem.",
        photo="img/terasa-kruhovy-svetlik.jpg", alt="Kruhový pochozí světlík v travertinové terase s výhledem do krajiny", cap="Kruhový formát v travertinové terase", pos="",
        facts=[("Tvar", "kruh"), ("Rám", "nerez, šířka 0,3 cm")],
        chips=["⌀ 60", "⌀ 80", "⌀ 100", "⌀ 120"], mimo="I kruh vyrobíme na zakázku, od průměru 40 cm.",
        tab=TAB_CIRCLE, rame="nerez 1.4301, viditelná šířka 0,3 cm",
        tab_intro="Tři čísla ke každému průměru: otvor, který se vynechá v konstrukci, výsledná prosklená plocha a vnější průměr rámu.",
        faq=[("Jaké průměry řada circle nabízí?", "Standardně čtyři průměry otvoru: 60, 80, 100 a 120 cm. Jiný průměr se vyrábí na zakázku od 40 cm."),
             ("Jak široký je rám u řady circle?", "Viditelná šířka nerezového rámu je jen 0,3 cm, výška rámu 12 cm. Ze světlíku zůstává především kruh skla."),
             ("Kdy zvolit kruhový světlík?", "Kruh vynikne jako protiváha pravoúhlé stavbě, nebo naopak doplní organickou architekturu. Hodí se také tam, kde má světlo dopadnout do jednoho konkrétního místa pod terénem."),
             PRICE_Q]),
}
ORDER = ["chrome", "pure", "circle"]

for slug in ORDER:
    d = RADY[slug]
    chips = "\n".join(f"            <li>{c}</li>" for c in d["chips"])
    facts = "\n".join(f"        <li><span>{a}</span>{b}</li>" for a, b in d["facts"])
    rows = "\n".join(f"            <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in d["tab"])
    tech = "\n".join(f"        <li><b>{a}:</b> {b}</li>" for a, b in COMMON_TECH[:5] + [("Rám", d["rame"])] + COMMON_TECH[5:])
    arts = "\n\n".join(dl_articles(slug))
    others = [o for o in ORDER if o != slug]
    style_img = f' style="{d["pos"]}"' if d["pos"] else ""
    body = page_head("produkty.html", "Všechny produkty", f"Řada {d['num']}", d["h1"], d["lead"], subnav(f"{slug}.html"))
    body += f"""

<section class="prod rada-blok">
  <div class="wrap g">
    <figure class="rada-foto rv">
      <img src="{d['photo']}" alt="{d['alt']}"{style_img}>
      <figcaption>{d['cap']}</figcaption>
    </figure>
    <div class="rada-text rv">
      <span class="meta-l">Základní údaje</span>
      <ul class="rada-fakta2">
{facts}
      </ul>
      <div class="rada-rozmery">
        <span class="meta-l">Typizované rozměry otvoru (cm)</span>
        <ul class="chipy">
{chips}
        </ul>
        <p class="mimo">{d['mimo']}</p>
      </div>
      <a class="lnk" href="#rozmery">Světlá plocha a vnější rozměry rámu</a>
    </div>
  </div>
</section>

<section class="prod" id="rozmery">
  <div class="wrap g">
    <div class="c6 rv">
      <span class="meta-l">Pro projekt</span>
      <h2 class="h2" style="margin:10px 0 clamp(16px,2vw,24px)">Rozměry do detailu.</h2>
      <p style="max-width:56ch;font-weight:260;color:#dde5ea">{d['tab_intro']} Výška rámu je 12 cm.</p>
      <div class="tab-wrap">
        <table class="tab-rozmery">
          <caption>Rozměry v centimetrech</caption>
          <thead><tr><th>Otvor ve stropě</th><th>Světlá plocha</th><th>Vnější rám</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p class="zdroj">Mimo tyto formáty vyrábíme na zakázku od 40 cm, bez horní hranice. Údaje vycházejí z produktových listů Heliobus AG.</p>
    </div>
    <div class="c6 rv">
      <span class="meta-l">Technické údaje</span>
      <ul class="doplnky">
{tech}
      </ul>
      <p class="zdroj">Posouzeno zkouškami Fraunhofer IBP Stuttgart a osvědčením IFT podle DIN 18008-5. Pro projekci platí výrobní dokumentace ke konkrétnímu kusu.</p>
    </div>
  </div>
</section>

<section class="prod tint" id="napojeni">
  <div class="wrap">
    <div class="sec-head g rv">
      <div class="c7">
        <span class="meta-l">Podklady ke stažení</span>
        <h2 class="h2">Napojení na konstrukci.</h2>
      </div>
      <p class="lead c5">Řezy pro řadu {slug} podle toho, kde leží tepelná izolace. Volně ke stažení, bez registrace. <a class="lnk" href="ke-stazeni.html">Všechny podklady</a></p>
    </div>
    <div class="dl-grid">

{arts}

    </div>
  </div>
</section>

{faq_section("Co lidé u řady " + slug + " zjišťují.", d["faq"])}

<section class="prod">
  <div class="wrap">
    <span class="meta-l rv">Další řady</span>
    <ul class="dalsi rv">
      <li><a href="{others[0]}.html">GLASSFLOOR <em>{others[0]}</em></a></li>
      <li><a href="{others[1]}.html">GLASSFLOOR <em>{others[1]}</em></a></li>
      <li><a href="firestop.html">Požární varianta FIRESTOP</a></li>
      <li><a href="na-miru.html">Na míru a výbava</a></li>
    </ul>
  </div>
</section>

{final_cta("Chcete řadu " + slug + " do svého projektu?", "Pošlete nám řez nebo základní výkres. Posoudíme, zda řada sedí na vaši konstrukci, a doporučíme rozměr i způsob osazení.")}"""
    page(f"{slug}.html", d["title"], d["desc"], "produkty", body,
         jsonld=product_ld(f"GLASSFLOOR {slug}", d["desc"]) + "\n" + faq_ld(d["faq"]))

# ---------------------------------------------------------------- FIRESTOP
fire = pick(PROD, 'id="firestop"').replace('<h2 class="h2" style="margin:10px 0 clamp(16px,2vw,24px)">FIRESTOP</h2>',
                                           '<h2 class="h2" style="margin:10px 0 clamp(16px,2vw,24px)">Požární odolnost REI 30 až REI 120</h2>')
fire_faq = [
    ("Co je GLASSFLOOR FIRESTOP?", "Pochozí světlík, který zároveň plní funkci požárně dělicí konstrukce. Podle výrobce jde o první schválené a certifikované řešení pochozího protipožárního zasklení v Evropě."),
    ("Jakou požární odolnost FIRESTOP má?", "REI 30 až REI 120, nejvyšší třída je REI 120-RF1. Zkoušky proběhly podle EN 1363-1 a EN 1365-2, certifikace VKF platí ve Švýcarsku."),
    ("V jakých řadách se FIRESTOP vyrábí?", "Jako FIRESTOP chrome, FIRESTOP pure i FIRESTOP circle. Rozměry jsou standardní i zakázkové, podle skladby stropu."),
    ("Kde se FIRESTOP používá?", "Ve školách, nemocnicích a komerčních budovách, tedy tam, kde strop mezi podlažími musí požáru odolat a přitom má propouštět denní světlo."),
]
fire_body = page_head("produkty.html", "Všechny produkty", "Požární varianta",
                      "FIRESTOP: pochozí světlík jako požárně dělicí konstrukce.",
                      "Světlo mezi podlažími a požární odolnost stropu už nejsou protiklady. FIRESTOP je k dispozici ve všech třech řadách, v odolnosti od REI 30 do REI 120.",
                      subnav("firestop.html"))
fire_body += f"""

{fire}

<section class="prod">
  <div class="wrap g">
    <figure class="c8 f2 rv">
      <img src="img/firestop-interier.jpg" alt="Pohled z interiéru na světlík GLASSFLOOR FIRESTOP, na skle silueta došlapu chodce" loading="lazy">
      <figcaption class="cap">GLASSFLOOR FIRESTOP z interiéru, nad stropem běžně pochozí plocha</figcaption>
    </figure>
    <div class="c4 rv" style="align-self:end">
      <span class="meta-l">Řady a rozměry</span>
      <ul class="doplnky">
        <li><a href="chrome.html"><b>FIRESTOP chrome</b></a>, přiznaný nerezový rám 4 cm</li>
        <li><a href="pure.html"><b>FIRESTOP pure</b></a>, minimální rám 0,5 cm</li>
        <li><a href="circle.html"><b>FIRESTOP circle</b></a>, kruh, rám 0,3 cm</li>
      </ul>
    </div>
  </div>
</section>

{faq_section("Co lidé u FIRESTOPU zjišťují.", fire_faq)}

{final_cta("Potřebujete světlo skrz požární strop?", "Pošlete nám řez stropní konstrukce a požadovanou třídu odolnosti. Posoudíme, jak FIRESTOP do skladby zapojit.")}"""
page("firestop.html", "GLASSFLOOR FIRESTOP · požárně odolný pochozí světlík REI 30 až 120",
     "GLASSFLOOR FIRESTOP: pochozí světlík, který plní funkci požárně dělicí konstrukce. Odolnost REI 30 až REI 120, certifikace VKF, provedení chrome, pure i circle.",
     "produkty", fire_body, jsonld=product_ld("GLASSFLOOR FIRESTOP", "Požárně odolný pochozí světlík REI 30 až REI 120.") + "\n" + faq_ld(fire_faq))

# ---------------------------------------------------------------- AIRFLOW a RWA
air = pick(PROD, 'id="airflow"')
air_faq = [
    ("Co je GLASSFLOOR AIRFLOW?", "Patentovaná varianta, která kromě světla přivádí do místnosti i čerstvý vzduch. Zasklení zůstává pevné a větrá se vodorovně vloženými klapkami s dálkovým ovládáním, konstrukce je řešená tak, aby při větrání nezatékalo."),
    ("K čemu slouží AIRFLOW?", "K trvalému větrání a nočnímu ochlazování prostoru pod terasou. Větrat lze jednostranně nebo oboustranně."),
    ("Co je GLASSFLOOR RWA?", "Podle výrobce první vodorovně otevíravý pochozí světlík svého druhu. Zasklení se otevře až o 60 stupňů a slouží k odvodu kouře a tepla při požáru, v běžném provozu k větrání a nočnímu ochlazování."),
    ("V jakých rámech se RWA vyrábí?", "V řadách chrome i pure."),
]
air_body = page_head("produkty.html", "Všechny produkty", "Větrání a odvod kouře",
                     "AIRFLOW a RWA: pochozí světlík, který větrá.",
                     "Světlo shora lze doplnit o čerstvý vzduch nebo o odvod kouře a tepla při požáru. Dvě varianty, které vycházejí z řad chrome a pure.",
                     subnav("airflow-rwa.html"))
air_body += f"""

{air}

{faq_section("Co lidé u větrání zjišťují.", air_faq)}

{final_cta("Má pod světlíkem proudit vzduch?", "Napište nám, jaký prostor je pod terasou. Doporučíme, zda se hodí AIRFLOW, RWA, nebo pevné zasklení.")}"""
page("airflow-rwa.html", "GLASSFLOOR AIRFLOW a RWA · pochozí světlík s větráním a odvodem kouře",
     "GLASSFLOOR AIRFLOW větrá vodorovnými klapkami, GLASSFLOOR RWA se otevře o 60 stupňů a odvede kouř a teplo. Pochozí světlíky v řadách chrome a pure.",
     "produkty", air_body, jsonld=faq_ld(air_faq))

# ---------------------------------------------------------------- NA MÍRU a výbava
miru = pick(PROD, 'id="na-miru"')
vybava = pick(PROD, 'id="vybava"')
miru_faq = [
    ("Jaký nejmenší rozměr se dá vyrobit na míru?", "Od 40 cm, bez horní hranice. Čtverec, obdélník i kruh."),
    ("Dá se kus vyrobit na hotový otvor?", "Ano. GLASSFLOOR umí vyrobit kus přesně na hotový otvor. Rozhoduje skladba konstrukce, způsob napojení a zatížení, ne katalog."),
    ("Jaké doplňky se k pochozímu světlíku nabízejí?", "Izolační trojsklo, systémový izolační rám, protiskluzová úprava, PRIVA-LITE, vyhřívané sklo se senzory, protisluneční sklo, LED osvětlení, pojezdové a poplachové sklo. Co dává smysl u vaší stavby, řekneme po prohlédnutí řezu."),
    PRICE_Q,
]
miru_body = page_head("produkty.html", "Všechny produkty", "Mimo standardní řadu",
                      "Pochozí světlík na míru a výbava podle situace.",
                      "Standardní rozměry pokrývají běžné případy. Když se do nich stavba nevejde, vyrobíme kus podle ní. A výbavu nevybíráme z ceníku, ale podle toho, co se pod sklem a nad ním děje.",
                      subnav("na-miru.html"))
miru_body += f"""

{miru}

{vybava}

{faq_section("Co lidé u zakázek zjišťují.", miru_faq)}

{final_cta("Máte stavbu, která se do katalogu nevejde?", "Pošlete nám řez nebo půdorys. Nejprve posoudíme, zda je GLASSFLOOR pro konstrukci vhodný, a teprve potom navrhneme konkrétní provedení.")}"""
page("na-miru.html", "GLASSFLOOR na míru · rozměry od 40 cm a výbava podle situace",
     "Pochozí světlíky GLASSFLOOR vyráběné na míru od 40 cm: čtverec, obdélník i kruh. Výbava podle situace na stavbě: vyhřívání, soukromí PRIVA-LITE, LED, protiskluz.",
     "produkty", miru_body, jsonld=faq_ld(miru_faq))

# ---------------------------------------------------------------- PRO ARCHITEKTY
aud = pick(BARVA, 'id="pro-koho"')
value = pick(BARVA, 'class="value')
tech_sec = pick(BARVA, 'id="technika"')
cut = tech_sec.index('    <div class="g" style="margin-top:clamp(32px,4vw,56px);align-items:end">')
tech_sec = tech_sec[:cut].rstrip() + "\n  </div>\n</section>"
nedava = pick(BARVA, 'id="nedava"')
arch_body = page_head("index.html", "Zpět na úvod", "Pro architekty a projektanty",
                      "Pochozí světlíky pro architekty: podklady a technika.",
                      "Technická data z produktových listů, výrobní detail napojení, kdo u projektu stojí s vámi a otevřeně i to, kdy vám GLASSFLOOR nedoporučíme.")
arch_body += f"\n\n{aud}\n\n{value}\n\n{tech_sec}\n\n{nedava}\n\n{final_cta('Představte nám svůj projekt.', 'Pošlete základní výkres, řez nebo popis záměru. Posoudíme vhodnost systému GLASSFLOOR a navrhneme další technický postup.')}"
arch_faq = [
    ("Jaké podklady pro projekt GLASSFLOOR nabízí?", "Osm výrobních detailů napojení v PDF (chrome, pure, circle a dělení skla), tři produktové listy a zkušební doklady. Výkresy DWG a DXF se dodávají přímo k projektu."),
    ("Čím je systém posouzen?", "Zkouškami Fraunhofer IBP Stuttgart a osvědčením IFT podle DIN 18008-5."),
    ("Jaké zatížení pochozí zasklení snese?", "Užitné zatížení je 5,0 kN/m², třída odolnosti P8B. Vyšší únosnost včetně pojezdu se navrhuje zakázkově."),
]
arch_body = arch_body.replace(final_cta('Představte nám svůj projekt.', 'Pošlete základní výkres, řez nebo popis záměru. Posoudíme vhodnost systému GLASSFLOOR a navrhneme další technický postup.'),
                              faq_section("Co projektanti zjišťují nejčastěji.", arch_faq) + "\n\n" +
                              final_cta('Představte nám svůj projekt.', 'Pošlete základní výkres, řez nebo popis záměru. Posoudíme vhodnost systému GLASSFLOOR a navrhneme další technický postup.'))
page("pro-architekty.html", "Pro architekty a projektanty · GLASSFLOOR® technická data a podklady",
     "GLASSFLOOR pro architekty a projektanty: technická data, výrobní detaily napojení, podklady ke stažení a otevřeně o tom, kdy pochozí světlík doporučit nebudeme.",
     "architekti", arch_body, jsonld=faq_ld(arch_faq))

# ---------------------------------------------------------------- REFERENCE
proj1 = pick(BARVA, 'id="projekty"')
proj23 = pick(BARVA, 'class="g proj2"')
galerie = pick(BARVA, 'class="gallery"')
ref_body = page_head("index.html", "Zpět na úvod", "Reference",
                     "Reference pochozích světlíků GLASSFLOOR.",
                     "Vybrané stavby ze Švýcarska, kde pochozí prosklení nahradilo šachty a dvorky denním světlem v rovině terasy, zahrady i střechy.")
proj1 = proj1.replace('<div class="wrap">', '<div class="wrap">\n    <h2 class="sr-only">Vybrané realizace</h2>', 1)
ref_body += f"\n\n{proj1}\n\n{proj23}\n\n{galerie}\n\n{final_cta('Chcete podobné řešení?', 'Pošlete nám základní výkres nebo popis záměru. Posoudíme vhodnost systému GLASSFLOOR a navrhneme další technický postup.')}"
page("reference.html", "Reference GLASSFLOOR® · realizace pochozích světlíků",
     "Realizace pochozích světlíků GLASSFLOOR: vila v Zumikonu, bazén u Tegernsee, pochozí střecha administrativní budovy a další stavby ze Švýcarska.",
     "reference", ref_body)

# ---------------------------------------------------------------- STÁVAJÍCÍ PODSTRÁNKY (nový rámec, obsah beze změny)
def inner(txt):
    a = txt.index("</header>") + len("</header>")
    b = txt.index("<footer>")
    body = txt[a:b].strip()
    body = re.sub(r'<a class="k crumb"[^>]*>.*?</a>', '%%CRUMBS%%', body, count=1)
    body = body.replace('<h1 class="h1">Podklady pro projekt.</h1>', '<h1 class="h1">Podklady pro projekt pochozího světlíku.</h1>')
    body = body.replace('<div class="spolecne rv">', '<h2 class="sr-only">Heliobus AG a WT: rozdělení rolí</h2>\n    <div class="spolecne rv">', 1)
    body = body.replace('<span class="meta-l">Přímý kontakt</span>', '<h2 class="sr-only">Přímý kontakt na WT</h2><span class="meta-l">Přímý kontakt</span>', 1)
    for s in sections(body):
        if 'class="team-grid' in s and '[doplnit]' in s:
            body = body.replace(s, '<!-- Sekce "S kým budete jednat" skryta do doplnění jmen, fotek a kontaktů (originál v _STARE/pred-restrukturalizaci-2026-10-02/kontakty.html) -->')
    body = body.replace('produkty.html#airflow', 'airflow-rwa.html').replace('produkty.html#chrome', 'chrome.html').replace('produkty.html#firestop', 'firestop.html')
    return body.replace('href="barva-CMYK.html#projekty"', 'href="reference.html"').replace('href="barva-CMYK.html#technika"', 'href="pro-architekty.html"') \
               .replace('href="barva-CMYK.html"', 'href="index.html"')


def styles(txt):
    head = txt[:txt.index("</head>")]
    return "\n".join(re.findall(r"<style>\n?(.*?)</style>", head, re.S))


for fname, key, title, desc, src in [
    ("ke-stazeni.html", "stazeni", None, None, KST),
    ("o-nas.html", "onas", None, None, ONAS),
    ("kontakty.html", "kontakty", None, None, KONT),
]:
    t = re.search(r"<title>(.*?)</title>", src).group(1)
    ds = re.search(r'<meta name="description" content="(.*?)">', src).group(1)
    page(fname, t, ds, key, inner(src), extra_style=styles(src))

# ---------------------------------------------------------------- sitemap
urls = ["index.html", "produkty.html", "chrome.html", "pure.html", "circle.html", "firestop.html", "airflow-rwa.html",
        "na-miru.html", "pro-architekty.html", "reference.html", "ke-stazeni.html", "o-nas.html", "kontakty.html"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{BASE}/{'' if u == 'index.html' else u}</loc><lastmod>{DATE}</lastmod></url>\n" for u in urls) + "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sm, encoding="utf-8", newline="\n")
print("hotovo")

# ---------------------------------------------------------------- robots.txt, llms.txt, favicon
bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot"]
robots = "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n"
(ROOT / "robots.txt").write_text(robots, encoding="utf-8", newline="\n")

llms = f"""# GLASSFLOOR

> GLASSFLOOR je pochozí světlík a prosklená podlaha švýcarského výrobce Heliobus AG (St. Gallen). Nosné zasklení v nerezovém rámu slouží jako běžně pochozí plocha terasy, střechy nebo podlahy a přivádí denní světlo do podlaží pod ní. V České republice ho dodává WT - WINDOWS TOMORROW s.r.o. Řady chrome, pure a circle, varianty FIRESTOP (REI 30 až 120), AIRFLOW a RWA. Standardní formáty i výroba na míru od 40 cm. Zakázkové řešení bez ceníku, menší standardní formáty od cca 100 000 Kč.

Klíčová fakta: vrstvené bezpečnostní sklo, Ug 1,1 až 0,5 W/m²K, propustnost světla 73 až 88 %, užitné zatížení 5,0 kN/m², třída odolnosti P8B, nerezový rám 1.4301, výška rámu 12 cm, doporučený spád osazení min. 1,5 %, Swiss made.

## Produkty
- [Přehled produktů]({BASE}/produkty.html): tři řady a varianty
- [GLASSFLOOR chrome]({BASE}/chrome.html): přiznaný nerezový rám 4 cm, šest standardních rozměrů
- [GLASSFLOOR pure]({BASE}/pure.html): minimální rám 0,5 cm, šest standardních rozměrů
- [GLASSFLOOR circle]({BASE}/circle.html): kruhový, průměry 60 až 120 cm, rám 0,3 cm
- [GLASSFLOOR FIRESTOP]({BASE}/firestop.html): požárně dělicí pochozí světlík REI 30 až REI 120
- [AIRFLOW a RWA]({BASE}/airflow-rwa.html): větrání klapkami a odvod kouře a tepla
- [Na míru a výbava]({BASE}/na-miru.html): rozměry od 40 cm, vyhřívání, PRIVA-LITE, LED, protiskluz

## Pro projektanty
- [Pro architekty a projektanty]({BASE}/pro-architekty.html): technická data, kdy GLASSFLOOR doporučit nebudeme
- [Ke stažení]({BASE}/ke-stazeni.html): 8 výrobních detailů napojení (PDF), produktové listy, zkušební doklady
- [Reference]({BASE}/reference.html): realizace ze Švýcarska

## Firma
- [O nás]({BASE}/o-nas.html): Heliobus AG a WT - WINDOWS TOMORROW s.r.o., tým
- [Kontakt]({BASE}/kontakty.html): telefon 608 918 484, info@glassfloor.cz, Horoměřice
"""
(ROOT / "llms.txt").write_text(llms, encoding="utf-8", newline="\n")

fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#1a242c"/><text x="32" y="30" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="17" letter-spacing="3" fill="#fff">GLASS</text><text x="32" y="48" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="17" letter-spacing="3" fill="#fff">FLOOR</text><rect x="18" y="53" width="28" height="2" fill="#ade8e8"/></svg>
"""
(ROOT / "favicon.svg").write_text(fav, encoding="utf-8", newline="\n")
print("robots.txt, llms.txt, favicon.svg zapsány")
