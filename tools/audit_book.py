import json,pathlib,difflib,re
root=pathlib.Path(__file__).resolve().parents[1];tmp=root/'tmp'/'pdfs'
book=json.loads((root/'seeds/book-data.json').read_text(encoding='utf8'));index=json.loads((tmp/'index.json').read_text(encoding='utf8'))
def norm(s):return re.sub(r'[^a-zäöüß]','',s.lower()).replace('jemanden','jemand').replace('jemandem','jemand')
matches=[]
for ref in index:
 candidates=[e for e in book['expressions'] if e['source']['page']==ref['page']]
 best=max(candidates,key=lambda e:difflib.SequenceMatcher(None,norm(e['word']),norm(ref['expression'])).ratio())
 score=difflib.SequenceMatcher(None,norm(best['word']),norm(ref['expression'])).ratio()
 matches.append(dict(index=ref,entry=best['word'],id=best['id'],similarity=round(score,3)))
report={'index_references':len(index),'extracted_expressions':len(book['expressions']),'individual_words':len(book['words']),'unmatched_index_references':[m for m in matches if m['similarity']<.72],'references_matching_same_entry':{id:[m['index']['expression']for m in matches if m['id']==id]for id in set(m['id']for m in matches)if sum(m['id']==id for m in matches)>1},'matches':matches}
(root/'docs/audits/book-import-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items()if k!='matches'},ensure_ascii=True,indent=2))
