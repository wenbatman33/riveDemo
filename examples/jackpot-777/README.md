# 777 大獎慶祝

紅金色固定機台、三個獨立轉輪、42 枚金幣噴泉及 26 個閃光。素材依使用者參考圖由 imagegen 生成。

`animation.riv` 的 Jackpot 動畫為六秒循環：轉輪內的 7 與金幣符號向下滾動，三輪依序減速停在 777，接著從獎金槽向上噴出旋轉金幣，再散落離場。機台背景不縮放。

`source/scene.rml` 保留各轉輪、裁切範圍、金幣軌跡與閃光動畫，可逐層調整。`source/build_scene.py` 可重建場景：先執行 Python，再用 `rive source --once`，將 `source/build/jackpot-777.riv` 複製至 `animation.riv`。

目前提供 RML 來源及播放用 .riv。原生編輯器 .rev 匯出需要 CLI 登入，可用 `rive source --once --rev=source/editable.rev` 產生。

網頁播放檔改用 assets/optimized 的 WebP 素材；原始 PNG 保留供編輯。轉輪符號縮至 384 px、金幣 192 px、閃光 128 px，機台保留原尺寸。執行 `python3 source/compress_assets.py` 可重新產生壓縮素材，再依上方流程重建 Rive。

招牌燈光以 MarqueeOdd／MarqueeEven 兩組圖層交替加亮，每 0.3 秒換組，保留原圖暖色底光。共用既有閃光素材，僅增加約 3 KB。
