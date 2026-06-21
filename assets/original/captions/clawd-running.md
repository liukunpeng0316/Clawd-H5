# clawd-running.svg

An animation of Clawd running back and forth, looping every 3 seconds.

## Body
Standard 11x7 torso at (2,6). The four legs are 1x4, split into an outer pair (3,11)/(11,11) and an inner pair (5,11)/(9,11), lifting in alternation to form a running stride. The eyes are 1x2 at (4,8)/(10,8); while running they squint with scaleY(0.7) and shift via translateX toward the running direction. The left arm 2x2 at (0,9) swings around the pivot (2px,10px), the right arm 2x2 at (13,9) swings around the pivot (13px,10px), both with a 0.25-opacity shadow. The leading arm in the running direction shifts forward via translate to in front of the body.

## Animation
- **run-move (3s loop)**: transform-origin (7.5px,13px), 0%~5% translate(-4px,0) at the left, 45% translate(4px,0) runs to the right, 55%~95% translate(4px,0)→translate(-4px,0) runs back to the left.
- **run-bounce (0.3s loop)**: 25%/75% translateY(-0.8px) bouncing on each step.
- **step-outer (0.3s loop)**: outer legs lift at 50% translateY(-1.5px).
- **step-inner (0.3s loop)**: inner legs out of phase, lift at 0% translateY(-1.5px), land at 50%.
- **arm-l-turn (3s loop)**: 55%~92% translate(3px,1px) the left arm extends forward when running left, otherwise resets.
- **arm-r-turn (3s loop)**: 0%~42% translate(-3px,1px) the right arm extends forward when running right, resets at 50%.
- **arm-swing-a (0.3s loop)**: left arm rotate(15deg)↔rotate(-10deg) fast arm swing.
- **arm-swing-b (0.3s loop)**: right arm rotate(-15deg)↔rotate(10deg) out-of-phase arm swing.
- **eyes-look (3s loop)**: when running right translateX(1px), 10%~42% scaleY(0.7) squinting sprint; when running left translateX(-1px), 60%~92% scaleY(0.7) squint; eyes open scaleY(1) at the instant of turning.
- **shadow-move (3s loop)**: follows the body horizontally translateX(-4px~4px), scaleX(0.9) opacity(0.45) while running, scaleX(1) opacity(0.5) when turning.

## Expression
Clawd runs back and forth across the frame, its four legs stepping in fast alternation, both arms swinging widely, eyes squinting toward the running direction, briefly opening when it turns.
