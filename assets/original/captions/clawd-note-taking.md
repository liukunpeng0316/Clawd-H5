# clawd-note-taking.svg

An animation of Clawd bowing his head and focusing on taking notes, with multiple animation durations layered (body 2.4s, blink 3.2s, text 4.8s).

## Body
Standard torso 11x7 at (2,6). Four legs 1x2 at y=13~15 (shorter). The eyes 1x2 at (4,8)/(10,8) continuously scaleY(0.7) squint and look down at the notebook, with step-end stepped left-right scanning. The left arm 2x2 at (0,9) moves forward via translate(3px,1px) to the holding position on the left side of the notebook. The right arm 2x2 at (13,9) moves forward via translate(-5px,1px) to the writing position on the right side of the notebook. Both arms have a 0.2-opacity black shadow.

## Props
- Notebook back cover: fill=#8D6E63, 5.4x0.3, at (3.8, 12.9)
- Notebook paper edge: fill=#FAFAFA, 5.8x0.3, at (3.6, 12.6), with two #DDD divider lines
- Notebook open page: fill=#FAFAF5, 6x0.6, at (3.5, 12), with a #BDBDBD border, rx=0.1
- Pencil eraser tip: fill=#F48FB1, 0.6x0.4
- Pencil metal ferrule: fill=#BDBDBD, 0.8x0.25
- Pencil body: fill=#FDD835, 0.6x1.8
- Pencil point: fill=#555 triangle
- The whole pencil is held tilted at rotate(25deg)
- Page text: three stroke=#444 line segments, whose opacity progressively appears with the write-text animation

## Animation
- **nod (2.4s loop)**: transform-origin (7.5px,15px), 30% translateY(0.5px) head down, 50% translateY(-0.3px) slight lift, 70% head down again
- **hold-pulse (2.4s loop)**: Left arm translate(3px,1px)~translate(3px,1.3px) slight holding pulse
- **write-stroke (0.35s loop)**: Right arm + pencil make quick writing micro-movements between translate(-5px,0.4px)~translate(-4.6px,1.2px)
- **eye-scan (3.2s loop, step-end)**: Eyes continuously scaleY(0.7) squint, translate stepping between (0,0.5px)/(0.5px,0.5px)/(-0.5px,0.5px) to simulate reading scans, with a brief head lift scaleY(0.8) at 75%~85%
- **blink (3.2s loop)**: 38%~40% scaleY(0.1) quick blink
- **ink-splash (0.7s loop)**: Three fill=#444 ink dots (0.3~0.4px), appearing at 15% opacity:0.6 and scattering in different directions (controlled via CSS custom properties --dx/--dy), each with a staggered animation-delay
- **write-text (4.8s loop, step-end)**: Page text opacity appears in stages from 0 → 0.35 → 0.55 → 0.75, resetting to 0 at 90%
- **shadow-breathe (2.4s loop)**: 50% scale(1.03) opacity(0.55) slight breathing

## Expression
Clawd reaches both arms forward to hold the notebook, writing quickly with a yellow pencil in his right hand, squinting his eyes as he focuses and scans the paper left and right, with the text on the page appearing line by line.
