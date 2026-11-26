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

// Catalogue filter. Separate scope: pages without cards must not stop the rest of the file.
// Search folds case and accents; filters persist in the query string; the count is announced.
(function(){
  var q=document.getElementById('q'), ty=document.getElementById('f-type'),
      st=document.getElementById('f-status'), mt=document.getElementById('f-maturity'),
      sg=document.getElementById('f-stage'), dc=document.getElementById('f-disc'),
      clear=document.getElementById('clear-filters'), pb=document.querySelectorAll('[data-path-jump]'),
      cards=[].slice.call(document.querySelectorAll('[data-skill]')),
      count=document.getElementById('count'), empty=document.getElementById('empty');
  if(!cards.length) return;
  var PATH='';
  function fold(s){
    s=(s||'').toString();
    if(s.normalize){ s=s.normalize('NFD').replace(/[̀-ͯ]/g,''); }
    return s.toLowerCase().trim();
  }
  function values(){
    return {
      q: q&&q.value||'', tipo: ty&&ty.value||'', status: st&&st.value||'',
      maturidade: mt&&mt.value||'', etapa: sg&&sg.value||'', disciplina: dc&&dc.value||''
    };
  }
  function apply(persist){
    var v=values(), term=fold(v.q), shown=0;
    cards.forEach(function(c){
      var hay=c.dataset.search||'';
      var ok=(!term||hay.indexOf(term)>-1)&&(!v.tipo||c.dataset.type===v.tipo)&&
             (!v.status||c.dataset.status===v.status)&&(!v.maturidade||c.dataset.maturity===v.maturidade)&&
             (!v.etapa||c.dataset.stage===v.etapa)&&(!v.disciplina||(c.dataset.disc||'').indexOf(v.disciplina)>-1)&&
             (!PATH||(c.dataset.paths||'').indexOf(PATH)>-1);
      c.hidden=!ok;
      if(ok) shown++;
    });
    if(count) count.textContent=shown;
    if(empty) empty.hidden=shown>0;
    if(persist) syncUrl(v);
  }
  function syncUrl(v){
    var p=new URLSearchParams();
    ['q','tipo','status','maturidade','etapa','disciplina'].forEach(function(k){
      if(v[k]) p.set(k, v[k]);
    });
    if(PATH) p.set('trilha', PATH);
    var qs=p.toString();
    try{ history.replaceState(null,'',location.pathname+(qs?'?'+qs:'')+location.hash); }catch(e){}
  }
  function readUrl(){
    var p=new URLSearchParams(location.search);
    if(q) q.value=p.get('q')||'';
    if(ty) ty.value=p.get('tipo')||'';
    if(st) st.value=p.get('status')||'';
    if(mt) mt.value=p.get('maturidade')||'';
    if(sg) sg.value=p.get('etapa')||'';
    if(dc) dc.value=p.get('disciplina')||'';
    PATH=p.get('trilha')||'';
    [].slice.call(pb).forEach(function(b){
      b.classList.toggle('on', !!PATH && b.dataset.pathJump===PATH);
    });
  }
  [q,ty,st,mt,sg,dc].forEach(function(el){
    if(!el) return;
    el.addEventListener('input',function(){ apply(true); });
    el.addEventListener('change',function(){ apply(true); });
  });
  [].slice.call(pb).forEach(function(b){
    b.addEventListener('click',function(){
      var on=b.classList.contains('on');
      [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); });
      PATH=on?'':b.dataset.pathJump;
      if(!on) b.classList.add('on');
      apply(true);
    });
  });
  if(clear){
    clear.addEventListener('click',function(){
      [q,ty,st,mt,sg,dc].forEach(function(el){ if(el) el.value=''; });
      PATH='';
      [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); });
      apply(true);
      if(q) q.focus();
    });
  }
  readUrl();
  apply(false);
})();

// Copy buttons. Independent scope, and the answer never depends on the clipboard permission:
// if the async API is blocked the text is selected so one keystroke finishes the job.
(function(){
  var live=document.getElementById('copy-status');
  function announce(msg){ if(live){ live.textContent=''; setTimeout(function(){ live.textContent=msg; },30); } }
  [].slice.call(document.querySelectorAll('[data-copy]')).forEach(function(btn){
    btn.addEventListener('click',function(){
      var target=document.getElementById(btn.dataset.copy);
      if(!target) return;
      var text=(target.innerText||target.textContent||'').trim();
      var label=btn.dataset.label||btn.textContent;
      function done(ok){
        if(ok){
          btn.textContent=btn.dataset.done||'Copied';
          announce(btn.dataset.done||'Copied');
          setTimeout(function(){ btn.textContent=label; },1600);
          return;
        }
        try{
          var r=document.createRange(); r.selectNodeContents(target);
          var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        }catch(e){}
        btn.textContent=btn.dataset.fail||label;
        announce(btn.dataset.fail||label);
        setTimeout(function(){ btn.textContent=label; },2400);
      }
      function legacy(){
        try{
          var ta=document.createElement('textarea');
          ta.value=text; ta.setAttribute('readonly','');
          ta.style.position='fixed'; ta.style.top='-1000px'; ta.style.opacity='0';
          document.body.appendChild(ta); ta.select();
          var ok=document.execCommand('copy');
          document.body.removeChild(ta); done(ok);
        }catch(e){ done(false); }
      }
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(text).then(function(){ done(true); }, legacy);
      } else { legacy(); }
    });
  });
})();
