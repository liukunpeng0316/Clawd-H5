# clawd-typing.svg

An animation of Clawd focused on typing, on a 3-second loop, with both arms alternating taps on the keyboard, eyes scanning the document, and text appearing line by line.

## Body
Standard torso with breathing (3.2s). lean-bob 0.4s micro-bounce translateY(±0.3px). The eyes do eyes-focus 1.8s step-end scaleY(0.7) for a half-squinted focus, with translateX scanning across 6 horizontal positions, and a single scaleY(0.1) blink at 48% within the 3s cycle. Both arms do high-frequency anti-phase taps with tap-l/tap-r at 0.25s.

## Props
- **Floating work page**: light gray background (#FAFAFA) + gray border (#B0BEC5), size 13×7, at y=-1
- **Dynamic content lines**: 3 gray-text lines (#B0BEC5), appearing via step at 6%-85%, staggered with delay 0/1/2s
- **Static background lines**: 2 even lighter (#CFD8DC) blurred text lines, opacity 0.3-0.4, serving only as background depth
- **Keyboard**: a dark gray (#424242) rectangle below the torso + light gray (#616161) double rows of keys

## Animation
- **breathe (3.2s)**: standard breathing
- **lean-bob (0.4s)**: micro-bounce translateY synced with the taps
- **tap-l / tap-r (0.25s)**: arms tapping rapidly in anti-phase
- **eyes-focus (1.8s step-end)**: eyes flatten and scan across 6 positions
- **eyes-blink (3s)**: a single blink at 48%
- **code-line1/2/3 (3s step-end)**: three content lines appear in a staggered step with delay 0/1/2s respectively
- **shadow-breathe (3.2s)**: shadow breathing

## Expression
Clawd types with full concentration, eyes squinted and scanning the screen left and right, hands tapping the keyboard at high speed in alternation, while text is typed out line by line on the floating document page.
