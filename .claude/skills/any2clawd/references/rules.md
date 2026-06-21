# Clawd Animation Main Rules (skeleton + key points + tiered reference paths)

**On the first generation in a session, read this file and `docs/reasoning-rules.md` in full** (the atomic-action dictionary is where the concrete parameters live — guessing them is the main cause of unstable output). On **later iterations**, the rules are already in context: run the self-check and use the tiered paths below to look up only the specific section the change touches — you don't need to re-read everything.

## Process Skeleton (six steps, every time)

1. **Semantic breakdown**: decompose the natural language into atomic actions (target part + motion type translate/rotate/scale/opacity + semantic intent).
2. **Reference lookup**: from the captions of all collections under `assets/`, find 1–3 most relevant animations, read their SVG to confirm coordinates and `@keyframes`. Use the canonical English `clawd-<name>.md`; the `*.zh.md` siblings are Chinese viewing copies — ignore them here.
3. **Spatial reasoning**: choose a transform for each part — use rotate for swinging around a joint, translate for moving across regions, scale for deformation, opacity for show/hide. When looking in a direction, the eyes move more than the body (parallax).
4. **Timing arrangement**: the main action sets the frequency; subordinate parts (body bob, shadow) follow that frequency; breathing at 3.2s can be independent; effects trigger within keyframe windows.
5. **Layering and constraint check**: draw in render z-order (shadow → legs → torso → eyes → arms/props → effects); verify collisions when translate crosses regions; look up the specialized technique when a specialized feature appears.
6. **Generate → self-check → fix**: write `workspace/<name>.svg`, run the full self-check, and for any problem found give a structured fix (part + value, not a vague description).

## General Rules and Key Points (hard rules, always obey)

- **No mouth**: convey emotion through eye shapes + body dynamics + effects; never add a mouth to the character itself.
- **Action first, text is a soft rule**: if an action/eyes/effects can express it, don't write a text bubble; when you genuinely need to make the point (memes like "PYTHON" / "JAVA"), you may add **2–4 characters of floating text** (not a dialog box). This is a soft rule — by default write nothing, and only add text when making the point really requires it.
- **A single clear action**, no complex narrative/background scene.
- **Limbs always attached**: arms and legs stay visually connected to the body across the whole cycle. Legs may have their own animation (steps, kicks) — what matters is that they read as connected to the body in **every sampled keyframe**, not that they share the body's animation group. Verify by sampling the motion extremes (not just the 0% frame, where offsets are 0 and any gap is hidden): if a leg visibly detaches at the motion peak, fix it. Arms are more forgiving — they naturally swing independently, so a small shoulder offset is fine; only avoid a clearly detached, floating arm.
- **Single blink timeline**, no stacking multiple blink durations.
- **Body single color `#DE886D`**, no gradient, no shadow.
- **Structural constraints**: character center x=7.5; torso scale X 0.9–1.18 / Y 0.7–1.1; arm translate ≤ ±6px; when an arm is in front, y≥10 (does not cover the eyes).
- **Size range**: all visible content across frames (including the farthest-flying particle/prop) falls within roughly a **20–33 viewBox-unit** square — the upper bound references `clawd-surrender-helpless` (largest, torso fills about 55% of the frame), the lower bound references `clawd-kick-football` (smallest, torso about 34%), with the farthest element ≤ about 16 units from the center (7.5,10).
- **Canvas**: viewBox `-15 -25 45 45`, width/height 500; any animation containing scale must set `transform-box: fill-box` + `transform-origin`.

## Tiered Reference Paths (look up when needed)

| Need | Look up |
|---|---|
| A given action's specific transform parameters/duration | `docs/reasoning-rules.md` "Atomic Action Dictionary" |
| Transform decision tree, parallax, timing duration table, sync rules | `docs/reasoning-rules.md` Step 3 / Step 4 |
| Render z-order, part collision math | `docs/reasoning-rules.md` Step 5 |
| Part specializations (arm shadow / held-object perspective / prop mounting / clothing jersey) | `docs/reasoning-rules.md` Step 5 corresponding subsection |
| Full technical checklist | `docs/reasoning-rules.md` "Common Mistakes Checklist" |
| Body coordinates / colors / eye-shape variants | `assets/original/captions/clawd-body-structure.md` |
| Full self-check process (common-sense review + render review) | `references/self-check.md` |
| Worked examples | `references/examples.md` |
