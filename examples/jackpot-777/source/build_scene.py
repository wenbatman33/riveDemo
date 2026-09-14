"""Stationary machine, three clipped reels, and a native Rive coin fountain."""
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as E
import random, math
p=Path(__file__).parent
r=E.Element('Rive',version='1',kind='fragment'); serial=100
def uid():
 global serial
 serial+=1
 return f'0:{serial}'
def add(parent,tag,**props):return E.SubElement(parent,tag,{k:str(v) for k,v in props.items()})
files={'base':'optimized/machine-blank.webp','seven':'optimized/seven.webp','coin':'optimized/coin.webp','spark':'optimized/sparkle.webp'}
assets={k:uid() for k in files}
sizes={k:Image.open(p/'../assets'/f).size for k,f in files.items()}
ab=add(r,'Artboard',id=uid(),name='Jackpot777',width=700,height=1000,clip='true')
tracks=[]
def track(obj,key,keys,ease='smooth'): tracks.append((obj,key,keys,ease))
def sprite(parent,asset,name,width,height=None,**props):
 w,h=sizes[asset]
 return add(parent,'Image',id=uid(),name=name,assetId=assets[asset],scaleX=width/w,scaleY=(height/h if height else width/w),originX=.5,originY=.5,**props)
rng=random.Random(777)
# Draw order: first child is foreground. Each coin follows a ballistic arc.
for i in range(42):
 obj=uid();start=130+(i%14)*3;life=rng.randint(95,130);x=350+rng.uniform(-25,25);y=725
 vx=rng.uniform(-310,310);height=rng.uniform(360,650);endY=1110+rng.uniform(0,100)
 g=add(ab,'Node',id=obj,name=f'CoinFountain{i+1:02}',x=x,y=y,opacity=0)
 sprite(g,'coin','GoldCoin',rng.uniform(27,51))
 track(obj,13,[(0,x),(start,x),(start+life,x+vx),(360,x+vx)],'linear')
 # Parabola through launch, peak and fall. Six keys keep arcs editable.
 keys=[]
 for q in [0,.2,.4,.6,.8,1]:
  yy=y-4*height*q*(1-q)+(endY-y)*q*q
  keys.append((round(start+life*q),round(yy,2)))
 track(obj,14,[(0,y)]+keys+[(360,endY)],'linear')
 track(obj,18,[(0,0),(start-1,0),(start,1),(start+life-10,1),(start+life,0),(360,0)],'linear')
 track(obj,15,[(0,0),(start,0),(start+life,rng.choice([-1,1])*math.pi*4),(360,0)],'linear')
 track(obj,16,[(0,1),(start,1),(start+20,.16),(start+40,1),(start+60,.16),(start+80,1),(start+life,.3),(360,1)])
for i in range(26):
 obj=uid();x=rng.uniform(55,645);y=rng.uniform(220,810);start=126+i*4
 g=add(ab,'Node',id=obj,name=f'WinSparkle{i+1:02}',x=x,y=y,opacity=0)
 sprite(g,'spark','GoldFlash',rng.uniform(24,64))
 track(obj,18,[(0,0),(start,0),(start+8,1),(start+28,0),(360,0)])
# Two shared opacity tracks alternate the marquee bulbs; reuse the sparkle texture.
upper=[(75,280),(91,282),(108,282),(126,282),(144,282),(163,276),(181,267),(200,259),(220,253),(240,247),(260,243),(280,240),(300,238),(320,237),(340,237),(360,238),(380,240),(400,243),(420,247),(440,253),(460,260),(480,269),(500,279),(521,282),(542,282),(561,282),(579,282),(598,282),(615,281)]
lower=[(83+i*20,350) for i in range(28)]
ends=[(71,298),(70,316),(622,298),(625,316)]
for phase in range(2):
 gid=uid();lamps=add(ab,'Node',id=gid,name='MarqueeOdd' if phase==0 else 'MarqueeEven')
 for i,(x,y) in enumerate(upper+lower+ends):
  if i%2==phase:sprite(lamps,'spark',f'Bulb{i+1:02}',27,x=x,y=y)
 keys=[]
 for frame in range(0,361,18):
  value=1 if (frame//18)%2==phase else 0
  if frame:keys.append((frame-3,1-value))
  keys.append((frame,value))
 track(gid,18,keys,'linear')
for col,cx in enumerate([192,352,511]):
 maskId=uid();mask=add(ab,'Shape',id=maskId,name=f'Reel{col+1}Window',x=cx,y=492)
 add(mask,'Rectangle',width=134,height=164,originX=.5,originY=.5)
 stripId=uid();strip=add(ab,'Node',id=stripId,name=f'Reel{col+1}Strip',y=0)
 for row in range(-18,2):
  key='seven' if row%2==0 else 'coin'
  im=sprite(strip,key,f'Symbol{row+18:02}',126 if key=='seven' else 92,140 if key=='seven' else None,x=cx,y=492+row*172)
  add(im,'ClippingShape',sourceId=maskId,name='ReelWindowClip')
 stop=86+col*19
 track(stripId,14,[(0,0),(8,0),(stop,18*172+6),(stop+7,18*172),(360,18*172)],'reel')
sprite(ab,'base','StationaryMachine',700,1000,x=350,y=500)
a=add(ab,'LinearAnimation',id=uid(),name='Jackpot',duration=360,fps=60,loopValue='loop')
for obj,key,keys,ease in tracks:
 ko=add(a,'KeyedObject',objectId=obj);kp=add(ko,'KeyedProperty',propertyKey=key)
 for j,(frame,value) in enumerate(keys):
  k=add(kp,'KeyFrameDouble',frame=frame,value=value,interpolationType='linear' if ease=='linear' else 'cubic')
  if ease!='linear':
   curve=(.15,.65,.35,1) if ease=='reel' and j==1 else (.25,.1,.25,1)
   add(k,'CubicEaseInterpolator',x1=curve[0],y1=curve[1],x2=curve[2],y2=curve[3])
for k,f in files.items():add(r,'ImageAsset',id=assets[k],name=k,file='../assets/'+f)
E.indent(r);E.ElementTree(r).write(p/'scene.rml',encoding='unicode');(p/'rive.yaml').write_text('name: jackpot-777\n')
