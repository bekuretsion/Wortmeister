"""Extract only German/English translation pairs using the PDF's documented typography."""
import pathlib,json,re,sys,unicodedata,hashlib,collections
from pypdf import PdfReader
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'tmp'/'dictionary';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=pathlib.Path(r'C:\Users\bekur\Downloads\tigrinischdeutschenglisches-worterbuch-tigrinyagermanenglish-dictionary-344711987x-9783447119870_compress.pdf')
ETHIOPIC=re.compile(r'[\u1200-\u139f\u2d80-\u2ddf\uab00-\uab2f]')
ETHIOPIC_LETTER=re.compile(r'[\u1200-\u135a\u2d80-\u2ddf\uab00-\uab2f]')
LATIN=re.compile(r'[A-Za-zÄÖÜäöüßÀ-ÿ]')
def clean(s):
 s=ETHIOPIC.sub('',s);s=unicodedata.normalize('NFC',s)
 s=re.sub(r'\s+',' ',s).strip(' \n\t,;:.║◊')
 s=re.sub(r'\s+([,;.!?)\]])',r'\1',s);s=re.sub(r'([\[(])\s+',r'\1',s)
 s=re.sub(r'([,;])(?=[A-Za-zÄÖÜäöüß])',r'\1 ',s)
 s=re.sub(r'\s+-\s*$','',s)
 s=re.sub(r'^\d+[.)]\s*','',s)
 return s
class Extractor:
 def __init__(self):self.de='';self.en='';self.side='idle';self.pairs=[];self.page=0;self.origin=0;self.prev=None;self.genders=[];self.separators=0;self.unpaired=[];self.pendingFlags=[];self.flags=[];self.trace=[];self.missingSamples=[];self.regular='';self.mode='lexical'
 def finish(self):
  de,en=clean(self.de),clean(self.en)
  if LATIN.search(de) and LATIN.search(en)and not any(t in de for t in ['Geografische Namen','Geographical Names','Gängige tigrinische','Common Tigrinya']):self.pairs.append({'german':de,'english':en,'pdfPage':self.origin+1,'page':self.origin-66,'section':'Geographical names'if 597<=self.origin<=608 else'Abbreviations'if self.origin>=609 else'Vocabulary','articles':[{'ተባ':'der','ኣን':'die','ኣጓ':'das'}[g]for g in self.genders],'labels':self.flags[:],'mode':self.mode})
  self.de='';self.en='';self.side='idle';self.genders=[];self.prev=None;self.flags=[];self.mode='lexical'
 def add(self,side,text,x,y):
  old=getattr(self,side)
  # A falling text baseline or a new column identifies a printed line wrap.
  wrap=self.prev and (abs(y-self.prev[1])>3 or (x-self.prev[0]>170))
  if wrap and old:
   if old.rstrip().endswith('-')and not re.search(r'[A-Za-z]+-[A-Za-z]+-$',old.rstrip()):old=old.rstrip()[:-1].rstrip()
   elif not old.endswith(' '):old+=' '
  setattr(self,side,old+text.replace('\n',' '));self.prev=(x,y)
 def visit(self,text,cm,tm,font,size):
  if not text:return
  font=str((font or {}).get('/BaseFont',''));x,y=tm[4],tm[5]
  if y and (y<70 or y>698):return
  if 'Helvetica'in font:return
  self.trace=(self.trace+[(ETHIOPIC.sub('[omitted]',text),font.split('PS')[-1],size)])[-15:]
  if ETHIOPIC.search(text):
   if size>=10 and ETHIOPIC_LETTER.search(text):
    if self.side=='en':self.finish()
    self.regular=''
   if self.side=='de' and size<10 and text.strip()in['ተባ','ኣን','ኣጓ']:self.genders.append(text.strip())
   return
  if '║'in text:
   self.separators+=1
   before,after=text.split('║',1)
   fallback=self.regular;self.regular=''
   if self.side=='en':self.finish()
   if not self.de and LATIN.search(fallback):
    self.de=clean(fallback);self.origin=self.page;self.mode='explanatory'
   if LATIN.search(before):
    if self.side=='idle':self.origin=self.page;self.side='de'
    self.add('de',before,x,y)
   if self.de:self.side='en';self.prev=None
   else:
    self.unpaired.append(self.page+1)
    if len(self.missingSamples)<20:self.missingSamples.append({'pdfPage':self.page+1,'context':self.trace[:]})
   if after.strip()and self.side=='en':self.add('en',after,x,y)
   return
  deBold=('Bold'in font or(self.page>=597 and 'TimesNewRomanPSMT'in font))and 'Italic'not in font
  enItalic='Italic'in font
  if deBold and LATIN.search(text):
   if re.fullmatch(r'\s*[IVX]+\s*',text):return
   if self.page>=597 and any(h in text for h in ['Geografische Namen','Geographical Names','Gängige tigrinische','Common Tigrinya']):return
   if self.side=='en':self.finish()
   self.regular=''
   if self.side=='idle':self.origin=self.page;self.side='de';self.flags=self.pendingFlags;self.pendingFlags=[]
   self.add('de',text,x,y)
  elif self.side=='en'and enItalic:self.add('en',text,x,y)
  elif self.side in['de','en'] and not LATIN.search(text) and re.search(r'[,;:/()\[\]?!\-–—.]',text):
   # Sense numbers are not vocabulary; punctuation is retained without source-language text.
   if not re.search(r'\d',text):self.add(self.side,text,x,y)
  elif self.side=='de'and enItalic:
   # A new transliteration without an English separator means an unfinished cross-reference.
   if LATIN.search(text):self.de='';self.side='idle';self.prev=None
  elif self.side=='idle'and enItalic:self.regular=''
  elif 'TimesNewRomanPSMT'in font and LATIN.search(text)and self.side!='de':
   self.regular+=' '+text.replace('\n',' ')
   self.pendingFlags.extend(re.findall(r'\b(?:tabu!|coll\.|vulg\.|fig\.|obs\.|arch\.|med\.|bot\.|zool\.|rel\.)',text))
  elif self.side=='idle':
   self.pendingFlags.extend(re.findall(r'\b(?:tabu!|coll\.|vulg\.|fig\.|obs\.|arch\.|med\.|bot\.|zool\.|rel\.)',text))
reader=PdfReader(SOURCE);extractor=Extractor()
start=int(sys.argv[1])if len(sys.argv)>1 else 69;stop=int(sys.argv[2])if len(sys.argv)>2 else 611
for i in range(start,min(stop,len(reader.pages))):
 extractor.page=i;reader.pages[i].extract_text(visitor_text=extractor.visit)
 if (i-start+1)%25==0:print(f'Processed {i-start+1}/{stop-start} pages; {len(extractor.pairs)} pairs',flush=True)
extractor.finish()
(OUT/'pairs.json').write_text(json.dumps(extractor.pairs,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'extraction-audit.json').write_text(json.dumps({'sourceSeparatorCount':extractor.separators,'translationPairs':len(extractor.pairs),'unpairedSeparatorCount':len(extractor.unpaired),'unpairedByPdfPage':dict(collections.Counter(extractor.unpaired))},indent=2),encoding='utf8')
(OUT/'missing-samples.json').write_text(json.dumps(extractor.missingSamples,ensure_ascii=False,indent=2),encoding='utf8')
print('Extracted translation pairs:',len(extractor.pairs))
print(json.dumps(extractor.pairs[:25],ensure_ascii=False,indent=2))
