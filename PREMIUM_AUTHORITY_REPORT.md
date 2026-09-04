# PREMIUM_AUTHORITY_REPORT.md — přepracování homepage na „quiet authority"

**Datum:** 16. 7. 2026
**Nová varianta:** `homepage-premium-authority.html` (samostatné preview)
**Původní `homepage-c.html` ponechána beze změny pro porovnání.**
**Produkční web nebyl měněn.**

---

## 1. Které prvky homepage-c snižovaly vnímanou hodnotu

| Prvek v homepage-c | Proč snižoval hodnotu | Řešení v nové verzi |
|---|---|---|
| Split-screen hero (šedý gradient vlevo + foto vpravo) | Vzorec klasické marketingové landing page; gradient působil jako „grafika místo architektury" | Jedna celistvá fotografická scéna přes celý viewport |
| Slogan „Bez GLASSFLOOR je to sklep. S GLASSFLOOR je to místnost." | Reklamní hláška — vtipná, ale katalogová | Věcný popis: „Pochozí plocha nad ním zůstává. Denní světlo pokračuje do podlaží pod ní." |
| „Kolik světla se skrývá pod vaší terasou?" + slib orientační ceny | Jazyk poptávkového webu; zve k porovnávání ceny | „Představte nám svůj projekt." + posouzení vhodnosti po obdržení výkresů |
| Dvě rovnocenná CTA tlačítka (bílé plné buttony) | Stránka „prosila" o kliknutí | Jediné hlavní CTA „Představit projekt" (podtržený text, ne button); druhá cesta jen textový odkaz |
| 4 obrazové „světelné scény" za sebou | Působilo jako kompletní databáze realizací → katalog | 3 kurátorované projekty (Projekt 01–03) s velkým prostorem a strukturou zakázky |
| Světelné záře („threshold" pruhy s glow efektem) | Dekorativní efekt bez funkce, marketingový rytmus | Odstraněno; rytmus tvoří negativní prostor a jemné linky |
| Barevné SVG schéma (modré výplně, žlutá záře) | Vysvětlující ilustrace pro spotřebitele | Čárový technický řez ve stylu výkresu (šrafury, kóty, legenda, bez barevných výplní) |
| Sekce „Proces — 4 kroky" | Standardní vzorec produktového webu | Odstraněna; proces nahrazuje kvalifikační logika kontaktní sekce |
| Množství textu | Stránka příliš vysvětlovala | Text zredukován zhruba o 40 % |

## 2. Jak nová verze vytváří selektivitu bez arogantních prohlášení

Nikde není napsáno „není pro každého" ani „exkluzivní". Selektivita vyplývá z chování stránky:

- hero obsahuje nenápadnou větu **„Každý projekt nejprve technicky posuzujeme."** — informuje, že spolupráce začíná posouzením, ne objednávkou;
- kontaktní sekce se jmenuje **„Začátek spolupráce"**, ne „Poptávka";
- formulář žádá **výkres, fázi projektu a roli návštěvníka** — tím přirozeně filtruje cenové turisty;
- stránka nikde neslibuje cenu, kalkulaci, dostupnost ani rychlost;
- jediné CTA se opakuje konzistentně: **„Představit projekt"**.

## 3. Jak komunikuje zakázkovost

- Hlavní nadpis hero: **„Každý GLASSFLOOR vzniká pro jedinou stavbu."**
- Přechodová sekce hned po hero: **„Ne z katalogu. Z konkrétního projektu."** se třemi řádky (Rozměr podle stavby · Skladba podle požadavků projektu · Kompletace a kontrola ve St. Gallen) — velká typografie a linky, žádné karty.
- Realizace jsou pojmenované **Projekt 01/02/03** a strukturované jako zakázky (požadavek → řešení → technická zvláštnost), ne jako galerie produktu.
- V technickém řezu jsou kóty popsané **„světlý rozměr dle projektu", „skladba dle projektu"** — i výkres říká, že nic není hotová položka.

## 4. Jak se odlišuje od běžného stavebního výrobku

Kontrolní otázka „mohl by web po výměně loga patřit výrobci oken či pergol?" — ne, protože:

- výrobce oken ukazuje produkt; tady se ukazuje **stavba, ve které produkt mizí** (hodnota = detaily, „které po dokončení téměř nevidíte");
- místo parametrové tabulky s cenami je **dokumentace systému pro projektanty** a poznámka, že neověřená čísla se neuvádějí — to si dovolí jen značka, která ví, že ji čtou architekti;
- výroba není „kvalita Made in Switzerland" jako nálepka, ale konkrétní činnost: kompletace kus po kusu, slícování, kontrola, expedice k osazení jeřábem.

## 5. Jak kvalifikuje vhodné projekty

Formulář „Představte nám svůj projekt" sbírá: roli (architekt/investor/firma), typ projektu, fázi (studie → realizace), lokalitu, předpokládaný rozměr, materiál okolního povrchu, přílohu (půdorys/řez PDF/DWG/foto), popis záměru a kontakt. Úvodní text sekce říká, že **nejprve se posuzuje vhodnost řešení** — návštěvník hledající „cenu za kus skla" odpadne, architekt s projektem dostane přesně ten vstup, který očekává.

## 6. Vybrané fotografie a proč

| Použití | Soubor | Důvod výběru |
|---|---|---|
| Hero (celá scéna) | `hero-zumikon-169.jpg` | Jediná profi fotografie (Pius Amrein), kde je zároveň vidět architektura, rozpoznatelný GLASSFLOOR v rovině kamene a dost klidné plochy pro typografii; ořez bez vodoznaku |
| Vložený pohled v hero | `pohled-shora-crop.jpg` | Vysvětluje funkci beze slov — pohled skrz totéž sklo do interiéru |
| „Ne z katalogu" detail | `detail-interier-strop.jpg` | Jediné profi foto bez vodoznaku; atmosférický důkaz z interiéru |
| Projekt 01 (Zumikon) | `zahrada-vodni-linie.jpg` + `zahrada-svetliky-chodnik.jpg` | Stejná realizace jako hero → působí jako skutečná případová studie, ne fotobanka |
| Hodnota v detailu | `detail-sklo-hrana-vodorovne.jpg` (velký, otočeno o 90° — sklo je pochozí, leží vodorovně) + `zahrada-svetliky-trava.jpg` (roh rámu zespodu) + `detail-roh-zespodu.jpg` (napojení na dřevěnou terasu) | Hrana/vrstvy zasklení, roh rámu, napojení na okolní povrch — přesně detaily ze zadání. **Pozor:** obsah souborů `detail-roh-zespodu.jpg` a `zahrada-svetliky-trava.jpg` je prohozený oproti názvům z IMAGE_AUDIT (terasa ↔ roh zespodu) |
| Projekt 02 | `interier-bazen.jpg` | Nejcinematičtější záběr; prémiová privátní architektura |
| Projekt 03 | `strecha-terasa-dron-1.jpg` | Komerční reference → šíře systému (jen jedna z dron-dvojice, druhá je duplicitní) |
| Výroba/osazení | `montaz-jerab-kolaz.jpg` + `montaz-jerab-silueta.jpg` (ČB) | Skutečná činnost místo deklarací; silueta v ČB kompenzuje nižší kvalitu snímku |

**Limit fotobanky:** ve zdrojích nejsou žádné snímky z výrobního prostředí (ruce, měření, kompletace v hale). Sekce St. Gallen proto zatím stojí na osazení na stavbě — pro finální web doporučuji vyžádat od Heliobus AG autentické výrobní fotografie. Většina fotek nese vodoznak; pro produkci získat čisté verze.

## 7. Tvrzení, která je před produkcí nutné ověřit z podkladů Heliobus

- materiál rámu „nerez + hliník, zateplený";
- skladba „kalené vrstvené sklo + izolační zasklení" (počet vrstev/dutin);
- že kompletace a kontrola probíhá kompletně ve výrobě v St. Gallen („kus po kusu");
- dostupné tvary (čtverec · obdélník · kruh) a limity rozměrů;
- vlastnosti varianty FIRESTOP a status požární zkoušky z fotografie;
- přesná čísla (U_g, třída protiskluzu, únosnost, požární klasifikace) — **záměrně neuvedena**, doplní se až po ověření;
- autor fotografií (Pius Amrein) a práva k jejich užití;
- reálie projektů: Zumikon, Tegernsee, administrativní budova (lokality, typologie).

## 8. Kontrolní otázky ze zadání (bod 13)

1. Web po výměně loga výrobci oken/pergol? **Ne** — stojí na zakázkové logice a kurátorovaných projektech.
2. Položka porovnávaná cenou? **Ne** — cena se nikde neslibuje, vstupem je výkres.
3. Příliš tlačítek? **Ne** — jediné CTA, opakované konzistentně.
4. Klidná značka? **Ano** — žádné superlativy, žádné záře, žádné slogany.
5. Zřejmá kusová výroba pro konkrétní projekt? **Ano** — hero věta + „Ne z katalogu" + kóty „dle projektu".
6. Zřejmé, proč je třeba technické posouzení? **Ano** — kvalifikační věta v hero + logika kontaktní sekce.
7. První obrazovka = mimořádné architektonické řešení? **Ano** — celoplošná autentická scéna s produktem v rovině kamene.
8. Kontakt jako začátek spolupráce? **Ano** — „Začátek spolupráce", posouzení vhodnosti, strukturovaný vstup.

---

## 9. Doplnění 16. 7. — posílení „Swiss made" a signálu vysoké hodnoty (zpětná vazba majitele)

Majitel: „necítím z toho, že to bude drahé, a nikde nevidím Made in Switzerland." Doplněno:

- **Hlavička:** pod logem trvale „Swiss made · Heliobus AG" — na každé obrazovce.
- **Hero vpravo nahoře:** malý červený švýcarský kříž + „Swiss made — výroba a kompletace · St. Gallen".
- **Nový pruh SWISS MADE** (mezi projekty a výrobou): kříž, nadpis „Vývoj, konstrukce a kompletace každého kusu — Švýcarsko.", věta „GLASSFLOOR není licencovaná ani přeprodávaná technologie…", souřadnice výroby 47°25′ s. š. — 9°22′ v. d. (vzor hodinářských značek — původ jako fakt, ne slogan).
- **Technická tabulka:** první řádek „Původ — Swiss made, Heliobus AG, St. Gallen".
- **Kontakt:** přidána věta **„GLASSFLOOR je zakázkové řešení bez ceníku — cena vychází z technického návrhu konkrétního kusu."** — přímý, ale klidný signál, že jde o nákladné individuální řešení (bez čísel).
- **Patička:** „GLASSFLOOR® — Swiss made · Heliobus AG, St. Gallen".

Ověřit: formulace „není licencovaná ani přeprodávaná technologie" a rozsah činností v St. Gallen (vývoj/konstrukce/kompletace) — potvrdit s Heliobus AG.

*Interní preview. Formulář neodesílá data. Produkční web nebyl měněn.*
