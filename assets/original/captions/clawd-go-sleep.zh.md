# clawd-go-sleep.svg

Clawd 戴睡帽打瞌睡的动画，6秒循环，眼睛逐级垂闭、身体歪斜、Zzz 飘起、背景月亮和星星闪烁。

## 身体结构
标准躯干。40-90% body-drowsy 渐进变形：scaleY(0.94~0.96) 压扁 + scaleX(1.03~1.04) 摊宽 + rotate(2~3°) 歪头 + translateY(0.5~0.8px) 下沉。双眼 eyes-drowsy 阶梯式垂闭：scaleY 1 → 0.5 → 0.25 → 0.15，同时 scaleX 1 → 1.2 → 1.4 → 1.5 越闭越扁宽。

## 道具
- **睡帽**: 蓝色 (#5C6BC0) 软塌锥形夜帽，向右歪倒，帽尖白色绒球，帽底白色镶边，跟随身体 sway
- **Zzz**: 三个字母 (#7986CB/#9FA8DA/#C5CAE9)，font-size 2.5/3/3.5，分别位于 (13,4)/(14,3)/(15,2)，错开 delay 上飘
- **月亮**: 黄色 (#FFF9C4) 圆形，位于左上角 (1,-1)，opacity 脉动
- **星星**: 3 颗小星错频闪烁

## 动画
- **body-drowsy (6s)**: 渐进压扁歪头
- **eyes-drowsy (6s)**: 眼睛分级 scaleY 越来越扁，宽度同步增加
- **cap-sway (6s)**: 睡帽 rotate(4~6°) + translate 微摇
- **zzz-float (6s ease-out)**: 三个 Zzz 错开 delay 0/2/4s，向右上 translate 5px/-15px 漂浮淡出
- **star-twinkle (2s ease-in-out)**: 星星 delay 0/0.6/1.2s 错频闪
- **moon-glow (3s)**: 月亮 opacity 脉动
- **shadow-drowsy (6s)**: 阴影同步压扁

## 动作表达
Clawd 头戴歪倒的蓝色软睡帽，眼睛分级越来越扁、越来越宽，最后眯成一条缝，身体压扁歪向一侧，Zzz 字母一个个从头边飘起，背景月亮温柔发亮、星星闪烁。
