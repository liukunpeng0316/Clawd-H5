# clawd-salute.svg

Clawd standing at attention and saluting, 3s loop, including foot-stomping, a raised-arm salute, and sparkle particle effects.

## Body
Standard upright stance, torso 11x7 at (2,6). Eyes (1x2 each) at (4,8) and (10,8), scaleY enlarged to 1.3 during the salute to indicate widened eyes. Left arm (2x2) stays still at (0,9); the right arm (2x2) rotates -30deg about the shoulder pivot (13px,10px) from (13,9) and moves up -1.5px to complete the salute. The four legs are split into an outer pair (x=3, x=11) and an inner pair (x=5, x=9), each 1x4, raising -1.5px alternately to simulate stomping.

## Props
- Sparkle particle 1: fill=#FFC107 (1x1) at (12,6.5), flying out to the upper right during the salute
- Sparkle particle 2: fill=#FFD700 (1x1) at (12,7.5), flying out to the right during the salute
- Sparkle particle 3: fill=#FFF59D (1x1) at (12,8.5), flying out to the lower right during the salute

## Animation
- **breathe (3.2s loop)**: centered on (7.5px,13px), a faint breathing rise and fall of scale(1.02,0.98)+translateY(0.3px)
- **legs-outer (3s loop)**: the outer legs raise -1.5px over the 8%-16% interval, stomping down before the inner legs
- **legs-inner (3s loop)**: the inner legs raise -1.5px over the 14%-22% interval, stomping down right after the outer legs
- **arm-salute (3s loop)**: the right arm, pivoting on (13px,10px), raises quickly at 7%-10% translate(-1px,-1.5px)+rotate(-30deg), holds the salute pose at 12%-40%, and lowers back at 45%
- **eyes-salute (3s loop)**: centered on (7.5px,9px), scaleY(1.3) widens the eyes during the 10%-40% salute, scaleY(1) the rest of the time
- **sp-salute-1 (3s loop)**: appears at 12% from (12,6.5) at scale(1), flying out to the upper right translate(7px,-2px), shrinking and vanishing
- **sp-salute-2 (3s loop)**: appears at 13%, flying out to the right translate(8px,0) and vanishing
- **sp-salute-3 (3s loop)**: appears at 14%, flying out to the lower right translate(7px,2px) and vanishing
- **shadow-salute (3s loop)**: centered on (7.5px,15.5px), slight expansion scaleX(1.06)+opacity(0.48) when stomping

## Expression
Clawd first stomps its feet quickly to stand at attention, then raises its right arm in a salute, widens its eyes, with gold sparkle particles bursting out beside its arm, and afterward returns to a standing pose.
