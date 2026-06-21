# clawd-rofl.svg

Clawd 笑到滚地的动画，4秒循环，从站立大笑到 90° 侧翻滚地、四脚蹬腿、笑线四溅。

## 身体结构
fall-rotate 4s rotate(0→90°) 侧翻，滚动阶段(33-60%) 叠加 ±4° 微抖。fall-compensate 22-62% translate(-7px,-2px) 修正位置。laugh-shake 0.12s linear 全程微震。腿 legs-kick-outer/inner 4s linear 异步乱蹬（外腿 20/36/52%、内腿 24/40/56%）。双眼为笑眼 polyline (^^)，47-53% scaleY 闪烁眨眼。双臂 arm-flail-l/r 4s rotate(0→±20°) 风车甩动。

## 道具
- **站立笑线**: 角色站立时左侧 3 条波浪笑线（棕色 #8D6E63），0.3s step 闪烁
- **滚地笑线**: 翻倒后右上方 3 条彩色笑线 (#FFD700/#FFC107/#FFA000)，滚地阶段 28-58% 闪现

## 动画
- **roll-move (4s ease-in-out)**: translateX 整体晃动
- **fall-compensate (4s)**: 22-62% 位置修正
- **fall-rotate (4s)**: rotate(0→90°) 侧翻 + 微抖
- **laugh-shake (0.12s linear)**: 高频颤抖
- **legs-kick-outer / legs-kick-inner (4s linear)**: 异步乱蹬
- **smile-blink (2.5s)**: 笑眼 47-53% 闪烁眨眼
- **arm-flail-l / arm-flail-r (4s)**: 双臂风车甩动
- **laugh-lines-vis / laugh-lines-roll-vis (4s)**: 两组笑线 opacity 互斥——站立组 0-12%/72-100%、滚地组 28-58%
- **ll-flash1/2/3 (0.3s step-end)**: 笑线脉冲闪烁
- **shadow-anim (4s)**: 阴影同步晃动

## 动作表达
Clawd 站着笑得前仰后合，旁边迸出棕色笑线，笑着笑着直接侧翻 90° 滚到地上，腿乱蹬手乱挥，金色笑线在身边闪烁不停。
