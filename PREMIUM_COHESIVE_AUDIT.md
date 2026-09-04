# PREMIUM_COHESIVE_AUDIT.md — audit a přestavba na jednotný designový systém

**Datum:** 16. 7. 2026
**Vstup:** `homepage-premium-authority.html` (ponechána beze změny)
**Výstup:** `homepage-premium-cohesive.html` + `IMAGE_BRAND_SAFETY.md`
**Produkční web nebyl měněn.**

---

## 1. Audit původní stránky — co způsobovalo vizuální nejednotnost

### Gridy (13 různých sloupcových systémů)
hero 7/4 · bespoke 8/4 · řádky principů 70px/1fr · projekt 4/5/3 (tři sloupce!) · duo 1/1 · meta 120/1fr · hodnota 8/4 · poznámky 3×1 · výroba 5/7 · výrobní fotky 7/5 s posunem · technika 7/5 · kontakt 5/7 · formulář 1/1. Každá sekce si definovala vlastní poměry → dojem „poskládaných šablon".

### Poměry fotografií (6+ formátů)
21:10 (hlavní projekt) · 3:4 (svislé detaily) · 4:3 (duo, výroba) · 16:10 (hodnota) · vložený rámeček v heru · posunuté dvojice (margin-top offset). K tomu `object-fit: cover` plošně — včetně fotek s logem.

### Typografie
Důležité texty v 7,5 px (podtitulek loga!), 10,5 px, 11 px; tělo 14–15 px; přemíra drobných uppercase popisků, které nesly design místo obsahu.

### Vertikální rytmus
Univerzální `padding: clamp(80px, 11vw, 170px)` u všech sekcí + velké vnitřní mezery → dlouhé bílé plochy bez funkce.

### Duplicitní obsah
Swiss made v heru + samostatný Swiss pruh + sekce výroby (3 místa) · detailové fotky rozeseté ve 3 sekcích · dvě identické karty projektů 02/03.

## 2. Které layouty byly zrušeny

- split tří sloupců u hlavního projektu (4/5/3) → **B-layout 8+4**
- kompozice 1 velká + 2 malé fotky + 3 sloupce textu u „Hodnoty" → **C-layout 8+4 s jednou dominantní scénou**
- vložený rámeček (inset) v heru → hero je **jedna scéna**
- posunuté dvojice fotek ve výrobě → hlavní foto 8 + jeden dokument 4
- katalog dvou stejných karet → **hierarchie Projekt 02 (7/5) + Projekt 03 (teaser 5/7)**
- samostatný Swiss pruh se souřadnicemi → **sloučen do sekce výroby** (souřadnice odstraněny — působily dekorativně)
- celý formulář na homepage → **modal „Zahájit konzultaci"** (první krok, homepage končí čistým CTA)

## 3. Jak byl sjednocen grid

Jeden 12sloupcový grid (`.g`, gap clamp 18–32 px), jeden `--max: 1400px`, jedny okraje `--gut`. Povolené kompozice: **A** hero (celý viewport), **B** projekt 8+4, **C** detail/technika 8+4 či 7+5, **D** celoplošný blok (výroba-lockup, závěrečné CTA). Všechny sekce sdílejí stejnou levou typografickou osu.

## 4. Tři fotografické formáty

- **F1 — Hero:** jedna scéna přes viewport; desktop `hero-zumikon-169.jpg` (focal center 45 %), mobil `hero-zumikon-mobil.jpg` (svislý ořez) přes `<picture>`. Obě bez loga.
- **F2 — Projekt (3:2):** hlavní + jeden detail téhož projektu. Fotky s logem mají nativní 3:2 → zobrazují se **celé, bez jakéhokoli ořezu** (`width:100%; height:auto`).
- **F3 — Dokument/detail:** celý snímek bez agresivního ořezu (ČB silueta konstrukce v bílém rámu, technický výkres).
- Ořez (`cover`) je povolen jen u fotek bez loga: detail-interier-strop (3:2, focal 60 %), detail-sklo-hrana-vodorovne (3:2, focal 42 %).

## 5. Ochrana log GLASSFLOOR / Heliobus

Kompletní audit všech 33 fotek v `IMAGE_BRAND_SAFETY.md`. 18 fotek nese logo (bílý štítek GLASS FLOOR + Heliobus; převážně pravý dolní roh, u dron záběrů a firestop-interiéru levý dolní). Na stránce použité logované fotky: `zahrada-vodni-linie`, `zahrada-svetliky-chodnik`, `strecha-terasa-dron-1`, `montaz-jerab-kolaz` — všechny **bez ořezu, bez překrytí textem/gradientem, bez zrcadlení**. Hero a detaily používají výhradně fotky bez loga.

## 6. Jak byla zvětšena typografie

| Prvek | Původně | Nyní |
|---|---|---|
| Hero H1 | clamp(36–70) | **clamp(58px, 6vw, 104px)**, mobil clamp(40, 11vw, 58) |
| Sekční H2 | clamp(30–64) | **clamp(42px, 4.4vw, 72px)** |
| Vedlejší H3 | clamp(24–40) | **clamp(28px, 3vw, 48px)** |
| Úvodní text | 15,5–18,5 | **clamp(20px, 1.7vw, 25px)** |
| Běžný text | 14–15 | **min. 18 px**, proklad 1,55–1,6 |
| Popisky/metadata | 7,5–11 | **12–13 px** |
| Lockup v hlavičce | 13,5 + 7,5 px | **19 + 12,5 px** |

Drobné uppercase popisky zůstaly jen jako kickery sekcí a čísla projektů.

## 7. O kolik klesly bílé plochy

Univerzální `clamp(80,11vw,170)` nahrazen systémem: velká kapitola `clamp(72,8.5vw,128)` · běžná sekce `clamp(56,6.5vw,96)` · související blok `clamp(36,4.2vw,64)`. Horní hranice odsazení klesla ze 170 na 128 px (−25 %), běžné sekce na 96 px (−44 %); vnitřní mezery úměrně. Celkové snížení prázdných ploch ~35 %. Bílé místo zůstalo tam, kde odděluje kapitoly a nese nadpisy.

## 8. Vztah GLASSFLOOR × Heliobus

Jednotný typografický lockup na 4 místech: **hlavička** (GLASSFLOOR® / by Heliobus AG · St. Gallen, Switzerland — čitelné velikosti), **hero eyebrow** se švýcarským křížkem, **značkový blok ve výrobní sekci** (GLASSFLOOR® / by Heliobus AG / Engineered and manufactured in St. Gallen, Switzerland v orámovaném poli), **patička**. Swiss made navíc v technické tabulce (řádek Původ). Originální logotypy nejsou ve zdrojích k dispozici → lockup je typografický, bez napodobování grafiky loga; pro produkci vyžádat oficiální podklady od Heliobus AG.

## 9. Sloučené sekce

Hero-údaj + Swiss pruh + výroba → jedna sekce **„GLASSFLOOR vzniká ve St. Gallen."** s podtitulem „Vývoj, konstrukce, kompletace a kontrola každého zakázkového kusu probíhají ve výrobě Heliobus AG.", značkovým blokem, hlavní fotografií osazení, jedním ČB dokumentem a třemi výrobními fakty. Výsledná struktura stránky: Hero → Zakázkový princip → Projekt 01 → Hodnota v detailu → Projekty 02+03 → Výroba St. Gallen → Technická autorita → CTA (8 sekcí, žádné přechodové pruhy).

## 10. Proč nová verze působí uceleněji a prémiověji

Jediný grid a jediná typografická osa odstranily dojem slepených šablon; tři obrazové formáty dávají fotografiím řád; větší písmo a menší bílé plochy působí sebejistě, ne nesměle; švýcarský původ je nesen oficiálně vypadajícím lockupem místo rozptýlených drobností; loga na fotografiích jsou vždy celá — značka se nikde „neztrácí"; homepage končí klidným CTA místo dlouhého formuláře (kvalifikace zůstala v modalu).

## 11. Ověřeno

Snímky ve 390 px (iframe), 768 px, 1440 px a 1920 px — texty čitelné, loga celá, layouty se stohují bez rozpadu. Kontrolní otázka „švýcarský systém × minimalistický web s bílou plochou": stránka nyní stojí na řádu, měřítku a důkazech, ne na prázdnu.

## 12. Doplněk (16. 7. večer) — reálná data, více fotografií, oprava hlavičky

- **Technická sekce přepsána podle skutečných podkladů:** produktové listy staženy z glassfloor.cz/na-stahnuti (Produkteinfo GLASSFLOOR chrome/pure, Heliobus AG). Hodnoty: VSG extra čiré · Ug 1,1 / Super ISO 0,5 W/m²K · světlo 73–88 % · Rw ≥ 40 dB · 5,0 kN/m² · P8B · rám nerez 1.4301 (fasáda 4 cm) · na míru od 40 cm · DIN 18008-5 (IFT), Fraunhofer IBP. Popisky řezu odpovídají skutečné skladbě (krycí sklo, statické VSG, vnitřní ISO VSG, nerezová zárubeň).
- **Více fotografií (10 → 17):** Projekt 02 dostal detail téhož projektu (terasa-tegernsee); nová sekce „Další realizace" — jednotná mřížka 3×2 ve formátu F2 (pohled-shora-interier, interier-pracovna, terasa-kruhovy-svetlik, zahrada-dva-svetliky, terasa-drevo-ctverec, terasa-pure-vyhled — všechny s logem zobrazeny celé); technická sekce doplněna o důkazy FIRESTOP (firestop-interier + firestop-pozarni-test, REI 30–120 dle glassfloor.cz).
- **Oprava hlavičky:** průhledná hlavička se dřív zabarvovala až po odscrollování 72 % výšky okna → texty hera se s ní vizuálně slévaly. Nyní se zabarví po 24 px a stav se vyhodnocuje i při načtení stránky.

## 13. Doplněk (16. 7. večer #2) — hodinářské hero vyzkoušeno a vráceno

Na přání majitele bylo hero přestavěno na tmavou rozdělenou scénu à la Patek/Rolex (serifový nadpis Constantia, SWISS MADE s křížkem dole jako na ciferníku, firestop-interier.jpg jako celý exponát na tmavém poli). **Majitel po zhlédnutí rozhodl vrátit původní celoplošné foto hero** (hero-zumikon-169 + svislá mobilní varianta, velký bezpatkový nadpis) — to je platný stav. Fotka došlapu (firestop-interier) zůstává v technické sekci u FIRESTOP.

## 14. Co zbývá ověřit (nezměněno z předchozích reportů)

Technické hodnoty a formulace o výrobě (Heliobus AG), práva k fotografiím (Pius Amrein), oficiální logotypy, reálie projektů Zumikon/Tegernsee/administrativa.
