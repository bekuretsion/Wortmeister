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
    show('Add WortMeister',`<p>Keep your German practice one tap away.</p>${ios?'<ol><li>Open this website in Safari.</li><li>Tap Share, then <strong>Add to Home Screen</strong>.</li><li>Turn on <strong>Open as Web App</strong> if shown, then tap Add.</li></ol>':'<ol><li>Open your browser menu (⋮ or ⋯).</li><li>Choose <strong>Install app</strong> or <strong>Add to Home screen</strong>.</li><li>Confirm to add WortMeister.</li></ol>'}<p class="muted">Your study progress stays in the browser or app where you saved it. Use Settings → Export backup to move your progress.</p>`);
  }
  async function install(){if(installPrompt){const prompt=installPrompt;installPrompt=null;await prompt.prompt();await prompt.userChoice}else installHelp()}
  $('#install-app').onclick=install;
  function draw(){
    const page=location.hash.slice(1)||'today',games=['shooter','rush','typeit','matching'],words=['browse','book','dictionary-import','lists'];
    const selected=games.includes(page)?'games':words.includes(page)?'browse':['today','review'].includes(page)?page:'more';
    bottom.innerHTML=[['today','Today','home'],['review','Review','review'],['browse','Words','book'],['games','Games','gameTarget'],['more','More','list']].map(([id,label,img])=>id==='games'||id==='more'?`<button data-mobile-menu="${id}" class="${selected===id?'active':''}" aria-label="${label}" aria-haspopup="dialog">${icon(img)}<span>${label}</span></button>`:`<a href="#${id}" class="${selected===id?'active':''}" ${selected===id?'aria-current="page"':''}>${icon(img)}<span>${label}</span></a>`).join('');
    $('#install-app').hidden=installed();
  }
  bottom.addEventListener('click',e=>{const b=e.target.closest('[data-mobile-menu]');if(!b)return;const isGames=b.dataset.mobileMenu==='games';const links=[...document.querySelectorAll('aside nav a')].filter(a=>isGames?['#shooter','#rush','#typeit','#matching'].includes(a.getAttribute('href')):!['#today','#review','#shooter','#rush','#typeit','#matching'].includes(a.getAttribute('href')));show(isGames?'Games':'Explore WortMeister',`<div class="sheet-links">${links.map(a=>a.outerHTML).join('')}</div>${!isGames&&!installed()?'<button id="sheet-install">＋ Add to Home Screen</button>':''}`);if($('#sheet-install'))$('#sheet-install').onclick=install});
  menu.addEventListener('click',e=>{if(e.target===menu||e.target.closest('a'))close()});
  window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e});
  window.addEventListener('appinstalled',()=>{installPrompt=null;$('#install-app').hidden=true;close()});
  window.addEventListener('hashchange',()=>{close();draw()});
  window.matchMedia('(min-width: 851px)').addEventListener('change',e=>{if(e.matches)close()});
  if('serviceWorker' in navigator)navigator.serviceWorker.register('./sw.js').catch(()=>{});
  draw();
})();
