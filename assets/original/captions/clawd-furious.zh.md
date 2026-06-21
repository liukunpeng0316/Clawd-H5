# clawd-furious.svg

Clawd 暴怒颤抖、地上跺脚、头顶喷火的动画，3秒+ 循环，多周期叠加。

## 身体结构
标准躯干。body-tremble 0.12s linear 高频微震 translate；body-hunch 1.5s scale(1.02~1.04, 0.94~0.96) + translateY(0.5~1px) 紧绷耸肩。双眼 scaleY(0.6) 怒目皱眉，91-94% 短暂 scaleY(0.05) 闭眼瞬间。双臂 0.1s 高频颤抖。腿部 outer/inner 0.7s ease-out 反相跺脚。

## 道具
- **面部红潮**: 红色 (#D32F2F) 覆盖层，opacity 0~0.38 脉动
- **火焰粒子**: 6 颗 (#FF3D00/#FF6D00/#FFC107)，从头顶升起、scale 缩小、opacity 淡出，错开 delay 0/0.15/0.3/0.1/0.25/0.4s

## 动画
- **breathe (3.2s)**: 标准呼吸
- **body-tremble (0.12s linear)**: 高频微震
- **body-hunch (1.5s)**: 耸肩绷紧
- **eyes-angry (3s)**: scaleY(0.6) 怒目，91-94% 短暂闭眼
- **arm-tremble-l / arm-tremble-r (0.1s linear)**: 双臂高频颤抖
- **stomp-outer / stomp-inner (0.7s ease-out)**: 内外腿反相跺地
- **flush-pulse (0.8s)**: 红潮脉动
- **flame-a/b/c (0.5-0.6s ease-out)**: 火焰粒子升起、缩小、淡出
- **shadow-tremble (0.12s linear)**: 阴影同步颤抖

## 动作表达
Clawd 气炸了，整个身体高频颤抖耸肩，双腿轮流跺地，脸涨得通红，眼睛瞪成怒目，头顶腾起一簇簇橙色火焰向上飘散。
