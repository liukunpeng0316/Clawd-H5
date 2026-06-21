# clawd-disgusted-retreat.svg

An animation of Clawd retreating in disgust, on a 4.5-second loop, with the body leaning back, wavy stink lines floating, and purple stink rings rising.

## Body
Standard torso. retreat-move 4.5s linear shifts the whole body translateX (+2 → -3 → +2px), retreating and then returning. From 20-72% the body does rotate(-4°) + scaleY(0.96) for a disgusted lean-back. The eyes do scaleY(0.6) translateX(1.5px) for a frowning, sidelong glance. The legs (outer/inner) do an alternating gait, 4.5s linear, stepping backward. The arms swing along with rotate(±10°).

## Props
- **Wavy stink lines**: 3 brown (#8D6E63) curves that begin appearing at 20%, each doing an out-of-sync wiggle at 0.3/0.35/0.4s
- **Purple stink rings**: 3 purple rings (#7B1FA2/#9C27B0/#AB47BC) that emanate from the body, translating upward as they rise, fading out with staggered delays

## Animation
- **retreat-move (4.5s linear)**: the whole body translateX retreats and returns
- **body-lean (4.5s)**: 20-72% rotate(-4°) + scaleY(0.96) lean-back
- **eyes-frown (4.5s)**: scaleY(0.6) + translateX(1.5px) frowning sidelong gaze
- **legs-outer / legs-kick-inner (4.5s linear)**: the two leg pairs step backward alternately
- **arm-left / arm-right (4.5s)**: arms swing rotate(0→±10°)
- **wave-show (4.5s)**: the stink wave lines pulse in opacity
- **wiggle1/2/3 (0.3-0.4s alternate)**: the three wave lines each wiggle out of sync
- **circle-rise-1/2/3 (4.5s ease-out)**: the purple stink rings rise + fade out with staggered delays
- **shadow-move (4.5s linear)**: the shadow follows the retreat

## Expression
Clawd smells something foul, frowns and glances sideways while backing away, body leaning back, legs stepping backward one at a time, with wavy stink lines wiggling nearby and purple stink rings slowly rising and drifting away.
