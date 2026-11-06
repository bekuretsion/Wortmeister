const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const files=['index.html','static/favicon.svg','.nojekyll','static/css/style.css','static/css/reference.css','seeds/words.js','seeds/domains.js','seeds/book.js','seeds/dictionary.js','app/app.js','app/reference.js','app/book-ui.js','app/dictionary-ui.js','app/games.js','static/css/games.css'];
const destination=path.join(root,'publish');
fs.mkdirSync(destination,{recursive:true});
for(const name of files){fs.mkdirSync(path.dirname(path.join(destination,name)),{recursive:true});fs.copyFileSync(path.join(root,name),path.join(destination,name));}
console.log(`Prepared ${files.length} public site files in publish/`);
