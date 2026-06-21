# clawd-rofl.svg

An animation of Clawd laughing so hard he rolls on the floor. 4s loop, going from standing and laughing hard to flipping 90° onto his side and rolling on the floor, kicking all four legs, with laugh lines splashing out.

## Body
fall-rotate 4s rotate(0→90°) flips onto his side, with ±4° micro-shaking layered on during the rolling phase (33-60%). fall-compensate 22-62% translate(-7px,-2px) corrects the position. laugh-shake 0.12s linear micro-shakes throughout. Legs legs-kick-outer/inner 4s linear kick wildly out of sync (outer legs at 20/36/52%, inner legs at 24/40/56%). The eyes are laughing-eye polylines (^^), flickering blinks via scaleY at 47-53%. Both arms arm-flail-l/r 4s rotate(0→±20°) windmill around.

## Props
- **Standing laugh lines**: When the character is standing, 3 wavy laugh lines on the left (brown #8D6E63), flickering at 0.3s step
- **Rolling laugh lines**: After flipping over, 3 colored laugh lines (#FFD700/#FFC107/#FFA000) on the upper right, flashing during the rolling phase 28-58%

## Animation
- **roll-move (4s ease-in-out)**: translateX overall sway
- **fall-compensate (4s)**: 22-62% position correction
- **fall-rotate (4s)**: rotate(0→90°) flip onto side + micro-shake
- **laugh-shake (0.12s linear)**: High-frequency trembling
- **legs-kick-outer / legs-kick-inner (4s linear)**: Kicking wildly out of sync
- **smile-blink (2.5s)**: Laughing eyes flicker a blink at 47-53%
- **arm-flail-l / arm-flail-r (4s)**: Both arms windmill around
- **laugh-lines-vis / laugh-lines-roll-vis (4s)**: The two laugh-line sets are mutually exclusive in opacity — standing set 0-12%/72-100%, rolling set 28-58%
- **ll-flash1/2/3 (0.3s step-end)**: Laugh lines pulse and flicker
- **shadow-anim (4s)**: Shadow sways in sync

## Expression
Clawd stands there laughing himself silly, brown laugh lines bursting out beside him, until mid-laugh he flips a full 90° onto his side and rolls onto the floor, legs kicking and arms flailing, while gold laugh lines flicker nonstop around him.
