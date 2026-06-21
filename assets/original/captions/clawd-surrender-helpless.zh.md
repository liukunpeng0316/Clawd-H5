# clawd-surrender-helpless.svg

Clawd 投降无奈、举白旗左右摇头的动画，2.2秒循环，头顶有天使光环漂浮。

## 身体结构
标准躯干带呼吸(2.2s)。head-shake 1.1s translateX(±0.8px) 左右摇头表达"不行了"。双眼为悲伤弧眼(⌢⌢)——polyline 向下弯曲，不带 scale。右臂 hand-wave 1.1s translate(-1px → 0px) 微抖动，持举白旗。

## 道具
- **白旗杆**: 棕色 (#795548) 0.5w × 7h 立杆，握在右臂位置
- **白布**: 白色布条 path 位于 (11, 3.9)-(11, 5.6)，绕握杆点 (14, 10) 摆动 rotate(±18°)，并在挥动中 scaleX(1 → -1) 翻转表示布的另一面
- **天使光环**: 金色 (#FFD700) 椭圆 + 内层光晕 (#FFF59D)，悬浮于头顶 (7.5, 3)

## 动画
- **breathe (2.2s)**: 呼吸
- **head-shake (1.1s)**: translateX(±0.8px) 左右摇头
- **halo-float (2.2s)**: 光环 translateY(±0.4px) 轻浮
- **halo-glow (2.2s)**: 光环 opacity 0.85 ↔ 1 微亮
- **hand-wave (1.1s)**: 右手 translate(-1px → 0px) 抖动
- **flag-wave (1.1s)**: 白旗 rotate(±18°) 绕握杆点摆动
- **flag-flip (1.1s)**: 白布 scaleX(1 → -1) 翻面，模拟旗布飘动正反面
- **shadow-sway (2.2s)**: 阴影 scaleX(1.02) opacity 脉动

## 动作表达
Clawd 一脸无奈地摇着头表示"不行了我不行了"，右手举着一面晃动翻飞的小白旗，头顶飘着一圈金色的天使光环，整个画面充满放弃挣扎的可爱感。
