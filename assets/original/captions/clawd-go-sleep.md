# clawd-go-sleep.svg

Clawd dozing off in a nightcap, 6s loop, with eyes drooping shut step by step, body slumping to one side, Zzz drifting up, and a moon and stars twinkling in the background.

## Body
Standard torso. 40-90% body-drowsy progressive deformation: scaleY(0.94~0.96) squash + scaleX(1.03~1.04) spread + rotate(2~3°) head tilt + translateY(0.5~0.8px) sink. The eyes eyes-drowsy droop shut in steps: scaleY 1 → 0.5 → 0.25 → 0.15, while scaleX 1 → 1.2 → 1.4 → 1.5 grows flatter and wider as they close.

## Props
- **Nightcap**: blue (#5C6BC0) soft floppy conical sleeping cap, tilted to the right, with a white pom-pom at the tip and white trim at the base, swaying along with the body
- **Zzz**: three letters (#7986CB/#9FA8DA/#C5CAE9), font-size 2.5/3/3.5, positioned at (13,4)/(14,3)/(15,2) respectively, drifting up with staggered delays
- **Moon**: yellow (#FFF9C4) circle, in the upper-left corner (1,-1), with pulsing opacity
- **Stars**: 3 small stars twinkling at offset frequencies

## Animation
- **body-drowsy (6s)**: progressive squash and head tilt
- **eyes-drowsy (6s)**: eyes' graded scaleY grows flatter and flatter, with width increasing in sync
- **cap-sway (6s)**: nightcap rotate(4~6°) + translate slight sway
- **zzz-float (6s ease-out)**: the three Zzz with staggered delays 0/2/4s, drifting up and to the right translate 5px/-15px and fading out
- **star-twinkle (2s ease-in-out)**: stars with delays 0/0.6/1.2s twinkling at offset frequencies
- **moon-glow (3s)**: moon opacity pulse
- **shadow-drowsy (6s)**: shadow squashes in sync

## Expression
Clawd wears a tilted blue floppy nightcap, its eyes growing flatter and wider in stages until they narrow to a slit, its body squashing and leaning to one side, Zzz letters drifting up one by one from beside its head, while the background moon glows gently and the stars twinkle.
