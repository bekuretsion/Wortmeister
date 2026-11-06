"""Build a German-English collection. No source-language text or transliteration is retained."""
import pathlib,re,json,hashlib,unicodedata,collections
ROOT=pathlib.Path(__file__).resolve().parents[1];TMP=ROOT/'tmp'/'dictionary'
raw=json.loads((TMP/'pairs.json').read_text(encoding='utf8'))
def clean(s):
 s=unicodedata.normalize('NFC',s).replace('\u00ad','')
 s=re.sub(r'\s+',' ',s).strip(' ,;:.║◊')
 s=re.sub(r'\(\s*\)|\[\s*\]','',s)
 s=re.sub(r'\s+([,;.?!])',r'\1',s)
 s=re.sub(r'([,;])(?=[A-Za-zÄÖÜäöüß])',r'\1 ',s)
 s=re.sub(r'^\s*(?:(?:[IVX]+|\d+)[.)]?\s+)+','',s)
 # An unfinished parenthetical cross-reference does not belong in a learning gloss.
 if s.count('(')>s.count(')'):s=s[:s.rfind('(')].strip()
 return re.sub(r'\s+',' ',s).strip(' ,;:')
def alternatives(text):
 result=[];part='';depth=0
 for ch in text:
  if ch in '([':depth+=1
  if ch in ')]':depth=max(0,depth-1)
  if depth==0 and ch in ',;':
   if part.strip():result.append(part.strip())
   part=''
  else:part+=ch
 if part.strip():result.append(part.strip())
 return result
pairs=[];entries={};excluded=[]
for original in raw:
 de,en=clean(original['german']),clean(original['english'])
 de=re.sub(r'^(?:(?:eth|er|gz|amh|fig|a|s)\.\s*)+','',de)
 de=re.sub(r'^(?:(?:n|v|adj|adv|num|pron|conj|prep|part|interj|med|bot|zool|coll|arch|obs|f|m|sg|pl|impers)\.\s*)+','',de)
 de=re.sub(r'^\s*[.()\s]+','',de)
 if(re.search(r'letter.*order|order.*letter',en,re.I)and len(de.split())<3)or re.search(r'[ǝʿʾḫḳḥṣṭǧ]',de)or not de or not en:
  excluded.append({'page':original['page'],'german':de,'reason':'Source-letter name, transliteration, or empty translation'});continue
 terms=alternatives(de)
 if not terms:continue
 rowid=len(pairs)
 pair={'german':de,'english':en,'page':original['page'],'pdfPage':original['pdfPage'],'section':original['section'],'labels':sorted(set(original.get('labels',[]))),'mode':original.get('mode','lexical'),'entryIds':[]}
 for position,term in enumerate(terms):
  forms=re.findall(r'\([^)]*(?:~|-[a-zäöüß])[^)]*\)',term)
  lemma=re.sub(r'\([^)]*(?:~|-[a-zäöüß])[^)]*\)','',term)
  lemma=clean(lemma)
  lemma=re.sub(r'^[!?,;:]+\s*','',lemma)
  if lemma.strip(' .…').lower()in['would','could','should','may','must','if','the','with','of']:continue
  if len(lemma)<2 or re.fullmatch(r'(?:etw|jmd|jdn|jdm|s|a|n|v|adj|adv|num|pl|f|m)\.?',lemma,re.I):continue
  article=''
  markers=original.get('articles',[])
  noun=bool(re.fullmatch(r'[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]+',lemma))
  if noun and len(markers)==len(terms):article=markers[position]
  elif noun and len(set(markers))==1:article=markers[0]
  key=article+'|'+lemma
  id='dict-'+hashlib.sha256(key.encode()).hexdigest()[:14]
  entry=entries.setdefault(key,{'id':id,'word':lemma,'article':article,'forms':'','meaning':en,'meaningLang':'en','level':'Dictionary','domain':'Dictionary vocabulary','domains':['Dictionary vocabulary'],'example':'','translation':'','note':'German-English translation extracted from the supplied dictionary. See the source sense and page reference.','entryType':'word'if ' 'not in lemma else'expression','dictionaryRefs':[],'source':{'collection':'dictionary','title':'German-English dictionary import','page':original['page'],'pdfPage':original['pdfPage'],'chapter':original['section']},'_forms':set(),'_sections':set(),'_meanings':set()})
  entry.setdefault('_modes',set()).add(original.get('mode','lexical'))
  entry['_forms'].update(forms);entry['_sections'].add(original['section']);entry['_meanings'].add(en)
  if rowid not in entry['dictionaryRefs']:entry['dictionaryRefs'].append(rowid)
  pair['entryIds'].append(id)
 if pair['entryIds']:pairs.append(pair)
 # If every term was a placeholder, rowid is reused safely by the next accepted pair.
words=[]
for entry in entries.values():
 entry['forms']='; '.join(sorted(entry.pop('_forms')))
 sections=entry.pop('_sections')
 modes=entry.pop('_modes')
 entry['searchText']=' '.join(sorted(entry.pop('_meanings')))
 if sections=={'Geographical names'}:entry['domains']=['Dictionary names'];entry['domain']='Dictionary names'
 elif sections=={'Abbreviations'}:entry['domains']=['Dictionary abbreviations'];entry['domain']='Dictionary abbreviations'
 elif entry['entryType']=='expression':entry['domains']=['Dictionary expressions'];entry['domain']='Dictionary expressions'
 if modes=={'explanatory'}:entry['domains']=['Dictionary explanations'];entry['domain']='Dictionary explanations';entry['lookupOnly']=True;entry['note']='Source grammatical explanation or reference text. Available for lookup; excluded from study and quizzes.'
 words.append(entry)
words.sort(key=lambda w:(w['word'].casefold(),w['article']))
data={'source':{'title':'German-English dictionary import','authors':'Yaroslav Gutgarts; Filip Busau','publisher':'Harrassowitz Verlag','isbn':'9783447119870'},'pairs':pairs,'entries':words}
serialized=json.dumps(data,ensure_ascii=False,separators=(',',':'))
if re.search(r'[\u1200-\u139f\u2d80-\u2ddf\uab00-\uab2f]',serialized):raise ValueError('Source-language characters in output')
(ROOT/'seeds/dictionary-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'seeds/dictionary.js').write_text('/* German and English only. Generated from the user-provided PDF. */\nconst DICTIONARY_DATA='+serialized+';\nconst DICTIONARY_PAIRS=DICTIONARY_DATA.pairs;\nWORDS.push(...DICTIONARY_DATA.entries);\nSCOPES.push("Dictionary · All","Dictionary · Words","Dictionary · Expressions","Dictionary · Names");\nDOMAINS["Dictionary · All"]=["Dictionary vocabulary","Dictionary expressions","Dictionary names","Dictionary abbreviations","Dictionary explanations"];\nDOMAINS["Dictionary · Words"]=["Dictionary vocabulary","Dictionary abbreviations"];\nDOMAINS["Dictionary · Expressions"]=["Dictionary expressions"];\nDOMAINS["Dictionary · Names"]=["Dictionary names"];\n',encoding='utf8')
audit={'sourceTranslationPairs':len(raw),'retainedTranslationPairs':len(pairs),'uniqueEntries':len(words),'words':sum(e['entryType']=='word'for e in words),'expressions':sum(e['entryType']=='expression'for e in words),'byDomain':dict(collections.Counter(e['domain']for e in words)),'excludedRows':excluded,'pdfPageRange':[min(p['pdfPage']for p in pairs),max(p['pdfPage']for p in pairs)],'containsSourceScript':False,'extraction':json.loads((TMP/'extraction-audit.json').read_text(encoding='utf8'))}
(ROOT/'docs/audits/dictionary-import-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in audit.items()if k!='excludedRows'},ensure_ascii=True,indent=2));print('Excluded source-letter/transliteration rows:',len(excluded));print('Browser data bytes:',len(serialized.encode()))
