// Progressive enhancement: without JS every card is visible and every link works.

(function(){
  var root=document.documentElement, KEY='smd-theme', btn=document.getElementById('theme-toggle');
  function current(){
    var set=root.getAttribute('data-theme');
    if(set) return set;
    return (window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';
  }
  function paint(){
    var t=current();
    if(btn){
      btn.setAttribute('aria-pressed', t==='dark'?'true':'false');
      btn.title = t==='dark' ? 'Mudar para tema claro' : 'Mudar para tema escuro';
    }
  }
  if(btn){
    btn.addEventListener('click',function(){
      var next = current()==='dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try{ localStorage.setItem(KEY, next); }catch(e){}
      paint();
    });
  }
  paint();
})();
(function(){
  var q=document.getElementById('q'), st=document.getElementById('f-status'),
      mt=document.getElementById('f-maturity'), sg=document.getElementById('f-stage'),
      dc=document.getElementById('f-disc'), pb=document.querySelectorAll('[data-path-jump]'),
      cards=[].slice.call(document.querySelectorAll('[data-skill]')),
      count=document.getElementById('count'), empty=document.getElementById('empty');
  if(!cards.length) return;
  var PATH='';
  function apply(){
    var term=(q&&q.value||'').toLowerCase().trim(),
        s=st&&st.value||'', m=mt&&mt.value||'', g=sg&&sg.value||'',
        d=dc&&dc.value||'', p=PATH||'', shown=0;
    cards.forEach(function(c){
      var hay=c.dataset.search||'';
      var show=(!term||hay.indexOf(term)>-1)&&(!s||c.dataset.status===s)
        &&(!m||c.dataset.maturity===m)&&(!g||c.dataset.stage===g)
        &&(!d||(' '+(c.dataset.disc||'')+' ').indexOf(' '+d+' ')>-1)
        &&(!p||(' '+(c.dataset.paths||'')+' ').indexOf(' '+p+' ')>-1);
      c.style.display=show?'':'none';
      if(show) shown++;
    });
    if(count) count.textContent=shown;
    if(empty) empty.hidden=shown!==0;
  }
  [q,st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('input',apply); });
  [st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('change',apply); });
  [].slice.call(pb).forEach(function(b){
    b.addEventListener('click',function(){
      var v=b.dataset.pathJump;
      if(PATH===v){ PATH=''; b.classList.remove('on'); }
      else { PATH=v; [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); }
      apply();
    });
  });
  [].slice.call(document.querySelectorAll('[data-disc-jump]')).forEach(function(a){
    a.addEventListener('click',function(){
      if(dc){ dc.value=a.dataset.discJump; apply(); }
    });
  });
  apply();
  [].slice.call(document.querySelectorAll('[data-copy]')).forEach(function(btn){
    btn.addEventListener('click',function(){
      var target=document.getElementById(btn.dataset.copy);
      if(!target||!navigator.clipboard) return;
      navigator.clipboard.writeText(target.innerText.trim()).then(function(){
        var label=btn.dataset.label||btn.textContent;
        btn.textContent=btn.dataset.done||'Copied';
        setTimeout(function(){ btn.textContent=label; },1600);
      });
    });
  });
})();
