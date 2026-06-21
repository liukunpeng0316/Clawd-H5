# clawd-coffee.svg

An animation of Clawd taking a coffee cup down from overhead and sipping it, on a 5-second loop.

## Body
Standard upright pose. The left arm rests still at the side. The right arm performs a grab-drink-return action sequence. The eyes switch between two sets: normal eyes (while waiting) and happy ^^ eyes (while sipping), transitioning via a scaleY blink.

## Props
- **Coffee cup (overhead)**: white cup body (#FFFFFF, 3x2.5) + gray handle (#CCCCCC) + brown coffee surface (#5D4037, 2.4x0.8), located at (5,3.5)
- **Coffee cup (in hand)**: same style, located at (10.5,8.5), alternating with the overhead cup via opacity
- **Steam**: 3 gray (#AAAAAA/#BBBBBB) rounded rectangles, floating up 5px over a 2-second period while enlarging and fading out, visible only while the cup is overhead

## Animation
- **Body sway (sway, 5s)**: scaleX 1-1.02, scaleY 1-0.98
- **Right arm grab (arm-grab, 5s)**: 0-18% at the side → 28% reaching overhead (-6,-5) → 38-58% holding the cup in front (-3.5,2) → 68% returning it overhead → 78% back to position
- **Cup switch**: 24-26% overhead cup disappears / in-hand cup appears, 66-68% switch in reverse
- **Eye switch**: 30-32% normal eyes close → 34-36% happy eyes open → 56-58% happy eyes close → 60-62% normal eyes open

## Expression
Clawd has a steaming coffee cup resting overhead. The right hand reaches overhead to take the cup down and sip, showing a satisfied ^^ expression, then puts the cup back overhead.
