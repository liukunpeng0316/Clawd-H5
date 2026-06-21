# clawd-panic.svg

Clawd 倒立挣扎、四脚朝天乱蹬手乱挥的恐慌动画，3秒循环，X 眼+乱飞泪滴。

## 身体结构
整体 fall-rotate 3s rotate(180°) 倒立翻转，并在保持阶段叠加 ±4° 微抖。fall-compensate translate(-5px, -9px) 修正翻转后的画布位置。body-shake 0.12s linear 高频微震。腿 legs-kick-outer/inner 0.35s linear 反相高频踢踏。双眼变为 X 形（斜线交叉 polyline），47-53% scaleY(0.1) 闪烁。双臂 arm-flail-l/r 0.7s ease-in-out 风车式旋转 rotate(0→±20°)。

## 道具
- **泪滴**: 三颗，分别向左右飞溅(-3/+3px offset)，100% 时淡出

## 动画
- **roll-move (3s ease-in-out)**: translateX 0 → -3 → 0px 整体晃动
- **fall-compensate**: 静态 transform 位置修正
- **fall-rotate (3s)**: rotate(180°) + 微抖 ±4°
- **body-shake (0.12s linear)**: 高频颤抖
- **legs-kick-outer / legs-kick-inner (0.35s linear)**: 双腿反相乱蹬
- **arm-flail-l / arm-flail-r (0.7s ease-in-out)**: 双臂风车式甩动
- **x-eyes-blink (2.5s)**: 47-53% X 眼闪烁
- **tear-fly1/2/3 (0.8s ease-out)**: 三颗泪 delay 0/0.3/0.6s 错开向外飞
- **shadow-anim (3s ease-in-out)**: 阴影跟随 translateX 晃动

## 动作表达
Clawd 整个翻了个倒立，四脚朝天蹬腿挣扎，双臂风车般乱挥，X 眼一闪一闪，泪滴向四面飞溅，身体在地上又抖又晃停不下来。
