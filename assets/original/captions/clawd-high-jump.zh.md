# clawd-high-jump.svg

Clawd 奋力高跳的弹跳动画，1.4秒循环，含蓄力下蹲、高空滞留和落地冲击特效。

## 身体结构
标准直立姿态，躯干 11x7 位于 (2,6)，#DE886D。四腿各 1x2 位于标准位置 (3,13)/(5,13)/(9,13)/(11,13)。双臂各 2x2 位于 y=9（左臂 (0,9) transform-origin 右中，右臂 (13,9) transform-origin 左中），随跳跃展开/收拢。眼睛为开心 ^^ 形态，使用 polyline 绘制（stroke #000000, 0.8px），带 scaleY 动画模拟用力眯眼和落地眯眼。地面阴影 9x1 位于 (3,15)，#000000 opacity 0.5。

## 动画
- **high-jump (1.4s循环, ease-in-out)**: 0-12% 静立 → 18% 深蹲压缩(translateY(1px) scaleY(0.7)) → 22% 弹射拉伸(scaleY(1.15)) → 38% 上升中(translateY(-24px) scaleY(1.08)) → 46-52% 最高点滞留(translateY(-26px) scaleY(1)) → 62% 下降拉伸(translateY(-24px) scaleY(1.08)) → 78% 落地压扁(scaleY(0.72)) → 85% 回弹过冲(scaleY(1.05)) → 92% 微调(scaleY(0.97)) → 100% 恢复。transform-origin: 50% 100%（底部中心）。
- **arm-left (1.4s循环, ease-in-out)**: 0-12% 归零 → 18% 蓄力内收(rotate(-10deg)) → 30% 展开(rotate(60deg)) → 46-52% 最高点大张(rotate(85deg)) → 70% 收回(rotate(50deg)) → 78% 落地内缩(rotate(-15deg)) → 92-100% 归零。transform-origin: 100% 50%。
- **arm-right (1.4s循环, ease-in-out)**: 与 arm-left 镜像，方向取反。46-52% 最高点 rotate(-85deg)。transform-origin: 0% 50%。
- **eyes-squint (1.4s循环, ease-in-out)**: 0-15% scaleY(1) → 18% 用力眯眼 scaleY(0.6) → 30-70% 恢复 scaleY(1) → 78% 落地眯眼 scaleY(0.5) → 90-100% 恢复。
- **shadow-shrink (1.4s循环, ease-in-out)**: 18% 下蹲扩大(scale(1.2) opacity 0.6) → 46-52% 最高点极小(scale(0.2) opacity 0.06) → 78% 落地冲击扩散(scale(1.3) opacity 0.65)。
- **speed-show (1.4s循环, ease-out)**: 上升阶段短暂显示速度线（24% opacity 0.6 → 44% 消失），4 条垂直线 stroke #000000 0.4px 分布在角色两侧。
- **impact-burst (1.4s循环, ease-out)**: 落地时 78% 处出现金色(#FFC107)十字像素星，从 scale(0.5) 放大至 scale(1.5) 后消失。左星位于 (1,14)，右星位于 (14,14)，右星延迟 0.03s。
- **puff-burst (1.4s循环, ease-out)**: 起跳瞬间 20% 处出现灰色烟尘（3 团 #000000 低透明度圆角矩形），向下飘散 translateY(5px) 并放大至 scale(2) 后消失。

## 动作表达
Clawd 奋力蹲下后一跃而起，冲至 26px 高空双臂大张，伴随速度线上升和金色冲击星落地，烟尘从脚下弹出。
