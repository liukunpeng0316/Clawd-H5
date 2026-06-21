# clawd-disgusted-retreat.svg

Clawd 嫌弃地后退的动画，4.5秒循环，身体后仰、波浪臭气线浮动、紫色臭气圈上升。

## 身体结构
标准躯干。retreat-move 4.5s linear 整体 translateX (+2 → -3 → +2px) 后退再回归。20-72% 身体 rotate(-4°) + scaleY(0.96) 后仰嫌弃。眼睛 scaleY(0.6) translateX(1.5px) 皱眉斜瞟。腿部 outer/inner 4.5s linear 交替步态后撤。双臂 rotate(±10°) 摆动配合。

## 道具
- **波浪臭气线**: 3 条棕色 (#8D6E63) 曲线，20% 开始显现，各自 0.3/0.35/0.4s 错频 wiggle 抖动
- **紫色臭气圈**: 3 个紫色圆环 (#7B1FA2/#9C27B0/#AB47BC)，从身体散发出来向上 translate 升起，错开 delay 淡出消失

## 动画
- **retreat-move (4.5s linear)**: 整体 translateX 后退又回归
- **body-lean (4.5s)**: 20-72% rotate(-4°) + scaleY(0.96) 后仰
- **eyes-frown (4.5s)**: scaleY(0.6) + translateX(1.5px) 皱眉斜视
- **legs-outer / legs-kick-inner (4.5s linear)**: 双侧腿交替步退
- **arm-left / arm-right (4.5s)**: 双臂 rotate(0→±10°) 摆动
- **wave-show (4.5s)**: 臭气波浪线 opacity 脉动
- **wiggle1/2/3 (0.3-0.4s alternate)**: 三条波浪线分别错频抖动
- **circle-rise-1/2/3 (4.5s ease-out)**: 紫色臭气圈错开 delay 上升 + 淡出
- **shadow-move (4.5s linear)**: 阴影跟随后退

## 动作表达
Clawd 闻到难闻气味，皱眉斜眼往后退，身体后仰，腿一步步往后撤，身边波浪状臭气线抖动，紫色臭气圈缓缓升起飘散。
