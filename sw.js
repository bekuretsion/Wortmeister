const CACHE='wortmeister-mobile-v1';
const FILES=['./','index.html','manifest.webmanifest','static/favicon.svg','static/icons/icon-192.png','static/icons/icon-512.png','static/icons/apple-touch-icon.png','static/css/style.css','static/css/reference.css','static/css/games.css','static/css/mobile.css','seeds/words.js','seeds/domains.js','seeds/book.js','seeds/dictionary.js','app/app.js','app/reference.js','app/book-ui.js','app/dictionary-ui.js','app/games.js','app/mobile.js'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES))));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('wortmeister-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);
  if(event.request.method!=='GET'||url.origin!==self.location.origin||!url.pathname.startsWith(new URL('./',self.location.href).pathname))return;
  const relative=url.pathname.slice(new URL('./',self.location.href).pathname.length);
  if(!FILES.includes(relative||'./'))return;
  event.respondWith(fetch(event.request).then(response=>{
    if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(event.request,copy)))}
    return response;
  }).catch(async()=>{
    const cache=await caches.open(CACHE);
    return await cache.match(event.request,{ignoreSearch:true})||(event.request.mode==='navigate'?await cache.match('index.html'):Response.error());
  }));
});
