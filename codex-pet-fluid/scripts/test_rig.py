from pathlib import Path
from PIL import Image,ImageChops
import json,math
import numpy as np
import rig
r=Path(__file__).resolve().parents[1]
arm=Image.open(r/'references/rig-arm.png').convert('RGBA');pivot=json.loads((r/'references/rig-arm.json').read_text())['pivot']
a,b=rig.render(0,arm,pivot)[0],rig.render(1,arm,pivot)[0]
assert np.abs(np.asarray(a).astype(int)-np.asarray(b).astype(int)).max()<=1,'Cycle seam discontinuity'
records=json.loads((r/'qa/rig-poses.json').read_text())['poses']
for p in records:
    for bone in p['bones']:
        assert abs(math.dist(bone['hip'],bone['knee'])-25.3)<1e-6
        assert abs(math.dist(bone['knee'],bone['ankle'])-25.3)<1e-6
        assert 176-1e-6<=bone['ankle'][1]<=185+1e-6
    near,far=p['bones'][1],p['bones'][0]
    assert abs((near['ankle'][0]-near['hip'][0])+(far['ankle'][0]-far['hip'][0]))<1e-6,'Legs not opposite phase'
frames=[Image.open(r/f'frames/running-right/{i:02d}.png').convert('RGBA') for i in range(8)]
assert len({im.tobytes() for im in frames})==8
heads=[im.crop((0,0,192,88)).tobytes() for im in frames];assert len(set(heads))==1,'Head drift'
for im in frames:
    box=im.getchannel('A').getbbox();assert box[0]>=3 and box[1]>=3 and box[2]<=189 and box[3]<=205,box
print('PASS: periodic endpoint, rigid leg lengths, opposite-phase feet, clearance, unique native frames, fixed head, safe margins.')
(r/'qa/rig-tests.json').write_text(json.dumps({'ok':True,'periodic_render_seam_max_channel_difference':int(np.abs(np.asarray(a).astype(int)-np.asarray(b).astype(int)).max()),'leg_lengths_constant':True,'opposite_leg_phase':True,'foot_clearance_bounds':[176,185],'all_frames_unique':True,'head_pixels_identical':True,'all_frames_inside_safe_margins':True},indent=2))
