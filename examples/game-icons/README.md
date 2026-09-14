# 遊戲封面

九款封面分別存放為 vampire.riv、fire.riv、egypt.riv、zeus.riv、aztec.riv、west.riv、tiger.riv、mahjong.riv、cards.riv。沿用原始 riveBanners/dist/icons 匯出檔案。每款使用同名 Artboard 及 State Machine 1。

app/catalog.json 的 items 各自指定 src。網頁分別下載，點選卡片後可單獨下載該款；不再載入合併檔。

內嵌 WebP 以 quality=78、method=6 重新編碼；保留原尺寸及無損 alpha，動畫資料不變。壓縮統計見 source/compression.json。重建需 Pillow 與原始獨立匯出檔：`python3 source/compress.py /path/to/original/dist/icons`。請勿將已壓縮檔案當作原始輸入。
