# clawd-confused-big-question.svg

Clawd 困惑下大问号从头顶向上猛弹的动画，6秒循环，身体跟随问号弹起腾空。

## 身体结构
标准躯干。10-56% 身体 rotate(±6°) 左右倾斜歪头，同时双眼 scaleY(0.55) 压扁迷茫；30-56% 全身 clawd-rise translateY(-13~-14.6px) 跟随问号腾空，阴影 scaleX 缩小。

## 道具
- **大蓝色问号**: 由 6 块圆角矩形拼接而成 (#4A90D9)，悬浮于头顶上方，跟随身体弹起

## 动画
- **breathe (3.2s)**: 标准呼吸
- **big-q-spring (6s)**: 问号 scaleY 弹簧 0.02 → 1.1 → 1，与身体腾空同步
- **clawd-rise (6s)**: 30-56% 身体腾空 translateY(-14.6px) 后回落
- **body-tilt (6s)**: 10-56% rotate(±6°) 困惑歪头
- **eyes-react (6s)**: 10-56% scaleY(0.55) 眼睛压扁迷茫
- **ground-shadow (6s)**: 腾空时 scaleX 收缩反映高度

## 动作表达
Clawd 困惑地歪头眯眼，头顶一个大蓝色问号像弹簧般 boing 弹起，整个身体随之腾空到空中，然后一起落回地面。
