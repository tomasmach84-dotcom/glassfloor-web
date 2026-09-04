# IMAGE_BRAND_SAFETY.md — ochrana log GLASSFLOOR / Heliobus na fotografiích

**Datum auditu:** 16. 7. 2026
**Kontrolováno:** všech 33 souborů v `img/` (optimalizované kopie zdrojové složky `OneDrive\Plocha\GLASSFLOOR WEB NEW`; zadaná cesta `%USERPROFILE%\Desktop\GLASSFLOOR WEB NEW` je tatáž složka — plocha je synchronizována přes OneDrive). Kontrola provedena vizuálně po jednotlivých snímcích (kontaktní archy).

**Podoba loga na fotografiích:** bílý obdélníkový štítek s textem „GLASS FLOOR" + logem „Heliobus® — The daylight company" (žlutý terč). U hero-zumikon-fasada jen bílý nápis GLASS FLOOR bez štítku. U firestop-interier varianta „GLASSFLOOR FIRESTOP".

## Hlavní pravidlo použité na stránce

**Fotografie s logem se zobrazují VŽDY CELÉ — bez `object-fit: cover`, bez `aspect-ratio` ořezu, bez zrcadlení, bez překrytí textem či gradientem.** Všechny logované fotografie mají nativní poměr 3:2, což je zároveň projektový formát stránky — ořez proto není potřeba. Ořezávat (cover) je povoleno jen fotky bez loga.

## Konfigurace (použitelná i pro budoucí build)

```js
const IMAGES = [
  // ——— FOTOGRAFIE S LOGEM (cropAllowed: false, zobrazit vždy celé) ———
  { src: "img/zahrada-vodni-linie.jpg",      logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, desktopObjectPosition: "center center", mobileObjectPosition: "center center", preferredFit: "contain/plná šířka (nativní 3:2)" },
  { src: "img/zahrada-svetliky-chodnik.jpg", logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/zahrada-dva-svetliky.jpg",     logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/zahrada-svetliky-trava.jpg",   logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)", pozn: "obsah = roh rámu zespodu (názvy prohozené, viz IMAGE_AUDIT gotcha)" },
  { src: "img/detail-roh-zespodu.jpg",       logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)", pozn: "obsah = dřevěná terasa" },
  { src: "img/pohled-shora-interier.jpg",    logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/interier-pracovna.jpg",        logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/interier-loznice.jpg",         logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/montaz-jerab-kolaz.jpg",       logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2, dvojkoláž)" },
  { src: "img/terasa-kruhovy-svetlik.jpg",   logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/terasa-drevo-ctverec.jpg",     logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/terasa-lehatko.jpg",           logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/firestop-pozarni-test.jpg",    logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (čtverec 1:1)" },
  { src: "img/firestop-interier.jpg",        logo: "GF FIRESTOP+Heliobus", pozice: "LEVÝ dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/strecha-terasa-dron-1.jpg",    logo: "GF+Heliobus", pozice: "LEVÝ dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/strecha-terasa-dron-2.jpg",    logo: "GF+Heliobus", pozice: "LEVÝ dolní", cropAllowed: false, preferredFit: "plná šířka (3:2)" },
  { src: "img/dron-fasada-okna.jpg",         logo: "GF+Heliobus", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (čtverec 1:1)" },
  { src: "img/hero-zumikon-fasada.jpg",      logo: "GLASS FLOOR (bílý text bez štítku)", pozice: "pravý dolní", cropAllowed: false, preferredFit: "plná šířka (4:3)" },

  // ——— FOTOGRAFIE BEZ LOGA (cropAllowed: true) ———
  { src: "img/hero-zumikon-169.jpg",           logo: null, cropAllowed: true,  desktopObjectPosition: "center 45%", mobileObjectPosition: "center center", preferredFit: "cover (hero desktop)" },
  { src: "img/hero-zumikon-mobil.jpg",         logo: null, cropAllowed: true,  preferredFit: "cover (hero mobil, svislý)" },
  { src: "img/detail-interier-strop.jpg",      logo: null, cropAllowed: true,  desktopObjectPosition: "60% center", preferredFit: "cover 3:2" },
  { src: "img/detail-sklo-hrana.jpg",          logo: null, cropAllowed: true,  preferredFit: "cover" },
  { src: "img/detail-sklo-hrana-vodorovne.jpg",logo: null, cropAllowed: true,  desktopObjectPosition: "center 42%", preferredFit: "cover 3:2 (otočená verze — sklo vodorovně)" },
  { src: "img/pohled-shora-crop.jpg",          logo: null, cropAllowed: true,  preferredFit: "cover" },
  { src: "img/interier-bazen.jpg",             logo: null, cropAllowed: true,  preferredFit: "plná šířka (3:2 nativně)" },
  { src: "img/interier-pure-jidelna.jpg",      logo: null, cropAllowed: true,  preferredFit: "cover (svislá)" },
  { src: "img/interier-pure-krb.jpg",          logo: null, cropAllowed: true,  preferredFit: "cover (svislá, malé rozlišení)" },
  { src: "img/montaz-jerab-silueta.jpg",       logo: null, cropAllowed: true,  preferredFit: "contain — zobrazovat celou (svislá, ČB dokumentární)" },
  { src: "img/terasa-klasicka-vila.jpg",       logo: null, cropAllowed: true,  preferredFit: "cover" },
  { src: "img/terasa-pure-vyhled.jpg",         logo: null, cropAllowed: true,  preferredFit: "cover" },
  { src: "img/terasa-tegernsee.jpg",           logo: null, cropAllowed: true,  preferredFit: "cover" },
  { src: "img/zahrada-ctvercovy-svetlik.jpg",  logo: null, cropAllowed: true,  preferredFit: "cover (svislá, dokumentační)" },
  { src: "img/zahrada-dva-ctverce-houpacka.jpg", logo: null, cropAllowed: true, preferredFit: "cover (svislá, mobilní kvalita)" },
];
```

## Jak je ochrana zajištěna v `homepage-premium-cohesive.html`

- Všechny fotografie s logem jsou vloženy jako `width:100%; height:auto` v rámu odpovídajícím nativnímu poměru — **žádný pixel se neořezává**, logo je vždy celé včetně bezpečné zóny.
- Fotky s logem nejsou překryty žádným textem, gradientem ani CTA (texty stojí vždle/pod fotografií, ne přes ni).
- Žádná fotografie není zrcadlena ani retušována.
- `object-fit: cover` je použit výhradně u fotek z bloku „bez loga".
- Hero používá `hero-zumikon-169.jpg` (desktop) a `hero-zumikon-mobil.jpg` (mobil) — obě bez loga; značka je v heru nesena typografickým lockupem GLASSFLOOR® by Heliobus AG, ne fotografií.

## Poznámky

- Originální vektorové logotypy GLASSFLOOR/Heliobus nejsou ve zdrojové složce k dispozici (jen fotografie) → lockup v hlavičce je řešen typograficky, bez napodobování grafické podoby loga. Pro produkci vyžádat oficiální logotypy od Heliobus AG.
- Obsah souborů `detail-roh-zespodu.jpg` × `zahrada-svetliky-trava.jpg` je prohozený oproti názvům (viz gotcha v paměti projektu).
