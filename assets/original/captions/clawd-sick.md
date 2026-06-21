# clawd-sick.svg

Clawd is sick with a fever, body trembling, legs staggering, eyes half-closed and listless, a crossed bandage on its forehead, flushed cheeks, and cold sweat beading up, on a 4-second loop.

## Body
Standard torso 11x7 at (2,6), with the whole `body-sick` trembling continuously (slight scale squeeze + small displacement and rotation). The eyes are in a half-closed, weary state, 1.5x1.5 black rectangles at (3.5,8.5)/(10,8.5), with `eyes-tired` doing a slow scaleY 0.2~0.55 squint. Two arms 2x2 at (0,9)/(13,9), drooping limply (left arm -10°, right arm +10° static tilt). Four legs in an outer pair (x=3,11) and an inner pair (x=5,9), alternating translateY in an unsteady, staggering stance.

> Note: the eyes use a 1.5-wide flat eye, corresponding to the continuously half-closed squint/weary state — a squint inherently needs to be flatter and wider; this is intentional design, distinct from the normal 1×2 eye.

## Props
- **Crossed bandage**: upper right of the head (translate 9,5.5), two white diagonal rectangles (#FFFFFF, ±45° rotation) crossing + a light gray center pad (#F5F5F5), conforming to the surface of the head.
- **Feverish flush**: 5 red diagonal lines in the center of the face (#E84040, opacity 0.6), simulating flushed cheeks.
- **Cold sweat**: 2 light blue sweat drops (#87CEEB), staggered (the second has delay 1.8s), drifting up and to the left and fading out.

## Animation
- **sick-shiver (4s loop)**: the torso trembles slightly and continuously (displacement ±0.8px + rotation ±2.5°), conveying chilled shivering.
- **eyes-tired (4s)**: the eyes' scaleY undulates slowly between 0.2~0.55, half-closed and listless.
- **leg-outer-stumble / leg-inner-stumble (4s)**: the outer and inner leg pairs lift and drop translateY out of sync, conveying an unsteady stagger.
- **sweat-float (4s)**: the two sweat drops drift up and to the left and fade out.
- **shadow-sick (4s)**: the ground shadow scales slightly with the trembling.

## Expression
Clawd stands sickly and trembling, eyes half-open and limbs limp, a crossed bandage on its forehead, cheeks burning red, cold sweat beading up drop by drop — a weak, miserable sickness loop.
