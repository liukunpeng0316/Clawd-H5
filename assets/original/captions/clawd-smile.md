# clawd-smile.svg

A gentle swaying animation of Clawd smiling contentedly, on a 4-second loop, with a ^^ curved-brow smiling-eye expression.

## Body
Standard upright pose, with the torso 11x7 located at (2,6). The eyes are a non-standard form — using stroke-outlined ^^ polylines to represent smiling eyes, the left eye vertices (3.5,9.5)→(4.5,8.5)→(5.5,9.5), the right eye vertices (9.5,9.5)→(10.5,8.5)→(11.5,9.5), stroke=#000000 width 0.7, no fill. Both arms (each 2x2) rest still at (0,9) and (13,9). The four legs (each 1x3) rest still at x=3,5,9,11, y from 12 to 15.

## Animation
- **breathe (3.2s loop)**: centered at (7.5px,13px), a faint breathing rise and fall of scale(1.02,0.98)+translateY(0.3px)
- **sway (4s loop)**: centered at (7.5px,15px), at 30% rotate(1.5deg)+translateX(0.5px) leaning right, at 70% rotate(-1.5deg)+translateX(-0.5px) leaning left, forming a gentle side-to-side sway
- **smile-blink (4s loop)**: centered at (7.5px,9px), in the 47%-53% interval scaleY(0.1) a quick blink of the smiling eyes, scaleY(1) keeping the ^^ expression the rest of the time
- **shadow-sway (4s loop)**: centered at (7.5px,15.5px), offsetting scaleX(1.03)+translateX(±0.3px) following the body's sway direction, opacity varying between 0.48-0.5

## Expression
Clawd, with a ^^ smiling-eye expression, sways gently side to side in contentment, occasionally blinking.
