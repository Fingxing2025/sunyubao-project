from pathlib import Path
import math,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageEnhance,ImageChops
R=Path(__file__).resolve().parents[1]; S=4; W,H=192,208
src=Image.open(R/'references/rig-source-cleaned.png').convert('RGBA')

def maskpoly(im,points):
    m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(round(x*S),round(y*S)) for x,y in points],fill=255)
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out
leg=maskpoly(src,[(79,131),(109,131),(112,143),(116,156),(117,178),(120,187),(131,193),(132,204),(92,204),(92,188),(92,174),(92,161),(91,158),(84,150),(79,139)])
# Stable shirt backing uses the existing navy texture under the moving shoulder.
shirt=Image.new('RGBA',src.size);tex=src.crop((94*S,104*S,108*S,125*S)).resize((32*S,43*S));shirt.paste(tex,(79*S,91*S))
shirt=maskpoly(shirt,[(91,91),(102,93),(108,98),(111,107),(112,133),(78,133),(79,118),(83,106),(88,97)])
orig=maskpoly(src,[(96,94),(107,96),(110,102),(111,134),(78,134),(80,119),(84,112),(91,106)])
shirt.alpha_composite(orig)
head=src.copy();mask=Image.new('L',src.size);ImageDraw.Draw(mask).rectangle((0,0,W*S,93*S),fill=255);head.putalpha(ImageChops.multiply(head.getchannel('A'),mask))
for name,im in [('leg',leg),('shirt',shirt),('head',head)]:im.save(R/f'qa/rig-{name}.png')
YY,XX=np.mgrid[0:H*S,0:W*S].astype(np.float32);P=np.stack([(XX+.5)/S,(YY+.5)/S],axis=-1)

def sim(a,b,c,d):
    a,b,c,d=map(lambda q:np.array(q,dtype=np.float32),(a,b,c,d));u=b-a;v=d-c
    scale=np.linalg.norm(v)/np.linalg.norm(u);ang=math.atan2(v[1],v[0])-math.atan2(u[1],u[0]);ca,sa=math.cos(ang),math.sin(ang)
    A=np.array([[ca,-sa],[sa,ca]],dtype=np.float32)*scale
    return A,c-A@a

def sample(im,xy):
    arr=np.asarray(im,dtype=np.float32)/255;arr[:,:,:3]*=arr[:,:,3:]
    x=xy[...,0]*S-.5;y=xy[...,1]*S-.5;xi=np.floor(x).astype(int);yi=np.floor(y).astype(int);fx=x-xi;fy=y-yi
    valid=(xi>=0)&(yi>=0)&(xi+1<W*S)&(yi+1<H*S);xi=np.clip(xi,0,W*S-2);yi=np.clip(yi,0,H*S-2)
    out=(arr[yi,xi]*(1-fx)[...,None]*(1-fy)[...,None]+arr[yi,xi+1]*fx[...,None]*(1-fy)[...,None]+arr[yi+1,xi]*(1-fx)[...,None]*fy[...,None]+arr[yi+1,xi+1]*fx[...,None]*fy[...,None])
    out*=valid[...,None];out[:,:,:3]/=np.maximum(out[:,:,3:],1e-8)
    return Image.fromarray(np.clip(out*255,0,255).astype('uint8'),'RGBA')

def warp_leg(root,knee,ankle):
    source=[(94,138),(105,161),(108,186)]
    A1,b1=sim(source[0],source[1],root,knee);A2,b2=sim(source[1],source[2],knee,ankle)
    r,j,e=map(np.array,(root,knee,ankle));v1=j-r;v2=e-j;L1=np.linalg.norm(v1);L2=np.linalg.norm(v2)
    t1=np.clip(np.sum((P-r)*v1,axis=-1)/(L1*L1),0,1);t2=np.clip(np.sum((P-j)*v2,axis=-1)/(L2*L2),0,1)
    d1=np.sum((P-(r+t1[...,None]*v1))**2,axis=-1);d2=np.sum((P-(j+t2[...,None]*v2))**2,axis=-1)
    w=np.clip((P[...,1]-knee[1]+6)/12,0,1);w=w*w*(3-2*w)
    xy1=(P-b1)@np.linalg.inv(A1).T;xy2=(P-b2)@np.linalg.inv(A2).T
    xy=xy1*(1-w[...,None])+xy2*w[...,None]
    # Feet remain level through low-clearance jogging; ankle blend avoids a rotating shoe/sole.
    wf=np.clip((P[...,1]-ankle[1]+4)/8,0,1);wf=wf*wf*(3-2*wf)
    xyfoot=P-np.array(ankle)+np.array(source[2])
    return sample(leg,xy*(1-wf[...,None])+xyfoot*wf[...,None])

def ik(root,foot,L1=25.3,L2=25.3):
    root=np.array(root);foot=np.array(foot);v=foot-root;dist=np.linalg.norm(v);assert dist<L1+L2
    along=(L1*L1-L2*L2+dist*dist)/(2*dist);h=math.sqrt(max(0,L1*L1-along*along));u=v/dist
    # Forward bending knee; the two legs use identical mechanics with a half-cycle delay.
    return tuple(root+u*along+np.array([u[1],-u[0]])*h)

def tint(im,f):
    a=im.getchannel('A');out=ImageEnhance.Brightness(im).enhance(f);out.putalpha(a);return out

def arm_at(arm,pivot,target,phase):
    # Swing the existing bent arm as a rigid cutout around its shoulder.
    angle=math.radians(20+28*math.cos(phase));c,s=math.cos(angle),math.sin(angle);A=np.array([[c,-s],[s,c]]);b=np.array(target)-A@np.array(pivot)
    return sample(arm,(P-b)@np.linalg.inv(A).T)

def render(t,arm,pivot):
    theta=t*2*math.pi;canvas=Image.new('RGBA',src.size);bones=[]
    # Place hips under the unchanged shirt. Far side is offset slightly right.
    for side,root,ph in [('far',(101,137),theta+math.pi),('near',(94,137),theta)]:
        foot=(root[0]+14*math.cos(ph),185-9*max(0,-math.sin(ph))**2)
        knee=ik(root,foot);limb=warp_leg(root,knee,foot)
        if side=='far':limb=tint(limb,.87)
        canvas.alpha_composite(limb);bones.append({'side':side,'hip':root,'knee':knee,'ankle':foot})
    canvas.alpha_composite(tint(arm_at(arm,pivot,(104,99),theta+math.pi),.91))
    canvas.alpha_composite(shirt)
    canvas.alpha_composite(arm_at(arm,pivot,(87,99),theta))
    canvas.alpha_composite(head)
    return canvas.resize((W,H),Image.Resampling.LANCZOS),bones
if __name__=='__main__':
    arm=Image.open(R/'references/rig-arm.png').convert('RGBA');pivot=json.loads((R/'references/rig-arm.json').read_text())['pivot']
    durations=[120]*7+[220];starts=np.cumsum([0]+durations[:-1]);centers=(starts+np.array(durations)/2)/1060
    phase_offset=1-centers[-1];phases=(centers+phase_offset)%1
    row=Image.new('RGBA',(1536,208));frames=[];log=[]
    out=R/'frames/running-right';out.mkdir(exist_ok=True)
    for i,t in enumerate(phases):
        im,b=render(float(t),arm,pivot);im.save(out/f'{i:02d}.png');row.paste(im,(192*i,0));frames.append(im);log.append({'frame':i,'phase':float(t),'bones':b})
    row.save(R/'qa/rig-row.png');row.save(R/'qa/right-cleaned.png')
    frames[0].save(R/'qa/rig-native.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
    (R/'qa/rig-poses.json').write_text(json.dumps({'durations_ms':durations,'phase_offset':float(phase_offset),'sample_at_duration_midpoints':True,'poses':log},indent=2))
    print('Rendered8 native frames from one continuous joint cycle.')
