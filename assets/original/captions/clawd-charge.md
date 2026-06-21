# clawd-charge.svg

A "Charge!" animation of Clawd wearing a red headband and flying upward within the frame, looping every 2 seconds.

## Body
Standard torso and four legs. The left arm is raised high in a Superman pose (rotate -85°, translate -1,-2), the right arm trails backward (rotate 25°, translate -1,1) with an arm shadow. The eyes pulse with scaleY 0.8-1 (a determined flicker). The whole character is masked with a clipPath, but the character itself stays visible for the entire cycle.

## Props
- **Red headband**: A dark-red (#B71C1C) horizontal bar at (1,6.5) sized 13x1, covering the forehead.
- **Headband streamers**: Two strands (#B71C1C/#8B0000) flowing out from the right side, with a 0.3s flutter wobble (15°-25°/20°-35°).
- **Speed lines**: 6 gold (#FFD700/#FFA000/#FFC107) thin tall rectangles, with a 0.4s downward streak animation.
- **Spark trail**: 3 gold (#FFD700/#FFC107/#FFF59D) small squares that float up from below the character, shrinking as they fade out.

## Animation
- **Flying (fly, 2s)**: translate(0,7px) → linear surge upward with ±0.4px lateral sway → reaches (-12px) → falls back to translate(0,7px); the character stays visible the whole cycle.
- **Headband flutter (flutter1/flutter2, 0.3s)**: rotate 15°-25° / 20°-35°, offset by a 0.1s delay.
- **Eye flicker (eyes-shine, 0.8s)**: scaleY 1→0.8→1.
- **Speed lines (streak, 0.4s)**: translateY 0→8px, opacity 0.9→0.
- **Spark trail (trail-spark, 0.6s)**: floats up from invisible → opacity 0.9 → translateY 5px, shrinking and fading out.

## Expression
Clawd, with a fluttering red headband, flies upward within the frame in a Superman pose as gold speed lines whoosh past, leaving a trail of glittering sparks behind.
