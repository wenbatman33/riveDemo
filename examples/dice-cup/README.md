# 金緣骰盅

三顆骰子，點數由外部 JS 指定。Rive 內含可編輯的 Closed、Shake、Open 動畫與每顆骰子六種點數圖層。沒有使用 Luau script；動作與結果切換由原生狀態機處理。

- `animation.riv`：自含 PNG 素材的網頁播放檔。
- `source/editable.rev`：CLI 匯出的真正 Rive 編輯器備份，可在 Rive 中開啟。
- `source/scene.rml`：可直接修改的 RML；`source/build_scene.py` 可重建它。
- `assets/`：imagegen 產生的骰盅、空白骰子、單一黑點、桌面 PNG。
- `controller.js`：可獨立匯入的外部 JS API 與首頁控制列。

## 在現有首頁呼叫

先選擇 `#dice-cup`，等待頁面顯示「播放中」。此時 `window.diceCup` 可使用：

```js
diceCup.setDice([2, 4, 6]); // 設定結果，不會自動開盅
diceCup.shake();          // 持續搖盅
diceCup.open();           // 停止搖盅並開盅
diceCup.close();          // 蓋盅（直接復位）
await diceCup.roll([1, 3, 5], { duration: 1400 }); // 搖 1.4 秒後開始開盅
```

`roll()` promise 在開始開盅時完成，掀盅本身另需約 1.08 秒。返回 `{ cancelled: false, dice: [...] }`。再次操作或切換範例會取消等待中的 roll，返回 `{ cancelled: true }`。點數必须為恰好三個 1～6 的整數，無效輸入會拋出 RangeError，不會局部套用。這是外部指定結果的展示動畫，不是物理模擬或隨機點數產生器。

## 在自己的網頁使用

```js
import { createDiceController } from './examples/dice-cup/controller.js';

let dice;
const player = new rive.Rive({
  src: './examples/dice-cup/animation.riv',
  canvas: document.querySelector('canvas'),
  artboard: 'DiceCup',
  stateMachine: 'DiceController',
  autoBind: true,
  autoplay: true,
  layout: new rive.Layout({ fit: rive.Fit.Contain }),
  onLoad() {
    player.resizeDrawingSurfaceToCanvas();
    dice = createDiceController(player);
    dice.roll([6, 2, 4]);
  }
});
// 卸載時：dice.dispose(); player.cleanup();
```

亦可完全不使用 controller.js，直接以 Rive SDK 寫 View Model：

```js
const vm = player.viewModelInstance;
vm.number('die1').value = 6;
vm.number('die2').value = 2;
vm.number('die3').value = 4;
vm.number('phase').value = 2;
```

`phase`：0 蓋盅、1 搖盅、2 開盅。直接操作 SDK 時由 host 驗證點數範圍。若已經 phase=2，再次寫 2 會維持打開；要重播應先經過搖盅或蓋盅狀態。保持 state machine 播放才能更新綁定。正式應用可把伺服器結果交給 `roll()`，不必重建 Rive。

## 重建

在 `source/` 內執行：

```sh
python3 build_scene.py
rive . --verify
rive inspect . --json
rive . --once --rev=editable.rev
cp build/dice-cup.riv ../animation.riv
```

匯出 .rev 需要 `rive login`。重新執行 Python 會覆蓋 scene.rml；若已手動調整 RML，直接編譯即可。

## 素材提示詞摘要

使用內建 imagegen：透明背景的深藍皮革、金邊倒扣骰盅；透明背景俯視象牙白空白骰子；透明背景單一深黑圓形骰點；深翡翠絨布與金邊空骰盤的 3:2 桌面。均要求精緻 3D 遊戲素材、無文字、無標誌。骰點以同一 PNG 在 Rive 的 Image 圖層中排列，未用 SVG 或 Canvas 繪製素材。

驗證：CLI verify、inspect；實際渲染 1/3/5 與 2/4/6 六種點數；外部 JS 邊界輸入與取消測試；首頁實際搖盅、開盅。

## 立方骰子修正

替換為有完整側面及接地陰影的 die-cube-v2.png；每種點數包含三個平面的 pip PNG 排列。六個結果的侧面配置均避開相同與對面點數。骰子移回骰盤內部；掀盅維持比例向上離場，沒有縮小懸浮。外部 API 不變。新增素材提示詞：32 度俯視、三面可見的真正象牙白立方骰子，無點數、透明背景、暖金側光、柔和接觸陰影，禁止薄板造型。

首頁可直接點擊／輕觸骰盅畫布，或以 Tab 聚焦後按 Enter／空白鍵，搖動 1.4 秒後自動開盅。使用目前選單指定點數；搖動中重複點擊不會重新計時。開盅後可再次點擊重播。
