# clawd-surprised.svg

Clawd 受惊后退的惊讶动画，4秒循环，包含身体向左跳退、双臂张开和红色感叹号弹出。

## 身体结构
标准躯干11x7位于(2,6)。双眼(各1x2)位于(4,8)和(10,8)，惊讶时scaleY(1.35)+scaleX(1.1)放大并translateX(0.8px)右移表示瞪大转向。左臂(2x2)以(2px,10px)为轴心向外下方rotate(-40deg)+translate(-1.5px,1px)张开；右臂(2x2)以(13px,10px)为轴心对称rotate(40deg)+translate(1.5px,1px)张开。左腿对(x=3,x=5各1x4)跟随身体translate(-5px)后退并跳起-1.5px；右腿对(x=9,x=11各1x4)以(10px,15px)为轴心rotate(-35deg)+translate(-3.5px)倾斜拉伸连接身体。

## 道具
- 感叹号竖杠: fill=#FF3D00 (1.5x3) rx=0.3，位于头顶上方transform translate(6.5,2)
- 感叹号圆点: fill=#FF3D00 (1x1) rx=0.2，位于竖杠下方(6.75,5.5)

## 动画
- **breathe (3.2s循环)**: 以(7.5px,13px)为中心，scale(1.02,0.98)+translateY(0.3px)的微弱呼吸起伏
- **body-surprise (4s循环)**: 以(7.5px,15px)为中心，15%时translate(-5px,-1.5px)+scaleX(0.85)向左跳退，20%-48%保持后退姿势translate(-5px,0)+scaleX(0.85)，58%弹回原位
- **legs-left (4s循环)**: 左腿对跟随身体，15%时translate(-5px,-1.5px)跳起后退，20%-48%保持translate(-5px,0)，58%归位
- **legs-right (4s循环)**: 右腿对以(10px,15px)为轴心，15%时translate(-3.5px,-1.5px)+rotate(-35deg)大幅倾斜，20%-48%保持，58%归位
- **eyes-surprise (4s循环)**: 12%-13%快速闭合scaleY(0)模拟惊吓眨眼，16%-48%放大scaleY(1.35)+scaleX(1.1)+translateX(0.8px)瞪大右移
- **arm-l-surprise (4s循环)**: 左臂16%时translate(-1.5px,1px)+rotate(-35deg)向外下张开，20%-48%保持rotate(-40deg)，58%归位
- **arm-r-surprise (4s循环)**: 右臂镜像，16%时translate(1.5px,1px)+rotate(35deg)张开，20%-48%保持rotate(40deg)，58%归位
- **exclaim-pop (4s循环)**: 16%时scale(1.3)弹出过冲，18%缩回scale(1)稳定，42%保持，50%时上浮translate(0,-3px)+scale(0.7)渐隐
- **shadow-surprise (4s循环)**: 跟随身体translate(-5px,0)+scaleX(0.85)+opacity(0.4)向左收缩，58%归位

## 动作表达
Clawd 突然受到惊吓，身体猛然向左后方跳退，双臂向两侧张开，眼睛瞪大，头顶弹出红色感叹号，随后慢慢恢复站姿。
