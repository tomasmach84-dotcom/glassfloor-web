# CONCEPT_02_REFINED_REPORT.md — Architectural Gallery with Cinematic Entrance

**Datum:** 16. 7. 2026
**Soubor:** `concept-02-refined.html` (interní preview; produkční web nezměněn — žádný zatím neexistuje)
**Zadání:** zachovat editorialové DNA konceptu 02, posílit první dojem full-screen herem z konceptu 04 a doplnit technický důkaz ceny z konceptu 03. Jednotný vizuální jazyk, ne slepenec tří šablon.

---

## Co zůstalo z konceptu 02

- Světlý minerální podklad (#f6f5f1) a klidný editorialový rytmus s velkorysým prázdným prostorem.
- Realizace jako architektonické příběhy: hlavní realizace Zumikon s velkoformátovou fotografií, popiskem autora fota a asymetrickou dvojicí snímků.
- Asymetrická galerie vybraných realizací (různá měřítka a formáty místo mřížky stejných karet).
- Serifové titulky, popisky pod fotografiemi, jemné linky (hairlines).
- Odstraněno oproti původnímu 02: označení „Kapitola I–IV“, iniciála, citátové uvozovky, převaha kurzívy a zlatohnědý akcent — vše, co táhlo výsledek k módnímu magazínu či hotelu.

## Co bylo převzato z konceptu 04

- Full-screen hero přes celý viewport s jednou nosnou fotografií, decentním overlay a bílou typografií.
- Transparentní navigace nad herem, která se při scrollu změní na světlý poloprůhledný header.
- Jemný scroll-indicator a velmi pomalé, téměř neznatelné přiblížení fotografie (60 s, scale 1→1,035; vypnuto při `prefers-reduced-motion`).
- Záměrně NEpřevzato: temná atmosféra, „akty“, dramatické vyprávění — hero zůstává světlé a denní.

## Co bylo převzato z konceptu 03

- Schématický SVG řez konstrukcí s vrstvami (protiskluzný potisk, nosné vrstvené sklo, izolační trojsklo, zateplený rám) a interaktivním zvýrazněním vrstvy při najetí na legendu.
- Sekce FIRESTOP s fotografií skutečné požární zkoušky.
- Kroky spolupráce (konzultace → návrh → výroba → montáž).
- Vizuálně kompletně přepracováno do světlého stylu 02: bílý papírový panel, tenké inkoustové linky, chladně modré sklo, jediný akcent; žádný tmavý dashboard, žádné zlato, žádný monospace.

## Typografie a barvy

- **2 rodiny písem:** Cambria (moderní architektonický serif — jen hlavní nadpisy a manifest) + Segoe UI (navigace, text, metadata, technické údaje). Bez externích fontů — prototyp funguje offline; pro produkci doporučuji ekvivalentní webfonty (např. Tiempos/Signifier + Neue Haas/Inter).
- **Barvy:** světlý minerál #f6f5f1 / panel #efede7, téměř černá #1a1a19, tlumená šedá #6e6e69, jediný decentní akcent „minerální modř“ #46626c (štítky, čísla, linky v řezu). Zlatohnědá z původního 02 odstraněna.

## Hero fotografie

- **Vybrána:** `heliobus-haus-nsur-zumikon…` (Zumikon, foto Pius Amrein, 5000×3747 px) — jediný snímek s rozlišením i kompozicí, které full-screen unesou; profi světlo, produkt v hlavní roli, denní atmosféra odpovídá značce.
- **Slabiny snímku a řešení:**
  1. Vodoznak GLASSFLOOR v pravém dolním rohu → vytvořen nový ořez `img/hero-zumikon-169.jpg` (16:9, spodních 890 px originálu s vodoznakem odříznuto).
  2. Světlá fasáda v horní části snižuje čitelnost bílého textu → dvojitý velmi jemný gradient (levý dolní roh + spodní hrana), obraz zůstává světlý a „denní“.
  3. Na výšku (mobil) kompozice nefunguje → samostatný svislý ořez `img/hero-zumikon-mobil.jpg` (900×1606, květináč + světlík, bez vodoznaku) podávaný přes `<picture>`; mobil má i vlastní silnější spodní scrim. Mobilní hero tedy není zmenšený desktop.

## Ověřeno responzivně

390 px (přes iframe kvůli limitu headless Edge), 768 px, 1440 px a 1920 px — hero, čitelnost, CTA, navigace i všechny sekce zkontrolovány na screenshotech; horizontální přetečení žádné. Váha stránky ≈ 3,5 MB (8 fotografií po ~150–800 kB); pro produkci viz doporučení níže.

## Co je ještě potřeba ověřit (před produkcí)

- Přesné technické hodnoty: U<sub>g</sub>, třídy protiskluzu (R…), požární klasifikace FIRESTOP, únosnost/normy, maximální vyrobitelné rozměry — v prototypu záměrně neuvedeny, jen popisné vlastnosti.
- Autorství fotografií (kredit „Pius Amrein“ převzat z názvu souboru) a práva k užití.
- Detaily procesu spolupráce (kdo montuje v ČR, dodací lhůty) a kontaktní údaje.
- Text manifestu a claimů schválit majitelem.

## Doporučení před aplikací na celý web

1. **Licencovat webfonty** odpovídající zvolenému páru (serif pro titulky, grotesk pro text) a nahradit systémová písma.
2. **Obrázky:** vyžádat od Heliobusu originály bez vodoznaku; generovat responzivní varianty (`srcset`, WebP/AVIF, lazy-load pod herem) — cíl pod 1,5 MB na první načtení.
3. **Rozpracovat komponenty jako systém:** karty referencí, šablona případové studie, technický list produktu, formulář konzultace — vše z vizuálního jazyka této stránky (štítek s linkou, hairline tabulky, serif jen v nadpisech, jeden akcent).
4. Do navigace „Produkty“ a „Pro architekty“ doplnit skutečné cílové stránky (zatím kotvy v rámci preview).
5. Zvážit krátké autentické video pro hero (pomalý statický záběr realizace) — až bude k dispozici; současné řešení s fotografií je plně funkční.

---

*Interní preview — neodkazovat veřejně. Otevřete `concepts.html` pro porovnání s původními čtyřmi koncepty, nebo přímo `concept-02-refined.html`.*
