# clawd-wow.svg

A wow animation of Clawd, on a 4-second loop, transitioning from normal eyes to gold star eyes, accompanied by bouncing, hands clasping together, and gold sparkle particles.

## Body
Standard torso 11x7 located at (2,6). It has a dual eye form — normal eyes (each 1x2 fill=#000000) at (4,8) and (10,8); star eyes are a four-pointed star path (fill=#FFD700), left star center (4.5,9), right star center (10.5,9), shown by switching opacity. Both arms (each 2x2) at (0,9) and (13,9) gather forward when wowing translate(±5px,1px), each with a 0.25 opacity black drop shadow. The four legs (each 1x4) rest still at x=3,5,9,11, y from 11 to 15.

## Props
- Sparkle particle 1: fill=#FFD700 (1x1) located at (-1,4), delay 0s
- Sparkle particle 2: fill=#FFC107 (1x1) located at (15,3), delay 0.5s
- Sparkle particle 3: fill=#FFF59D (1x1) located at (7,2), delay 1.0s
- Sparkle particle 4: fill=#FFA000 (1x1) located at (-3,8), delay 0.3s
- Sparkle particle 5: fill=#FFD700 (1x1) located at (17,9), delay 0.8s

## Animation
- **breathe (3.2s loop)**: centered at (7.5px,13px), a faint breathing rise and fall of scale(1.02,0.98)+translateY(0.3px)
- **wow-bounce (4s loop)**: centered at (7.5px,15px), 24% crouch scale(1.02,0.97)+translate(1px,0), 28% bounce up translate(1px,-1.5px)+scale(0.98,1.03), 36% crouch again, 40% bounce to the highest translate(1px,-2px), 44%-60% hold the peak, 68% slowly returns to position. Still during 0-18% and 74%-100%
- **eyes-normal-vis (4s loop)**: normal eyes opacity(1) visible during 0-18% and 74%-100%, hidden opacity(0) during 20%-72%
- **star-vis (4s loop)**: star eyes opacity(0) hidden before 22% and after 66%, opacity(1) shown during 24%-64%, alternating with the normal eyes
- **star-pulse (0.8s loop)**: star eyes continuously pulse scale varying between 1→1.2→1.5→1.2, reaching the maximum scale(1.5) at 50%
- **sparkle-vis (4s loop)**: sparkle particles opacity(1) visible only in the 28%-62% interval, synced with the star-eye phase
- **sparkle-pop (1.5s loop)**: particles swell from scale(0.3) to scale(1), then float up translateY(-4px) and shrink to scale(0.3) and disappear, the 5 particles staggered via different delays
- **arm-l-wow (4s loop)**: the left arm at 24% translate(5px,1px) moves forward to the body's center, 64% holds, 72% returns to position
- **arm-r-wow (4s loop)**: the right arm mirrors it, at 24% translate(-5px,1px) moving forward, clasping with the left arm in front of the body
- **shadow-wow (4s loop)**: during the bounce scaleX varies between 0.92-1.05, opacity varies between 0.4-0.5, reflecting the body's bounce height

## Expression
Clawd first stands with a normal expression, then blinks and switches to gold star eyes, excitedly bouncing twice in a row, clasping its hands in front of its body, gold sparkle particles bursting all around, and finally blinks to return to the normal expression.
