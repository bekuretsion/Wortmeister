(() => {
  let installPrompt=null;
  const installed=()=>window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  const top=document.createElement('header');top.className='mobile-brand';top.innerHTML='<a href="#today"><b>W</b> WortMeister</a><button id="install-app">＋ Install app</button>';document.body.append(top);
  const bottom=document.createElement('nav');bottom.className='mobile-bottom';bottom.setAttribute('aria-label','Mobile navigation');document.body.append(bottom);
  const menu=document.createElement('dialog');menu.className='mobile-sheet';menu.setAttribute('aria-label','More navigation');document.body.append(menu);
  function close(){menu.close()}
  function show(title,content){const pause=$('#game-pause');if(pause?.textContent==='Pause')pause.click();menu.innerHTML=`<div class="sheet-heading"><h2>${title}</h2><button id="close-mobile-menu" aria-label="Close menu">✕</button></div>${content}`;if(!menu.open)menu.showModal();$('#close-mobile-menu').onclick=close}
  function installHelp(){
    const ios=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
    show('Add WortMeister',`<p>Keep your German practice one tap away.</p>${ios?'<ol><li>Open this website in Safari.</li><li>Tap Share, then <strong>Add to Home Screen</strong>.</li><li>Turn on <strong>Open as Web App</strong> if shown, then tap Add.</li></ol>':'<ol><li>Open your browser menu (⋮ or ⋯).</li><li>Choose <strong>Install and create shortcut</strong>, then <strong>Install</strong>. Older Chrome versions may show <strong>Add to Home screen</strong> or <strong>Install app</strong>.</li><li>Confirm to add WortMeister.</li></ol>'}<p class="muted">Your study progress stays in the browser or app where you saved it. Use Settings → Export backup to move your progress.</p>`);
  }
  async function install(){if(installPrompt){const prompt=installPrompt;installPrompt=null;try{await prompt.prompt();await prompt.userChoice}catch{installHelp()}}else installHelp()}
  $('#install-app').onclick=install;
  const hubs={
    practice:['Practice','Build your German with a little practice each day.',[['flashcards','Flashcards','Recall a meaning, then flip.','flash'],['quiz','Quiz','Choose the correct meaning.','quiz'],['listen','Listen','Hear the German and type it.','listen'],['pronounce','Pronounce','Listen, record, and compare.','mic'],['sounds','German sounds','Practice the sounds of German.','sounds']]],
    games:['Games','Play with your German vocabulary.',[['shooter','Word Shooter','Find the word before it falls.','gameTarget'],['rush','Word Rush','A fast round of German words.','gameRush'],['typeit','Type It','Type the German from a clue.','gameType'],['matching','Matching','Connect words and meanings.','gameMatch']]],
    words:['Words','Explore German words, expressions, and subjects.',[['browse','Dictionary','Search all your German words.','book'],['dictionary-import','German–English','Explore every meaning.','book'],['book','Idioms','Expressions and their words.','book'],['subjects','Subjects','Vocabulary by topic.','list']]],
    more:['More','Your words, your progress, settings, and about WortMeister.',[['lists','My words','Your own saved words.','list'],['stats','Progress','See how you are doing.','stats'],['settings','Settings','How you study; save your work.','settings'],['about','About','About WortMeister.','info']]]
  };
  Object.assign(icons,{mobileGames:'M7 7h10a5 5 0 0 1 4 8l-2 2-4-3H9l-4 3-2-2a5 5 0 0 1 4-8M6 10v4M4 12h4M16 10h.1M19 13h.1',mobileMore:'M5 12h.1M12 12h.1M19 12h.1'});
  function paint(){
    const page=location.hash.slice(1)||'today';document.body.dataset.page=page;
    if(page==='today'&&!installed()&&!$('#home-install')){
      $('.top')?.insertAdjacentHTML('afterend','<section class="mobile-install-card"><div><strong>WortMeister on your phone</strong><p>Add the W icon to your home screen.</p></div><button id="home-install" class="dark">Install app</button></section>');
      if($('#home-install'))$('#home-install').onclick=install;
    }
    const hub=hubs[page];
    if(hub&&(page!=='practice'||window.matchMedia('(max-width: 850px)').matches)){
      $('#app').innerHTML=`<div class="mobile-hub-heading"><h1>${hub[0]}</h1><p>${hub[1]}</p></div><div class="mobile-hub-grid">${hub[2].map(([id,label,sub,img])=>`<a class="card mobile-hub-card" href="#${id}">${icon(img)}<h2>${label}</h2><p>${sub}</p></a>`).join('')}</div>${page==='more'&&!installed()?'<button id="hub-install" class="mobile-install-link">＋ Add WortMeister to Home Screen</button>':''}`;
      if($('#hub-install'))$('#hub-install').onclick=install;
    }
    if(page==='review'&&window.matchMedia('(max-width: 850px)').matches){const listen=$('.study [data-speak]');if(listen&&!listen.classList.contains('mobile-review-audio')){listen.classList.add('mobile-review-audio');listen.textContent='▶';listen.insertAdjacentHTML('afterend',`<button class="mobile-review-speed" data-speed aria-label="Change pronunciation speed">${state.speed}×</button>`)}document.querySelectorAll('[data-grade]').forEach(b=>b.textContent=['Again','Hard','Good','Easy'][Number(b.dataset.grade)])}
    draw();
  }
  function draw(){
    const page=location.hash.slice(1)||'today',games=['games','shooter','rush','typeit','matching'],words=['words','browse','book','dictionary-import','subjects'],practice=['practice','flashcards','quiz','listen','pronounce','sounds'];
    const selected=games.includes(page)?'games':words.includes(page)?'words':practice.includes(page)?'practice':['today','review'].includes(page)?page:'more';
    bottom.innerHTML=[['today','Today','home'],['review','Review','review'],['practice','Practice','flash'],['games','Games','mobileGames'],['words','Words','book'],['more','More','mobileMore']].map(([id,label,img])=>`<a href="#${id}" class="${selected===id?'active':''}" ${selected===id?'aria-current="page"':''}>${icon(img)}${id==='review'?`<small class="mobile-review-badge">${due().length}</small>`:''}<span>${label}</span></a>`).join('');
    $('#install-app').hidden=installed();
  }
  const beforeMobileRender=render;
  render=function(){beforeMobileRender();paint()};
  menu.addEventListener('click',e=>{if(e.target===menu||e.target.closest('a'))close()});
  window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e});
  window.addEventListener('appinstalled',()=>{installPrompt=null;$('#install-app').hidden=true;$('.mobile-install-card')?.remove();$('#hub-install')?.remove();close()});
  window.addEventListener('hashchange',()=>{close();paint()});
  window.matchMedia('(min-width: 851px)').addEventListener('change',()=>{close();render()});
  if('serviceWorker' in navigator)navigator.serviceWorker.register('./sw.js').catch(()=>{});
  paint();
})();
