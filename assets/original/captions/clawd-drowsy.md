# clawd-drowsy.svg

An animation of Clawd drowsily dozing off, on a 6-second loop.

## Body
The torso stays continuously squashed (scaleX 1.06-1.09, scaleY 0.91-0.94), simulating heavy drowsiness. The legs are extended to 1x3 (y=12). Both arms splay outward slightly and droop (rotate ±15°, translate 0,1), held still. The eyes are widened 1.5x1.5 squares, drifting slowly via scaleY between 0.2-0.6 (half-open, half-closed).

## Props
- **Low-battery icon**: gray (#888888) battery outline 5x3 + right-side terminal 0.8x1.4, containing a red (#F44336) charge bar 1x1.8, blinking on a 2-second period (opacity 1→0.2)

## Animation
- **Drowsy breathing (drowsy-nod, 6s)**: scaleX 1.06→1.09, scaleY 0.94→0.91, translateY 0.8→1.5px, a continuous heavy compression
- **Eyes drooping (eyes-droop, 6s)**: scaleY drifts slowly between 0.6→0.25→0.55→0.2, always half-closed
- **Battery blink (battery-blink, 2s)**: opacity 1→0.2 blinking alternately
- **Shadow (shadow-breathe, 6s)**: scaleX 1→1.06

## Expression
Clawd is so sleepy its eyes are squinting, its body breathing slowly under heavy compression, while the low-battery icon overhead blinks red.
