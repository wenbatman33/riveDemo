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
