# clawd-typing.svg

Clawd 专注打字的动画，3秒循环，双臂交替敲键盘、眼睛扫读文档、文字逐行出现。

## 身体结构
标准躯干带呼吸(3.2s)。lean-bob 0.4s 微弹 translateY(±0.3px)。双眼 eyes-focus 1.8s step-end scaleY(0.7) 半眯专注，translateX 在 6 个水平位置扫读，3s 周期内 48% 单次 scaleY(0.1) 眨眼。双臂 tap-l/tap-r 0.25s 高频反相敲击。

## 道具
- **浮动工作页**: 浅灰底 (#FAFAFA) + 灰边框 (#B0BEC5)，size 13×7，位于 y=-1
- **动态内容行**: 3 条灰字 (#B0BEC5)，6%-85% step 出现，delay 0/1/2s 错开
- **静态背景行**: 2 条更浅 (#CFD8DC) 模糊文字，opacity 0.3-0.4 仅作背景层次
- **键盘**: 躯干下方深灰 (#424242) 矩形 + 浅灰 (#616161) 双排按键

## 动画
- **breathe (3.2s)**: 标准呼吸
- **lean-bob (0.4s)**: 微弹 translateY 与敲击同步
- **tap-l / tap-r (0.25s)**: 双臂高频反相敲击
- **eyes-focus (1.8s step-end)**: 眼睛压扁并 6 段位扫读
- **eyes-blink (3s)**: 48% 单次眨眼
- **code-line1/2/3 (3s step-end)**: 三行内容分别 delay 0/1/2s 阶梯式出现
- **shadow-breathe (3.2s)**: 阴影呼吸

## 动作表达
Clawd 全神贯注地打字，眼睛眯起在屏幕上左右扫读，双手在键盘上高速交替敲击，浮动文档页面上文字一行一行被打出来。
