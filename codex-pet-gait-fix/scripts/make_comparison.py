from pathlib import Path
import base64,re
r=Path(__file__).resolve().parents[1]
s=(r.parent/'codex-pet-smooth/动作对比.html').read_text()
images=[r/'references/before.webp',r/'final/spritesheet.webp']
for kind,path in zip(['old','new'],images):
    data=base64.b64encode(path.read_bytes()).decode()
    s=re.sub(r'\.'+kind+r" \.sprite\{background-image:url\('data:image/webp;base64,[^']+'\)\}",'.'+kind+" .sprite{background-image:url('data:image/webp;base64,"+data+"')}",s)
s=s.replace('姿势优化对比','小跑步态修复对比').replace('同样的帧数，更轻柔的动作','这次，手脚真正交替').replace('新旧版本使用相同的播放间隔，直接比较动作衔接。','左右小跑各 8 帧：观察前半圈和后半圈的摆臂与迈腿互换。').replace('姿势优化版','手脚交替版')
start=s.index('const states=[');end=s.index('const idleDur=',start)
s=s[:start]+'''const states=[
{id:'running-right',label:'向右小跑',row:1,dur:[120,120,120,120,120,120,120,220],old:'同侧手脚一直留在前后两侧',fresh:'左右腿轮换，手臂反向摆动'},
{id:'running-left',label:'向左小跑',row:2,dur:[120,120,120,120,120,120,120,220],old:'同侧手脚一直留在前后两侧',fresh:'保留相同节奏，向左交替小跑'}];
'''+s[end:]
s=s.replace('grid-template-columns:repeat(6,1fr)','grid-template-columns:repeat(2,1fr)').replace('grid-template-columns:repeat(3,1fr)','grid-template-columns:repeat(2,1fr)')
s=s.replace('原生版仍为 9 组动作、57 帧；本次优化指定的六组动作。原版保留在原工作文件夹中。','本次更新左右小跑的 16 帧，其余 7 组动作像素保持一致。支持暂停后逐帧对照；文件已备份。')
(r/'小跑修复对比.html').write_text(s)
print('Comparison written with embedded before/after atlases.')
