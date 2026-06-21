# clawd-pleading.svg

An animation of Clawd pleading with big watery eyes and hands clasped together, on a 5-second loop, with the eyes enlarging, welling with tears, and stars twinkling around.

## Body
Standard torso with breathing (3.2s). From 15-78%, body-plead does scaleX(1.03) scaleY(0.97) for a slight shrink. The eyes switch between two sets: normal eyes and "pleading big eyes" — scaleY(1.15) scaleX(1.1), enlarged and round. The arms clasp together in front of the body with translate(±5px). Below the eyes are two small rectangles, tears-group, serving as tear pools (appearing at opacity 18-75%).

## Props
- **Twinkling stars**: 5 four-pointed stars (#FFD700/#FFC107/#FFF59D), scattered at (-2,5)/(16,4)/(-4,11)/(18,10)/(7.5,1), formed by crossed rectangles in an X shape
- **Eye highlights**: 0.5×0.5 small white squares, pulsing and twinkling at 0-100% opacity

## Animation
- **breathe (3.2s)**: standard breathing
- **body-plead (5s)**: 15-78% body slightly shrinks
- **eyes-normal-vis (5s)**: normal eyes visible (opacity) during the non-pleading phase
- **eyes-plead-scale / eyes-plead-vis (5s)**: during the pleading phase the big eyes enlarge and become visible
- **eye-shine (1.5s ease-in-out)**: eye highlights twinkle opacity 0.9 ↔ 0.4
- **tears-vis (5s)**: tear pools appear at opacity 18-75%
- **stars-vis (5s)**: the star group appears at opacity 18-75%
- **star-twinkle (1.2s ease-in-out)**: each star scales 1 → 1.5, twinkling with staggered delays
- **arm-l-plead / arm-r-plead (5s)**: arms clasp together in front of the body
- **shadow-plead (5s)**: the shadow shrinks in sync

## Expression
Clawd's eyes enlarge into big round watery eyes with white highlights twinkling inside, tear pools hanging beneath the eyes, hands clasped pitifully together in front, while a ring of four-pointed stars twinkles gently nearby.
