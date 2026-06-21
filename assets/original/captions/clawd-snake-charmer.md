# clawd-snake-charmer.svg

Scene animation of Clawd becoming a snake charmer playing a flute, 3s loop, with a snake poking out of the basket swaying to the music and colorful wavy "PYTHON..." text above.

## Body
Standard torso 11x7 at (2,6). The eyes (1x2 each) at (4,8) and (10,8), fill=#000000, using a fill-box transform-origin centered, with a serene blinking animation. Both arms (2x2 each) gather forward to hold the flute — the left arm translate(5,1) moves to the (5,10) position, the right arm translate(-5,1) moves to the (8,10) position, both with a 0.2-opacity black shadow. The four legs (1x3 each) stay still at x=3,5,9,11, y from 12 to 15.

## Props
- Flute pipe (pungi body): fill=#8D6E63 (1x5) at (6.5,7) after translate(6.5,0)
- Flute mouth: fill=#6D4C41 (0.8x0.5) rx=0.2, at the top of the pipe (6.6,5.5)
- Resonator gourd outer ring: fill=#A1887F circle r=1.2, center (7,6.5)
- Resonator gourd inner ring: fill=#8D6E63 circle r=0.8, center (7,6.5)
- Snake head: fill=#388E3C (3x2) rx=0.3, at (19.5,5)
- Snake eyes: fill=#FFEB3B (0.6x0.6) rx=0.3 two of them, each with a fill=#000000 (0.3x0.4) black pupil inside
- Snake body: fill=#4CAF50 pixel-block segments, light-colored belly fill=#81C784
- Snake tongue: stroke=#F44336 forked red line of width 0.3
- Basket rim: fill=#6D4C41 (6.6x0.5) rx=0.3, at (17.7,12.8) after translate(18,12)
- Basket body: fill=#8D6E63 (6x2) rx=0.5, at (18,13)
- Basket stripes: fill=#A1887F (5.4x0.4) two decorative horizontal stripes
- Musical notes: three text notes (♫♩♪), fill respectively #FFD700, #40C4FF, #B388FF, font-size 3.5-4
- "PYTHON..." text: monospace font font-size=2.4, each letter colored in turn #40C4FF/#66BB6A/#FFD54F/#FF8A65/#B388FF/#40C4FF, the ellipsis #FFFFFF

## Animation
- **sway (3s loop)**: centered on (7.5px,11px), at 25% rotate(-1deg)+translate(-0.3px,0.2px), at 75% rotate(1deg)+translate(0.3px,0.2px), the performer swaying gently to the music
- **breathe (1.8s loop)**: centered on (7.5px,11px), scale(1.02,0.98) breathing, a faster cycle than the standard 3.2s
- **fluteBob (3s loop)**: the whole flute group floats up slightly at 50% via translateY(-0.3px)
- **shadowPulse (3s loop)**: centered on (7.5px,15.5px), at 50% scaleX(1.06)+opacity(0.38) pulsing
- **sereneBlink (3.2s loop)**: double blink — 18%-22% quick close scaleY(0.2), 58%-62% half close scaleY(0.35), conveying a serene expression
- **floatNote (2.2s loop)**: notes start from translate(2px,7px)+scale(0.6), appear at 20% opacity(0.9), float up to translate(2px,-6px)+scale(0.9) then disappear, the three notes staggered with animation-delay 0s, 0.7s, 1.4s
- **snakeSway (3s loop)**: centered on (21px,15px), the whole snake body sways gently ±0.8deg
- **snakeHeadWave (1.4s loop)**: centered on (21px,7px), the snake head independently translateX(±0.6px) swings side to side, a faster cycle than the body
- **text-pulse (1s loop)**: each letter of "PYTHON..." pulses opacity between 0.15-1, with animation-delay increasing 0.1s per letter from 0s to 0.8s to form a wave effect

## Expression
Clawd sits cross-legged playing an Indian flute (pungi), as a green pixel snake pokes out of a brown woven basket and sways to the music, colorful notes float in the air, and the "PYTHON..." text above flashes in a wave pattern.
