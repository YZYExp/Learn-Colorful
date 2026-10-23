#!/usr/bin/env python3
"""Build the current precise figure set; redundant v1 diagrams live in Git history."""
from pathlib import Path
import argparse,hashlib,json
from PIL import Image
from redraw_foundations import main as foundations
from redraw_systems import main as systems
from redraw_editorial import main as editorial
ROOT=Path(__file__).resolve().parents[1]
GROUPS=[(foundations,{'03','04','05','07','08','08b','02b'}),(systems,{'02','18','21','22','22b','23'}),(editorial,{'01','06','14','15','16','17'})]
RETIRED={'09','10','11','12','13','19','20','24'}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',nargs='+',help='Current IDs, e.g. --only 04 02b');args=parser.parse_args()
 current=set().union(*(ids for _,ids in GROUPS));selected=set(args.only) if args.only else current
 invalid=selected-current
 if invalid:parser.error('Unknown or retired IDs: '+', '.join(sorted(invalid)))
 written=[]
 for drawer,ids in GROUPS:
  if selected&ids:written.extend(drawer(selected&ids))
 images=[]
 for key in sorted(current):
  path=ROOT/'assets/images'/f'fig-{key}.png'
  with Image.open(path) as im:im.load();width,height=im.size;mode=im.mode
  images.append({'id':key,'width':width,'height':height,'mode':mode,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 meta={'version':3,'method':'precise editorial drawing with annotated applied designs','generator':'scripts/draw_figures.py','shared_style':'scripts/figure_style.py','figure_count':len(current),'retired_figure_ids':sorted(RETIRED),'retirement_reason':'Redundant coarse symbolic scenes replaced by complete illustrated cases in the same chapters; originals remain in Git history.','font':'COLOR_BOOK_FONT or Noto CJK','images':images}
 (ROOT/'editorial/figure-production.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 print('Rebuilt',len(written),'current figures; validated',len(images),'images')
if __name__=='__main__':main()
