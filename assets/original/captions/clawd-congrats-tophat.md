# clawd-congrats-tophat.svg

An animation of Clawd wearing a party hat and celebrating with a confetti party popper held in both hands. 4s loop, with confetti bursting and scattering from the popper's mouth.

## Body
Standard torso. At 38% scaleY compresses to wind up, at 42% it springs up translateY(-1.5px), and at 50% it returns to position. The eyes switch between two sets: 0-33% normal eyes, 40-79% switching to happy laughing eyes (^^). Both arms hold the popper in front of the body (left translate(-5,1), right translate(5,1)).

## Props
- **Party hat**: A cone scale(0.7) + rotate(-10°), with overlaid red/blue/yellow horizontal stripes + a white pom-pom, worn on top of the head, bouncing once along with the body at 42%
- **Party popper**: Red barrel (#FF5252) + blue mouth (#4FC3F7) + gold band (#FFD54F), located on the right at (14, 6.5), pushed to the front of the body to fire during 38-50% with translate(-5px, 1.5px)
- **Confetti pieces**: 6 small squares (pink/blue/yellow/green/purple/orange) flying out in a fan from the popper's mouth (9, 6.5), spinning with rotate, fading to zero opacity at 85%

## Animation
- **body-bob (4s)**: 38% compress, 42% spring up, 50% return
- **hat-bounce (4s)**: 42% translateY(-1px), the hat bounces with a slight lag
- **eyes-normal-vis / eyes-happy-vis (4s)**: The two eye sets switch via opacity
- **arm-l-hold / arm-r-hold (4s)**: 18-80% both arms hold the popper in front of the body
- **popper-move (4s)**: 38-50% the popper moves to the front of the body and rotates into firing pose
- **conf-fly-1 ~ conf-fly-6 (4s)**: The 6 confetti pieces each translate + rotate, flying out in a fan, fading out at 85%
- **shadow-bob (4s)**: Shadow bounces in sync with the body

## Expression
Clawd, wearing a party hat, lifts the popper in both hands and pushes it forward, pops it off with a bang, confetti scatters everywhere, he hops up once, and his eyes squint into happy laughing eyes.
