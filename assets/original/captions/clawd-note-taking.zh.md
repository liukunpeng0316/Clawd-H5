# clawd-note-taking.svg

Clawd 低头专注记笔记的动画，多层动画周期叠加（身体 2.4s、眨眼 3.2s、文字 4.8s）。

## 身体结构
标准躯干 11x7 位于 (2,6)。四腿 1x2 位于 y=13~15（较短）。双眼 1x2 位于 (4,8)/(10,8)，持续 scaleY(0.7) 眯眼低头看笔记本，带有 step-end 阶梯式左右扫视。左臂 2x2 位于 (0,9) 通过 translate(3px,1px) 前移至笔记本左侧托持位置。右臂 2x2 位于 (13,9) 通过 translate(-5px,1px) 前移至笔记本右侧书写位置。双臂均带有 0.2 透明度黑色投影。

## 道具
- 笔记本背封：fill=#8D6E63，5.4x0.3，位于 (3.8, 12.9)
- 笔记本纸张侧面：fill=#FAFAFA，5.8x0.3，位于 (3.6, 12.6)，含两条 #DDD 分隔线
- 笔记本打开页面：fill=#FAFAF5，6x0.6，位于 (3.5, 12)，带 #BDBDBD 边框，rx=0.1
- 铅笔橡皮头：fill=#F48FB1，0.6x0.4
- 铅笔金属箍：fill=#BDBDBD，0.8x0.25
- 铅笔笔身：fill=#FDD835，0.6x1.8
- 铅笔笔尖：fill=#555 三角形
- 铅笔整体以 rotate(25deg) 倾斜握持
- 页面文字：三条 stroke=#444 线段，透明度随 write-text 动画渐进显现

## 动画
- **nod (2.4s循环)**: transform-origin (7.5px,15px)，30% translateY(0.5px) 低头，50% translateY(-0.3px) 微抬，70% 再次低头
- **hold-pulse (2.4s循环)**: 左臂 translate(3px,1px)~translate(3px,1.3px) 微幅握持脉动
- **write-stroke (0.35s循环)**: 右臂+铅笔在 translate(-5px,0.4px)~translate(-4.6px,1.2px) 之间快速书写微动
- **eye-scan (3.2s循环, step-end)**: 眼睛持续 scaleY(0.7) 眯起，translate 在 (0,0.5px)/(0.5px,0.5px)/(-0.5px,0.5px) 之间阶梯跳动模拟阅读扫视，75%~85% 短暂抬头 scaleY(0.8)
- **blink (3.2s循环)**: 38%~40% scaleY(0.1) 快速眨眼
- **ink-splash (0.7s循环)**: 三个 fill=#444 墨点（0.3~0.4px），15% opacity:0.6 出现，向不同方向飞散（通过 CSS 自定义属性 --dx/--dy 控制），各带 animation-delay 错开
- **write-text (4.8s循环, step-end)**: 页面文字 opacity 从 0 → 0.35 → 0.55 → 0.75 分阶段显现，90% 重置为 0
- **shadow-breathe (2.4s循环)**: 50% scale(1.03) opacity(0.55) 微幅呼吸

## 动作表达
Clawd 双臂前伸托着笔记本，右手持黄色铅笔快速书写，眯着眼专注地左右扫视纸面，页面上的文字逐行浮现。
