# clawd-nodding-serious.svg

Clawd 严肃敬礼后连续点头的动画，4.2秒循环。

## 身体结构
标准直立姿态，躯干 11x7 位于 (2,6)。双眼 1x2 位于 (4,8) 和 (10,8)，敬礼阶段 scaleY(1.1) 瞪大，点头阶段 scaleY(0.7) 眯起。左臂 2x2 位于 (0,9) 静止不动，右臂 2x2 位于 (13,9) 以肩部 (13px,10px) 为轴心执行敬礼动作。四腿分外侧对 (3,11)/(11,11) 和内侧对 (5,11)/(9,11)，敬礼时交替踏步。

## 道具
- 敬礼闪光粒子 ×3：fill=#FFC107 / #FFD700 / #FFF59D，各 1x1，位于手部接触头部区域 (12, 6.5~8.5)

## 动画
- **legs-outer (4.2s循环)**: 外侧腿在 8%~12% 抬起 translateY(-1.5px)，14% 落回
- **legs-inner (4.2s循环)**: 内侧腿在 14%~18% 抬起 translateY(-1.5px)，20% 落回，与外侧腿交替形成踏步
- **breathe (3.2s循环)**: transform-origin (7.5px,13px)，50% 处 scale(1.02,0.98) translate(0,0.3px) 微幅呼吸
- **arm-salute (4.2s循环)**: 7% 快速举起 translate(-1px,-1.5px) rotate(-30deg)，8%~30% 长时间保持敬礼姿势，35% 放下归位
- **nod (4.2s循环)**: transform-origin (7.5px,13px)，35%~38% 第一次点头 scale(1.03,0.95) translateY(1px)，48%~51% 第二次点头，同参数
- **eyes-nod (4.2s循环)**: 7%~30% scaleY(1.1) 瞪大配合敬礼，33% 切换至 scaleY(0.7) 眯眼，点头时 translateY(0.8px) 随头部下沉，58% 恢复正常
- **sp-salute-1 (4.2s循环)**: 10% opacity:1 scale(1)，向右上方飞散 translate(7px,-2px)，14% 消失
- **sp-salute-2 (4.2s循环)**: 10.5% 出现，向右水平飞散 translate(8px,0)，14.5% 消失
- **sp-salute-3 (4.2s循环)**: 11% 出现，向右下方飞散 translate(7px,2px)，15% 消失
- **shadow-nod (4.2s循环)**: 点头压缩时 scaleX(1.06) opacity(0.48)，其余时段 scaleX(1) opacity(0.5)

## 动作表达
Clawd 先严肃地举右臂敬礼，闪光粒子从手部迸出，随后放下手臂连续两次郑重点头。
