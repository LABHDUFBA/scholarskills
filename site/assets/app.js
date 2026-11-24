// Progressive enhancement: without JS every card is visible and every link works.
(function(){
  var q=document.getElementById('q'), st=document.getElementById('f-status'),
      mt=document.getElementById('f-maturity'), sg=document.getElementById('f-stage'),
      dc=document.getElementById('f-disc'),
      cards=[].slice.call(document.querySelectorAll('[data-skill]')),
      count=document.getElementById('count'), empty=document.getElementById('empty');
  if(!cards.length) return;
  function apply(){
    var term=(q&&q.value||'').toLowerCase().trim(),
        s=st&&st.value||'', m=mt&&mt.value||'', g=sg&&sg.value||'',
        d=dc&&dc.value||'', shown=0;
    cards.forEach(function(c){
      var hay=c.dataset.search||'';
      var show=(!term||hay.indexOf(term)>-1)&&(!s||c.dataset.status===s)
        &&(!m||c.dataset.maturity===m)&&(!g||c.dataset.stage===g)
        &&(!d||(' '+(c.dataset.disc||'')+' ').indexOf(' '+d+' ')>-1);
      c.style.display=show?'':'none';
      if(show) shown++;
    });
    if(count) count.textContent=shown;
    if(empty) empty.hidden=shown!==0;
  }
  [q,st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('input',apply); });
  [st,mt,sg,dc].forEach(function(el){ if(el) el.addEventListener('change',apply); });
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
