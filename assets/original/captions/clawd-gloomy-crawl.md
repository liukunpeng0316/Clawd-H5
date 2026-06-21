# clawd-gloomy-crawl.svg

An animation of Clawd crawling slowly and gloomily, with a 0.5-second gait cycle.

## Body
The torso is widened and flattened (1,7) to 13x6, making it shorter and chubbier than the standard build. The eyes are flat dead-fish eyes (2x1), completely still and expressionless. Both arms (-1,10)/(14,10) rest motionless at the sides of the widened torso. The four legs step in alternation: the outer pair (2,12)/(12,12) and the inner pair (4,12)/(10,12) move out of phase.

## Props
- **Dark-purple aura particles**: 8 deep-purple (#4A148C) 1-1.5px squares scattered around the character, floating upward 10px over a 2.5-second cycle while scaling up 1.3x and fading out, with staggered delays (0-2s).

## Animation
- **Crawl movement (crawl-move, 0.5s)**: translateX ±0.7px swaying side to side.
- **Outer-leg step (step-outer, 0.5s)**: translateY 0→-1.2px lift.
- **Inner-leg step (step-inner, 0.5s)**: out of phase with the outer legs, translateY -1.2→0px.
- **Aura rise (aura-rise, 2.5s)**: opacity 0→0.8→0, translateY 0→-10px, scale 0.6→1.3.
- **Shadow follow (shadow-move, 0.5s)**: translateX ±0.7px in sync.

## Expression
Clawd crawls slowly and gloomily in a flattened posture, dead-fish eyes expressionless, as dark-purple aura particles keep rising and drifting around it.
