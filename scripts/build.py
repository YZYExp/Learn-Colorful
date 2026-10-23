#!/usr/bin/env python3
"""Validate Markdown/assets and build a self-contained EPUB. No web deployment."""
from pathlib import Path
import argparse, datetime, html, json, mimetypes, posixpath, re, zipfile
import xml.etree.ElementTree as ET
import markdown

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build'
CSS='''body{font-family:serif;line-height:1.85;margin:5%;color:#202824}h1{font-size:1.9em;line-height:1.4;color:#24544B;margin:1em 0}h2{font-size:1.35em;line-height:1.5;margin-top:1.8em}h3{font-size:1.15em}p{margin:.8em 0}img{display:block;width:auto;max-width:100%;height:auto;margin:1.5em auto;break-inside:avoid}table{border-collapse:collapse;width:100%;font-size:.88em}th,td{padding:.5em;border-bottom:1px solid #CCC;text-align:left;vertical-align:top}th{background:#F6F1E7}a{color:#24544B;text-decoration:underline;overflow-wrap:anywhere}blockquote{margin:1em 0;padding:.3em 1em;border-left:3px solid #C86345}code{font-size:.9em;overflow-wrap:anywhere}pre{white-space:pre-wrap}nav li{margin:.6em 0}.subtitle{font-size:1.2em;color:#555}'''

def docs(book):
    return [ROOT/c['source'] for c in book['frontmatter']+book['chapters']+book['backmatter']]

def validate(book):
    files=docs(book); errors=[]; images=set(); urls=set(); count=0
    for f in files:
        if not f.is_file(): errors.append(f'Missing {f}');continue
        text=f.read_text(); count+=len(re.findall(r'[\u3400-\u9fff]',text))
        if re.search(r'\bTODO\b|待补|占位图',text):errors.append(f'Unfinished marker {f.name}')
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
            t=(f.parent/target).resolve()
            if not t.is_file():errors.append(f'Missing image {f.name}: {target}')
            else:images.add(t)
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
            if target.startswith(('http://','https://')):urls.add(target)
            elif not target.startswith('#') and not (f.parent/target.split('#')[0]).exists():errors.append(f'Missing link {f.name}: {target}')
    for ch in book['chapters']:
        f=ROOT/ch['source']
        if f.exists():
            t=f.read_text()
            if len(re.findall(r'[\u3400-\u9fff]',t))<1100:errors.append(f'Chapter too short for planned treatment {f.name}')
            if not re.search(r'https?://',t):errors.append(f'No sources {f.name}')
            if f'fig-{ch["order"]:02}.png' not in t:errors.append(f'Missing chapter figure reference {f.name}')
    if errors:raise SystemExit('\n'.join(errors))
    return {'chapters':len(book['chapters']),'documents':len(files),'han_characters':count,'embedded_images':len(images),'distinct_source_urls':len(urls),'checks':'chapter coverage, image and local-link existence, unfinished markers; external source reachability was checked during research, not exhaustively re-fetched here'}

def xhtml(title,body):
    return '<?xml version="1.0" encoding="utf-8"?>\n'+f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN"><head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="../style.css"/></head><body>{body}</body></html>'

def build(book):
    OUT.mkdir(exist_ok=True); report=validate(book)
    files=docs(book); paths={p.resolve():f'text/{i:02}.xhtml' for i,p in enumerate(files)}
    content={}; spine=[]; manifest=[]; nav=[]
    if book.get('cover'):
        content['assets/cover.png']=(ROOT/book['cover']).read_bytes()
        content['text/cover.xhtml']=xhtml(book['title'],'<div><img src="../assets/cover.png" alt="色彩的语言：从看懂颜色到建立配色系统"/></div>').encode()
        manifest.append('<item id="coverdoc" href="text/cover.xhtml" media-type="application/xhtml+xml"/>')
        spine.append('<itemref idref="coverdoc"/>')
    for i,p in enumerate(files):
        raw=p.read_text(); title=raw.splitlines()[0].lstrip('# ').strip()
        def image_repl(m):
            asset=(p.parent/m.group(2)).resolve();dest='assets/'+asset.name
            content[dest]=asset.read_bytes()
            return f'![{m.group(1)}](../{dest})'
        raw=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',image_repl,raw)
        def link_repl(m):
            target=m.group(2)
            if target.startswith(('http:','https:','#')):return m.group(0)
            file_target,_,anchor=target.partition('#')
            dest=paths.get((p.parent/file_target).resolve())
            return f'[{m.group(1)}]({posixpath.basename(dest)}{("#"+anchor) if anchor else ""})' if dest else m.group(0)
        raw=re.sub(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)',link_repl,raw)
        body=markdown.markdown(raw,extensions=['tables','fenced_code'],output_format='xhtml')
        dest=paths[p.resolve()];content[dest]=xhtml(title,body).encode()
        manifest.append(f'<item id="d{i}" href="{dest}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="d{i}"/>');nav.append(f'<li><a href="{dest}">{html.escape(title)}</a></li>')
    content['nav.xhtml']=xhtml(book['title'],f'<nav epub:type="toc" id="toc"><h1>{book["title"]}</h1><p>{book["subtitle"]}</p><ol>{"".join(nav)}</ol></nav>').replace('href="../style.css"','href="style.css"').encode()
    content['style.css']=CSS.encode()
    manifest+=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="css" href="style.css" media-type="text/css"/>']
    for i,k in enumerate(k for k in content if k.startswith('assets/')):
        manifest.append(f'<item id="im{i}" href="{k}" media-type="{mimetypes.guess_type(k)[0]}"'+(' properties="cover-image"' if k=='assets/cover.png' else '')+'/>')
    modified=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">urn:tingly:color-language:2026</dc:identifier><dc:title>{book['title']}：{book['subtitle']}</dc:title><dc:language>zh-CN</dc:language><meta property="dcterms:modified">{modified}</meta></metadata><manifest>{''.join(manifest)}</manifest><spine>{''.join(spine)}</spine></package>'''
    content['content.opf']=opf.encode()
    for name,data in content.items():
        if name.endswith(('.xhtml','.opf')):ET.fromstring(data)
    destination=OUT/'色彩的语言.epub'
    with zipfile.ZipFile(destination,'w') as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        for name,data in content.items():z.writestr('OEBPS/'+name,data,compress_type=zipfile.ZIP_DEFLATED)
    # Validate local EPUB resources and spine references in the actual archive.
    with zipfile.ZipFile(destination) as z:
        names=set(z.namelist())
        for name in names:
            if name.endswith('.xhtml'):
                root=ET.fromstring(z.read(name))
                for element in root.iter():
                    for attr in ['src','href']:
                        v=element.get(attr)
                        if v and not v.startswith(('http:','https:','#')):
                            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),v.split('#')[0]))
                            if target not in names:raise SystemExit(f'EPUB broken resource {name}: {v}')
        report['epub_archive_integrity']=z.testzip() is None
    report['epub_xml_and_local_resources']='passed'
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
    print(destination)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    book=json.loads((ROOT/'book.json').read_text())
    if args.check:print(json.dumps(validate(book),ensure_ascii=False))
    else:build(book)
