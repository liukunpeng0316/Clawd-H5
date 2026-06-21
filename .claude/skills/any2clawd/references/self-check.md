# Self-Check Process

**After every SVG generation, and after any modification to an already-generated SVG (adjusting the action, swapping props, changing the rhythm, etc.), you must run this entire process through completely — it cannot be skipped.** Every change can introduce floating, disconnection, or broken z-order; only re-running the self-check guarantees quality.

## 1. Common-Sense Logic Review (before the technical check)

First examine it from the angle of "what should this animation look like in reality," then look at the source coordinates:

- **Attachment plausibility**: a hat/headwear should overlap the top of the head rather than float; a held prop should meet the end of the arm; a backpack/cape should sit against the back of the torso. Any part that should be touching the body but has a visible gap is a floating error.
- **Physical consistency**: objects under gravity (sweat drops, tears, falling leaves) should move downward; thrown objects should follow an arc rather than a straight line; when jumping, the shadow should shrink or move away.
- **Occlusion order**: the front arm should occlude the side of the torso; the hat brim should occlude the top edge of the head; a tail/cape behind the body should not appear in front of the torso.
- **Motion semantics**: when bowing, the head should be lower than its normal position; when waving, the arm should leave its rest position; when jumping, the overall y should decrease (move up). If an animation keyframe's described semantics contradict the actual motion direction, it is a logic error.
- **Proportion**: prop size should be in proportion to Clawd's body (a coffee cup should not be bigger than the body, a hat should not be narrower than the head).

When you find a problem, fix it first before continuing with the subsequent checks.

## 2. Technical Checklist

Go through the source item by item — the full checklist is in `docs/reasoning-rules.md` "Common Mistakes Checklist" (transform-box/origin, front-arm collision and shadow, prop mounting z-order, held-in-front-of-body perspective, effect timing, XML validity, CSS structure and conflicts, frame-sampling check, etc.). Run through it after generating or modifying.

## 3. Render Review (critical)

In the source the parts may look connected, but the render can come out floating, broken, or drifting — only looking at the real render is reliable:

```bash
python tools/render_review.py --input workspace/<name>.svg
```

It renders to PNG using the system Chrome; after it generates, **READ these images** and confirm item by item: is the hat/prop really stuck to the head/hand? are the limbs connected to the body? is the face readable? are the particle directions reasonable? Add `--pause <seconds>` to freeze on a given frame to inspect details.

**Important — the default frame is `t=0`, where every animation sits at its identity transform (offset 0), so motion-induced gaps are invisible there.** To judge attachment you must also freeze at the **motion extremes** with `--pause`: pick the seconds where the body translate/rotate peaks (e.g. the top of a bob, the bottom of a slam-recoil) and re-render. Legs may run their own animation (stepping, kicking) — they don't have to share the body's group — but in every sampled frame, including the extremes, a leg must still read as joined to the body; if one visibly detaches mid-cycle, fix it. Arms are more forgiving: they swing on their own and a small shoulder offset is natural, so only flag an arm that is clearly detached and floating.
