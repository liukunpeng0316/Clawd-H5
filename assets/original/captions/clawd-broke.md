# clawd-broke.svg

A broke animation of Clawd with an empty money bag, shaking out his last coin. 5s loop, going from shaking the bag to the coin dropping to sad eyes + a teardrop.

## Body
Standard torso with breathing (3.2s). At 65-85% the torso sags with scaleY(0.95) translateY(0.5px) to convey dejection. The eyes come in two sets: normal eyes and sad arched eyes (⌢⌢), switched via opacity; during 42-55% the eyes look right with translateX(1.5px), watching the bag-shaking motion. The right arm swings way back with rotate(-70°) to shake out the bag.

## Props
- **Money bag**: A gold (#DEAF42) inverted trapezoid hanging from the end of the right arm, shaking violently at 37-42% with rotate(±32° → 10°)
- **Falling coin**: A gold (#FFD700) circle that drops out of the bottom of the bag at 42%, falling along an arc to the ground
- **Teardrop**: A tear hanging below the sad eyes at opacity 0.8, appearing during 68-85%

## Animation
- **breathe (3.2s)**: Standard breathing
- **sag (5s)**: 65-85% torso sags
- **normal-eyes-vis / sad-eyes-vis (5s)**: The two eye sets switch via mutually exclusive opacity
- **eyes-look (5s)**: 42-55% glance right with translateX(1.5px)
- **arm-right-anim (5s)**: Right arm swings back with rotate(-70°)
- **bag-vis / bag-shake (5s)**: The money bag appears and shakes violently with rotate(±32°)
- **coin-fall (5s)**: From 42%, the coin drops out of the bag's mouth to the ground
- **tear-hang (5s)**: 68-85% the teardrop hangs at opacity 0.8
- **shadow-breathe (3.2s)**: Shadow breathes in sync

## Expression
Clawd realizes he's penniless, reaches back and shakes his money bag, his one remaining gold coin clinks as it falls out, he switches to sad eyes with a teardrop hanging, and his body slumps dejectedly.
