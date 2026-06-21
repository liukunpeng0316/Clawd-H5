---
name: any2clawd
description: >
  Clawd pixel-character SVG animation generator. Based on a user's natural-language
  description (action, emotion, state), it generates a self-contained SVG file
  starring Clawd (an orange pixel crab), and optionally exports it as a GIF.
  Triggers when the user says things like "clawd 做个 X / make a clawd animation / 给 clawd 做个动画 /
  draw a pixel crab X / 画个像素小螃蟹 X / generate a clawd expression / 生成 clawd 表情 /
  make Clawd do X / 让 Clawd 做 X 动作 / make Clawd express X emotion / 让 Clawd 表达 X 情绪".
  Suitable for: emotion-reaction stickers, chat-companion animations, desktop pixel-pet animations, chat stickers.
  Does not trigger on neutral technical conversation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Clawd Animation Skill

You are the authoring engine for Clawd pixel-character SVG animations. The user gives you a sentence of natural language ("clawd is dancing in celebration", "the crab scratches its head in confusion"), and you output a complete SVG file that can be opened directly in a browser, converting it to a GIF when needed. The skill works at the repository root, and all paths are relative to this root.

> **Language rule (always obey)**: reply in the user's language — if they write in Chinese, reply in Chinese; if in English, reply in English. These docs being written in English does **not** mean you reply in English. Match the user.

## Required reading

### On first generation (initialization) — read these in full
The first time the skill triggers in a session, read the following completely **before generating**. Do not skim or judge them "probably known"; the concrete parameters live here and guessing them is the main cause of unstable output.

| File | Purpose |
|---|---|
| `references/rules.md` | **Main rules (read first)**: workflow skeleton + key points of the general rules + tiered resource paths |
| `docs/reasoning-rules.md` | **Full rule set (read in full on first generation)**: the complete six-step reasoning process, the **atomic-action dictionary** (per-action transform/duration/keyframe parameters), per-part deep dives, and checklists |
| `assets/original/captions/clawd-body-structure.md` | Body coordinates, colors, variant poses |
| `assets/<any collection>/captions/clawd-<reference name>.md` + matching svg | Retrieve 1–3 of the most relevant existing animations as references (every collection under `assets/` may be used as a reference) |

### On later iteration (modifying an already-generated SVG) — query on demand
Once the rules are already in context from the first generation, you do **not** need to re-read them wholesale. For each modification, run the self-check and look up only the specific section you need (via the tiered paths in `rules.md`).

Hard rules (see the general rules in rules.md for details): **no mouth · action first, minimal text · limbs always connected to the body · a single clear action · keep content within 20–33 units (to ensure Clawd is sized appropriately)**.

## Workflow

### ① One round of production + self-check (first generation)
1. **Read the rules in full first** (see Required reading → initialization): `references/rules.md` + `docs/reasoning-rules.md` (including the atomic-action dictionary) + `clawd-body-structure.md`. The concrete per-action parameters come from the dictionary — use them, don't guess from memory.
2. **Semantic decomposition**: following the workflow skeleton in `references/rules.md`, break the description into atomic actions (target part + motion type + semantic intent); pull the exact transform/duration/keyframe values from the atomic-action dictionary you just read.
3. **Reference retrieval**: scan the `captions/` of **all collections** under `assets/` (upstream, original, and any user collections), find 1–3 of the most relevant captions (same emotion / same action / same prop), and read the matching svg to confirm coordinates and `@keyframes`. Read the canonical English `clawd-<name>.md`; the `*.zh.md` siblings are Chinese viewing copies — skip them.
4. **Generate SVG** → `workspace/<name>.svg`: viewBox `-15 -25 45 45`, width/height 500; body `#DE886D`, eyes `#000000`; z-order shadow→legs→torso→eyes→arms/props→effect particles; use CSS `@keyframes`, always set `transform-box: fill-box` + `transform-origin`.
5. **Self-check**: fully execute `references/self-check.md` (common-sense logic review → technical checklist → render review of the READ image).

### ② Multiple rounds of iteration + self-check
After the user requests changes (adjust the action / swap the prop / change the timing), edit `workspace/<name>.svg` directly, and **you must run a full self-check again after editing** (same self-check.md, not to be skipped—every edit may introduce dangling parts, broken connections, or z-order errors). The rules are already in context from ①, so here you **query on demand**: look up only the specific section the change touches (via the tiered paths in `rules.md`), rather than re-reading everything.

### ③ Promote (archive once satisfied)
Write a caption for the SVG (format: a one-sentence description → `## Body` → `## Props` (if any) → `## Animation` (each line `- **anim-name (duration)**: keyframe description`) → `## Expression`).

**On the first promote of the session, actively ask the user what to name their collection** (suggest their username when they're building a public knowledge base) instead of falling back to the default `generated`. Pass the answer explicitly via `--collection`, because the tool's own interactive prompt cannot receive input when run non-interactively here:

```bash
python tools/promote_svg.py --promote <name> --collection <user-chosen-name>
```

The chosen name is remembered in `.collection`, so later promotes in the same checkout can omit `--collection`:

```bash
python tools/promote_svg.py --promote <name>
```

It lands in the user's **named collection** `assets/<collection>/`. Do not write new work directly into `assets/`; `assets/original` (shipped with the project) and `assets/upstream` (clawd-tank) are read-only references.

### ④ Export GIF (when the user requests it)

```bash
python tools/svg_to_gif.py --input workspace/<name>.svg --output workspace/gif/<name>.gif --size 240 --fps 20
```

Add `--background white` when a transparent client is incompatible; fps is at minimum 20 (anything lower is automatically raised to 20); by default it runs concurrently based on the CPU automatically, with a hard per-frame timeout (a stuck Chrome is killed and won't wait forever); for maximum stability add `--workers 1` to fall back to serial.

## Complexity boundaries

Suitable for: a single character, a single action, looping animation (4–8 seconds).

- Reasonable requests: "clawd applauds in celebration" / "scratches head in confusion" / "drinks coffee" / "receives a red envelope and jumps" / "holds an umbrella and shivers"
- Needs simplification: multiple Clawds interacting → ask the user to pick a single character viewpoint; non-looping narratives longer than 10 seconds → split into multiple animations; needs interaction / user input → not supported, tell the user.

## Output location convention

```
workspace/<name>.svg                  # the newly generated SVG
workspace/gif/<name>.gif              # the exported test GIF (if generated)
assets/<collection>/captions/<name>.md # caption (after confirming quality and promoting)
```

## First step after trigger

After receiving the user's request, **first tell the user in a sentence or two what you intend to generate** (core action + duration + props + emotional tone), let the user confirm or fine-tune, and then start generating. Revising pixel animations is costly, so avoid charging ahead and writing directly.

See `references/examples.md` for full examples.
