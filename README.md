# Motion Library

統一入口的 Rive 展示專案，使用原生 HTML、CSS 與 JavaScript modules，無需安裝套件或打包。

## 開啟

在本目錄執行 `python3 -m http.server 8767 --bind 127.0.0.1`，開啟 http://127.0.0.1:8767/ 。請勿使用 file:// 開啟。

## 檔案結構

```text
index.html                 唯一展示入口與共用頁面結構
app/
  main.js                  共用播放器、切換、控制與生命週期
  styles.css               共用樣式與響應式版面
  catalog.json             所有展示的清單與播放設定
examples/
  fighter/animation.riv
  school-run/
  mummy/
  anime-banner/
  kids-banner/
  game-icons/
    animation.riv          正式播放檔
vendor/                    共用 Rive JS / WASM（只保留一份）
archive/legacy-pages/      重整前的 HTML 文字備份，僅供歷史參考
scripts/validate.mjs       路徑、清單與搬移完整性檢查
```

各範例採用相同分類：`animation.riv` 為正式播放檔；`source/editable.rev` 為可編輯備份（若有提供）；`assets/` 為製作用素材；`archive/` 為歷史版本。未接入展示的原始 `animte_girl/anime_girl.riv` 保留在 `examples/anime-banner/archive/imported-original/`，沒有當作插畫版覆蓋。

歷史 HTML 以 .html.txt 保存，不是可運行的入口，保留當時內容和舊路徑作參考。原 `fighter.html`、`icons.html`、`school-run/`、`mummy/`、`banners/` 頁面已整合到首頁，請更新書籤。首頁 hash 連結維持有效。

## 範例網址

| 範例 | 網址 |
| --- | --- |
| Red Fighter | `/#fighter` |
| 放學以後 | `/#school-run` |
| 鷹隼守衛 | `/#mummy` |
| Neon Anime Girl | `/#anime-banner` |
| PlayPals | `/#kids-banner` |
| 九款遊戲封面 | `/#game-icons` |

放學跑步的參考節奏與原加速版本在「播放內容」中切換。PlayPals 的選單與角色 trigger 在共用控制列操作。遊戲封面共用一次下載的 buffer；點擊只顯示選取狀態，沒有實際遊戲或交易。

## 新增展示

1. 建立 `examples/<id>/`，放入 `animation.riv`；有備份或素材時分別放入 `source/`、`assets/`。
2. 在 `app/catalog.json` 加入一筆設定。無需複製 HTML 或播放器 JS。
3. 執行 `node scripts/validate.mjs`，透過首頁確認動畫與互動。

基本欄位：`id`、`title`、`description`、`short`、`src`。可選：`artboard`、`editable`、`note`、`autoBind`。`choices` 指定動畫或狀態機（`name`、`type`、`label`），也可用 `src` 指定版本檔。`extraAnimations` 指定同時播放的附加動畫。未提供 choices 時，自動讀取檔案內的動畫名稱。

`controls` 可宣告 `{ "label": "進入選單", "property": "screen", "value": 2 }` 或 `{ "label": "熊跳", "trigger": "tapBear" }`，搭配 autoBind。多畫板展示使用 `kind: "grid"`，並以 `items` 宣告每個畫板的 id 與 title。

## 素材與已知限制

鷹隼守衛沿用 ersanakpinarr 的 Mummy 骨骼與動畫（CC BY 4.0）。腳、裙甲、法杖為剛性骨骼跟隨；原預覽縮圖仍保留。詳見 `examples/mummy/REFERENCE.md`。

放學跑步的骨盆独立變形仍待調整，製作紀錄見 `examples/school-run/ASSETS.md`。Banner 與九款遊戲封面來自使用者提供的 riveBanners/web。Banner 原頁註明靈感來源 Anime Girl / xandercorp 與 Kidoo / oneweekwonders，插畫為原創重繪。首頁切換互動參考 Journey / irmate210。
