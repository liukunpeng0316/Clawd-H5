# clawd-punching.svg

A continuous combat animation of Clawd angrily throwing punches, on a 0.7-second loop.

## Body
Standard torso 11x7 located at (2,6), the body held continuously in a crouched fighting stance (scale(1.02~1.04, 0.94~0.97) translate slight sway). The four legs 1x4 at (3,11)/(5,11)/(9,11)/(11,11) stay still. The two eyes 1x2 at (4,8)/(10,8) stay continuously scaleY(0.7) in an angry squint, blinking once every 3 seconds. The left arm 2x2 at (0,9) and the right arm 2x2 at (13,9) are both moved forward in front of the body (left arm translate(3px,1px), right arm translate(-3px,1px)), with a 0.2 opacity drop shadow.

## Props
- Impact particles ×4: fill=#FFC107 (0.8x0.8) ×2 + fill=#FF9800 (0.7x0.7) ×2, appearing respectively when the left and right fists strike
- Anger symbol: located at (12,4), composed of four L-shaped polylines forming a cross shape, stroke=#FF3D00 stroke-width=0.6, with an overall rotate(45deg)

## Animation
- **body-bob (0.7s loop)**: transform-origin (7.5px,15px), 15% lean-left press-down translate(-0.4px,1px) scale(1.04,0.94), 65% lean-right press-down translate(0.4px,1px) scale(1.04,0.94), returning to center in between
- **punch-l (0.7s loop)**: the left arm enlarges scale(1.4) at 15% to simulate the punch impact, scale(1) otherwise
- **punch-r (0.7s loop)**: the right arm enlarges scale(1.4) at 65% to punch, alternating with the left fist
- **eyes-squint (3s loop)**: continuous scaleY(0.7) angry glare, 93%~96% scaleY(0.05) quick blink
- **imp-l1 (0.7s loop)**: at 15% appears at translate(4px,7.5px) opacity:0.9, 25% shrinks and disappears toward the upper left
- **imp-l2 (0.7s loop)**: at 16% appears at translate(5.5px,9px), 26% disappears
- **imp-r1 (0.7s loop)**: at 65% appears at translate(9px,7.5px), 75% disappears
- **imp-r2 (0.7s loop)**: at 66% appears at translate(7.5px,9px), 76% disappears
- **shadow-pulse (0.7s loop)**: during a punch scaleX(1.06) opacity(0.45), recovering to scale(1) opacity(0.5) in between
- **anger-pulse (0.7s loop)**: during a punch scale(1.15) swells, returning to scale(1) in between, always opacity:1

## Expression
Clawd glares wide-eyed and crouches its center of gravity low, throwing fierce punches alternating left and right, each punch accompanied by a burst of gold-orange impact particles, the anger symbol overhead pulsing along with the punching momentum.
