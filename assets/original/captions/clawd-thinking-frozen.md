# clawd-thinking-frozen.svg

Clawd thinking until it crashes, its body fading in color, its eyes squashed into dead-fish eyes, with a spinning loading ring above its head, 6s loop.

## Body
Standard torso. 20-62% body-fade the color gradually shifts from #DE886D to grayish-brown #C4A99A, restored at 72%. Synchronized eye-fade eyes #000000 → #555555. During the freeze phase breathe pauses. eyes-state 20-62% scaleY(0.1 → 0.7) + scaleX(1.1) squashes flat and stretches wide to form a "dead-fish eye" stare.

## Props
- **Loading ring**: 8 rounded squares (#7B8FA0) arranged in a ring, opacity grading 1 → 0.08 to create a spinning visual, positioned above the head

## Animation
- **body-fade (6s)**: torso fill fades to gray
- **eye-fade (6s)**: eye fill fades to gray
- **breathe (6s)**: active only during the normal phase (0-10%/80-100%), paused during the freeze phase
- **eyes-state (6s)**: 20-62% eyes squash flat and stretch wide into dead-fish eyes
- **spin (1.2s steps(8))**: loading ring rotates 0-360° in 8 stepped segments
- **spinner-fade (6s)**: 14-24% opacity 0→1 appears, 68-100% hides
- **shadow-fade (6s)**: opacity 0.5 → 0.35 when frozen

## Expression
Clawd is standing there and suddenly seems to crash: its body color slowly fades to grayish-brown, its eyes squash flat and stretch wide into vacant "dead-fish eyes", a segmented spinning gray loading ring appears above its head, and finally it returns to its normal color and demeanor.
