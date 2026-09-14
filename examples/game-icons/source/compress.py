"""Re-encode embedded WebP payloads; preserve every Rive animation byte.
Usage: python3 compress.py /path/to/original/dist/icons
Requires Pillow. Always use original exports, not already compressed output.
"""
from pathlib import Path
from PIL import Image
from io import BytesIO
import argparse, json

def varuint(n):
    out = bytearray()
    while n > 127:
        out.append((n & 127) | 128)
        n >>= 7
    out.append(n)
    return bytes(out)

def compress(data, quality):
    chunks = []
    cursor = 0
    count = 0
    while True:
        start = data.find(b'RIFF', cursor)
        if start < 0:
            break
        if data[start+8:start+12] != b'WEBP':
            cursor = start + 4
            continue
        size = int.from_bytes(data[start+4:start+8], 'little') + 8
        length = varuint(size)
        prefix = start-len(length)
        if data[prefix:start] != length:
            raise ValueError('Unexpected Rive byte-array length')
        payload = data[start:start+size]
        original = Image.open(BytesIO(payload))
        output = BytesIO()
        original.save(output, format='WEBP', quality=quality, method=6, exact=True)
        encoded = output.getvalue()
        # Keep alpha lossless and the original dimensions/layout unchanged.
        check = Image.open(BytesIO(encoded))
        assert check.size == original.size
        if 'A' in original.getbands():
            assert check.getchannel('A').tobytes() == original.getchannel('A').tobytes()
        if len(encoded) < size:
            chunks.append((prefix, start+size, varuint(len(encoded))+encoded))
        count += 1
        cursor = start+size
    assert count == 4, f'Expected four images, found {count}'
    for start, end, replacement in reversed(chunks):
        data = data[:start] + replacement + data[end:]
    return data

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('original_dir', type=Path)
    ap.add_argument('--quality', type=int, default=78)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    report = []
    for name in ['vampire','fire','egypt','zeus','aztec','west','tiger','cards','mahjong']:
        before = (args.original_dir / (name+'.riv')).read_bytes()
        after = compress(before, args.quality)
        (root / (name+'.riv')).write_bytes(after)
        report.append(dict(name=name, before=len(before), after=len(after), savedPercent=round((1-len(after)/len(before))*100,1)))
    (root / 'source/compression.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
