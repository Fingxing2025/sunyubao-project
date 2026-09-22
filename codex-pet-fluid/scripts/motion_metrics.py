from PIL import Image
from pathlib import Path
import json,sys,math,statistics

def metrics(path):
    a=Image.open(path).convert('RGBA');cells=[a.crop((c*192,208,(c+1)*192,416)) for c in range(8)] if a.height>208 else [a.crop((c*192,0,(c+1)*192,208)) for c in range(8)]
    anchors=[];masks=[]
    for im in cells:
        pts=[(x,y) for y in range(5,88) for x in range(192) if im.getpixel((x,y))[3]>128]
        anchors.append([sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts)])
        masks.append([im.getpixel((x,y))[3]>128 for y in range(105,208) for x in range(192)])
    changes=[sum(x!=y for x,y in zip(masks[i],masks[(i+1)%8]))/max(1,sum(x or y for x,y in zip(masks[i],masks[(i+1)%8]))) for i in range(8)]
    head_steps=[math.dist(anchors[i],anchors[(i+1)%8]) for i in range(8)]
    return {'head_anchor_centroids':anchors,'max_head_anchor_step_px':max(head_steps),'lower_body_adjacent_silhouette_change':changes,'largest_to_median_change_ratio':max(changes)/statistics.median(changes),'note':'Image registration and silhouette diagnostics only; semantic gait and playback need visual review.'}
if __name__=='__main__':
    res=metrics(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
