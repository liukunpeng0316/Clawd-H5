# clawd-lion-dance.svg

Clawd cheerfully hopping while holding up a lion-dance head, 0.6s bounce loop, with an opening mouth, stepping feet, and gold confetti.

## Body
Standard torso 11x7 at (2,6), #DE886D. Four legs each 1x3 at (3,12)/(5,12)/(9,12)/(11,12), slightly longer than standard, with the two outer legs and two inner legs stepping alternately. Both arms each 2x2 at y=7 (left arm (0,7), right arm (13,7)), raised in a head-holding pose. Eyes in a happy ^^ shape, drawn with polyline (stroke #000000, 0.8px). Ground shadow 13x1 at (1,15), wider than standard (total width of character + lion-head drape).

## Props
- **Lion-dance head**: positioned above Clawd's head, made of several components:
  - **Main body**: 17x7 red block (#E53935, rx=0.5) at (-1,-8)
  - **Gold crown**: 17x1.5 (#FFC107, rx=0.3) at (-1,-9), with three protrusions (left 2x1.5 at (1,-10), center 3x2 at (6,-10.5), right 2x1.5 at (12,-10))
  - **Gold sides**: 1x7 each on left and right (#FFC107) at (-1,-8) and (15,-8)
  - **Lion eyes**: 4x3 white base each on left and right (#FFFFFF, rx=0.5) at (1,-6) and (10,-6), with 2x2 black pupils each (#000000, rx=0.3) at (2.5,-5.5) and (11.5,-5.5), with pupil-bob bobbing up and down
  - **Nostrils**: 1x1 each on left and right (#B71C1C) at (6,-4) and (8,-4)
  - **Upper jaw**: 15x1 (#FFD54F) at (0,-2), fixed in place
  - **Lower jaw**: 15x1.5 (#FFD54F) at (0,-1), with a mouth-chomp open/close animation; the lower jaw has 4 white teeth (each 1.5x0.8 #FFFFFF) at x=2/5/8.5/11.5
- **Green drape**: 3x11 each on left and right (#43A047) hanging down from the lion head along both sides of the character (left (-1,0), right (13,0)), each with a 3x1 gold border at the top and a gold triangular zigzag trim at the bottom
- **Gold confetti**: 6 1x1 pixel particles, colored #FFD700/#FFC107/#FF6F00/#FFA000, scattered high around the character (y=-8 to y=-14), each with CSS custom properties --dx/--dy controlling its drift direction, with animation-delay staggered from 0s to 1.0s at 0.2s intervals

## Animation
- **lion-bounce (0.6s loop, ease-in-out)**: transform-origin: 7.5px 15px. 0%/100% landing squash (scaleY(0.92)) → 15% launch stretch (scaleY(1.05)) → 40% peak (translateY(-8px) scaleY(1.02)) → 45% hang (scaleY(1)) → 70% falling stretch (scaleY(1.05)) → 85% landing squash (scaleY(0.92)).
- **step-outer (0.3s loop, ease-in-out)**: outer legs (left 1/right 4) raise alternately translateY(-1.5px), half-period loop.
- **step-inner (0.3s loop, ease-in-out)**: inner legs (left 2/right 3) out of phase with the outer legs, forming a quick alternating step.
- **mouth-chomp (0.6s loop, ease-in-out)**: transform-origin: 7.5px -1px. The lower jaw moves down at 40-50% translateY(1.5px) to open the mouth (corresponding to the peak of the jump), closed the rest of the time.
- **pupil-bob (0.6s loop, ease-in-out)**: pupils move up at 40-50% translateY(-0.5px), in sync with the bounce.
- **shadow-lion (0.6s loop, ease-in-out)**: 0%/85%/100% normal (scale(1) opacity 0.5) → 40-45% peak minimal (scale(0.5) opacity 0.2).
- **confetti-burst (1.2s loop, ease-out)**: the 6 confetti pieces each start from their initial position, fully appear at 10% with opacity 1, then drift along their --dx/--dy direction and shrink to scale(0.3) and vanish. Each triggers in turn at 0.2s intervals, forming a continuous shower effect.

## Expression
Clawd cheerfully hops while holding a red lion-dance head high in both hands, the green drape swaying with its body, the lion's mouth opening at the peak, gold confetti flying everywhere, brimming with a festive holiday atmosphere.
