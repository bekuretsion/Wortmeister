// Vocabulary games share the existing library and study scope.
const gameTools = {
  normalize: s => String(s).normalize('NFC').toLocaleLowerCase('de').trim().replace(/\s+/g,' '),
  shuffle(items) { const a=[...items]; for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]} return a; },
  sentence(w) {
    if(!w.example||!w.word)return '';
    const escaped=w.word.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    const masked=w.example.replace(new RegExp('(?<![\\p{L}\\p{N}])'+escaped+'(?![\\p{L}\\p{N}])','giu'),'_____');
    return masked===w.example?'':masked;
  },
  accepts(w,answer) { return [w.word,title(w)].some(s=>this.normalize(s)===this.normalize(answer)); },
  pool(words,scope,rating,list) {
    return words.filter(w=>!w.lookupOnly&&w.word&&w.meaning&&inScope(w,scope)&&
      (list!=='saved'||state.saved.includes(w.id))&&
      (rating==='any'||rating==='new'&&!state.cards[w.id]||rating==='learning'&&state.cards[w.id]&&state.cards[w.id].interval<21||rating==='familiar'&&state.cards[w.id]?.interval>=21));
  },
  unique(words,mode) {
    const terms=new Set(),clues=new Set();
    return words.filter(w=>{const term=this.normalize(title(w)),clue=this.normalize(mode==='sentence'?this.sentence(w):w.meaning);if(!clue||terms.has(term)||clues.has(clue))return false;terms.add(term);clues.add(clue);return true});
  }
};
(() => {
  const pages={shooter:['Word Shooter','Read the clue or hear the German. Tap the matching word before it falls.'],rush:['Word Rush','How many German words can you recognize in 60 seconds?'],typeit:['Type It','Read the meaning or hear the word. Type the German before time runs out.'],matching:['Matching','Match each German word to its meaning or to a sentence it fits.']};
  const options={mode:'meaning',rating:'any',list:'all',pairs:6};
  let game=null,timer=null;
  const stop=()=>{if(timer)clearInterval(timer);timer=null;game=null};
  const route=()=>location.hash.slice(1);
  const baseSidebar=sidebar;
  sidebar=function(page){return baseSidebar(page).replace('<div class="nav-label">WORDS</div>',`<div class="nav-label">GAMES</div>${Object.entries(pages).map(([id,[label]])=>`<a href="#${id}" class="${page===id?'active':''}" ${page===id?'aria-current="page"':''}>${icon(id==='shooter'?'quiz':id==='rush'?'stats':id==='typeit'?'list':'flash')}${label}</a>`).join('')}<div class="nav-label">WORDS</div>`)};
  function page(id) {
    const modes=id==='matching'?[['meaning','Meanings'],['sentence','Example sentences']]:id==='typeit'?[['meaning','Meanings'],['hear','Hear it']]:[['meaning','Meanings'],['sentence','Sentences'],['mixed','Mixed'],['hear','Hear it']];
    if(!modes.some(([m])=>m===options.mode))options.mode='meaning';
    return header(...pages[id])+`<div class="game-toolbar"><label>Clues <select id="game-mode">${modes.map(([m,label])=>`<option value="${m}" ${m===options.mode?'selected':''}>${label}</option>`).join('')}</select></label>${id==='matching'?`<label>Pairs <select id="game-pairs">${[4,6,8].map(n=>`<option ${n===options.pairs?'selected':''}>${n}</option>`).join('')}</select></label>`:''}<button id="game-new">New round</button></div><details class="game-settings"><summary>Settings</summary><div class="game-toolbar"><label>Learning stage <select id="game-rating"><option value="any">Any stage</option><option value="new" ${options.rating==='new'?'selected':''}>New words</option><option value="learning" ${options.rating==='learning'?'selected':''}>Learning</option><option value="familiar" ${options.rating==='familiar'?'selected':''}>Familiar · 21+ days</option></select></label><label>Word list <select id="game-list"><option value="all">All words</option><option value="saved" ${options.list==='saved'?'selected':''}>My saved words</option></select></label></div></details><div id="game-stage"><section class="card game-intro"><h2>${id==='matching'?'Find every pair.':id==='typeit'?'Put your German into words.':'Ready for a round?'}</h2><p>${id==='matching'?'Select a word on the left, then its match on the right.':id==='typeit'?'Type the German and press Enter. The first letter is given. Noun articles are optional. You have 3 hearts and 20 seconds per word.':id==='shooter'?'Choose the correct falling word. You have 3 hearts and 12 seconds per word.':'Choose the word that fits. Correct answers earn points; mistakes cost points. You have 60 seconds.'}</p><p class="muted">Uses your selected study scope. ${id==='matching'?'Your time and mistakes affect your score.':id==='rush'?'Keep going until the timer ends.':'Each round has up to 15 words.'}</p><button id="game-start" class="dark">Start</button></section></div>`;
  }
  function available() {
    return gameTools.unique(gameTools.shuffle(gameTools.pool(all(),state.scope,options.rating,options.list)),options.mode==='sentence'?'sentence':'meaning');
  }
  function start() {
    stop(); const words=available(),id=route();
    if(words.length<(id==='matching'?2:id==='typeit'?1:2)){$('#game-stage').innerHTML='<section class="card"><h2>More words needed</h2><p>Choose a broader study scope, another learning stage, or all words. Sentence mode needs examples containing the exact word.</p></section>';return}
    const chosen=words.slice(0,id==='matching'?options.pairs:id==='rush'?100:15);
    game={id,words:chosen,pool:words,index:0,score:0,hearts:3,misses:[],paused:false,done:false,answered:false,remaining:id==='rush'?60000:id==='typeit'?20000:12000,elapsed:0,last:Date.now(),matched:new Set(),selected:null,feedback:''};
    if(id==='matching')game.right=gameTools.shuffle(chosen);
    question(); timer=setInterval(tick,100);
  }
  function clue(w) {
    const mode=options.mode==='mixed'?(gameTools.sentence(w)&&Math.random()<.5?'sentence':'meaning'):options.mode;
    return mode==='hear'?'<button id="game-hear">▶ Hear German again</button>':esc(mode==='sentence'?gameTools.sentence(w):w.meaning);
  }
  function question() {
    if(!game||game.done)return;
    if(game.index>=game.words.length||game.hearts<=0)return finish();
    game.answered=false;game.feedback='';
    if(game.id!=='rush')game.remaining=game.id==='typeit'?20000:12000;
    game.last=Date.now();
    const w=game.words[game.index];
    if(game.id!=='matching'&&game.id!=='typeit'){
      const alternatives=game.pool.filter(x=>x.id!==w.id&&gameTools.normalize(x.meaning)!==gameTools.normalize(w.meaning)&&(x.meaningLang||'en')===(w.meaningLang||'en'));
      game.choices=gameTools.shuffle([w,...gameTools.shuffle(alternatives).slice(0,3)]);
    }
    game.clue=game.id==='matching'?'':clue(w); draw();
    if(options.mode==='hear'&&game.id!=='matching')speak(w);
  }
  function status() {
    return `<div class="game-status"><span>${game.id==='matching'?`<strong id="game-clock">${Math.floor(game.elapsed/1000)}s</strong> · ${game.matched.size}/${game.words.length} matched · ${game.misses.length} misses`:`<strong id="game-clock">${Math.ceil(game.remaining/1000)}s</strong> · Score ${game.score} ${game.id==='rush'?'':`· ${'♥'.repeat(game.hearts)} · Word ${game.index+1} of ${game.words.length}`}`}</span><button id="game-pause">${game.paused?'Resume':'Pause'}</button></div>`;
  }
  function draw() {
    if(!game||game.done)return;const w=game.words[game.index];
    let body='';
    if(game.paused)body='<section class="card game-intro"><h2>Paused</h2><button id="game-resume" class="dark">Go on</button></section>';
    else if(game.id==='matching')body=`<div class="matching-grid"><div>${game.words.map(x=>`<button class="match-tile ${game.selected===x.id?'selected':''} ${game.matched.has(x.id)?'matched':''}" data-match-word="${esc(x.id)}" ${game.matched.has(x.id)?'disabled':''} lang="de">${esc(title(x))}</button>`).join('')}</div><div>${game.right.map(x=>`<button class="match-tile ${game.matched.has(x.id)?'matched':''}" data-match-clue="${esc(x.id)}" ${game.matched.has(x.id)?'disabled':''}>${esc(options.mode==='sentence'?gameTools.sentence(x):x.meaning)}</button>`).join('')}</div></div><p role="status">${esc(game.feedback||'Select a German word, then its match.')}</p>`;
    else body=`<section class="card game-clue"><div class="eyebrow">${options.mode==='hear'?'WHICH GERMAN WORD DO YOU HEAR?':'WHICH GERMAN WORD FITS?'}</div><div class="game-clue-text">${game.clue}</div></section>${game.answered?`<section class="card game-feedback"><h2>${esc(game.feedback)}</h2><p lang="de">${esc(title(w))}</p><p>${esc(w.meaning)}</p><button id="game-next" class="dark">${game.hearts>0&&game.index+1<game.words.length?'Next word':'See results'}</button></section>`:game.id==='typeit'?`<section class="card"><p class="game-hint" lang="de">${esc(Array.from(w.word).map((c,i)=>i===0||!/[\p{L}\p{N}]/u.test(c)?c:'_').join(' '))}</p><form id="game-type-form"><label for="game-answer">German word or expression</label><input id="game-answer" lang="de" autocomplete="off" spellcheck="false" autocapitalize="off" required><div class="actions">${['ä','ö','ü','ß'].map(c=>`<button type="button" data-game-letter="${c}">${c}</button>`).join('')}<button class="dark" type="submit">Check answer ↵</button><button type="button" id="game-skip">Skip</button></div></form></section>`:`<div class="${game.id==='shooter'?'shooter-arena':'rush-choices'}">${game.choices.map((x,i)=>`<button data-game-choice="${esc(x.id)}" class="${game.id==='shooter'?'falling-word':''}" style="--lane:${i}" lang="de">${esc(title(x))}</button>`).join('')}</div>`}`;
    $('#game-stage').innerHTML=status()+body;
    if(game.id==='typeit'&&!game.paused&&!game.answered)$('#game-answer')?.focus();
  }
  function tick() {
    if(!game||game.done)return;const now=Date.now(),delta=now-game.last;game.last=now;
    if(game.paused||(game.answered&&game.id!=='rush'))return;
    if(game.id==='matching'){game.elapsed+=delta;const clock=$('#game-clock');if(clock)clock.textContent=Math.floor(game.elapsed/1000)+'s';return}
    game.remaining=Math.max(0,game.remaining-delta);
    const clock=$('#game-clock');if(clock)clock.textContent=Math.ceil(game.remaining/1000)+'s';
    if(game.id==='shooter'){$('.shooter-arena')?.style.setProperty('--fall',String((1-game.remaining/12000)*220)+'px')}
    if(game.remaining===0){if(game.id==='rush')finish();else answer(false,'Time’s up.');}
  }
  function answer(ok,feedback) {
    if(!game||game.done||game.paused||game.answered)return;
    game.answered=true;game.feedback=feedback||(ok?'Correct!':'Keep this word in mind.');
    game.score=Math.max(0,game.score+(ok?100:-25));
    if(!ok){game.misses.push(game.words[game.index]);if(game.id!=='rush')game.hearts--}
    draw();
  }
  function finish() {
    if(!game||game.done)return;game.done=true;clearInterval(timer);timer=null;
    if(game.id==='matching')game.score=Math.max(0,game.words.length*100-game.misses.length*25-Math.floor(game.elapsed/1000));
    const missed=[...new Map(game.misses.map(w=>[w.id,w])).values()];
    $('#game-stage').innerHTML=`<section class="card game-intro"><div class="eyebrow">ROUND COMPLETE</div><h2>${game.score} points</h2><p>${game.id==='matching'?`${game.words.length} pairs matched in ${Math.floor(game.elapsed/1000)} seconds.`:`${game.index+(game.answered?1:0)} words played · ${game.misses.length} missed.`}</p><button id="game-start" class="dark">Play again</button></section>${missed.length?`<h2>Words to revisit</h2><div class="game-revisit">${missed.map(w=>`<div class="card"><h3 lang="de">${esc(title(w))}</h3><p>${esc(w.meaning)}</p>${audio(w)}</div>`).join('')}</div>`:''}`;
  }
  const beforeGamesRender=render;
  render=function(){stop();beforeGamesRender();const id=route();if(pages[id])$('#app').innerHTML=page(id)};
  document.addEventListener('change',e=>{const key={'game-mode':'mode','game-rating':'rating','game-list':'list','game-pairs':'pairs'}[e.target.id];if(key){options[key]=key==='pairs'?Number(e.target.value):e.target.value;render()}});
  document.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b||!pages[route()])return;
    if(b.id==='game-start'||b.id==='game-new'){start();return}
    if(!game||game.done)return;
    if(b.id==='game-pause'||b.id==='game-resume'){game.paused=!game.paused;game.last=Date.now();draw();return}
    if(game.paused)return;
    if(b.id==='game-hear')speak(game.words[game.index]);
    else if(b.id==='game-next'){game.index++;game.answered=false;question()}
    else if(b.id==='game-skip')answer(false,'Skipped.');
    else if(b.dataset.gameChoice)answer(b.dataset.gameChoice===game.words[game.index].id);
    else if(b.dataset.gameLetter){const input=$('#game-answer');const start=input.selectionStart,end=input.selectionEnd;input.setRangeText(b.dataset.gameLetter,start,end,'end');input.focus()}
    else if(b.dataset.matchWord){game.selected=b.dataset.matchWord;game.feedback='Now choose its match.';draw()}
    else if(b.dataset.matchClue){if(!game.selected){game.feedback='Select a German word first.';draw();return}if(game.selected===b.dataset.matchClue){game.matched.add(game.selected);game.feedback='Correct pair!'}else{game.misses.push(game.words.find(w=>w.id===game.selected));game.feedback='Try another pair.'}game.selected=null;if(game.matched.size===game.words.length)finish();else draw()}
  });
  document.addEventListener('submit',e=>{if(e.target.id==='game-type-form'){e.preventDefault();if(game&&!game.paused)answer(gameTools.accepts(game.words[game.index],$('#game-answer').value))}});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&game&&!game.done&&!game.paused){game.paused=true;draw()}});
  window.addEventListener('pagehide',stop);
  render();
})();
