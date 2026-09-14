"""Build individual, compressed banners from the user's layered reference projects."""
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as E
import copy,json,subprocess
root=Path(__file__).resolve().parent.parent
rive=Path.home()/'.rive/bin/rive'
refs=Path.home()/'codex/spriteAnimation/rive-source'
report=[]
def simplify(points,tolerance):
 if len(points)<3:return points
 a,b=points[0],points[-1]
 if a[0]==b[0]:return points
 errors=[abs(y-(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))) for x,y in points[1:-1]]
 error=max(errors)
 if error<=tolerance:return [a,b]
 k=errors.index(error)+1
 return simplify(points[:k+1],tolerance)[:-1]+simplify(points[k:],tolerance)
for slug,project,prefix in [('shield-banner','shield18-medium','shield18'),('casino-banner','luck18','casino18')]:
 folder=root/'examples'/slug;source=folder/'source';assets=folder/'assets';assets.mkdir(parents=True,exist_ok=True);source.mkdir(exist_ok=True)
 reference=source/'reference.rml'
 if not reference.exists():reference.write_bytes((refs/project/'scene.rml').read_bytes())
 original=E.parse(reference).getroot()
 for width,height in [(531,200),(764,288)]:
  board=copy.deepcopy(next(a for a in original.findall('Artboard') if a.get('name')==f'{prefix}_{width}x{height}'))
  board.set('name','Banner');board.set('x','0');board.set('y','0')
  used={x.get('assetId') for x in board.iter('Image')}
  r=E.Element('Rive',version='1',kind='fragment');ratios={}
  for node in original.findall('ImageAsset'):
   if node.get('id') not in used:continue
   asset=copy.deepcopy(node);name=Path(asset.get('file')).name;dest=assets/('ref-'+name)
   if not dest.exists():
    image=Image.open(refs/project/asset.get('file'))
    image.save(dest,format='WEBP',quality=82,method=6,exact=True)
   im=Image.open(dest);ow,oh=im.size
   factor=width/764
   nw,nh=max(1,round(ow*factor)),max(1,round(oh*factor))
   scaled=assets/f'{width}-{dest.name}'
   im.resize((nw,nh),Image.Resampling.LANCZOS).save(scaled,format='WEBP',quality=90,method=6,exact=True)
   ratios[asset.get('id')]=(nw/ow,nh/oh)
   asset.set('file','../../assets/'+scaled.name);r.append(asset)
  objectRatios={}
  for im in board.iter('Image'):
   rx,ry=ratios[im.get('assetId')];objectRatios[im.get('id')]=(rx,ry)
   im.set('scaleX',str(float(im.get('scaleX','1'))/rx));im.set('scaleY',str(float(im.get('scaleY','1'))/ry))
  for ko in board.iter('KeyedObject'):
   if ko.get('objectId') not in objectRatios:continue
   rx,ry=objectRatios[ko.get('objectId')]
   for kp in ko.findall('KeyedProperty'):
    key=kp.get('propertyKey')
    if key in ['16','17']:
     for k in kp.findall('KeyFrameDouble'):k.set('value',str(float(k.get('value'))/(rx if key=='16' else ry)))
  bg=next(x for x in board.findall('Image') if x.get('name')=='background')
  bgid=bg.get('id')
  for animation in board.findall('LinearAnimation'):
   animation.set('name','Ambient')
   for ko in list(animation):
    if ko.get('objectId')==bgid:animation.remove(ko);continue
    for kp in ko.findall('KeyedProperty'):
     keys=list(kp)
     if len(keys)>2 and all(k.tag=='KeyFrameDouble' and k.get('interpolationType')=='linear' for k in keys):
      tolerance=.12 if kp.get('propertyKey') in ['13','14'] else .001
      keep={f for f,v in simplify([(int(k.get('frame')),float(k.get('value'))) for k in keys],tolerance)}
      for k in keys:
       if int(k.get('frame')) not in keep:kp.remove(k)
  r.append(board);dest=source/str(width);dest.mkdir(exist_ok=True);(dest/'.gitignore').write_text('build/\n')
  E.indent(r);E.ElementTree(r).write(dest/'scene.rml',encoding='unicode');(dest/'rive.yaml').write_text(f'name: banner-{width}\n')
  subprocess.run([str(rive),str(dest),'--once'],check=True)
  output=folder/f'banner-{width}x{height}.riv';output.write_bytes((dest/'build'/f'banner-{width}.riv').read_bytes())
  report.append(dict(banner=slug,width=width,height=height,bytes=output.stat().st_size,keyframes=len(list(board.iter('KeyFrameDouble')))))
 (folder/'README.md').write_text('# '+slug+'\n\n沿用使用者 spriteAnimation 的分層 Rive 參考來源（'+project+'），保留人物、標題、道具及特效動作，背景固定。每個尺寸為獨立 .riv，使用 Banner 畫布與 Ambient 動畫。\n\nsource/reference.rml 保留原始參考，source/531 與 source/764 為各尺寸動畫來源。assets/ref-*.webp 為壓縮素材。線性軌跡以誤差上限 0.12 像素、其他屬性 0.001 精簡，原本的 cubic 曲線保留。執行 python3 scripts/build_promo_banners.py 重建。\n')
(root/'examples/banner-sizes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
