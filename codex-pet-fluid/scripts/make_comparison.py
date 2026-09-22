from pathlib import Path
import base64,re
r=Path(__file__).resolve().parents[1]
s=(r.parent/'codex-pet-smooth/动作对比.html').read_text()
images=[r/'references/before.webp',r/'final/spritesheet.webp']
for kind,path in zip(['old','new'],images):
    data=base64.b64encode(path.read_bytes()).decode()
    s=re.sub(r'\.'+kind+r" \.sprite\{background-image:url\('data:image/webp;base64,[^']+'\)\}",'.'+kind+" .sprite{background-image:url('data:image/webp;base64,"+data+"')}",s)
s=s.replace('姿势优化对比','自然小跑对比').replace('同样的帧数，更轻柔的动作','轻轻小跑，连贯迈步').replace('新旧版本使用相同的播放间隔，直接比较动作衔接。','同样的原生播放节奏，对照头部稳定、落地过渡与手脚交替。').replace('姿势优化版','自然小跑版')
start=s.index('const states=[');end=s.index('const idleDur=',start)
s=s[:start]+'''const states=[
{id:'running-right',label:'向右小跑',row:1,dur:[120,120,120,120,120,120,120,220],old:'上一版：跨步与循环接回有顿挫',fresh:'短步交替，头部稳定，过渡更均匀'},
{id:'running-left',label:'向左小跑',row:2,dur:[120,120,120,120,120,120,120,220],old:'上一版：跨步与循环接回有顿挫',fresh:'相同自然步态，向左轻轻小跑'}];
'''+s[end:]
s=s.replace('grid-template-columns:repeat(6,1fr)','grid-template-columns:repeat(2,1fr)').replace('grid-template-columns:repeat(3,1fr)','grid-template-columns:repeat(2,1fr)')
s=s.replace('原生版仍为 9 组动作、57 帧；本次优化指定的六组动作。原版保留在原工作文件夹中。','本次更新左右小跑的 16 帧，其余 7 组动作像素保持一致。支持暂停后逐帧对照；文件已备份。')
(r/'自然小跑对比.html').write_text(s)
print('Comparison written with embedded before/after atlases.')
