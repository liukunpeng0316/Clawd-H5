# clawd-coding.svg

An animation of Clawd focused on coding, on a 3-second loop, with both arms rapidly alternating taps on the keyboard, eyes scanning the lines of code left and right, and a floating code panel appearing line by line.

## Body
Standard torso with breathing (3.2s) and a lean-bob (0.4s) micro-bounce. The eyes are shifted down to y=10 (originally y=8), with scaleY(0.7) for a slightly squinted, focused look. Both arms tap rapidly and alternately with tap-l/tap-r at 0.25s, with phases offset by 180°.

## Props
- **Floating code panel**: a dark (#263238) 15x8 rectangle, positioned above the torso
- **Title bar**: dark gray (#37474F), containing red/yellow/green dots (window controls)
- **Code lines**: 3 colored lines (green/blue/purple/orange) that appear line by line via step, with 0/1/2s delays
- **Keyboard**: a dark gray (#424242) rectangle below the torso + light gray (#616161) key blocks

## Animation
- **breathe (3.2s)**: standard breathing
- **lean-bob (0.4s)**: torso translateY micro-bounce synced with the taps
- **tap-l / tap-r (0.25s)**: arms tapping alternately, 180° phase difference
- **eyes-scan (1.8s step-end)**: eyes scanning across 6 horizontal positions
- **blink (3s)**: a single blink at 48% with scaleY(0.1)
- **code-type (3s step-end)**: three lines of code appearing in a staggered step from 6%-85%, delay 0/1/2s

## Expression
Clawd codes intently, squinting and scanning the screen left and right, hands tapping the keyboard at high speed in alternation, while code is typed out line by line on the floating code panel.
