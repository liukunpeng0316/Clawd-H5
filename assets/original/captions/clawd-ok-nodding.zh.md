# clawd-ok-nodding.svg

Clawd 顶着对勾牌子连续蹦跳点头的动画，1.5秒循环，无缝两连跳。

## 身体结构
标准躯干带呼吸(3.2s)。body-translate 1.5s translateY 弧形 0.8 → -4.5 → 0.8px，一个周期内完成两次弹跳无停顿。body-squash 1.5s 蹲下 scaleY(0.94) scaleX(1.04)、顶点 scaleY/X(1.0,1.0)。双眼 eyes-blink 27% 单次 scaleY(0.1) 眨眼。

## 道具
- **对勾牌子**: 棕色边框 (#795548) + 白色填充 (#FFFFFF)，size 11×6.5，scale(0.6) 戴在头顶
- **绿色对勾**: (#7CB342) polyline 描边，无文字标签

## 动画
- **breathe (3.2s)**: 标准呼吸
- **body-translate (1.5s)**: 两连跳无缝循环，25-30%/75-80% 在最高点稍稍停留
- **body-squash (1.5s)**: 落地 scaleY(0.94)/scaleX(1.04) 蹲、顶点 1.0
- **sign-bounce (1.5s)**: 牌子 translateY(±0.8px) 滞后效果——落地时被压、顶点时上冲
- **eyes-blink (1.5s)**: 27% 单次眨眼
- **shadow-jump (1.5s)**: 阴影 scaleX 1.1 → 0.7、opacity 脉动反映高度

## 动作表达
Clawd 不停地蹦蹦跳跳点头同意，头顶顶着白底绿色对勾牌子，每次落地都蹲一下立刻又蹦起，牌子在他头上一弹一弹，地上阴影也跟着收缩展开。
