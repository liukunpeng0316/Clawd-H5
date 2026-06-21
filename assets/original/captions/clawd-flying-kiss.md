# clawd-flying-kiss.svg

Clawd raises its right hand to its mouth then sends out a flying kiss, eyes squinted in a smile and a pixel heart flies off to the upper right, 3s loop.

## Body
Standard torso 11x7 at (2,6), with `kiss-body` tilting slightly side to side in the direction of the kiss and `breathe` breathing. The four legs (x=3,5,9,11) do a small `legs-bounce` hop. The eyes have two forms switched via opacity: at rest, normal 1x2 black eyes at (4,8)/(10,8); when blowing the kiss, they switch to smiling eyes ^^ (polyline stroke, stroke 0.7). The left arm (0,9) sways gently, and the right arm (13,9) performs the kiss-blowing motion with a 0.2-opacity shadow.

## Props
- **Pixel heart**: a red (#E84057) compact pixel heart shape (about 5x3, twin bumps on top + full row + narrowing + sharp point), which follows `heart-float` to fly off from the right-hand position toward the upper right, scaling up then fading out.

## Animation
- **kiss-body (3s loop)**: 35% slight left tilt (hand approaching face) → 50% right tilt and lift to send (the moment of blowing the kiss) → recover.
- **arm-kiss (3s)**: the right arm at 30% rises to the face translate(-4px,1px) (staying below the eyes) → 50% extends out and up translate(2px,-2px) to send the kiss → falls back.
- **arm-l-sway (3s)**: the left arm sinks and sways gently.
- **eyes-norm / eyes-hap (3s)**: shows normal eyes at rest, switching to smiling eyes ^^ at 25–75% (complementary opacity switch).
- **heart-float (3s)**: the heart appears at the hand position at 52% → drifts to the upper right and scales up → fades out at 85%.
- **legs-bob (3s)**: the legs hop slightly when the kiss is blown.
- **shadow-pulse (3s)**: the ground shadow scales slightly.

## Expression
Clawd raises its right hand to its mouth, eyes curving into a smile, then flicks it outward to send a flying kiss as a red heart flies from its hand toward the upper right and fades out — a sweet, playful flying-kiss loop.
