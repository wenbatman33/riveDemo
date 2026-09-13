"""Build editable RML from PNG assets; no raster/vector artwork is generated here."""
from pathlib import Path
import xml.etree.ElementTree as E
import math
out=Path(__file__).parent
root=E.Element('Rive',version='1',kind='fragment')
n=100
def uid():
 global n
 n+=1;return f'0:{n}'
def add(parent,tag,**props):return E.SubElement(parent,tag,{k:str(v) for k,v in props.items()})
vm=uid();instance=uid();props={p:uid() for p in ['die1','die2','die3','phase']};smid=uid()
assets={p:uid() for p in ['cup','die','pip','table']}
ab=add(root,'Artboard',name='DiceCup',id=uid(),width=1200,height=800,clip='true',viewModelId=vm,viewModelInstanceId=instance,defaultStateMachineId=smid)
cup=uid();add(ab,'Image',id=cup,name='Cup',assetId=assets['cup'],x=600,y=380,scaleX=.40,scaleY=.40,originX=.5,originY=.5)
diceSet=uid();diceRoot=add(ab,'Node',name='DiceResults',id=diceSet,opacity=0)
faces=[]
patterns=[[(0,0)],[(-25,-25),(25,25)],[(-25,-25),(0,0),(25,25)],[(-25,-25),(25,-25),(-25,25),(25,25)],[(-25,-25),(25,-25),(0,0),(-25,25),(25,25)],[(-25,-25),(25,-25),(-25,0),(25,0),(-25,25),(25,25)]]
for i,(x,y,rot) in enumerate([(530,452,0),(680,463,0),(590,535,0)]):
 d=add(diceRoot,'Node',name=f'Die{i+1}',id=uid(),x=x,y=y,rotation=rot)
 fids=[]
 for face,pattern in enumerate(patterns,1):
  fid=uid();fids.append(fid)
  group=add(d,'Node',name=f'Face{face}',id=fid,opacity=1 if face==i+1 else 0)
  # Project each pip PNG onto the three planes of the cube, including its ellipse.
  sides=[(2,3),(6,3),(2,6),(2,1),(1,3),(5,3)]
  planes=[('Top',pattern,(625,410),(210,-135),(210,135)),
          ('Left',patterns[sides[face-1][0]-1],(400,750),(200,140),(0,210)),
          ('Right',patterns[sides[face-1][1]-1],(830,750),(200,-140),(0,210))]
  for plane,dots,center,u,v in planes:
   aa=(u[0]**2+v[0]**2)/62500;bb=(u[1]**2+v[1]**2)/62500;cross=(u[0]*u[1]+v[0]*v[1])/62500
   disc=math.sqrt((aa-bb)**2+4*cross*cross)
   sx=.012*math.sqrt((aa+bb+disc)/2);sy=.012*math.sqrt((aa+bb-disc)/2)
   angle=.5*math.atan2(2*cross,aa-bb)
   for j,(px,py) in enumerate(dots):
    x=(center[0]+u[0]*px/50+v[0]*py/50-640)*.115
    y=(center[1]+u[1]*px/50+v[1]*py/50-640)*.115
    add(group,'Image',name=f'{plane}Pip{j+1}',id=uid(),assetId=assets['pip'],x=x,y=y,rotation=angle,scaleX=sx,scaleY=sy,originX=.5,originY=.5)
 add(d,'Image',name='IvoryDie',id=uid(),assetId=assets['die'],scaleX=.115,scaleY=.115,originX=.5,originY=.5)
 faces.append(fids)
diceRoot[:]=list(reversed(list(diceRoot)))
add(ab,'Image',name='Table',id=uid(),assetId=assets['table'],x=600,y=400,scaleX=1200/1536,scaleY=800/1024,originX=.5,originY=.5)
def animation(name,tracks,duration=60,loop='oneShot'):
 aid=uid();a=add(ab,'LinearAnimation',id=aid,name=name,duration=duration,fps=60,loopValue=loop)
 for obj,key,keys in tracks:
  ko=add(a,'KeyedObject',objectId=obj);kp=add(ko,'KeyedProperty',propertyKey=key)
  for frame,value in keys:
   k=add(kp,'KeyFrameDouble',frame=frame,value=value,interpolationType='cubic')
   add(k,'CubicEaseInterpolator',x1=.25,y1=.1,x2=.25,y2=1)
 return aid
closed=animation('Closed',[(diceSet,18,[(0,0)])]+[(cup,k,[(0,v)]) for k,v in [(13,600),(14,380),(15,0),(16,.4),(17,.4)]])
shake=animation('Shake',[(diceSet,18,[(0,0)]),(cup,13,[(0,600),(5,580),(10,625),(15,578),(20,622),(25,590),(30,600)]),(cup,14,[(0,380),(5,360),(10,375),(15,350),(20,372),(25,365),(30,380)]),(cup,15,[(0,0),(5,-.12),(10,.14),(15,-.13),(20,.13),(25,-.07),(30,0)]),(cup,16,[(0,.4)]),(cup,17,[(0,.4)])],30,'loop')
opened=animation('Open',[(diceSet,18,[(0,0),(12,0),(18,1)]),(cup,13,[(0,600),(22,615),(65,680)]),(cup,14,[(0,380),(22,120),(65,-300)]),(cup,15,[(0,0),(22,-.08),(65,.14)]),(cup,16,[(0,.4),(65,.4)]),(cup,17,[(0,.4),(65,.4)])],65)
faceanims=[]
for i,fids in enumerate(faces):
 faceanims.append([animation(f'Die{i+1}_{value}',[(fid,18,[(0,1 if j+1==value else 0)]) for j,fid in enumerate(fids)],1) for value in range(1,7)])
sm=add(ab,'StateMachine',id=smid,name='DiceController')
def layer(name,prop,values,anims,initial):
 l=add(sm,'StateMachineLayer',name=name,id=uid());states=[uid() for _ in values]
 any=add(l,'AnyState',x=0,y=-150);add(l,'ExitState',x=220,y=-150)
 entry=add(l,'EntryState',x=-200,y=0);add(entry,'StateTransition',stateToId=states[initial])
 for value,state,anim in zip(values,states,anims):
  t=add(any,'StateTransition',stateToId=state,duration=0)
  c=add(t,'TransitionViewModelCondition',opValue='equal');comp=add(c,'TransitionPropertyViewModelComparator');b=add(comp,'BindablePropertyNumber');add(b,'DataBindContext',sourcePathIds=f'{vm}-{props[prop]}',propertyKey=636);add(c,'TransitionValueNumberComparator',value=value)
  add(l,'AnimationState',id=state,animationId=anim,x=values.index(value)*220,y=70,reset='true')
layer('Cup motion','phase',[0,1,2],[closed,shake,opened],0)
for i,anims in enumerate(faceanims):layer(f'Die {i+1} result',f'die{i+1}',list(range(1,7)),anims,i)
v=add(root,'ViewModel',name='DiceModel',id=vm,defaultInstanceId=instance)
for name,pid in props.items():add(v,'ViewModelPropertyNumber',name=name,id=pid)
inst=add(v,'ViewModelInstance',name='Default',id=instance,exports='true')
for name,pid in props.items():add(inst,'ViewModelInstanceNumber',viewModelPropertyId=pid,propertyValue=0 if name=='phase' else int(name[-1]))
for name,aid in assets.items():add(root,'ImageAsset',id=aid,name=name,file='../assets/die-cube-v2.png' if name=='die' else f'../assets/{name}.png')
E.indent(root);E.ElementTree(root).write(out/'scene.rml',encoding='unicode')
(out/'rive.yaml').write_text('name: dice-cup\n')
