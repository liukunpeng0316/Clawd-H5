# clawd-nodding-serious.svg

An animation of Clawd giving a serious salute then nodding repeatedly, on a 4.2-second loop.

## Body
Standard upright pose, with the torso 11x7 located at (2,6). The two eyes 1x2 are at (4,8) and (10,8), opening wide scaleY(1.1) during the salute phase and squinting scaleY(0.7) during the nodding phase. The left arm 2x2 at (0,9) stays still, while the right arm 2x2 at (13,9) performs the salute action pivoting on the shoulder (13px,10px). The four legs split into an outer pair (3,11)/(11,11) and an inner pair (5,11)/(9,11), stepping in alternation during the salute.

## Props
- Salute shine particles ×3: fill=#FFC107 / #FFD700 / #FFF59D, each 1x1, located in the area where the hand contacts the head (12, 6.5~8.5)

## Animation
- **legs-outer (4.2s loop)**: the outer legs lift at 8%~12% translateY(-1.5px), landing back at 14%
- **legs-inner (4.2s loop)**: the inner legs lift at 14%~18% translateY(-1.5px), landing back at 20%, alternating with the outer legs to form a stepping motion
- **breathe (3.2s loop)**: transform-origin (7.5px,13px), at 50% scale(1.02,0.98) translate(0,0.3px) a slight breathing
- **arm-salute (4.2s loop)**: 7% quickly raises translate(-1px,-1.5px) rotate(-30deg), 8%~30% holds the salute pose for a long time, 35% lowers back to position
- **nod (4.2s loop)**: transform-origin (7.5px,13px), 35%~38% first nod scale(1.03,0.95) translateY(1px), 48%~51% second nod, same parameters
- **eyes-nod (4.2s loop)**: 7%~30% scaleY(1.1) wide open to match the salute, 33% switches to scaleY(0.7) squint, translateY(0.8px) following the head sinking during nods, 58% returns to normal
- **sp-salute-1 (4.2s loop)**: 10% opacity:1 scale(1), scattering toward the upper right translate(7px,-2px), 14% disappears
- **sp-salute-2 (4.2s loop)**: 10.5% appears, scattering horizontally to the right translate(8px,0), 14.5% disappears
- **sp-salute-3 (4.2s loop)**: 11% appears, scattering toward the lower right translate(7px,2px), 15% disappears
- **shadow-nod (4.2s loop)**: during nod compression scaleX(1.06) opacity(0.48), otherwise scaleX(1) opacity(0.5)

## Expression
Clawd first solemnly raises its right arm in a salute, shine particles bursting from its hand, then lowers its arm and gives two earnest nods in a row.
