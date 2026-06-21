# clawd-bow-thanks.svg

Animation of Clawd bowing in thanks, 4s loop: the body presses forward, both arms fold together in front, and a heart pops out above the head.

## Body
Standard torso with breathing (3.2s). During the bow phase (22-48%) the torso uses scaleY(0.82) to compress and lean forward; the eyes switch to a smiling-eye variant — the normal eyes squint half-closed via scaleY(0.45) translateY(1.5px); both arms fold together in front (left translate(5,2), right translate(-5,2)), paired with a bottom-right shadow to resolve same-color legibility.

## Props
- **Big heart**: a pixel-assembled pink heart (#F28B9E) floating above the head, its heart outline built from multiple rectangles

## Animation
- **breathe (3.2s)**: standard breathing scale(1.02, 0.98)
- **body-bow (4s)**: 22-48% scaleY(0.82) bow compression, returns to position the rest of the time
- **eyes-normal-vis (4s)**: normal eyes opacity visible at 0-22%/48-100%, switched out during the bow
- **eyes-normal-transform (4s)**: during the bow phase scaleY(0.45) + translateY(1.5px) to squint
- **arm-l-bow / arm-r-bow (4s)**: 22-48% both arms fold together in front translate(±5px, 2px)
- **big-heart-vis (4s)**: 26% pops out scale(1.1), 48% holds, 54% fades out opacity 0

## Expression
Clawd bends down in a deep bow of thanks, both arms folded gracefully in front, eyes squinted into smiling curved slits, and a pink heart drifts up above the head to express gratitude.
