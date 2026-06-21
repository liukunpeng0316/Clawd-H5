# clawd-nodding-smile.svg

Animation of Clawd nodding with a smile to show agreement, 2s loop.

## Body
Standard upright posture, torso 11x7 at (2,6). The four legs 1x4 stay still. Both arms 2x2 at (0,9) and (13,9) rest motionless at the sides of the body. There are two sets of eyes: normal rectangular eyes 1x2 at (4,8)/(10,8), and smiling ^^ eyes drawn with a polyline (stroke=#000000, stroke-width=0.7), switched in when nodding.

## Animation
- **breathe (3.2s loop)**: transform-origin (7.5px,13px), at 50% scale(1.02,0.98) translate(0,0.3px)
- **nod (2s loop)**: transform-origin (7.5px,13px), 30%~34% first nod scale(1.03,0.95) translateY(1px), 48%~52% second nod with the same parameters, returns to original position the rest of the time
- **eyes-normal-vis (2s loop)**: 0%~22% opacity:1 shows normal eyes, 24%~68% opacity:0 hidden, 70% restored to shown
- **eyes-smile-vis (2s loop)**: 0%~26% opacity:0 hidden, 28%~64% opacity:1 shows smiling eyes, 66% switches back to hidden
- **eyes-nod-shift (2s loop)**: when nodding translateY(0.8px) sinks with the body, on rebound translateY(-0.2px) a slight bounce back
- **shadow-nod (2s loop)**: during the nod compression scaleX(1.06) opacity(0.48), otherwise scaleX(1) opacity(0.5)

## Expression
Clawd nods amiably in succession, and as it nods its eyes switch from the normal state to ^^ smiling curved eyes, expressing agreement and delight.
