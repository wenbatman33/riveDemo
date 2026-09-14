from pathlib import Path
import xml.etree.ElementTree as E
p=Path(__file__).parent
r=E.Element('Rive',version='1',kind='fragment')
def add(parent,tag,**props):return E.SubElement(parent,tag,{k:str(v) for k,v in props.items()})
n=100
def uid():
 global n
 n+=1;return f'0:{n}'
vm=uid();inst=uid();sm=uid();anim=uid();asset=uid();dark=uid();props={k:uid() for k in ['pointerX','pointerY','scaleX','scaleY']}
ab=add(r,'Artboard',name='Luck18',id=uid(),width=800,height=600,viewModelId=vm,viewModelInstanceId=inst,defaultStateMachineId=sm)
g=add(ab,'Node',name='LogoPivot',id=uid(),x=400,y=300)
for name,key in [('scaleX',16),('scaleY',17)]:add(g,'DataBindContext',sourcePathIds=f'{vm}-{props[name]}',propertyKey=key)
for i in range(23):
 depth=1-i/22
 node=add(g,'Node',name='Front' if i==0 else f'Extrusion{i:02}',id=uid(),opacity=1)
 for name,key,base,amount in [('pointerX',13,(1-depth)*-10,depth*19),('pointerY',14,(1-depth)*12,depth*14)]:
  conv=uid();add(r,'DataConverterRangeMapper',name=f'{name}_{i}',id=conv,minInput=-1,maxInput=1,minOutput=base-amount,maxOutput=base+amount,clampLower='true',clampUpper='true')
  add(node,'DataBindContext',sourcePathIds=f'{vm}-{props[name]}',propertyKey=key,converterId=conv)
 # Match the generated silhouette alpha bounds to the original 150 x 168 shield.
 if i==0:
  add(node,'Image',name='OriginalLogo',id=uid(),assetId=asset,scaleX=1.7,scaleY=1.7,originX=.5,originY=.5)
 else:
  add(node,'Image',name='CharcoalSide',id=uid(),assetId=dark,scaleX=255/970,scaleY=285.6/1145,originX=.5,originY=.5)
a=add(ab,'LinearAnimation',id=anim,name='Hold',duration=60,loopValue='loop')
s=add(ab,'StateMachine',id=sm,name='LogoController');l=add(s,'StateMachineLayer',name='Parallax')
add(l,'AnyState',x=0,y=-120);add(l,'ExitState',x=220,y=-120);e=add(l,'EntryState',x=-200,y=0);state=uid();add(e,'StateTransition',stateToId=state);add(l,'AnimationState',id=state,animationId=anim,x=200,y=0)
v=add(r,'ViewModel',id=vm,name='LogoModel',defaultInstanceId=inst)
for k,pid in props.items():add(v,'ViewModelPropertyNumber',name=k,id=pid)
i=add(v,'ViewModelInstance',id=inst,name='Default',exports='true')
for k,pid in props.items():add(i,'ViewModelInstanceNumber',viewModelPropertyId=pid,propertyValue=1 if k.startswith('scale') else 0)
add(r,'ImageAsset',id=asset,name='Original18Shield',file='../assets/logo.png')
add(r,'ImageAsset',id=dark,name='CharcoalShield',file='../assets/depth-charcoal.png')
E.indent(r);E.ElementTree(r).write(p/'scene.rml',encoding='unicode');(p/'rive.yaml').write_text('name: luck18-logo\n')
