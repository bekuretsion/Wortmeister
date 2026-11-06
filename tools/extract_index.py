import json,re,pathlib,collections
out=pathlib.Path(__file__).resolve().parents[1]/'tmp'/'pdfs';items=[];pending=''
for i in range(124,130):
    text=(out/f'page-{i:03d}.txt').read_text(encoding='utf8')
    for line in text.splitlines():
        line=line.strip()
        if not line or re.fullmatch(r'[A-Za-z]|\d{3}',line) or line.startswith(('Alphabetisches','Die Zahlen','Eigene Notizen')):continue
        m=re.match(r'(.+?)\s+(\d{1,3})\s*$',line)
        if m and 6<=int(m[2])<=104:
            items.append({'expression':re.sub(r'\s+',' ',pending+' '+m[1]).strip().replace(' I ',' / ').replace(' und 0',' und O'),'page':int(m[2])});pending=''
        else:pending+=' '+line
items=list({(x['expression'],x['page']):x for x in items}.values())
(out/'index.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
print('Index entries:',len(items));print(collections.Counter(x['page'] for x in items));print('Pending:',pending)
