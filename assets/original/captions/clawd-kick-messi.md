# clawd-kick-messi.svg

Clawd, wearing an Argentina No. 10 jersey, raises its right leg to kick a soccer ball to the left, looping every 4 seconds, with sparks bursting at the point of impact.

## Body
The same kicking structure as clawd-kick-football: a standard 11x7 torso at (2,6) that tilts forward and back via `body-kick`; the eyes are standard 1x2 black rectangles at (4,8)/(10,8) that track the ball; the left leg pair (x=3,5) supports while the right leg pair (x=9,11) kicks around (10,12); both arms (0,9)/(13,9) swing for balance. The difference is an Argentina jersey layered over the torso and arms (see Props).

## Props
- **Argentina jersey**: A white base covering the torso below the eyes (y≥10.2), overlaid with 3 sky-blue vertical stripes (#75AADB, x=2/5.6/9.2, width 1.8); the V-neck is cut out with a body-colored polygon (#DE886D, points 5.5,10 7.5,11.4 9.5,10); the chest shows No. 10 — the "1" is a solid rectangle (#222222) and the "0" is a stroked rectangle (stroke-width 0.4, visually the same height as the "1").
- **Sleeves**: The inner half-cells of the left and right arms (x=1 / x=13) are layered white + sky-blue on top, while the outer half-cells keep the skin color as the hand.
- **Soccer ball**: A white circle (cx=1,cy=14,r=2) + dark-gray stroke + black pentagon patches, flying left via `ball-move` and rotating via `ball-spin`.
- **Impact sparks**: 3 gold small squares (#FFC107) that flash at the lower left the moment of the kick.

## Animation
- **kick-body (4s loop)**: wind up → lean back at 38% → push forward at 48% → recover.
- **legs-right-kick (4s)**: right leg swings back -30° to wind up → kicks forward +40° → falls back.
- **legs-left-kick (4s)**: the support leg lifts slightly to keep balance.
- **arm-l-balance / arm-r-balance (4s)**: both arms swing in opposite directions for balance.
- **ball-move (4s)**: the ball rolls in from translate(14px), then accelerates left to -22px after being kicked at 48%.
- **ball-spin (4s linear)**: the ball spins counterclockwise continuously.
- **eyes-watch (4s)**: the eyes track the ball from right to left, squinting with scaleY(0.7) at the moment of the kick.
- **spark-1/2/3 (4s)**: three sparks scatter to the upper left at the instant of impact.
- **shadow-kick-anim (4s)**: the shadow enlarges slightly at the moment of the kick.

## Expression
Clawd, in an Argentina No. 10 jersey, winds up and raises its right leg to send the ball flying left; the ball spins out at high speed, sparks burst at the impact point, and the body tilts forward with the kick before recovering — a kicking loop with a star-player nod.
