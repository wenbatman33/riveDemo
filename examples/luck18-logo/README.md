# 18 Luck Faux 3D

原圖來源：spriteAnimation/參考/logo.png（192×192，盾牌可視區域 150×168）。正面保留原始 PNG；22 個深炭色盾牌層提供厚度與深度視差。depth-charcoal.png 由 imagegen 依原圖生成，尺寸及位置在 Rive 內對齊。這是 2D 分層的 Faux 3D，不是立體模型；大幅旋轉不適用。

controller.js 把滑鼠位置平滑映射至 View Model 的 pointerX、pointerY（-1～1），並用 scaleX、scaleY 輕微壓縮投影。離開畫布回正；切換範例釋放事件及 animation frame。

source/scene.rml 可由 CLI 編輯及重建。執行 rive source --once；若已登入，可加 --rev=source/editable.rev 匯出編輯器備份。
