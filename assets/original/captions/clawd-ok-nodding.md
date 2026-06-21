# clawd-ok-nodding.svg

An animation of Clawd hopping and nodding continuously while holding up a checkmark sign, looping every 1.5 seconds with a seamless double-hop.

## Body
Standard torso with breathing (3.2s). body-translate is a 1.5s translateY arc 0.8 → -4.5 → 0.8px, completing two bounces per cycle without pausing. body-squash is a 1.5s crouch scaleY(0.94) scaleX(1.04) with scaleY/X(1.0,1.0) at the peak. The eyes do a single eyes-blink at 27% with scaleY(0.1).

## Props
- **Checkmark sign**: A brown border (#795548) + white fill (#FFFFFF), size 11×6.5, scale(0.6), worn on top of the head.
- **Green checkmark**: A (#7CB342) stroked polyline, with no text label.

## Animation
- **breathe (3.2s)**: standard breathing.
- **body-translate (1.5s)**: a seamless double-hop loop, dwelling briefly at the peak at 25-30%/75-80%.
- **body-squash (1.5s)**: landing crouch scaleY(0.94)/scaleX(1.04), peak 1.0.
- **sign-bounce (1.5s)**: the sign's translateY(±0.8px) lag effect — compressed on landing, surging up at the peak.
- **eyes-blink (1.5s)**: a single blink at 27%.
- **shadow-jump (1.5s)**: the shadow's scaleX 1.1 → 0.7, opacity pulsing to reflect the height.

## Expression
Clawd hops and nods nonstop in agreement, holding a white sign with a green checkmark above its head; on every landing it crouches and immediately springs back up, the sign bouncing on its head while the shadow on the ground contracts and expands along with it.
