# shield-banner

沿用使用者 spriteAnimation 的分層 Rive 參考來源（shield18-medium），保留人物、標題、道具及特效動作，背景固定。每個尺寸為獨立 .riv，使用 Banner 畫布與 Ambient 動畫。

source/reference.rml 保留原始參考，source/531 與 source/764 為各尺寸動畫來源。assets/ref-*.webp 為壓縮素材。線性軌跡以誤差上限 0.12 像素、其他屬性 0.001 精簡，原本的 cubic 曲線保留。執行 python3 scripts/build_promo_banners.py 重建。
