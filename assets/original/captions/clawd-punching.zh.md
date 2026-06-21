# clawd-punching.svg

Clawd 愤怒出拳的连续搏击动画，0.7秒循环。

## 身体结构
标准躯干 11x7 位于 (2,6)，身体持续处于下蹲战斗姿态（scale(1.02~1.04, 0.94~0.97) translate 微幅晃动）。四腿 1x4 位于 (3,11)/(5,11)/(9,11)/(11,11) 静止。双眼 1x2 位于 (4,8)/(10,8)，持续 scaleY(0.7) 怒目眯眼，每 3秒眨一次。左臂 2x2 位于 (0,9)，右臂 2x2 位于 (13,9)，均前移至身体前方（左臂 translate(3px,1px)，右臂 translate(-3px,1px)），带 0.2 透明度投影。

## 道具
- 冲击粒子 ×4：fill=#FFC107 (0.8x0.8) ×2 + fill=#FF9800 (0.7x0.7) ×2，分别在左右拳出击时出现
- 怒气符号：位于 (12,4)，由四个 L 形 polyline 组成十字形，stroke=#FF3D00 stroke-width=0.6，整体 rotate(45deg)

## 动画
- **body-bob (0.7s循环)**: transform-origin (7.5px,15px)，15% 左倾下压 translate(-0.4px,1px) scale(1.04,0.94)，65% 右倾下压 translate(0.4px,1px) scale(1.04,0.94)，间歇回中
- **punch-l (0.7s循环)**: 左臂在 15% 处 scale(1.4) 放大模拟出拳冲击，其余时段 scale(1)
- **punch-r (0.7s循环)**: 右臂在 65% 处 scale(1.4) 放大出拳，与左拳交替
- **eyes-squint (3s循环)**: 持续 scaleY(0.7) 怒目，93%~96% scaleY(0.05) 快速眨眼
- **imp-l1 (0.7s循环)**: 15% 时在 translate(4px,7.5px) 处 opacity:0.9 出现，25% 向左上缩小消失
- **imp-l2 (0.7s循环)**: 16% 时在 translate(5.5px,9px) 处出现，26% 消失
- **imp-r1 (0.7s循环)**: 65% 时在 translate(9px,7.5px) 处出现，75% 消失
- **imp-r2 (0.7s循环)**: 66% 时在 translate(7.5px,9px) 处出现，76% 消失
- **shadow-pulse (0.7s循环)**: 出拳时 scaleX(1.06) opacity(0.45)，间歇恢复 scale(1) opacity(0.5)
- **anger-pulse (0.7s循环)**: 出拳时 scale(1.15) 膨胀，间歇回 scale(1)，始终 opacity:1

## 动作表达
Clawd 怒目圆睁蹲低重心，左右拳交替猛烈出击，每拳伴随金橙色冲击粒子迸射，头顶怒气符号随拳势搏动。
