# clawd-approved.svg

A satisfied animation of Clawd raising a green "approved" round sign, on a 3-second loop.

## Body
Standard upright pose, with the left arm resting still at the side. The right arm acts as the pivot for raising the sign (pivot 14,10), swinging counterclockwise 270° from behind the back up to overhead. The eyes switch between two sets: normal vertical-bar eyes → happy ^^ eyes, transitioning via an opacity+scaleY blink. The eyes have a small drift (glance right → up → center).

## Props
- **Wooden stick handle**: brown (#795548) horizontal connecting rod, (15,9.5) 5.5x1
- **Green round sign**: double-layered circle (#43A047/#4CAF50), radius 2.5/2, with a white ✓ checkmark in the center
- **Sign-face shine**: a white dot that flashes twice via shine-pulse after the sign reaches the top

## Animation
- **Body sway (sway, 2.5s)**: scaleX 1-1.02, scaleY 1-0.98, a slight up-and-down breathing feel
- **Right arm raising sign (arm-swing-up, 3s)**: 0-33% rotate(180°) hidden behind the back → 45% rotate(-95°) overshoot up to overhead → 48% rebound (-83°) → 52% settle (-90°) → 93% hold → instant cut back behind the back
- **Eye switch**: 0-31% normal eyes → 31-35% double-blink transition → 35-93% happy ^^ eyes → 93-95% blink back → 95-100% normal eyes
- **Eye drift (eye-drift, 3s)**: look right → return to center during blink → look upward (looking at the sign) → return to center
- **Shadow (shadow-breathe, 2.5s)**: scale 1-1.02

## Expression
Clawd happily flings a green ✓ round sign up overhead from behind its back, the eyes change from normal to a happy ^^ state, gazing admiringly at the raised sign.
