// Filtering is client-side and progressive: with JS off, all cards remain visible.
(function(){
  const q = document.getElementById('q');
  const status = document.getElementById('f-status');
  const maturity = document.getElementById('f-maturity');
  const cards = Array.from(document.querySelectorAll('[data-skill]'));
  const count = document.getElementById('count');
  if(!cards.length) return;

  function apply(){
    const term = (q?.value || '').toLowerCase().trim();
    const st = status?.value || '';
    const mt = maturity?.value || '';
    let shown = 0;
    cards.forEach(card => {
      const hay = card.dataset.search || '';
      const okTerm = !term || hay.includes(term);
      const okStatus = !st || card.dataset.status === st;
      const okMaturity = !mt || card.dataset.maturity === mt;
      const show = okTerm && okStatus && okMaturity;
      card.style.display = show ? '' : 'none';
      if(show) shown++;
    });
    if(count) count.textContent = shown + (shown === 1 ? ' skill' : ' skills');
    const empty = document.getElementById('empty');
    if(empty) empty.hidden = shown !== 0;
  }
  q?.addEventListener('input', apply);
  status?.addEventListener('change', apply);
  maturity?.addEventListener('change', apply);
  apply();

  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const target = document.getElementById(btn.dataset.copy);
      if(!target) return;
      try{
        await navigator.clipboard.writeText(target.innerText);
        const old = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = old, 1600);
      }catch(e){ /* clipboard blocked: the text is still selectable */ }
    });
  });
})();
