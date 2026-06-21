# clawd-broke.svg

Clawd 钱袋空空、抖出最后一枚硬币的破产动画，5秒循环，从抖袋到落币再到悲伤眼+泪滴。

## 身体结构
标准躯干带呼吸(3.2s)。65-85%躯干下沉 scaleY(0.95) translateY(0.5px) 表现颓丧。双眼有两套：普通眼和悲伤弧眼(⌢⌢)，通过 opacity 切换，42-55%阶段眼睛向右看 translateX(1.5px) 盯着抖袋动作。右臂大幅 rotate(-70°) 向后挥出抖袋。

## 道具
- **钱袋**: 金色(#DEAF42)倒置梯形，挂在右臂端部，37-42%剧烈 rotate(±32° → 10°) 抖动
- **掉落硬币**: 金色(#FFD700)圆形，42% 时从袋底掉出，沿弧形轨迹坠落到地面
- **泪滴**: 悲伤眼下方挂泪 opacity 0.8，68-85%期间显现

## 动画
- **breathe (3.2s)**: 标准呼吸
- **sag (5s)**: 65-85% 躯干下沉
- **normal-eyes-vis / sad-eyes-vis (5s)**: 双套眼睛 opacity 互斥切换
- **eyes-look (5s)**: 42-55% 向右瞟 translateX(1.5px)
- **arm-right-anim (5s)**: 右臂 rotate(-70°) 向后挥
- **bag-vis / bag-shake (5s)**: 钱袋显现并剧烈抖动 rotate(±32°)
- **coin-fall (5s)**: 42% 起硬币从袋口掉落到地面
- **tear-hang (5s)**: 68-85% 泪滴 opacity 0.8 挂着
- **shadow-breathe (3.2s)**: 阴影同步呼吸

## 动作表达
Clawd 发现身无分文，向后伸手抖晃钱袋，仅剩的一枚金币叮当掉落，他切换为悲伤眼挂着泪珠，身体颓然下沉。
