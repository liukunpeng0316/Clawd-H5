# clawd-running.svg

Clawd 左右来回奔跑的动画，3秒循环。

## 身体结构
标准躯干 11x7 位于 (2,6)。四腿 1x4 分外侧对 (3,11)/(11,11) 和内侧对 (5,11)/(9,11)，交替抬腿形成跑步步伐。双眼 1x2 位于 (4,8)/(10,8)，跑动时 scaleY(0.7) 眯起并 translateX 朝奔跑方向偏移。左臂 2x2 位于 (0,9) 以 (2px,10px) 为轴心摆动，右臂 2x2 位于 (13,9) 以 (13px,10px) 为轴心摆动，均带 0.25 透明度投影。奔跑方向的前臂通过 translate 前移至身体前方。

## 动画
- **run-move (3s循环)**: transform-origin (7.5px,13px)，0%~5% translate(-4px,0) 在左侧，45% translate(4px,0) 跑到右侧，55%~95% translate(4px,0)→translate(-4px,0) 跑回左侧
- **run-bounce (0.3s循环)**: 25%/75% translateY(-0.8px) 每步弹跳
- **step-outer (0.3s循环)**: 外侧腿 50% translateY(-1.5px) 抬起
- **step-inner (0.3s循环)**: 内侧腿反相，0% translateY(-1.5px) 抬起，50% 落地
- **arm-l-turn (3s循环)**: 55%~92% translate(3px,1px) 向左跑时左臂前伸，其余归位
- **arm-r-turn (3s循环)**: 0%~42% translate(-3px,1px) 向右跑时右臂前伸，50% 归位
- **arm-swing-a (0.3s循环)**: 左臂 rotate(15deg)↔rotate(-10deg) 快速摆臂
- **arm-swing-b (0.3s循环)**: 右臂 rotate(-15deg)↔rotate(10deg) 反相摆臂
- **eyes-look (3s循环)**: 向右跑时 translateX(1px)，10%~42% scaleY(0.7) 眯眼冲刺；向左跑时 translateX(-1px)，60%~92% scaleY(0.7) 眯眼；转向瞬间 scaleY(1) 睁眼
- **shadow-move (3s循环)**: 跟随身体水平移动 translateX(-4px~4px)，奔跑中 scaleX(0.9) opacity(0.45)，转向时 scaleX(1) opacity(0.5)

## 动作表达
Clawd 在画面中左右来回奔跑，四腿快速交替踏步，双臂大幅摆动，眼睛朝奔跑方向眯起注视，转向时短暂睁眼。
