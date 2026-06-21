# Animation Generation Reasoning Rules

## Overall Flow

```
Natural language input
    │
    ▼
Step 1: Semantic decomposition — break into a list of atomic actions
    │
    ▼
Step 2: Reference retrieval — find the nearest reference from the caption library
    │
    ▼
Step 3: Spatial reasoning — determine the transform for each part
    │
    ▼
Step 4: Timing/sequencing — design keyframes and inter-part synchronization
    │
    ▼
Step 5: Layering and constraint checks — prevent clipping/occlusion errors
    │
    ▼
Step 6: Generate SVG → verify → correct
```

---

## Step 1: Semantic Decomposition

Decompose the natural language description into a combination of atomic actions. Each atomic action must specify:
- **Target part**: which body part participates (torso, left arm, right arm, leg, eyes)
- **Motion type**: translate / rotate / scale / opacity
- **Semantic intent**: what this action expresses

### Generation Boundaries

- Prefer expressing semantics through action: if it can be expressed with body/eyes/effects, don't use a text bubble; by default, no speech bubbles, explanation boxes, or long sentences. When a caption is needed, you may add short floating text of 2–4 characters (soft constraint, not a hard ban: by default don't write text, only add it when a caption is truly needed).
- Do not generate complex background scenes; prefer a single character, a single action, and a loopable animation.
- Clawd itself has no mouth; emotion is expressed through the eyes, body rhythm, arms, and small effects.
- The arms and legs must stay visually connected to the body throughout the entire animation cycle. Legs may carry their own animation (stepping, kicking, crawling) — they do **not** have to share the body's animation group. The actual requirement is that in **every sampled keyframe** the leg still reads as joined to the body. Because most transforms sit at offset 0 at the 0% frame, sample the motion extremes too: if a leg visibly separates from the body at the motion peak, that is a gap to fix. Arms are looser still — they naturally swing on their own timeline, so a modest offset at the shoulder reads as normal motion; only rule out an arm that is clearly detached and floating well away from the shoulder.
- Blinking and expression switching must use a unified timeline; avoid stacking multiple blink cycles.
- After generation, you must do a frame-sampling check: keyframes must cover at least the three stages of start, main-action peak, and recovery.
- Control Clawd's size range: export automatically crops to the union of content and then fills, so the farther a flying element travels, the smaller Clawd becomes. The visible content of every frame (including the farthest position of particles/props) should fall within an approximately 20–33 viewBox-unit square (the upper bound is Clawd at maximum, see surrender-helpless; the lower bound is the minimum, see kick-football), and the farthest element should not exceed about 16 units from the character center (7.5,10).

### Decomposition Examples

| Input | Decomposition |
|------|------|
| "clap" | both arms move forward (translate) + both arms close/open (alternating translate) + body bob (translateY) + clap spark (opacity) |
| "happy jump" | crouch in preparation (scaleY compression) + spring up (translateY) + both arms spread (rotate) + landing (scaleY) + starlight (opacity) |
| "confused looking around" | body moves left/right (translate) + eyes move with larger amplitude (translate, parallax) + one arm raised/paused |

### Atomic Action Dictionary (continuously accumulated)

**Torso**
- Breathing: scale(1.02, 0.98) translate(0, 0.5px), duration 3.2s
- Bounce: translateY(-10~-12px) + scaleY compression/stretch, duration 0.5-1s
- Sway/tilt: translate(±1-2px) + rotate(±2-3°), duration 2-6s
- Bob rhythm: translateY(±0.5-1px), same frequency as the action
- Lean: only the upper body translate(±1px, -1~-1.5px) tilting in a direction, legs static (lengthened to prevent disconnection), expresses engagement/enthusiasm
- Jump: whole body (including legs) translateY upward + shadow shrinks + landing scaleY compression, expresses excitement/bounce

**Arm**
- Side wave: rotate(±45°~±85°), about the shoulder joint
- Forward (to in front of body): translate(±3~5px, -2px), no rotate
- Scratch: rapid rotate bounce 3 times (alternating 0°→35°→0°)
- Held prop: translate to a fixed position + prop mounting
- Raise hand/lift arm: when moving upward via translate, it must be combined with rotate (e.g. salute rotate(-30°) about the shoulder joint); pure translate lacks a sense of swinging
- Both hands cupped in front of body (amazement/anticipation): left arm translate(5px, 1px), right arm translate(-5px, 1px); both arms centered in front of the body with about a 1-cell (2px) gap between them. Combine with a shadow rect (offset 0.5px, opacity 0.25) to solve same-color recognition. Note: arms are originally at x=0/13, after translate ±5px they reach x=5~7 and x=8~10 respectively
- Direction indication (running): the arm toward the direction of travel translate(±3px, 1px) to in front of the body, kept throughout, swapped when turning. Combine with a shadow (0.5px offset black rect) to solve same-color recognition

**Eye**
- Blink: scaleY(1→0.1→1), lasting 2-4 frames
- Look in a direction: translate(±1-3px, 0), amplitude larger than the body (produces parallax)
- Frown/strain: scaleY(0.7), eyes squashed to indicate effort or tension, with transform-origin centered
- Closed eyes: scaleY fixed at 0.1
- Happy squint: replace rect with polyline, drawing a "^^" arc
- Sad eyes: vertical flip of the happy squint; swap the y values of the polyline up and down to get a "⌢⌢" shape
- Star eyes (amazement/admiration): draw a four-pointed star with `<path>`, using Bézier curves for smooth rounded tips. Center-aligned with the normal eye center (x=4.5/10.5, y=9). Combine with a scale pulse animation (0.8s, scale 1→1.3→1) for twinkling. At specific moments the pulse can be amplified (scale 1.5) for emphasis
- Blink to switch expression: place two sets of eyes at once (e.g. rect normal eyes + polyline smiling eyes), and control their visibility mutually exclusively with an opacity animation. During the switch, both sets' opacity reach 0 at the same time, forming a "closed-eye" transition that avoids an abrupt jump. Note: the two sets of eyes must share the same animation cycle; do not stack blink animations with independent cycles (this causes uncontrollable random blinking)

**Leg**
- Standing still: no animation
- Tiptoe (sneaking): two groups alternating rotate(-25°) scaleY(0.7), duration 0.3-0.5s, with the body leaning forward rotate(2°)
- Stepping (running): outer group (x=3,11) and inner group (x=5,9) alternate translateY(-1.5px), duration 0.25-0.35s, purely vertical up/down, visually like two legs stepping
- Trembling: very short duration (0.1s) with tiny translate

**Effect**
- Starlight/spark: step-end frame animation, center → cross expansion → disappear
- Smoke/Zzz: translateY rising + scale enlarging + opacity fade out
- Small symbols/particles: can only serve as auxiliary effects, cannot be placed in speech bubbles, explanation boxes, or text labels. Semantics like confusion and surprise are preferably expressed through head tilt, eyes, pauses, and arm actions
- Sweat drop: translate drifting to the upper-left + opacity fade out
- Collision particle (clap/salute/slap): bursts out from the contact point at the instant two parts touch, fanning outward (translate 4~8px + scale 1→0.2 + opacity 1→0). Three particles stagger their start times by 0.5-1% to create a sense of layering. Very short duration (2-4% of the cycle) to convey the instantaneous impact

---

## Step 2: Reference Retrieval

Retrieve the most relevant caption files for the target animation from the `captions/` of **all collections** under `assets/` (not only `upstream/` and `original/`, but also any user-named collection). Use the canonical English `clawd-<name>.md` files; the `*.zh.md` siblings are Chinese viewing copies, ignore them here. Retrieval strategy:

1. **Action similarity**: which atomic actions in the target action have appeared in existing animations?
2. **Emotion similarity**: which existing animations' emotions match the target emotion (happy/confused/tired)?
3. **Structure similarity**: which existing animations' body deformations are similar to the target pose (standing/lying down/floating)?

Key information to extract after retrieval:
- Specific transform parameters (numeric references)
- Animation duration and easing functions
- Timing relationships between parts

---

## Step 3: Spatial Reasoning

### Transform Selection Decision Tree

```
Need to move a part?
    │
    ├─ Movement direction aligned with the joint's rotation axis?
    │   ├─ Yes → use rotate (e.g. arm swinging up and down)
    │   └─ No → use translate (e.g. arm from the side to in front of the body)
    │
    ├─ Need to deform the part?
    │   └─ Yes → use scale (e.g. torso compresses/expands while breathing)
    │
    └─ Need the part to appear/disappear?
        └─ Yes → use opacity (e.g. effect particles, prop highlights)
```

### Key Judgment for rotate vs translate

**Use rotate when:**
- The part swings about a fixed joint (e.g. arm swinging about the shoulder, leg kicking about the hip)
- The motion path is an arc
- Reference: arm wave (±45°~85°), leg tiptoe (rotate -25°)

**Use translate when:**
- The part needs to move from one region to another (e.g. arm from the side to in front of the body)
- The motion path is a straight line
- rotate would send the part to the wrong position (e.g. rotate 60°+ sends a side arm to the top of the head)
- Reference: clap (translate ±5px moves the arms to the front midline), eyes looking in a direction (translate ±3px)

### Parallax Effect

When the body and eyes move in the same direction, the eyes' translate amplitude should be **larger** than the body's (usually 2-3×), producing a natural parallax tracking effect:
- Body moves 1px → eyes move 2-3px
- This is the general rule for all "look in a direction" animations

---

## Step 4: Timing/Sequencing

### Duration Selection Reference

| Action type | Typical duration | Notes |
|----------|----------|------|
| Breathing | 3.2s | Background layer, always running |
| Blinking | 2-4s | Exists independently only when there is no expression switch |
| Fast action (typing/fanning/clapping) | 0.1-0.5s | High frequency, conveys tension/energy |
| Medium action (waving/swaying) | 0.5-2s | Everyday rhythm |
| Slow sequence (looking around/yawning) | 6-16s | Contains multiple sub-action segments |

### Multi-Part Synchronization Rules

1. **Main action sets the frequency**: first determine the core action's duration (e.g. clap 0.4s)
2. **Subordinate parts follow the frequency**: body bob and shadow pulse share the main action's duration
3. **Independent layers stack**: breathing (3.2s) can run independently; blinking keeps an independent cycle only when there is no expression switch
4. **Time-window alignment**: effects trigger at the main action's keyframes (e.g. sparks appear at the instant of closing, 45%-55%)

---

## Step 5: Layering and Constraint Checks

### SVG Render Layering (bottom to top)

```
1. Ground shadow (bottommost, y=15)
2. Legs (static or independently animated, y=12-15)
3. Torso (main rectangle, y=6-13)
4. Eyes (on the torso, y=8-10)
5. Arms/held props (can be in front of or behind the torso, depending on the action)
6. Effect particles (topmost)
```

**Key**: in SVG, elements drawn later are on top. When an arm needs to appear **in front of** the torso (e.g. clapping, holding a prop), the arm's `<g>` must be placed **after** the torso `<rect>`.

### Body Structure Constraints

- Torso scaleX range: 0.9 ~ 1.18 (beyond this looks unnatural)
- Torso scaleY range: 0.7 ~ 1.1 (squash/stretch limits)
- Arm translate range: not exceeding ±6px (otherwise it detaches from the body)
- In standing animations, legs' y coordinate should not be below 15 (the ground line)
- Shadow width should be positively correlated with body width: when the body squashes, the shadow widens; when it stretches, the shadow narrows

### Part Collision Check (must be performed)

When a part moves across regions via translate, you must verify region by region against the y/x ranges of every other part along the path:

```
Eye occupancy:   y = 8 ~ 10
Arm origin:      y = 9 ~ 11
Torso occupancy: y = 6 ~ 13

Arm forward safe zone: y ≥ 10 (does not cover the eyes), y ≤ 13 (does not exceed the bottom of the torso)
→ When the arm is forward, the y component of translate should be +1px (so y starts at 10)
→ Absolutely no negative y component (it would move up into the eye region)
```

### Standard Arm Shadow Practice

When the arm is forward over the top of the torso, the same color is not distinguishable, so a drop shadow must be added:
- **Layer order**: draw the shadow rect first, then the arm rect (shadow on the bottom layer)
- **Offset direction**: always to the lower right (+0.5px, +0.5px)
- **Shadow style**: same size as the arm, `fill="#000000" opacity="0.2"`
- The arm covers most of the shadow, with only the lower-right corner exposed, forming a natural drop shadow

### In-Front Held-Prop Viewpoint Rules

When the character faces the viewer head-on, the object held in hand needs a viewpoint chosen by how it is held:
- **Held horizontally** (book, notebook, tablet, plate): draw it as a **top side view**—showing the object's top surface + side thickness, rather than a head-on flat view
- **Held vertically** (phone, sign, flag): keep the **front view**

### Prop Mounting Rules

A held prop must follow:
1. The prop goes inside the corresponding arm's animation `<g>`, with coordinates based on the arm's local space
2. **Layer order**: draw the prop first, then the arm (the arm covers the gripping area of the prop, leaving both ends exposed → "hand gripping" effect)
3. Do not give the prop an independent animation group, or it will become disconnected from the arm motion

### Clothing/Jersey Rules

When Clawd needs to wear clothing (jersey, uniform, etc.):

- **Coverage**: clothing only covers the torso below the eyes (y≥10.2), without covering the eyes or head.
- **Color**: use a solid color (opacity=1), no transparency.
- **Neckline**: "carve out" the neckline by layering a body-color (`#DE886D`) shape over the clothing, rather than adding extra lines.
- **Sleeves**: sleeves cover the inner half-cell of the arm near the body (left arm x=1~2, right arm x=13~14), with the outer half-cell keeping skin color as the hand.
- **Number/text**: build the number from solid-filled or stroked rectangles; stroked elements need to account for the effect of stroke-width on visual size, ensuring they are visually the same height as the solid elements.
- **Layering**: draw the clothing above the torso and below the eyes.

### Common-Error Checklist

After each SVG generation or modification, check each item:

- [ ] **transform-box/origin**: do all CSS animation classes set `transform-box: fill-box` and `transform-origin`? (Especially for animations with scale; missing them causes parts to fly off)
- [ ] **Arm forward collision**: is the arm's y range after translate ≥10? (Must not cover the eyes y=8~10)
- [ ] **Arm closing gap**: in closing actions like clapping, do the arms' x ranges actually touch? (There should be no gap)
- [ ] **Same-color part recognition**: is the forward arm (#DE886D) layered over the torso (#DE886D) distinguishable? (Shadow on the lower-right bottom layer)
- [ ] **Arm shadow layer**: is the shadow drawn before the arm (bottom layer), offset to the lower right?
- [ ] **Prop mounting**: is the held prop inside the arm's animation group? Is the prop drawn before the arm (bottom layer, with the gripping area covered by the arm)?
- [ ] **Leg attachment across keyframes**: do the legs read as connected to the body in **every sampled keyframe**, including the motion extremes? Legs may have their own animation — they need not share the body's group — but sample the peak frames (not just 0%, where offsets are 0 and gaps hide) and confirm no leg visibly detaches mid-cycle. Arms are exempt — independent swing is fine; only flag an arm that floats clearly detached from the shoulder.
- [ ] **In-front object viewpoint**: is a horizontally held object drawn as a top side view? (Not a head-on flat view)
- [ ] Does the arm exceed the visible range of the viewBox after translate?
- [ ] Is rotate's transform-origin set at the correct joint position?
- [ ] Do the effect particles appear in the correct time window and the correct position?
- [ ] Is the shadow synchronized with the body motion? (When jumping up, the shadow should shrink)
- [ ] **XML validity**: validate the SVG with `xmllint --noout`; XML-illegal characters like `&` must not appear in CSS comments
- [ ] **CSS structural integrity**: are all `@keyframes` correctly closed, with no duplicate definitions and no nesting? After editing, confirm there are no leftover extra braces
- [ ] **CSS animation vs SVG attribute conflict**: the same `<g>` cannot have both a CSS `animation` (which sets `transform`) and an SVG `transform` attribute, otherwise the CSS overrides the SVG attribute. They must be split across `<g>` at different levels (outer holds the static SVG transform, inner holds the CSS animation)
- [ ] **Frame-sampling check**: check at least 0%, the main-action peak, and the recovery frame, confirming that hands and feet are not detached, props have not flown off, and blinking does not flicker repeatedly. **Do not judge attachment from the 0% frame alone** — at 0% most transforms are at their identity (offset 0), so seam gaps are invisible there; you must look at the translate/rotate extremes.

---

## Step 6: Correction Strategy

### No Vague Corrections

Bad example: `"move the arm a bit"` → cannot be executed

### Must Give Structured Corrections

Good example:
```
Problem: left arm overlaps the right eye
Reason: after left arm translate(5px, -2px), x range is 5-7; right eye is at x=10, no overlap;
        but y range 7-9 intersects the eye y=8-10
Fix: change the y component of the left arm translate from -2px to +1px, making the arm y range 10-12,
     avoiding the eye y=8-10 while still keeping the in-front action semantics
```
