# clawd-snake-charmer.svg

Clawd 化身弄蛇人吹奏笛子的场景动画，3秒循环，蛇从篮中探出随笛声摇摆，上方有"PYTHON..."彩色波浪文字。

## 身体结构
标准躯干11x7位于(2,6)。双眼(各1x2)位于(4,8)和(10,8)，fill=#000000，使用fill-box的transform-origin居中，有安详眨眼动画。双臂(各2x2)向前聚拢持笛——左臂translate(5,1)移至(5,10)位置，右臂translate(-5,1)移至(8,10)位置，均带有0.2透明度黑色投影。四腿(各1x3)静止于x=3,5,9,11，y从12到15。

## 道具
- 笛管(pungi管身): fill=#8D6E63 (1x5) 位于translate(6.5,0)后的(6.5,7)
- 笛口: fill=#6D4C41 (0.8x0.5) rx=0.2，位于管身顶端(6.6,5.5)
- 共鸣葫芦外圈: fill=#A1887F 圆形r=1.2，中心(7,6.5)
- 共鸣葫芦内圈: fill=#8D6E63 圆形r=0.8，中心(7,6.5)
- 蛇头: fill=#388E3C (3x2) rx=0.3，位于(19.5,5)
- 蛇眼: fill=#FFEB3B (0.6x0.6) rx=0.3 两颗，内有fill=#000000 (0.3x0.4)黑色瞳孔
- 蛇身: fill=#4CAF50 像素方块分段，浅色腹部fill=#81C784
- 蛇舌: stroke=#F44336 宽度0.3的分叉红线
- 篮筐边框: fill=#6D4C41 (6.6x0.5) rx=0.3，位于translate(18,12)后的(17.7,12.8)
- 篮筐主体: fill=#8D6E63 (6x2) rx=0.5，位于(18,13)
- 篮筐条纹: fill=#A1887F (5.4x0.4) 两条装饰横纹
- 音符: 三颗文字音符(♫♩♪)，fill分别为#FFD700、#40C4FF、#B388FF，font-size 3.5-4
- "PYTHON..."文字: 等宽字体font-size=2.4，各字母颜色依次为#40C4FF/#66BB6A/#FFD54F/#FF8A65/#B388FF/#40C4FF，省略号为#FFFFFF

## 动画
- **sway (3s循环)**: 以(7.5px,11px)为中心，25%时rotate(-1deg)+translate(-0.3px,0.2px)，75%时rotate(1deg)+translate(0.3px,0.2px)，表演者随音乐轻柔摇摆
- **breathe (1.8s循环)**: 以(7.5px,11px)为中心，scale(1.02,0.98)呼吸，周期比标准3.2s更快
- **fluteBob (3s循环)**: 笛子组整体50%时translateY(-0.3px)微微上浮
- **shadowPulse (3s循环)**: 以(7.5px,15.5px)为中心，50%时scaleX(1.06)+opacity(0.38)脉动
- **sereneBlink (3.2s循环)**: 双重眨眼——18%-22%快速闭合scaleY(0.2)，58%-62%半闭scaleY(0.35)，表现安详神态
- **floatNote (2.2s循环)**: 音符从translate(2px,7px)+scale(0.6)出发，20%时opacity(0.9)显现，向上漂浮至translate(2px,-6px)+scale(0.9)后消失，三颗音符animation-delay分别为0s、0.7s、1.4s错开
- **snakeSway (3s循环)**: 以(21px,15px)为中心，蛇身整体±0.8deg轻柔摇摆
- **snakeHeadWave (1.4s循环)**: 以(21px,7px)为中心，蛇头独立translateX(±0.6px)左右摆动，周期快于身体
- **text-pulse (1s循环)**: "PYTHON..."各字母opacity在0.15-1之间脉动，animation-delay从0s到0.8s每字母递增0.1s形成波浪效果

## 动作表达
Clawd 盘坐吹奏印度笛(pungi)，一条绿色像素蛇从棕色编织篮中探出随音乐摇摆，空中飘浮彩色音符，上方"PYTHON..."文字以波浪形式闪烁。
