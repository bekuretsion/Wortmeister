import json,re,pathlib,pdfplumber
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp'/'pdfs'
chapters=[(6,'Arbeiten und Lernen'),(22,'Freizeit'),(30,'Familie'),(40,'Persönlichkeit und Charakter'),(50,'Alltag'),(64,'Geld'),(72,'Von Mensch zu Mensch'),(86,'Kommunikation'),(96,'Tierisches')]
def clean(s):
    s=re.sub(r'\s+',' ',s).strip()
    s=s.replace(' I ',' / ').replace(' und 0',' und O').replace('Ieiter','leiter')
    return s
entries=[]
with pdfplumber.open(r'C:\Users\bekur\Downloads\das-a-und-o-deutsche-redewendungen_compress.pdf') as doc:
    for page in range(6,105,2):
        p=doc.pages[page]
        words=p.extract_words(extra_attrs=['fontname'])
        left=[w for w in words if 48<w['x0']<159 and 65<w['top']<785]
        lines=[]
        for w in sorted(left,key=lambda w:(round(w['top']/3),w['x0'])):
            if not lines or abs(w['top']-lines[-1][0]['top'])>3:lines.append([w])
            else:lines[-1].append(w)
        groups=[]
        for line in lines:
            if not groups or line[0]['top']-groups[-1][-1][0]['top']>19:groups.append([line])
            else:groups[-1].append(line)
        for i,g in enumerate(groups):
            top=min(w['top'] for line in g for w in line)-2
            bottom=(min(w['top'] for line in groups[i+1] for w in line)-3) if i+1<len(groups) else 780
            expression=clean(' '.join(w['text'] for line in g for w in sorted(line,key=lambda w:w['x0'])))
            keywords=clean(' '.join(w['text'] for line in g for w in sorted(line,key=lambda w:w['x0']) if 'Bold' in w['fontname']))
            meaning=clean(p.crop((160,top,299,bottom)).extract_text() or '')
            example=clean(p.crop((300,top,550,bottom)).extract_text() or '')
            if len(expression)>3:
                entries.append(dict(expression=expression,keywords=keywords,meaning=meaning,example=example,page=page,chapter=next(t for start,t in reversed(chapters) if page>=start)))
(OUT/'book-entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'review.txt').write_text('\n'.join(f"{i:03d} | {e['page']} | {e['expression']} | {e['keywords']} | {e['meaning']}" for i,e in enumerate(entries)),encoding='utf8')
print('Extracted',len(entries),'entries')
