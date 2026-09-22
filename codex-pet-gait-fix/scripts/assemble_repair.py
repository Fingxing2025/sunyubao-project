from pathlib import Path
from PIL import Image
import sys
r=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path.home() / '.codex/skills/hatch-pet/scripts'))
from derive_running_left_from_running_right import mirror_strip_preserving_frame_order
from compose_atlas import save_outputs
# Reassemble already-generated/extracted artwork only; no pose synthesis.
mode=sys.argv[1]
if mode=='raw-row':
    strip=Image.new('RGBA',(1536,208))
    for c in range(8):
        im=Image.open(r/f'frames/running-right/{c:02d}.png').convert('RGBA')
        strip.paste(im,(c*192,0))
    strip.save(r/'qa/right-uncleaned.png')
elif mode=='final':
    strip=Image.open(r/'qa/right-timed.png').convert('RGBA')
    left=mirror_strip_preserving_frame_order(strip)
    atlas=Image.open(r/'references/before.webp').convert('RGBA')
    atlas.paste(strip,(0,208));atlas.paste(left,(0,416))
    save_outputs(atlas,r/'final/spritesheet.png',r/'final/spritesheet.webp')
    for state,im in [('running-right',strip),('running-left',left)]:
        out=r/'frames'/state;out.mkdir(exist_ok=True)
        for c in range(8):im.crop((c*192,0,(c+1)*192,208)).save(out/f'{c:02d}.png')
    print('Assembled repaired rows; all other atlas pixels reused unchanged.')
else:raise SystemExit(mode)
