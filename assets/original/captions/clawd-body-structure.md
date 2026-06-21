# Clawd Character Body Structure Reference

## Base Skeleton (clawd-static-base.svg)

Clawd is a pixel-art character composed entirely of rectangles; every part is a `<rect>` element.

### Colors
- Body color: `#DE886D` (salmon / terracotta)
- Eye color: `#000000` (black)
- Ground shadow: `#000000`, opacity 0.5

### Body Part Coordinates (based on a 15x16 unit canvas)

| Part | Position (x, y) | Size (w x h) | Notes |
|------|-------------|--------------|------|
| torso | (2, 6) | 11 x 7 | Main rectangle, the largest part |
| left-eye | (4, 8) | 1 x 2 | Small vertical black rectangle (normal open eye) |
| right-eye | (10, 8) | 1 x 2 | Small vertical black rectangle (normal open eye) |
| left-arm | (0, 9) | 2 x 2 | Left side of the torso |
| right-arm | (13, 9) | 2 x 2 | Right side of the torso |
| outer-left-leg | (3, 13) | 1 x 2 | |
| inner-left-leg | (5, 13) | 1 x 2 | |
| inner-right-leg | (9, 13) | 1 x 2 | |
| outer-right-leg | (11, 13) | 1 x 2 | |
| ground shadow | (3, 15) | 9 x 1 | Semi-transparent black |

### Design Constraints
- **Clawd has no mouth**; no expression may add any mouth element. Emotion is conveyed entirely through eye shape, body motion, and effects.
- **Prefer action over words**: do not use speech bubbles, caption boxes, or long sentences. To express semantics like confusion, thinking, or tiredness, prefer a tilted head, eye rhythm, arm position, and body pauses. When it is truly necessary to make the point, a short floating text of 2-4 characters may be added (a soft constraint, not a hard ban).
- The arms and legs must stay visually connected to the torso throughout the animation; they cannot float or detach.

### Structural Characteristics
- The character's center is roughly at x=7.5
- Eye spacing is 6 units (x=4 to x=10)
- Eye shape: a normal open eye is a 1-wide vertical rectangle (1x2); a continuously half-closed squint/tired state can be flattened and widened (e.g. a 1.5-wide flat eye) — a squint inherently needs to be flatter and wider
- There is no gap between the arms and the torso (left arm x=0~2 abuts torso x=2, right arm x=13~15 abuts torso x=13)
- The four legs are distributed in pairs: the two left legs are 2 units apart, the right side likewise, with 4 units of spacing in the middle
- The legs at y=13 directly meet the bottom of the torso at y=13 (6+7=13)

### Structural Changes in Variant Poses
- **Standing animation**: legs are usually extended to 1x3 (starting at y=12), with a 1px overlap with the torso to ensure connection
- **Sleeping / sprawled**: the torso becomes a wide flat shape (about 13x5), and the legs shrink to 1x1 stubs
- **Overheated**: the torso is fully horizontal (x=1, y=10, 13x5), and the eyes become crosses or thin lines
