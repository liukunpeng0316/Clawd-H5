# clawd-nodding-smile.svg

Clawd 微笑点头表示赞同的动画，2秒循环。

## 身体结构
标准直立姿态，躯干 11x7 位于 (2,6)。四腿 1x4 静止不动。双臂 2x2 位于 (0,9) 和 (13,9) 静止在身体两侧。具有两套眼睛：普通矩形眼 1x2 位于 (4,8)/(10,8)，以及微笑 ^^ 眼由 polyline 折线绘制（stroke=#000000, stroke-width=0.7），点头时切换显示。

## 动画
- **breathe (3.2s循环)**: transform-origin (7.5px,13px)，50% 处 scale(1.02,0.98) translate(0,0.3px)
- **nod (2s循环)**: transform-origin (7.5px,13px)，30%~34% 第一次点头 scale(1.03,0.95) translateY(1px)，48%~52% 第二次点头同参数，其余时段恢复原位
- **eyes-normal-vis (2s循环)**: 0%~22% opacity:1 显示普通眼，24%~68% opacity:0 隐藏，70% 恢复显示
- **eyes-smile-vis (2s循环)**: 0%~26% opacity:0 隐藏，28%~64% opacity:1 显示微笑眼，66% 切回隐藏
- **eyes-nod-shift (2s循环)**: 点头时 translateY(0.8px) 随身体下沉，回弹时 translateY(-0.2px) 轻微反弹
- **shadow-nod (2s循环)**: 点头压缩时 scaleX(1.06) opacity(0.48)，其余 scaleX(1) opacity(0.5)

## 动作表达
Clawd 友善地连续点头，点头时眼睛从普通状态切换为 ^^ 微笑弯眼，表达认同与愉悦。
