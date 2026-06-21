# clawd-confused-big-question.svg

Animation of a big question mark springing sharply upward above a confused Clawd, 6s loop, with the body following the question mark up into the air.

## Body
Standard torso. At 10-56% the body tilts side to side with rotate(±6°), cocking the head, while the eyes flatten in confusion via scaleY(0.55); at 30-56% the whole body uses clawd-rise translateY(-13 to -14.6px) to lift into the air following the question mark, and the shadow shrinks via scaleX.

## Props
- **Big blue question mark**: assembled from 6 rounded rectangles (#4A90D9), floating above the head, springing up along with the body

## Animation
- **breathe (3.2s)**: standard breathing
- **big-q-spring (6s)**: the question mark scaleY springs 0.02 → 1.1 → 1, synced with the body lifting off
- **clawd-rise (6s)**: 30-56% the body lifts off translateY(-14.6px) then falls back down
- **body-tilt (6s)**: 10-56% rotate(±6°) confused head cock
- **eyes-react (6s)**: 10-56% scaleY(0.55) eyes flattened in confusion
- **ground-shadow (6s)**: shadow scaleX contracts to reflect the height while airborne

## Expression
Clawd cocks its head and squints in confusion as a big blue question mark boings up above its head like a spring, the whole body lifting into the air along with it, then they fall back to the ground together.
