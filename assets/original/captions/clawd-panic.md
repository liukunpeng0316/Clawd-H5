# clawd-panic.svg

Clawd flipped upside down and struggling, legs kicking skyward and arms flailing in panic, 3s loop, with X eyes + flying tears.

## Body
The whole thing fall-rotate 3s rotate(180°) flips upside down, with a ±4° micro-jitter layered on during the hold phase. fall-compensate translate(-5px, -9px) corrects the canvas position after the flip. body-shake 0.12s linear high-frequency micro-tremor. Legs legs-kick-outer/inner 0.35s linear out-of-phase high-frequency kicking. The eyes turn into X shapes (crossed-diagonal polyline), 47-53% scaleY(0.1) blink. Both arms arm-flail-l/r 0.7s ease-in-out windmill rotation rotate(0→±20°).

## Props
- **Tears**: three, splashing to the left and right respectively (-3/+3px offset), fading out at 100%

## Animation
- **roll-move (3s ease-in-out)**: translateX 0 → -3 → 0px overall wobble
- **fall-compensate**: static transform position correction
- **fall-rotate (3s)**: rotate(180°) + micro-jitter ±4°
- **body-shake (0.12s linear)**: high-frequency tremor
- **legs-kick-outer / legs-kick-inner (0.35s linear)**: legs kicking out of phase
- **arm-flail-l / arm-flail-r (0.7s ease-in-out)**: arms flailing windmill-style
- **x-eyes-blink (2.5s)**: 47-53% X eyes blink
- **tear-fly1/2/3 (0.8s ease-out)**: three tears with delays 0/0.3/0.6s flying outward in stagger
- **shadow-anim (3s ease-in-out)**: shadow wobbles following translateX

## Expression
Clawd flips entirely upside down, legs kicking skyward in struggle, arms flailing like windmills, X eyes flickering, tears splashing in every direction, the body shaking and wobbling on the ground unable to stop.
