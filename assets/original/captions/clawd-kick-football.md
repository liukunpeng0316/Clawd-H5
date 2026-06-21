# clawd-kick-football.svg

Clawd lifts his right leg to kick the football off to the left. 4s loop, with the body first winding up by leaning back then sending forward, and sparks bursting at the point of impact.

## Body
Standard torso 11x7 at (2,6), fill=#DE886D, the whole thing `body-kick` leaning back and forth and squashing along with the kicking leg. The eyes are standard 1x2 black rectangles at (4,8)/(10,8), scanning left and right with the ball and squinting via scaleY at the instant of impact. The four legs split into two groups: the left pair (x=3,5) supporting, and the right pair (x=9,11) swinging widely around (10,12) to complete the kick. Both arms 2x2 at (0,9)/(13,9) swing side to side for balance.

## Props
- **Football**: A white circle (cx=1,cy=14,r=2) + dark gray stroke (#333333) + two black pentagon patches (path), flying from right to left with `ball-move` and rotating counterclockwise with `ball-spin`.
- **Impact sparks**: 3 small gold squares (#FFC107) that flash and scatter at the lower-left impact point only at the instant of the kick (48–57%).

## Animation
- **kick-body (4s loop)**: 25% start winding up, 38% slight lean back, 48% send forward (rotate -4deg), then recover.
- **legs-right-kick (4s)**: The right leg pair swings back -30° to wind up at 38% → kicks forward +40° at 48% → drops back.
- **legs-left-kick (4s)**: The supporting legs lift slightly to keep balance.
- **arm-l-balance / arm-r-balance (4s)**: Both arms swing in the opposite direction to keep balance.
- **ball-move (4s)**: The ball rolls in from translate(14px), and after being kicked at 48% accelerates left to -22px.
- **ball-spin (4s linear)**: The ball spins continuously counterclockwise (accelerating after the kick).
- **eyes-watch (4s)**: The eyes follow the ball from right to left, squinting scaleY(0.7) at the instant of impact.
- **spark-1/2/3 (4s)**: At the instant of impact, three sparks scatter up and to the left and fade out.
- **shadow-kick-anim (4s)**: The ground shadow enlarges slightly at the instant of impact.

## Expression
Clawd watches the football rolling toward him, winds up, then lifts his right leg to kick the ball off to the left, sparks burst at the point of impact, and his body leans forward with the kicking leg before recovering to a standing position.
