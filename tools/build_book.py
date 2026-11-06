import json,re,pathlib,hashlib,collections
root=pathlib.Path(__file__).resolve().parents[1];out=root/'tmp'/'pdfs'
rows=json.loads((out/'rows.json').read_text(encoding='utf8'))
gloss=dict(line.split('=',1) for line in (root/'seeds/book-glosses.txt').read_text(encoding='utf8').splitlines() if '=' in line)
aliases={}
for lemma,forms in {
 'Arm':'Arme Armen','Auge':'Augen','Bein':'Beine Beinen','Berg':'Berge','Beste':'Besten','Bruch':'Brüche','Buchstabe':'Buchstaben','Bär':'Bären','Baum':'Bäume','Dach':'Dächern','Ei':'Eier','Elefant':'Elefanten','Eule':'Eulen','Faden':'Fäden','Fliege':'Fliegen','Fuß':'Füßen','Haar':'Haare Haaren','Hand':'Hände Händen','Herz':'Herzen','Hochzeit':'Hochzeiten','Hose':'Hosen','Horn':'Hörnern','Huhn':'Hühner Hühnern','Jubeljahr':'Jubeljahre','Kaiser':'Kaisers','Karte':'Karten','Kastanie':'Kastanien','Katze':'Katz','Kinderschuh':'Kinderschuhen','Kürzere':'Kürzeren','Leiche':'Leichen','Loch':'Löcher','Löffel':'Löffeln','Nacht':'Nächte','Nessel':'Nesseln','Niere':'Nieren','Ohr':'Ohren','Perle':'Perlen','Pferd':'Pferde','Pfund':'Pfunden','Pilz':'Pilze','Rippe':'Rippen','Rolle':'Rollen','Saite':'Saiten','Samthandschuh':'Samthandschuhen','Sand':'Sande','Schild':'Schilde','Schuh':'Schuhe','Schwarz':'Schwarze','Segel':'Segeln','Socke':'Socken','Spatz':'Spatzen','Stein':'Steine','Stern':'Sternen','Strang':'Stränge','Stuhl':'Stühle','Sau':'Säue','Teufel':'Teufels','Tomate':'Tomaten','Trockene':'Trockenen','Wasser':'Wassern','Weg':'Wege','Weiche':'Weichen','Zelt':'Zelte','Zahn':'Zähne Zähnen',
 'abholen':'abgeholt','anbinden':'angebunden','bestellen':'bestellt','beißen':'beißt','drücken':'drückt','erfinden':'erfunden','fallen':'fällt gefallen','geben':'gibt','gehen':'geht','geraten':'geraten','haben':'hat','halten':'hält','hängen':'hängt','kommen':'kommt','krähen':'kräht','laufen':'läuft','legen':'legt','liegen':'liegt','lügen':'lügt','machen':'macht','reißen':'reißt','sein':'ist sind sei','stehen':'steht','stören':'stört','waschen':'wäscht gewaschen','wachsen':'gewachsen','werfen':'geworfen','zerstören':'zerstört','treten':'getreten','schneiden':'geschnitten','springen':'gesprungen','brechen':'gebrochen',
 'alt':'alter','böse':'bösen','eng':'enger','falsch':'falsche falschen','frei':'freie','frech':'freches','fest':'festen','golden':'goldene','grau':'grauen','groß':'große großem großen größer','grün':'grünen','gut':'gute guten gutes','heiß':'heißen heißes','hoch':'hohe hohen hohes','inner':'inneren','kalt':'kalte','klein':'kleinen','komisch':'komischer','lang':'lange langes','leicht':'leichte','letzte':'letzten','links':'linke','los':'loses','neu':'neuen','recht':'rechten','rein':'reinen','richtig':'richtigen','roh':'rohes','sauer':'sauren','schief':'schiefe','schlecht':'schlechte','schmutzig':'schmutzige','schräg':'schräger','schwarz':'schwarze schwarzen','schön':'schöne','tot':'tote','unbeschrieben':'unbeschriebenes','wahr':'wahres','wirtschaftlich':'wirtschaftlichen','zweischneidig':'zweischneidiges',
 'blau':'blauen blaues Blaue','wenden':'gewendet','pellen':'gepellt','eigen':'eigene','Loch':'loch','machen':'gemachte gemachter','verlieren':'verloren','fressen':'gefressen','herrschen':'herrscht','drucken':'gedruckt','wund':'wunder','begossen':'begossener'
}.items():
 for form in forms.split():aliases[form]=lemma
aliases.update({'macht':'machen','Löcher':'Loch','herauskönnen':'können'})
functionGloss='''ab=away; off
aber=but; however
alle=all
allen=all (inflected form)
aller=all (inflected form)
alles=everything
als=as; than
am=at the; on the (an dem)
an=at; on; to
andere=other
ans=to the (an das)
auf=on; onto
aufs=onto the (auf das)
beide=both
beiden=both (inflected form)
beim=at the; while (bei dem)
da=there
danach=after that; according to that
das=the; that (neuter)
dass=that (conjunction)
dem=the (dative masculine or neuter)
den=the (accusative masculine or dative plural)
der=the (masculine nominative and other case forms)
des=the (genitive masculine or neuter)
die=the (feminine or plural)
dieselbe=the same
diesem=this (dative)
durch=through; by
durchs=through the (durch das)
ein=a; an; one
eine=a; an; one (feminine)
einem=a; an; one (dative)
einen=a; an; one (accusative masculine)
einer=a; an; one (inflected)
einmal=once
einzeln=individually; separately
erste=first
es=it
etwas=something; somewhat
für=for
heran=toward; closer
heraus=out; outward
hinein=in; inward
hinter=behind
hinters=behind the (hinter das)
hier=here
im=in the (in dem)
in=in; into
ins=into the (in das)
ja=yes; indeed
jedes=each; every (neuter)
jemand=someone
jemandem=someone (dative)
jemanden=someone (accusative)
jemandes=someone’s (genitive)
jetzt=now
kein=no; not a
keine=no; none (inflected)
keinen=no; none (inflected)
keiner=no one; none
man=one; people in general
mehr=more
mehrere=several
mich=me (accusative)
mit=with
nach=after; to; according to
nur=only
oder=or
raus=out (colloquial)
seine=his; her; its; one’s (inflected possessive)
seinem=his; its; one’s (dative possessive)
seinen=his; its; one’s (inflected possessive)
seiner=his; its; one’s (inflected possessive)
sich=oneself; himself; herself; itself; themselves
so=so; like that
um=around; at; about
ums=around the (um das)
und=and
unter=under; among
unterm=under the (unter dem)
vier=four
vom=from the (von dem)
von=from; of; by
vor=before; in front of
vorm=before the; in front of the (vor dem)
weder=neither
weg=away
wegen=because of
wie=how; like; as
wo=where
zehn=ten
zu=to; too
zuleide=harm (in jemandem etwas zuleide tun)
zum=to the (zu dem)
zur=to the (zu der)
zusammen=together
zwei=two
zwischen=between
über=over; about
übers=over the (über das)'''
gloss.update(dict(line.split('=',1)for line in functionGloss.splitlines()))
patches={'die Hände in den Schoßlegen':'die Hände in den Schoß legen','auf dem laufenden sein':'auf dem Laufenden sein','die Kohle heran schaffen':'die Kohle heranschaffen','nurBahnhofve~tehen':'nur Bahnhof verstehen'}
expressions=[]
for row in rows:
 text=row['index'][0] if row['index'] and row['index'][1]>.72 else row['expression']
 for a,b in patches.items():text=text.replace(a,b)
 text=re.sub(r'\((?:ugs|sal|geh)\.?\)','',text).strip().replace(' so/.',' sal.')
 text=text.replace(' den leim ',' den Leim ').replace(' licht ',' Licht ').replace(' laufenden ',' Laufenden ').replace(' an land ',' an Land ').replace(' eine laus ',' eine Laus ').replace('hera us','heraus')
 text=re.sub(r'\s+',' ',text)
 text=re.sub(r'^\d+\s+','',text);text=re.sub(r'\s+([,.!?])',r'\1',text)
 text=text.replace(' loch ',' Loch ').replace('viel von jemanden halten','viel von jemandem halten')
 meaning=row['meaning'].replace('einerneuen','einer neuen').replace('trotzgroßer','trotz großer').replace('viel leisten','viel leisten').replace('Weft','Welt').replace('Vergongenes','Vergangenes').replace('Geschwindig keit','Geschwindigkeit').replace('vielleisten','viel leisten').replace(' v o r ',' vor ').replace('odernehmen','oder nehmen')
 meaning=re.sub(r'\s+\d+$','',meaning)
 example=row['example']
 if not example:example={'den Bach runtergehen':'Ohne einen neuen Plan geht das Projekt den Bach runter.','jemanden an den Bettelstab bringen':'Die hohen Schulden haben ihn an den Bettelstab gebracht.','im Schneckentempo':'Im Stau kommen wir nur im Schneckentempo voran.'}.get(text,'')
 id='book-expr-'+hashlib.sha256((str(row['page'])+text).encode()).hexdigest()[:12]
 reg=next((v for k,v in [('ugs','colloquial'),('sal','very informal'),('geh','formal / literary')]if k in row['expression']),'not marked')
 expressions.append(dict(id=id,word=text,article='',forms='',meaning=meaning,meaningLang='de',level='Book',domain='Idioms & expressions',domains=['Idioms & expressions','Book expressions'],example=example,translation='',note='Study the figurative meaning of the whole expression. Register: '+reg+'.',entryType='expression',source={'title':'Das A und O · Deutsche Redewendungen','authors':'Katja Ullmann; Carlos Ampie Loria','page':row['page'],'chapter':row['chapter']},keywords=row['keywords']))
words={};unknown=collections.Counter()
for e in expressions:
 text=e['word'].replace('Geld(beutel)','Geldbeutel').replace('alle(s)','alles').replace('sein(e)','seine').replace('Hals(e)','Hals').replace('(heraus)können','herauskönnen')
 for token in re.findall(r'[A-Za-zÄÖÜäöüß]+',text):
  if token in ['I','s','e','ugs','sal','geh']:continue
  lemma=aliases.get(token,aliases.get(token.lower(),token))
  if lemma not in gloss and lemma.lower()in gloss:lemma=lemma.lower()
  if lemma not in gloss:
   candidates=[lemma[:-len(s)]for s in ['en','er','em','es','e','n']if lemma.endswith(s)]
   lemma=next((c for c in candidates if c in gloss),lemma)
  if lemma not in gloss:unknown[lemma]+=1
  w=words.setdefault(lemma,dict(word=lemma,relatedExpressions=[],surfaceForms=set()))
  w['surfaceForms'].add(token)
  if e['id']not in w['relatedExpressions']:w['relatedExpressions'].append(e['id'])
result=[]
for lemma,w in sorted(words.items(),key=lambda x:x[0].casefold()):
 related=next(e for e in expressions if e['id']==w['relatedExpressions'][0]);known=lemma in gloss
 result.append(dict(id='book-word-'+hashlib.sha256(lemma.encode()).hexdigest()[:12],word=lemma,article='',forms='Source forms: '+', '.join(sorted(w['surfaceForms'])),meaning=gloss.get(lemma,'Source word; see the linked expression and dictionary for its literal meaning.'),level='Book',domain='Book words',domains=['Book words'],example=related['example'],translation='',note='Literal word meaning is separate from the figurative meaning of an expression. '+(''if known else'Literal definition is not yet reviewed; this word is excluded from review and quizzes.'),entryType='word',lookupOnly=not known,relatedExpressions=w['relatedExpressions'],source=related['source']))
data={'expressions':expressions,'words':result}
for expression in expressions:
 expression['componentIds']=[w['id'] for w in result if expression['id']in w['relatedExpressions']]
(root/'seeds/book-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
(root/'seeds/book.js').write_text('// Extracted from the user-provided PDF; see individual source page references.\nconst BOOK_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\nWORDS.push(...BOOK_DATA.expressions,...BOOK_DATA.words);\nSCOPES.push("Book · Expressions","Book · Words");\nDOMAINS["Book · Expressions"]=["Book expressions"];\nDOMAINS["Book · Words"]=["Book words"];\n',encoding='utf8')
(out/'unknown.json').write_text(json.dumps(unknown,ensure_ascii=False,indent=2),encoding='utf8')
print('Expressions:',len(expressions),'Words:',len(result),'Missing literal glosses:',len(unknown));print(json.dumps(unknown,ensure_ascii=True))
