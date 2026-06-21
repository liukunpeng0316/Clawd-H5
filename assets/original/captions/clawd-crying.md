# clawd-crying.svg

An animation of Clawd crying sadly, looping continuously.

## Body
The torso breathes (3.2s). The legs are extended to 1x4 (y=11) and stay still. Both arms hang motionless at the sides. The eyes are downward arcs ⌢⌢ (a sad expression), with a 3-second blink cycle. The entire upper body has a fast 0.3-second micro-tremble (±0.4px) to simulate sobbing.

## Props
- **Tears**: 4 light-blue (#4FC3F7/#81D4FA) rounded rectangles (0.7x1.2) that fall from beneath the eyes, in two staggered waves (left 0/0.75s, right 0.5/1.25s).

## Animation
- **Breathing (breathe, 3.2s)**: scaleX 1-1.02, scaleY 1-0.98.
- **Sobbing tremble (sob, 0.3s)**: translateY ±0.4px in a fast loop.
- **Sad blink (sad-blink, 3s)**: a quick close (opacity 0) and reopen between 42-50%.
- **Tear fall (tear-fall, 1.5s)**: appears below the eye → translateY 3px falling → fades out as it nears the ground.
- **Shadow tremble (shadow-sob, 0.3s)**: scaleX 1-1.02 in sync with the micro-tremble.

## Expression
Clawd hangs both arms down as its arched, sad eyes keep dropping tears, its body trembling slightly from sobbing.
