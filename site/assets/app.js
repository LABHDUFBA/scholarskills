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
      var ok=(!term||hay.indexOf(term)>-1)&&(!s||c.dataset.status===s)&&(!m||c.dataset.maturity===m)&&
             (!g||c.dataset.stage===g)&&(!d||(c.dataset.disc||'').indexOf(d)>-1)&&
             (!p||(c.dataset.paths||'').indexOf(p)>-1);
      c.hidden=!ok;
      if(ok) shown++;
    });
    if(count) count.textContent=shown;
    if(empty) empty.hidden=shown>0;
  }
  [q,st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('input',apply); });
  [st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('change',apply); });
  [].slice.call(pb).forEach(function(b){
    b.addEventListener('click',function(){
      var on=b.classList.contains('on');
      [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); });
      PATH=on?'':b.dataset.pathJump;
      if(!on) b.classList.add('on');
      apply();
    });
  });
  apply();
})();

// Copy buttons. Independent scope, and the answer never depends on the clipboard permission:
// if the async API is blocked the text is selected so one keystroke finishes the job.
(function(){
  [].slice.call(document.querySelectorAll('[data-copy]')).forEach(function(btn){
    btn.addEventListener('click',function(){
      var target=document.getElementById(btn.dataset.copy);
      if(!target) return;
      var text=(target.innerText||target.textContent||'').trim();
      var label=btn.dataset.label||btn.textContent;
      function done(ok){
        if(ok){
          btn.textContent=btn.dataset.done||'Copied';
          setTimeout(function(){ btn.textContent=label; },1600);
          return;
        }
        try{
          var r=document.createRange(); r.selectNodeContents(target);
          var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        }catch(e){}
        btn.textContent=btn.dataset.fail||label;
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
