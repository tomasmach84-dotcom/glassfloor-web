# CONCEPT_COMPARISON.md — čtyři koncepty homepage GLASSFLOOR

**Datum:** 16. 7. 2026
**Stav:** fáze porovnání směrů — žádný koncept není vybraný, produkční web nebyl měněn (žádný zatím neexistuje; vše jsou nové soubory v této složce).

**Soubory:**

| Soubor | Obsah |
|---|---|
| `concepts.html` | porovnávací stránka s živými náhledy (desktop + mobil), výhodami, riziky a tabulkou kritérií |
| `concept-01.html` | Swiss Editorial Precision |
| `concept-02.html` | Architectural Gallery |
| `concept-03.html` | Engineering Luxury |
| `concept-04.html` | Cinematic Minimalism |
| `IMAGE_AUDIT.md` | audit všech 29 fotografií (kategorie A/B/C, ořezy, duplicity) |
| `img/` | optimalizované kopie fotografií (originály zůstaly nedotčené na ploše v `GLASSFLOOR WEB NEW`) |

Všechny prototypy jsou čisté HTML/CSS/JS bez závislostí — fungují offline, otevřením souboru v prohlížeči. Všechny sdílejí stejný positioning (eyebrow „GLASSFLOOR® · ST. GALLEN · SWITZERLAND“, titulek „Švýcarská preciznost. Světlo bez kompromisů.“, podtitulek o milimetrech) a stejnou sadu fotografií, aby se porovnával design, ne marketing.

---

## Koncept 01 — Swiss Editorial Precision

- **Hlavní kreativní myšlenka:** švýcarský grafický design jako důkaz původu — přísný grid, viditelné linky (hairlines), číslované sekce, červený akcent. Web sám je „vyrobený na milimetr“.
- **Cílová emoce:** klid, řád, důvěra, intelektuální respekt.
- **Cílová skupina:** architekti, projektanti, designově orientovaní investoři.
- **Typografie:** Helvetica/Arial (systémová), pevná hierarchie: malé verzálkové štítky s prostrkáním × velké tučné titulky se záporným prokladem.
- **Barevný princip:** bílá + inkoustová čerň + šedé linky; jediný akcent švýcarská červená (#d0342c) na číslech a mikroprvcích.
- **Práce s fotografiemi:** fotky vždy v přesném rámu gridu s popiskem jako v katalogu; hero jako split-screen (5/7), realizace v mřížce 8+4; slabší fotky drží pevné orámování a menší formáty.
- **Struktura homepage:** sticky nav → split hero → „Vyrobeno ve Švýcarsku“ (4 fakta v mřížce) → manifest na šedé desce → hlavní realizace Zumikon (velká + 2 malé fotky + datový pruh) → 3 další realizace → tmavá technická sekce s tabulkou parametrů a makro detailem skla → CTA → patička.
- **Interakční princip:** minimum — jemný fade-in při scrollu, podtržení odkazů, hover na kartách. Nic se nehýbe samo.
- **Hlavní výhoda:** nejuniverzálnější a nejsnáze rozšiřitelný designový systém; nejvyšší důvěryhodnost u odborného publika.
- **Hlavní slabina:** nejmenší okamžitá emoce; při špatné správě obsahu může sklouznout k nudě.
- **Náročnost rozpracování:** nízká — grid a komponenty se přímočaře přenesou na produktové stránky, reference i formuláře.

## Koncept 02 — Architectural Gallery

- **Hlavní kreativní myšlenka:** homepage jako první číslo architektonické monografie o značce — kapitoly, popisky fotografií, iniciála, citát přes stránku, horizontální galerie „k listování“.
- **Cílová emoce:** okouzlení, touha „chci, aby můj dům vypadal takhle“.
- **Cílová skupina:** nároční soukromí investoři, čtenáři architektonických médií; sekundárně architekti.
- **Typografie:** serif (Georgia) pro titulky i text, kurzíva jako akcent; drobné bezserifové verzálky pro popisky a navigaci.
- **Barevný princip:** teplý papír (#f7f4ee), tmavě hnědočerný inkoust, mosazný akcent (#8a6d3b). Žádné čistě bílé plochy — atmosféra tištěné publikace.
- **Práce s fotografiemi:** fotografie jsou hlavním nositelem — velké celky přes celou šíři s popiskem „Foto: …“, asymetrické trojice (text + 2 svislé výřezy), horizontální pás galerie se střídáním formátů 4:3 a 3:4; slabší fotky jen v malých formátech pásu.
- **Struktura homepage:** transparentní nav → „obálka“ (obří titulek + hlavní foto + editorial sloupek) → Kapitola I Ateliér St. Gallen (text s iniciálou × svislé foto) → citátový manifest → Kapitola II Zumikon (celoplošné foto + tři sloupce) → Kapitola III horizontální galerie → Kapitola IV řemeslo v detailu (foto × seznam parametrů) → Epilog CTA.
- **Interakční princip:** pomalé odhalování bloků, horizontální scroll galerie se snap-body; jinak ticho.
- **Hlavní výhoda:** nejsilnější emoce a nejvýraznější odlišení; nejlépe maskuje omezenou kvalitu fotografií.
- **Hlavní slabina:** závislost na kvalitním copywritingu; hůř se do ní vkládají tvrdá technická data a konfigurátory.
- **Náročnost rozpracování:** střední — editorialový styl je třeba udržet i na produktových stránkách, jinak se rozpadne.

## Koncept 03 — Engineering Luxury

- **Hlavní kreativní myšlenka:** cena vychází z konstrukce — web ji dokazuje: interaktivní SVG řez vrstvami skla, datové panely, výrobní záběry, požární test FIRESTOP. Luxus vyjádřený inženýrstvím, ne pozlátkem.
- **Cílová emoce:** respekt, jistota, „teď chápu, proč to stojí tolik“.
- **Cílová skupina:** projektanti, stavební firmy, racionální investoři; ideální i pro B2B.
- **Typografie:** systémový grotesk pro titulky, monospace (Consolas) pro štítky, kóty a číselné údaje — jazyk výkresu.
- **Barevný princip:** grafitová tma (#101418), lomená bílá, mosazně-zlatý akcent (#c9a227) výhradně na datech a akcích; sklo v řezu chladně modré.
- **Práce s fotografiemi:** fotografie jako důkazní materiál s popisky ve stylu výkresu; makro hrany skla jako hero pozadí; montáž jeřábem a požární test jako unikátní obsah, který konkurence nemá; tmavé ladění sjednocuje různou kvalitu snímků.
- **Struktura homepage:** sticky nav → hero s datovým pruhem (4 parametry) → interaktivní řez konstrukcí s legendou → manifest „luxus = klid“ → výroba St. Gallen (koláž + 3 fakta) → case study Zumikon (panel + foto) → mřížka referencí → FIRESTOP testováno ohněm → CTA se 3 kroky spolupráce.
- **Interakční princip:** najetí na položku legendy zvýrazní vrstvu v SVG řezu; hover stavy na kartách; jemné odhalování. Vše účelové.
- **Hlavní výhoda:** nejsilnější argumentace ceny a technická autorita; nejméně závislý na dalších fotkách (schémata lze kreslit).
- **Hlavní slabina:** tmavý svět může působit v rozporu s produktem „denní světlo“; tvorba dalších schémat vyžaduje čas.
- **Náročnost rozpracování:** vyšší — každá další stránka si říká o vlastní technické ilustrace a ověřená data.
- **Poznámka k datům:** číselné/technické údaje v prototypu jsou popisné (bez konkrétních certifikací); před produkcí je nutné je doplnit a ověřit z podkladů Heliobus.

## Koncept 04 — Cinematic Minimalism

- **Hlavní kreativní myšlenka:** homepage jako krátký film o světle — celoplošná scéna bazénu s pomalým pohybem, akty místo sekcí, minimum slov, hlavní realizace vyprávěná třemi „záběry“ (celek → polodetail → pointa).
- **Cílová emoce:** úžas, zpomalení, pocit luxusu; „nejprve pocítíte, pak pochopíte“.
- **Cílová skupina:** prémioví soukromí investoři; silné pro kampaně a sociální sítě.
- **Typografie:** velmi lehký grotesk (váha 200–300) s výrazným prostrkáním verzálkových štítků; tučné jen pointy vět.
- **Barevný princip:** téměř černá (#0a0a0c), teplá lomená bílá, žádný barevný akcent — barvu dodávají výhradně fotografie; světlo je hlavní „barva“ webu.
- **Práce s fotografiemi:** jedna nosná fotografie na obrazovku, ztmavené okraje a gradienty pro čitelnost; pomalý Ken-Burns pohyb jen v hero (respektuje `prefers-reduced-motion`); galerie ve tmě s odkrytím na hover; slabší fotky se nepouštějí do velkých formátů vůbec.
- **Struktura homepage:** neviditelná nav (objeví se po scrollu) → celoplošné hero → Akt I manifest jednou větou + panoramatický detail → Akt II Zumikon ve třech záběrech → Akt III švýcarská „deska“ (3 fakta) → Akt IV galerie ve tmě → Akt V technický důkaz šeptem → finále CTA na celoplošné fotografii.
- **Interakční princip:** kontrolovaný pohyb — pomalé odhalování s dlouhým easingem, žádný parallax, žádné efekty blokující čtení; scroll-cue v hero.
- **Hlavní výhoda:** nejsilnější první dojem a zapamatovatelnost; skvěle funguje na mobilu (málo textu, svislé vyprávění).
- **Hlavní slabina:** stojí a padá s 1–2 špičkovými záběry (ideálně by časem chtěl autentické video); málo prostoru pro SEO obsah a technické podklady.
- **Náročnost rozpracování:** vyšší — udržet filmový rytmus na produktových a technických stránkách je disciplína; hrozí, že zbytek webu bude „obyčejnější“ než homepage.

---

## Srovnání (1–5, 5 = nejlepší)

| Kritérium | 01 Swiss | 02 Gallery | 03 Engineering | 04 Cinematic |
|---|---|---|---|---|
| První prémiový dojem | 4 | 4 | 4 | **5** |
| Důvěryhodnost pro architekty | **5** | 4 | **5** | 3 |
| Emocionální síla | 3 | **5** | 3 | **5** |
| Technická autorita | 4 | 3 | **5** | 3 |
| Odolnost vůči slabším fotkám | 4 | **5** | 4 | 2 |
| Srozumitelnost produktu | **5** | 4 | **5** | 3 |
| Odlišitelnost od konkurence | 3 | **5** | 4 | **5** |
| Dlouhodobá rozšiřitelnost | **5** | 3 | 4 | 3 |
| Předpokládaný výkon webu | **5** | 4 | 4 | 3 |
| Náročnost implementace (5 = snadná) | **5** | 4 | 3 | 3 |

## Odborné doporučení (nezávazné)

Rozhodnutí je na majiteli. Pokud má pomoci názor:

1. **Nejbezpečnější dlouhodobá volba: 01 Swiss Editorial Precision** — nejlépe se škáluje na celý web, buduje důvěru u architektů a unese jakýkoli budoucí obsah.
2. **Nejvyšší návratnost emocí: kombinace 01 + prvky 03** — švýcarský grid jako systém, do něj technické řezy a „testováno ohněm“ z konceptu 03 jako důkaz ceny. Tato kombinace nejlépe odpovídá zadání „prémiovost + preciznost + zdůvodnění ceny“.
3. Koncept **02** volit, pokud je prioritou emoce a značka „architektonického kurátora“; koncept **04**, pokud vznikne špičkové video/foto hlavní realizace.

Po výběru směru se zvolený koncept **nerozkopíruje mechanicky**, ale rozpracuje jako designový systém (typografická škála, mřížka, komponenty, stavy formulářů, šablony referencí a produktů) pro všechny stránky webu.
