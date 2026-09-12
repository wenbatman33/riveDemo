# 放學街頭跑步素材

使用內建 imagegen 生成，供可編輯 Rive 骨骼動畫與網頁展示使用。

- assets/street-background.png：1536 × 1024，溫暖手繪街景，含校園、店面、樹木與人行道。
- assets/schoolchild.png：1024 × 1536 RGBA，側面小朋友、制服、藍綠書包、紅鞋，透明背景。

## 生成提示詞摘要

背景：Warm hand-painted 2D animation background of a Taiwanese neighborhood after school, golden late afternoon light, school perimeter wall and gate, pastel shopfronts, trees, broad uninterrupted horizontal sidewalk, side-on camera, no people, no text, no logos.

角色：Isolated full-body schoolchild age eight facing right in side profile, short dark hair, cream school shirt, navy shorts, socks and red sneakers, teal backpack, professional hand-drawn 2D animation style, separated arms and legs in an open gentle stride for skeletal rigging, alpha-transparent background, no floor or shadow.

## 製作狀態

V2 改為五個圖片實例：完整頭身／書包／骨盆主體、前側手臂、後側手臂及兩隻腿。四肢各有自己的網格與兩根骨骼，共八根骨骼；每張四肢圖片只綁定自己的骨骼，主體不受四肢權重影響。前後手臂使用不同圖檔，兩腿使用同一圖檔的獨立實例。

Timeline 1 控制一秒跑步循環：左右手與對側腿交替、膝蓋回收彎曲、身體起伏。Street Travel 控制八秒橫向行進；State Machine 1 以兩個圖層同時播放。畫板為 1200 × 800。

V2 原始生成素材位於 assets/v2，使用內建 imagegen，以原角色為參考。生成的背景不是真透明，因此另用 macOS Finder 的「移除背景」產生 RGBA PNG，匯入檔位於 assets/v2/rig。保留生成來源與去背版本，邊緣仍有少量淺色描邊。

V2 提示詞摘要：
- body-core-source.png：Exact schoolboy identity, right-facing head, cream shirt, teal backpack and complete round navy-short pelvis; remove both arms and legs, fully paint obscured regions for puppet assembly.
- near-arm-source.png：Complete near-side arm, full cream sleeve shoulder cap, tan upper arm, elbow bent 90 degrees, forearm pointing right and relaxed fist with thumb visible; no torso or other limbs.
- far-arm-source.png：Complete far-side arm with back of hand visible, full cream sleeve shoulder, bent elbow, matching warm illustrated rendering; no torso or other limbs.
- leg-source.png：Complete side-view child leg from navy shorts hip overlap to red sneaker, nearly vertical leg with slight knee bend, same costume and warm illustration style.

school-run-v5-faster.riv / school-run-v5-faster.rev 與目前 school-run.riv / school-run.rev 內容相同。V4 保留供版本比較。V3 保留供版本比較。V2 保留供版本比較。被替換的 V1 檔案保留在 versions/v1。

- school-run.rev：可重新匯入 Rive 編輯的完整備份。
- school-run.riv：包含角色、背景及動畫的網頁播放檔。
- index.html：展示頁，播放程式直接放在 HTML 內，使用上一層 vendor 的 Rive runtime。

本機預覽：http://localhost:8766/school-run/ 。部署時保留上一層 vendor 資料夾。

線上編輯：https://editor.rive.app/file/untitled/2572579

背景目前為固定街景，角色從左向右行進；不是捲動背景或影片。

## V3 手部與手腳配對修正

近側手臂素材 assets/v3/near-arm.png 改成手背朝鏡頭、掌心朝身體，維持 1219 × 1290 透明 PNG。以 imagegen 編輯原圖，再用 Finder 移除背景。提示詞要點：preserve canvas, sleeve, elbow and wrist alignment; show smooth back of near-side left hand, thumb-up relaxed running fist, palm facing inward away from camera.

修正原本兩腿顛倒的繪製順序：near-arm、body、leg、leg 2、far-arm。leg 使用第一組腿骨骼，與近側手臂相反相位。骨骼動畫數值保留，修正近遠側視覺配對。已在 Rive 檢查 0、16、31、46 幀的跨步與交會姿勢。

## V4 跑步姿勢與節奏

角色根群組在設計模式向前傾 12 度。Timeline 1 使用 1.6 倍速，完整左右腳循環約 0.625 秒；網頁 onLoop 暫時量測約 633ms，確認速度存在匯出檔，量測碼已移除。Street Travel 使用 1.4 倍速，穿越循環約 5.714 秒。

第一組腿骨骼在 0/16/31/46/60 幀的大腿角度為 60/100/120/40/60 度，膝蓋為 15/20/110/75/15 度。第二組腿使用交替的 120/40/60/100/120 與 110/75/15/20/110 度。身體 Y 為 430/440/430/440/430。沿用 V3 手背素材與修正的前後腿圖層。這是分層圖片骨骼動畫，沒有新增腳踝關節或逐格重繪。

## V5 誇張奔跑

加大大腿擺動至 -15～135 度，膝蓋回收到 130 度；雙臂根骨骼交替 5～145 度。角色根群組旋轉在 24～30 度間變化，使肩膀連同手臂骨骼朝髖部前方移動；Y 在 410～446 間交替，強化卡通騰空與低姿勢差異。保留 1.6 倍步頻、1.4 倍行進速度與 V3 手部素材。

## V5-fast 速度調整

僅調整速度：Timeline 1 由 1.6 改為 1.92，Street Travel 由 1.4 改為 1.68，均比 V5 快 20%。完整步頻循環約 0.521 秒，街道行進循環約 4.762 秒。使用者指出的手腳配對與骨盆獨立變形尚未修復，此版本不代表跑姿問題已解決。

## V5-faster

依要求比 V5-fast 再快 60%，Timeline 1 倍速 3.072（約 0.326 秒），Street Travel 倍速 2.688（約 2.976 秒）。僅改速度，手腳配對與骨盆變形仍待修正。

## Reference timing trial

參考 https://rive.app/marketplace/12284-23321-5-state-walk-run-jump-box-dock-a-blow/ 的唯讀 Run 時間軸：60fps，工作區段 30–90 幀（1 秒），腿、鞋與 Body 約每 15 幀交替，手部時間略有錯開。僅觀察動作，沒有複製或匯入範例素材。

試版沿用 V5 姿勢，近側手臂在 16/46 幀新增 25/130 度，遠側新增 130/25 度，補足換步中段。Timeline 1 倍速回到 1.6（0.625 秒），Street Travel 回到 1.4（5.714 秒）。網頁預設試版，?version=fast 可比較保留的 V5-faster。匯出 school-run-reference-trial.riv/.rev 並更新標準檔案。

這是節奏試驗，並非完整重建參考動畫。身體與褲子仍是單張素材，沒有獨立骨盆變形；跑姿品質與所有相位的手腳視覺配對仍待使用者確認。

## Reference quick +10%

試版步頻由 1.6 提高至 1.76，行進由 1.4 提高至 1.54，均加快 10%。循環約 0.568 秒／5.195 秒；關鍵影格姿勢保留。匯出 school-run-reference-quick.riv/.rev，更新標準檔與網頁試版。


檔案結構更新：正式播放檔為 animation.riv；可編輯備份為 source/editable.rev；歷史檔名移至 archive/。本文較早的檔名為製作過程紀錄。
