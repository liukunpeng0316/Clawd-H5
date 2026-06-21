# clawd-bow-thanks.svg

Clawd 鞠躬感谢的动画，4秒循环，身体前压、双臂在身前合拢、头顶弹出爱心。

## 身体结构
标准躯干带呼吸(3.2s)。鞠躬阶段(22-48%)躯干 scaleY(0.82) 压缩前倾；双眼切换为笑眼变体——普通眼 scaleY(0.45) translateY(1.5px) 半闭眯起；双臂在身前合拢(左 translate(5,2)、右 translate(-5,2))，配合右下阴影解决同色辨识。

## 道具
- **大爱心**: 像素拼接的粉红心(#F28B9E)，悬浮于头顶上方，由多块矩形组成心形轮廓

## 动画
- **breathe (3.2s)**: 标准呼吸 scale(1.02, 0.98)
- **body-bow (4s)**: 22-48% scaleY(0.82) 鞠躬压缩，其余时间归位
- **eyes-normal-vis (4s)**: 普通眼 opacity 在 0-22%/48-100% 可见，鞠躬时切换
- **eyes-normal-transform (4s)**: 鞠躬阶段 scaleY(0.45) + translateY(1.5px) 眯起
- **arm-l-bow / arm-r-bow (4s)**: 22-48% 双臂在身前合拢 translate(±5px, 2px)
- **big-heart-vis (4s)**: 26% 弹出 scale(1.1)，48% 维持，54% 淡出 opacity 0

## 动作表达
Clawd 弯腰深深鞠躬致谢，双臂在身前优雅合拢，眼睛眯成笑弯弯的细线，头顶飘出一颗粉色爱心表达感激。
