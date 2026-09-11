# Rive 網頁示範

在此資料夾啟動靜態伺服器：

```sh
git clone https://github.com/wenbatman33/riveDemo.git
cd riveDemo
python3 -m http.server 8766
```

瀏覽 http://localhost:8766 。請透過 HTTP 開啟，不要直接雙擊 HTML。

部署時把整個儲存庫的內容放到靜態網站，保持相對路徑即可。播放器 JS、WASM 與角色檔都在本機，不需要 CDN。使用 @rive-app/webgl2 2.42.0。

index.html 包含頁面與播放設定，直接載入 .riv 並提供播放、暫停與重新播放，無須額外的 player.js。播放清單由檔案內的動畫及狀態機自動讀取，預設播放第一個動畫。響應式 canvas 使用 ResizeObserver 更新解析度。

.riv 是網頁執行用檔案；修改骨骼與關鍵影格仍要回到 Rive 編輯專案，完成後重新匯出並替換 .riv。

官方文件：https://rive.app/docs/runtimes/web/web-js

## 放學以後

`school-run/` 是含午後街景的小朋友跑步動畫展示，提供原地跑姿與街頭行進兩種模式。目前預設參考節奏試版，跑姿循環約 0.57 秒、行進循環約 5.2 秒，可切換原加速版比較。`school-run/school-run.rev` 是可編輯備份，`school-run/school-run.riv` 是網頁播放檔。

試版保留分層素材與骨骼；骨盆獨立變形仍待調整，詳細版本紀錄見 `school-run/ASSETS.md`。

## 範例首頁

首頁整合 Red Fighter、放學跑步與鷹隼守衛，可使用底部卡片、左右按鈕或鍵盤方向鍵切換。網址 `#fighter`、`#school-run`、`#mummy` 可直接開啟指定範例。切換會釋放前一個 Rive 播放器，避免背景持續播放；支援減少動態效果偏好。

原格鬥展示保留於 `fighter.html`。新增作品時，在 `index.html` 的 `demos` 清單新增 id、標題、說明、riv 路徑與完整範例網址；首頁自動建立卡片與編號。可用 choices 指定顯示的動畫或狀態機。首頁轉場使用網頁動畫，沒有改動各 Rive 檔案。

選單互動參考 Journey by irmate210：https://rive.app/marketplace/23461-43911-journey/ 。未複製其插畫或 Rive 素材。

## 鷹隼守衛

`mummy/` 提供全身換装與待機、跑步、跳躍、攻擊切換。`mummy-guardian.rev` 是可編輯備份，`mummy-guardian.riv` 是網頁播放檔。沿用 ersanakpinarr 的 Mummy 骨骼與動畫（CC BY 4.0），素材與修改限制見 `mummy/REFERENCE.md`。
