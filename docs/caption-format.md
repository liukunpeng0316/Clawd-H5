# Caption Format

Captions are the structured knowledge base used by the Claude Code skill. Each
caption file under any collection's `assets/<collection>/captions/`, except
`clawd-body-structure.md`, should match a same-named SVG in the sibling
`assets/<collection>/svg/` directory.

## Template

```markdown
# clawd-action-name.svg

One sentence describing the action, mood, and loop length.

## Body
Describe the body pose, eyes, arms, legs, and any structural deviations from
the base body.

## Props
- List each prop or visual effect.
- Include color, position, size, and attachment point when useful.
- Write `None.` when there are no props.

## Animation
- **animation-name (duration, easing)**: describe key phases and synchronization.
- Mention body/arm/eye/prop timing relationships.

## Expression
Describe the animation as a single action. Avoid full scene narratives.
```

## Language

English is the canonical language. Each caption pairs with its SVG as
`clawd-<name>.md`. A Chinese version may be kept alongside it as
`clawd-<name>.zh.md`. English identifiers are fine for SVG class names,
animation names, and exact tooling terms.

## Content Rules

- Do not describe dialogue bubbles, explanation boxes, or text labels.
- Do not add a mouth to Clawd's core body.
- Keep the action centered on one Clawd and one readable motion.
- Mention how limbs remain connected when body movement is large.
- Mention blink timing when eyes change state.
- Describe props as attached to hands, body, or a stable world position.

## Promotion

Use:

```bash
python tools/promote_svg.py --promote clawd-action-name
```

Then replace all `{TODO: ...}` placeholders before committing the caption.
