"""Create size-appropriate WebP assets from the original PNG artwork."""
from pathlib import Path
from PIL import Image
import json
root = Path(__file__).resolve().parent.parent
out = root / 'assets/optimized'
out.mkdir(exist_ok=True)
report = []
for name, limit, quality in [('machine-blank',1504,84), ('seven',384,88), ('coin',192,86), ('sparkle',128,85)]:
    src = root / 'assets' / (name+'.png')
    im = Image.open(src)
    original_size = im.size
    im.thumbnail((limit,limit), Image.Resampling.LANCZOS)
    dst = out / (name+'.webp')
    im.save(dst,format='WEBP',quality=quality,method=6,exact=True)
    report.append(dict(asset=name,originalDimensions=original_size,dimensions=im.size,before=src.stat().st_size,after=dst.stat().st_size))
(root/'source/compression.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
