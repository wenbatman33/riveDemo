# Mummy reference inspection

Reference: https://rive.app/marketplace/16547-31173-mummy/ by ersanakpinarr, CC BY 4.0 as displayed by Marketplace.
Read-only editor: https://editor.rive.app/preview/16547-31173-mummy/15696604?mode=animate&artboard=mummy&animation=State%20Machine%201

Observed directly in the editor:
- Main artboard `mummy` contains AttackGroup, JumpGroup, RunGroup and RootGroup.
- Timelines: Staff, eyeBlink, Run, Jump, Attack, Idle.
- State Machine 1 has Staff, Action and eyeBlink layers. Action enters Idle and connects Idle with Jump, Run, Attack.
- Run keys target R-legTip-IK, R-legAnkle-IK, L-legTip-IK, L-legAnkle-IK, L-Arm-Ik, R-Arm-Ik and Root Bone.
- Visible Run keys at frames 0, 15, 30, 45, 60 for feet/root; arms at 0, 30, 60. Work-area end appears at frame 60. Playback speed not yet inspected.
- Reference is read-only in Chrome. MCP currently connects to the separate native-editor file 2573673, not this reference.

Implementation implication: use paired foot-tip/ankle targets and hand IK with body root motion. Do not approximate solely by rotating whole limbs. Inspect actual constraints and bind-pose geometry before retargeting. The character replacement now uses the forked source rig and existing animation keys in Mummy_fork.

New character image was generated using built-in imagegen and saved at assets/mummy-guardian.png. Prompt: original full-body three-quarter right-facing Egyptian mummy guardian, lapis-blue and antique-gold falcon crown, amber eyes, ivory bandages, ceremonial sun-jewel staff, hand-painted game illustration, transparent background, no text or UI.

## Whole-body replacement, 2026-09-11

Edited directly in the native Rive app, in Mummy_fork. Replaced torso, upper arms, forearms, open/closed hands, thighs, shins, feet, hip fabric and staff, in addition to the head. Hidden the old belt buckle. Existing bone hierarchy and animation timelines retained. Run, Jump and Attack were played in the native editor after replacement.

Feet, hip fabric and staff use rigid parent-bone attachment: their old image meshes were removed to accommodate the new artwork. They do not retain original vertex deformation. Small preview characters, eye/finger overlays and other source artboards retain original artwork. The three existing missing-target listener warnings in the Attack artboard remain; the web demo uses direct timelines.

Exports: mummy-guardian.rev is the editable Rive backup; mummy-guardian.riv is the web runtime export.

Asset prompt family (built-in imagegen): match the original generated falcon mummy guardian reference, lapis-blue and antique-gold armor, ivory wrapped bandages, dark teal skin, hand-painted game illustration, three-quarter right-facing view. Generate each isolated torso / upper arm / forearm / thigh / shin / boot / hand / hip skirt / falcon staff, transparent background, tightly framed, no other body parts, text or UI. PNGs are stored in assets and assets/parts; some matching limb artwork is reused for both sides.


檔案結構更新：正式播放檔為 animation.riv；可編輯備份為 source/editable.rev；歷史檔名移至 archive/。本文較早的檔名為製作過程紀錄。
