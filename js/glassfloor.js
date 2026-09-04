/* GLASSFLOOR — společné chování webu (hlavička, odhalování sekcí, mobilní menu).
   Vytaženo z barva-CMYK.html 1. 9. 2026 kvůli sdílení s podstránkami. */
  const hd = document.getElementById('hd');
  const updHd = () => hd.classList.toggle('scrolled', scrollY > 24);
  addEventListener('scroll', updHd, { passive: true });
  addEventListener('load', updHd);
  updHd();
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
  }), { threshold: .1 });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));

  /* ---- mobilni menu (25.8.2026 faze 1) ---- */
  const mbtn = document.getElementById('mbtn');
  const mmenu = document.getElementById('mmenu');
  const setMenu = open => {
    hd.classList.toggle('menu-open', open);
    mbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  };
  mbtn.addEventListener('click', () => setMenu(!hd.classList.contains('menu-open')));
  mmenu.querySelectorAll('a, .cta').forEach(el => el.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  /* pri prechodu na sirku pocitace menu zavrit, at nezustane viset otevrene */
  const mq = matchMedia('(min-width:941px)');
  const onMq = e => { if (e.matches) setMenu(false); };
  if (mq.addEventListener) mq.addEventListener('change', onMq); else mq.addListener(onMq);
