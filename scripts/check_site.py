#!/usr/bin/env python3
"""Check generated local resources, chapter coverage, fragments, and image ratios."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,json,struct
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.images=[];self.title=False;self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:raise ValueError('Duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag=='title':self.title=True
  if tag=='h1':self.h1+=1
  if tag in ['a','link','script','img']:
   key='src' if tag in ['script','img'] else 'href'
   if a.get(key):self.links.append(a[key])
  if tag=='img':self.images.append(a)
def main():
 p=argparse.ArgumentParser();p.add_argument('--base-path',default='/Learn-Colorful/');p.add_argument('--output',default='build/site');a=p.parse_args();base=a.base_path.rstrip('/')+'/' if a.base_path!='/' else '/';out=(ROOT/a.output).resolve();pages={};count=0
 for f in out.rglob('*.html'):
  parsed=Page();parsed.feed(f.read_text());pages[f]=parsed
  if not parsed.title or parsed.h1!=1:raise SystemExit(f'Expected title and one h1: {f}')
 for f,page in pages.items():
  for value in page.links:
   url=urlsplit(value)
   if url.scheme or url.netloc:continue
   path=unquote(url.path)
   if path.startswith('/'):
    if not path.startswith(base):raise SystemExit(f'Incorrect base path: {f} {value}')
    target=out/path[len(base):]
   else:target=f.parent/path
   target=target.resolve()
   if not target.is_relative_to(out):raise SystemExit(f'Path escapes output: {value}')
   if target.is_dir():target=target/'index.html'
   if not target.is_file():raise SystemExit(f'Broken resource: {f} {value}')
   if url.fragment and target.suffix=='.html' and unquote(url.fragment) not in pages[target].ids:raise SystemExit(f'Broken fragment: {f} {value}')
   count+=1
  for im in page.images:
   if not im.get('alt') or not im.get('width') or not im.get('height'):raise SystemExit('Missing image accessibility/size '+str(f))
   target=out/unquote(urlsplit(im['src']).path)[len(base):];data=target.read_bytes()[:24];w,h=struct.unpack('>II',data[16:24])
   if (str(w),str(h))!=(im['width'],im['height']):raise SystemExit('Image aspect ratio mismatch '+str(f))
 manifest=json.loads((ROOT/'book.json').read_text());expected=manifest['frontmatter']+manifest['chapters']+manifest['backmatter']
 for c in expected:
  if not (out/'read'/c['slug']/'index.html').is_file():raise SystemExit('Missing chapter '+c['slug'])
 index=json.loads((out/'search-index.json').read_text())
 if len(index)!=len(expected):raise SystemExit('Search coverage mismatch')
 print(json.dumps({'html_pages':len(pages),'checked_links_and_resources':count,'reading_documents':len(expected),'search_documents':len(index),'result':'passed'}))
if __name__=='__main__':main()
