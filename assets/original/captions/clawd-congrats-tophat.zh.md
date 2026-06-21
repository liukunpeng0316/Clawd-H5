# clawd-congrats-tophat.svg

Clawd 头戴派对帽、双手持彩花拉炮庆祝的动画，4秒循环，彩花从拉炮口喷发四散。

## 身体结构
标准躯干。38% scaleY 压缩蓄势，42% 弹起 translateY(-1.5px)，50% 归位。双眼两套切换：0-33% 普通眼，40-79% 切换为开心笑眼(^^)。双臂在身前持握拉炮 (左 translate(-5,1)、右 translate(5,1))。

## 道具
- **派对帽**: 锥形 scale(0.7) + rotate(-10°)，红/蓝/黄三色横纹叠加 + 白色绒球，戴在头顶，42% 跟身体一起弹一下
- **拉炮**: 红色筒身 (#FF5252) + 蓝色拉口 (#4FC3F7) + 金色绑带 (#FFD54F)，位于右侧 (14, 6.5)，38-50% translate(-5px, 1.5px) 推到身前点火
- **彩花碎片**: 6 块小方块（粉/蓝/黄/绿/紫/橙），从拉炮口 (9, 6.5) 扇形飞出，带 rotate 旋转，85% 透明度归零消失

## 动画
- **body-bob (4s)**: 38% 压缩、42% 弹起、50% 归位
- **hat-bounce (4s)**: 42% translateY(-1px) 帽子滞后弹一下
- **eyes-normal-vis / eyes-happy-vis (4s)**: 双套眼睛 opacity 切换
- **arm-l-hold / arm-r-hold (4s)**: 18-80% 双臂在身前持拉炮
- **popper-move (4s)**: 38-50% 拉炮移到身前并 rotate 喷射姿势
- **conf-fly-1 ~ conf-fly-6 (4s)**: 6 块彩花各自 translate + rotate 扇形飞出，85% 淡出
- **shadow-bob (4s)**: 阴影与身体同步弹动

## 动作表达
Clawd 戴着派对帽，双手举着拉炮推到身前，砰的一声拉响，彩花四散飞舞，他随之蹦起一下，眼睛眯成开心的笑眼。
