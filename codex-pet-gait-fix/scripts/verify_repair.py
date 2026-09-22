from pathlib import Path
from PIL import Image,ImageChops,ImageOps
import json,hashlib
r=Path(__file__).resolve().parents[1]
a=Image.open(r/'references/before.webp').convert('RGBA')
b=Image.open(r/'final/spritesheet.webp').convert('RGBA')
assert a.size==b.size==(1536,1872)
rows=[]
for row in range(9):
    crop=(0,row*208,1536,(row+1)*208)
    same=a.crop(crop).tobytes()==b.crop(crop).tobytes()
    assert same==(row not in [1,2]),f'Unexpected row change: {row}'
    rows.append({'row':row,'pixels_unchanged':same})
for c in range(8):
    right=b.crop((c*192,208,(c+1)*192,416))
    left=b.crop((c*192,416,(c+1)*192,624))
    assert ImageOps.mirror(right).tobytes()==left.tobytes(),f'Mirror timing mismatch: {c}'
for row in [1,2]:
    assert len({b.crop((c*192,row*208,(c+1)*192,(row+1)*208)).tobytes() for c in range(8)})==8
result={'ok':True,'rows':rows,'mirror_preserves_frame_order':True,'eight_unique_frames_per_run':True,'sha256':hashlib.sha256((r/'final/spritesheet.webp').read_bytes()).hexdigest(),'note':'Pixel checks do not prove gait semantics; see visual review.'}
(r/'qa/row-preservation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
