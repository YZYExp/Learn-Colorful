#!/usr/bin/env python3
"""Decode every raster embedded in the completed EPUB export."""
from pathlib import Path
from io import BytesIO
import zipfile,json,re
from PIL import Image
p=Path(__file__).resolve().parents[1]/'build/色彩的语言.epub'
with zipfile.ZipFile(p) as z:
 images=[n for n in z.namelist() if n.endswith('.png')]
 for n in images:
  with Image.open(BytesIO(z.read(n))) as image:image.load()
 root=p.parents[1];book=json.loads((root/'book.json').read_text());sources=book['frontmatter']+book['chapters']+book['backmatter'];expected_images={Path(book['cover']).name}
 for item in sources:
  expected_images.update(Path(name).name for name in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',(root/item['source']).read_text()))
 expected=len(expected_images)
 if len(images)!=expected:raise SystemExit(f'Expected {expected} embedded images including cover, got {len(images)}')
 print(json.dumps({'epub':str(p),'decoded_images':len(images),'result':'passed'}))
