# clawd-rejected.svg

Animation of Clawd raising a rejection sign and shaking its head to show disapproval, 3s loop.

## Body
Standard torso 11x7 at (2,6). The four legs 1x2 at y=13~15 (shorter). The left arm 2x2 at (0,9) stays still. The right arm 2x2 at (13,9) performs the sign-waving motion pivoting on (14px,10px), and the sign group uses the same animation. The eyes have two sets: normal rectangular eyes 1x2 and a frowning squint (same shape but scaleY(0.7)), switched via a blink-style swap. The eyes are wrapped in an eyes-drift group to achieve a left-right head-shake parallax.

## Props
- Sign handle: fill=#795548, 5.5x1, at (15, 9.5), rx=0.2
- Circular rejection sign: outer ring fill=#C62828 r=2.5, inner ring fill=#E53935 r=2, center (21,10)
- White X mark: two crossing lines stroke=#FFFFFF stroke-width=0.6, from (19.9,8.9) to (22.1,11.1)
- Reflective highlight: fill=#FFFFFF r=0.6 at (22, 9.3), flashing via shine-pulse

## Animation
- **sway (2.5s loop)**: transform-origin (7.5px,15px), 50% scale(1.02,0.98) translate(0,0.5px) breathing sway
- **arm-swing-up (3s loop)**: 0%~33% rotate(180deg) the sign hidden behind the body, 45% rotate(-95deg) quickly waves it up overhead, 48%~52% spring rebound to rotate(-90deg)/-83deg/-90deg to settle, 93% begins to retract rotate(180deg)
- **shine-pulse (3s loop)**: 52%~62% opacity 0→0.5 first flash, 72%~82% second flash, otherwise opacity:0
- **eyes-normal-vis (3s loop)**: 0%~29% opacity:1 scaleY(1) eyes open normally, 31% scaleY(0.05) closing, 31.01% opacity:0 hidden, 95.01% reappears and opens
- **eyes-frown-vis (3s loop)**: 33.01% opacity:1 opens from scaleY(0.05) to scaleY(0.7) frowning squint, 91%~93% closes and disappears
- **eye-drift (3s loop)**: 20%~28% translateX(1px) looking right, 40% translateX(-1px) looking left, 50% translateX(1px), 60% translateX(-1px), a decaying oscillation simulating a head shake
- **shadow-breathe (2.5s loop)**: 50% scale(1.02) slight breathing

## Expression
Clawd first stands normally, then its right arm quickly waves the red X rejection sign up overhead from behind its back, the eyes switch to a frowning squint and shake side to side to show disapproval, and the sign's surface flashes with reflected light.
