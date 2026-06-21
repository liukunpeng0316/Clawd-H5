# clawd-pleading.svg

Clawd 大眼汪汪、双手合十乞求的动画，5秒循环，眼睛放大、含泪、周围星星闪烁。

## 身体结构
标准躯干带呼吸(3.2s)。15-78% body-plead scaleX(1.03) scaleY(0.97) 微缩。双眼两套切换：普通眼与"乞求大眼"——scaleY(1.15) scaleX(1.1) 放大圆润。双臂在身前合十 translate(±5px)。眼下方有两小块矩形 tears-group 充当泪窝(opacity 18-75% 显现)。

## 道具
- **闪光星**: 5 颗四角星 (#FFD700/#FFC107/#FFF59D)，散布在 (-2,5)/(16,4)/(-4,11)/(18,10)/(7.5,1)，由交叉矩形构成 X 形
- **眼内高光**: 0.5×0.5 小白方块，0-100% opacity 脉动闪烁

## 动画
- **breathe (3.2s)**: 标准呼吸
- **body-plead (5s)**: 15-78% 身体微缩
- **eyes-normal-vis (5s)**: 普通眼 opacity 在非乞求阶段可见
- **eyes-plead-scale / eyes-plead-vis (5s)**: 乞求阶段大眼放大并可见
- **eye-shine (1.5s ease-in-out)**: 眼内高光 opacity 0.9 ↔ 0.4 闪烁
- **tears-vis (5s)**: 泪窝 opacity 18-75% 显现
- **stars-vis (5s)**: 星星组 opacity 18-75% 显现
- **star-twinkle (1.2s ease-in-out)**: 每颗星 scale 1 → 1.5，错开 delay 闪烁
- **arm-l-plead / arm-r-plead (5s)**: 双臂在身前合十
- **shadow-plead (5s)**: 阴影同步微缩

## 动作表达
Clawd 眼睛放大成水汪汪的大圆眼，里面闪烁着白色高光，眼下挂着泪窝，双手在身前可怜地合十乞求，身边一圈四角星跟着轻轻闪烁。
