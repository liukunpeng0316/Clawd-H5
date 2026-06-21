# clawd-rejected.svg

Clawd 举起拒绝标志并摇头表示不赞同的动画，3秒循环。

## 身体结构
标准躯干 11x7 位于 (2,6)。四腿 1x2 位于 y=13~15（较短）。左臂 2x2 位于 (0,9) 静止。右臂 2x2 位于 (13,9)，以 (14px,10px) 为轴心执行挥牌动作，同时牌子组也使用相同动画。双眼具有两套：普通矩形眼 1x2 和皱眉眯眼（同形状但 scaleY(0.7)），通过 blink 式切换。眼睛包裹在 eyes-drift 组中实现左右摇头视差。

## 道具
- 牌子手柄：fill=#795548，5.5x1，位于 (15, 9.5)，rx=0.2
- 圆形拒绝标志：外圈 fill=#C62828 r=2.5，内圈 fill=#E53935 r=2，圆心 (21,10)
- 白色 X 标记：两条交叉线 stroke=#FFFFFF stroke-width=0.6，从 (19.9,8.9) 到 (22.1,11.1)
- 反光高光：fill=#FFFFFF r=0.6 位于 (22, 9.3)，通过 shine-pulse 闪烁

## 动画
- **sway (2.5s循环)**: transform-origin (7.5px,15px)，50% scale(1.02,0.98) translate(0,0.5px) 呼吸摇摆
- **arm-swing-up (3s循环)**: 0%~33% rotate(180deg) 牌子藏于身后，45% rotate(-95deg) 快速挥到头顶，48%~52% 弹簧回弹至 rotate(-90deg)/-83deg/-90deg 稳定，93% 开始收回 rotate(180deg)
- **shine-pulse (3s循环)**: 52%~62% opacity 0→0.5 第一次闪光，72%~82% 第二次闪光，其余 opacity:0
- **eyes-normal-vis (3s循环)**: 0%~29% opacity:1 scaleY(1) 正常睁眼，31% scaleY(0.05) 闭合，31.01% opacity:0 隐藏，95.01% 重新出现并睁开
- **eyes-frown-vis (3s循环)**: 33.01% opacity:1 从 scaleY(0.05) 睁开至 scaleY(0.7) 皱眉眯眼，91%~93% 闭合消失
- **eye-drift (3s循环)**: 20%~28% translateX(1px) 右看，40% translateX(-1px) 左看，50% translateX(1px)，60% translateX(-1px)，衰减振荡模拟摇头
- **shadow-breathe (2.5s循环)**: 50% scale(1.02) 微幅呼吸

## 动作表达
Clawd 先正常站立，随后右臂将红色 X 拒绝牌从身后快速挥到头顶，眼睛切换为皱眉眯眼并左右摇头表示不赞同，牌面反光闪烁。
