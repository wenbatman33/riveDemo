/** Public host API. Motion and face selection live inside the .riv state machine. */
export function createDiceController(player) {
  let timer = null;
  let finish = null;
  let disposed = false;
  function model() {
    if (disposed) throw new Error('Dice controller has been disposed');
    if (!player.viewModelInstance) throw new Error('Wait for the Rive onLoad callback');
    return player.viewModelInstance;
  }
  function validate(values) {
    if (!Array.isArray(values) || values.length !== 3 || values.some(v => !Number.isInteger(v) || v < 1 || v > 6)) {
      throw new RangeError('Expected exactly three integer dice values from 1 to 6');
    }
    return [...values];
  }
  function cancel() {
    clearTimeout(timer); timer = null;
    if (finish) { finish({ cancelled: true }); finish = null; }
  }
  function phase(value) { model().number('phase').value = value; }
  const api = {
    setDice(values) {
      const checked = validate(values); const vm = model();
      checked.forEach((v, i) => { vm.number(`die${i + 1}`).value = v; });
      return checked;
    },
    getDice() { return [1, 2, 3].map(i => model().number(`die${i}`).value); },
    close() { model(); cancel(); phase(0); },
    shake() { model(); cancel(); phase(1); },
    open(values) { model(); if (values !== undefined) api.setDice(values); cancel(); phase(2); },
    roll(values, { duration = 1400 } = {}) {
      const checked = validate(values);
      if (!Number.isFinite(duration) || duration < 50 || duration > 10000) throw new RangeError('duration must be 50–10000 ms');
      model(); cancel(); api.setDice(checked); phase(1);
      return new Promise(resolve => {
        finish = resolve;
        timer = setTimeout(() => { timer = null; finish = null; phase(2); resolve({ cancelled: false, dice: checked }); }, duration);
      });
    },
    dispose() { cancel(); disposed = true; },
  };
  return api;
}

export function mount({ player, container }) {
  const api = createDiceController(player);
  window.diceCup = api;
  container.hidden = false;
  const inputs = [1, 2, 3].map((i) => {
    const label = document.createElement('label'); label.textContent = `骰子 ${i} `;
    const select = document.createElement('select'); select.setAttribute('aria-label', `骰子 ${i} 點數`);
    for (let n = 1; n <= 6; n++) select.add(new Option(String(n), String(n)));
    select.value = String(i * 2); label.append(select); container.append(label); return select;
  });
  const status = document.createElement('span'); status.setAttribute('role', 'status'); status.textContent = '點擊骰盅即可搖動並開盅，也可先指定點數。';
  const values = () => inputs.map(el => Number(el.value));
  const canvas = document.querySelector('#viewer canvas');
  let rolling = false;
  async function rollFromClick() {
    if (rolling) return;
    rolling = true;
    canvas.setAttribute('aria-busy', 'true');
    if (document.body.dataset.playback === 'paused') document.querySelector('#toggle').click();
    status.textContent = '搖盅中…';
    try {
      const result = await api.roll(values());
      if (!result.cancelled) status.textContent = `開盅：${result.dice.join('、')}，再點一下可重新搖盅。`;
    } finally {
      rolling = false;
      canvas.setAttribute('aria-busy', 'false');
    }
  }
  function keydown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (!event.repeat) rollFromClick();
    }
  }
  canvas.tabIndex = 0;
  canvas.setAttribute('role', 'button');
  canvas.setAttribute('aria-label', '骰盅：點擊搖動並開盅');
  canvas.style.cursor = 'pointer';
  canvas.addEventListener('click', rollFromClick);
  canvas.addEventListener('keydown', keydown);
  const actions = [
    ['搖盅並開盅', rollFromClick],
    ['直接開盅', () => { api.open(values()); status.textContent = `開盅：${values().join('、')}`; }],
    ['蓋盅', () => { api.close(); status.textContent = '已蓋盅'; }],
  ];
  for (const [name, action] of actions) { const b = document.createElement('button'); b.textContent = name; b.onclick = action; container.append(b); }
  container.append(status);
  return () => { canvas.removeEventListener('click', rollFromClick); canvas.removeEventListener('keydown', keydown); api.dispose(); if (window.diceCup === api) delete window.diceCup; };
}
