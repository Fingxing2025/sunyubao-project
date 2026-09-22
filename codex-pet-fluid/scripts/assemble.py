from pathlib import Path
from PIL import Image
import sys,json,statistics
sys.path.insert(0, str(Path.home() / '.codex/skills/hatch-pet/scripts'))
from derive_running_left_from_running_right import mirror_strip_preserving_frame_order
from compose_atlas import save_outputs
r=Path(__file__).resolve().parents[1]
mode=sys.argv[1]
if mode=='register':
    ims=[Image.open(r/f'frames/running-right/{i:02d}.png').convert('RGBA') for i in range(8)]
    xs=[]
    for im in ims:
        pts=[x for y in range(5,88) for x in range(192) if im.getpixel((x,y))[3]>128]
        xs.append(sum(pts)/len(pts))
    baseline=json.loads((r/'qa/before-motion.json').read_text())
    target=statistics.mean(v[0] for v in baseline['head_anchor_centroids'])
    strip=Image.new('RGBA',(1536,208));offsets=[]
    for i,(im,x) in enumerate(zip(ims,xs)):
        dx=round(target-x);offsets.append(dx)
        box=im.getbbox();assert 0<=box[0]+dx and box[2]+dx<=192,'Registration clips frame'
        cell=Image.new('RGBA',(192,208));cell.paste(im,(dx,0));strip.paste(cell,(i*192,0))
    strip.save(r/'qa/right-registered.png')
    (r/'qa/registration.json').write_text(json.dumps({'method':'shared row scale with horizontal head-anchor registration','head_centroids_before':xs,'target_x':target,'dx':offsets,'no_vertical_shift':True},indent=2))
elif mode=='final':
    row=Image.open(r/'qa/right-cleaned.png').convert('RGBA')
    left=mirror_strip_preserving_frame_order(row)
    before=Image.open(r/'references/before.webp').convert('RGBA');atlas=before.copy()
    atlas.paste(row,(0,208));atlas.paste(left,(0,416))
    save_outputs(atlas,r/'final/spritesheet.png',r/'final/spritesheet.webp')
    states=['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']
    counts=[6,8,8,4,5,8,6,6,6]
    for y,(state,count) in enumerate(zip(states,counts)):
        out=r/'frames'/state;out.mkdir(exist_ok=True)
        for x in range(count):atlas.crop((x*192,y*208,(x+1)*192,(y+1)*208)).save(out/f'{x:02d}.png')
    print('Final atlas assembled; only directional run rows replaced.')
else:raise SystemExit(mode)
