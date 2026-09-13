import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = path.resolve(import.meta.dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'app/catalog.json'), 'utf8'));
const ids = new Set();
for (const d of catalog) {
  assert(!ids.has(d.id), `Duplicate id: ${d.id}`); ids.add(d.id);
  assert(d.title && d.src, `Missing fields: ${d.id}`);
  for (const file of [d.src, d.editable, d.controller, ...(d.choices || []).flatMap(c => [c.src, c.editable])].filter(Boolean)) {
    const resolved = path.resolve(root, file);
    assert(resolved.startsWith(root + path.sep), `Path outside project: ${file}`);
    assert(fs.statSync(resolved).size > 0, `Empty file: ${file}`);
  }
  if (d.kind === 'grid') assert(d.items.length && new Set(d.items.map(i => i.id)).size === d.items.length);
  for (const c of d.choices || []) assert(['state', 'animation'].includes(c.type) && c.name && c.label);
}
for (const f of ['index.html', 'app/main.js', 'app/styles.css', 'vendor/rive.js', 'vendor/rive.wasm']) assert(fs.existsSync(path.join(root, f)), `Missing ${f}`);
console.log(`Validated ${catalog.length} examples and their runtime/source/version paths.`);
