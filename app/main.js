// One gallery for every example. All content and playback settings live in catalog.json.
const $ = selector => document.querySelector(selector);
const viewer = $('#viewer');
const loading = $('#loading');
const motion = $('#motion');
const tabs = $('#tabs');
let catalog = [];
let index = 0;
let generation = 0;
let players = [];
let activeFile = '';
let choices = [];
let playing = false;
let ready = false;
let request = null;

function playback(value) {
  playing = value;
  $('#toggle').textContent = value ? '暫停' : '播放';
  $('#status').textContent = value ? '播放中 · Rive' : '已暫停';
  document.body.dataset.playback = value ? 'playing' : 'paused';
}
function setReady() {
  ready = true;
  loading.hidden = true;
  document.body.dataset.loaded = 'true';
  $('#toggle').disabled = $('#restart').disabled = false;
  motion.disabled = !choices.length;
  $('#banner-controls').querySelectorAll('button').forEach(b => b.disabled = false);
  playback(true);
}
function fail(message, token) {
  if (token !== generation) return;
  loading.hidden = false;
  loading.textContent = message;
  $('#status').textContent = '載入失敗';
  document.body.dataset.loaded = 'error';
}
function cleanup() {
  request?.abort();
  request = null;
  players.forEach(p => p.cleanup());
  players = [];
  viewer.querySelectorAll('canvas,.icon-grid').forEach(el => el.remove());
  ready = false;
}
function playbackOptions(d, choice) {
  if (!choice) return {};
  return choice.type === 'state'
    ? { stateMachine: choice.name }
    : { animations: [choice.name, ...(d.extraAnimations || [])] };
}
function populateChoices(d, player) {
  choices = d.choices || [
    ...player.animationNames.map(name => ({ name, type: 'animation', label: name })),
    ...player.stateMachineNames.map(name => ({ name, type: 'state', label: name })),
  ];
  motion.replaceChildren();
  choices.forEach((c, i) => motion.add(new Option(c.label, String(i))));
}
function buildControls(d) {
  const controls = $('#banner-controls');
  controls.replaceChildren();
  controls.hidden = !d.controls?.length;
  for (const c of d.controls || []) {
    const b = document.createElement('button');
    b.textContent = c.label;
    b.disabled = true;
    b.onclick = () => {
      if (!ready) return;
      const model = players[0]?.viewModelInstance;
      if (c.trigger) model?.trigger(c.trigger)?.trigger();
      else {
        const property = model?.number(c.property);
        if (property) property.value = c.value;
      }
    };
    controls.append(b);
  }
}
function loadSingle(d, token, selection = 0) {
  const choice = d.choices?.[selection];
  const src = choice?.src || d.src;
  activeFile = src;
  $('#download').href = src;
  if (choice?.editable || d.editable) $('#editable').href = choice?.editable || d.editable;
  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-label', d.title + ' 動畫');
  viewer.prepend(canvas);
  const p = new rive.Rive({
    src, canvas, artboard: d.artboard, autoBind: !!d.autoBind,
    autoplay: !!choice, ...playbackOptions(d, choice),
    layout: new rive.Layout({ fit: rive.Fit.Contain, alignment: rive.Alignment.Center }),
    onLoad() {
      if (token !== generation) return;
      populateChoices(d, p);
      motion.value = String(selection);
      if (!choices.length) { fail('此檔案沒有可播放的動畫。', token); return; }
      if (!choice) p.play(choices[0].name);
      p.resizeDrawingSurfaceToCanvas();
      setReady();
    },
    onLoadError() { fail('動畫載入失敗，請重新整理或檢查檔案。', token); },
  });
  players.push(p);
}
async function loadGrid(d, token) {
  const grid = document.createElement('div');
  grid.className = 'icon-grid';
  viewer.prepend(grid);
  request = new AbortController();
  try {
    const response = await fetch(d.src, { signal: request.signal });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const buffer = await response.arrayBuffer();
    if (token !== generation) return;
    let loaded = 0;
    let failed = false;
    for (const item of d.items) {
      const tile = document.createElement('button');
      tile.className = 'icon-tile';
      tile.setAttribute('aria-label', item.title);
      tile.setAttribute('aria-pressed', 'false');
      const canvas = document.createElement('canvas');
      tile.append(canvas);
      grid.append(tile);
      tile.onclick = () => {
        grid.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === tile)));
        $('#status').textContent = '已選取：' + item.title;
      };
      const p = new rive.Rive({
        buffer, canvas, artboard: item.id, stateMachine: 'State Machine 1', autoplay: true,
        layout: new rive.Layout({ fit: rive.Fit.Cover, alignment: rive.Alignment.Center }),
        onLoad() {
          if (token !== generation) return;
          p.resizeDrawingSurfaceToCanvas();
          loaded++;
          if (loaded === d.items.length && !failed) setReady();
        },
        onLoadError() { failed = true; fail('部分封面載入失敗，請重新整理。', token); },
      });
      players.push(p);
    }
  } catch (error) {
    if (error.name !== 'AbortError') fail('封面載入失敗，請重新整理。', token);
  }
}
function selectDemo(next, updateUrl = true, selection = 0) {
  const token = ++generation;
  cleanup();
  index = (next + catalog.length) % catalog.length;
  const d = catalog[index];
  choices = [];
  motion.replaceChildren();
  motion.hidden = d.kind === 'grid';
  motion.disabled = $('#toggle').disabled = $('#restart').disabled = true;
  buildControls(d);
  viewer.dataset.kind = d.kind || 'single';
  viewer.dataset.theme = d.theme || '';
  loading.hidden = false;
  loading.textContent = '正在準備動畫…';
  $('#title').textContent = d.title;
  $('#description').textContent = d.description;
  $('#note').textContent = d.note || '';
  $('#count').textContent = `${String(index + 1).padStart(2, '0')} / ${String(catalog.length).padStart(2, '0')}`;
  $('#status').textContent = '載入中';
  $('#download').href = d.src;
  $('#editable').hidden = !d.editable;
  if (d.editable) $('#editable').href = d.editable;
  document.title = d.title + ' · Motion Library';
  document.body.dataset.demo = d.id;
  document.body.dataset.loaded = 'loading';
  [...tabs.children].forEach((el, i) => {
    el.setAttribute('aria-selected', String(i === index));
    el.tabIndex = i === index ? 0 : -1;
  });
  if (updateUrl) {
    history.replaceState(null, '', '#' + d.id);
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
  if (d.kind === 'grid') loadGrid(d, token);
  else loadSingle(d, token, selection);
}
function restart() {
  if (!ready) return;
  const d = catalog[index];
  if (d.kind === 'grid') { selectDemo(index); return; }
  const selection = Number(motion.value) || 0;
  const choice = choices[selection];
  if ((choice.src || d.src) !== activeFile) { selectDemo(index, true, selection); return; }
  players[0].reset({ artboard: d.artboard, autoBind: !!d.autoBind, autoplay: true, ...playbackOptions(d, choice) });
  players[0].resizeDrawingSurfaceToCanvas();
  playback(true);
}
$('#toggle').onclick = () => {
  if (!ready) return;
  players.forEach(p => playing ? p.pause() : p.play());
  playback(!playing);
};
$('#restart').onclick = restart;
motion.onchange = restart;
$('#prev').onclick = () => selectDemo(index - 1);
$('#next').onclick = () => selectDemo(index + 1);
new ResizeObserver(() => players.forEach(p => p.resizeDrawingSurfaceToCanvas())).observe(viewer);
window.addEventListener('pagehide', () => { generation++; cleanup(); });
window.addEventListener('pageshow', event => { if (event.persisted && catalog.length) selectDemo(index, false); });
window.addEventListener('hashchange', () => {
  const next = catalog.findIndex(d => '#' + d.id === location.hash);
  if (next >= 0 && next !== index) selectDemo(next, false);
});
try {
  const response = await fetch('./app/catalog.json');
  if (!response.ok) throw new Error('Cannot load catalog');
  catalog = await response.json();
  if (!window.rive || !catalog.length) throw new Error('No runtime or examples');
  rive.RuntimeLoader.setWasmUrl('./vendor/rive.wasm');
  catalog.forEach((d, i) => {
    const b = document.createElement('button');
    b.className = 'card';
    b.setAttribute('role', 'tab');
    for (const [tag, className, text] of [['span', 'num', 'STUDY ' + String(i + 1).padStart(2, '0')], ['strong', '', d.title], ['span', 'desc', d.short]]) {
      const el = document.createElement(tag); el.className = className; el.textContent = text; b.append(el);
    }
    b.onclick = () => selectDemo(i);
    b.onkeydown = e => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
      e.preventDefault();
      selectDemo(e.key === 'Home' ? 0 : e.key === 'End' ? catalog.length - 1 : index + (e.key === 'ArrowRight' ? 1 : -1));
      tabs.children[index].focus();
    };
    tabs.append(b);
  });
  selectDemo(Math.max(0, catalog.findIndex(d => '#' + d.id === location.hash)), false);
} catch (error) {
  fail('範例清單或播放器載入失敗，請透過 HTTP 開啟並確認 app 與 vendor 資料夾完整。', generation);
}
