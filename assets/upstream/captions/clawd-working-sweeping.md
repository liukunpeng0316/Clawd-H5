# clawd-working-sweeping.svg

Clawd diligently sweeps the floor, the whole figure horizontally mirrored (facing left).

## Body
Standard torso and four legs. The right arm carries a sweeping animation.

## Props
- **Broom**: A brown long handle (#795548, width 1 height 10) + a yellow brush head at the bottom (#FFC107, 4x2).
- **Dust particles**: Two small gray rectangles (#9E9E9E/#B0BEC5).

## Animation
- **Broom (1.5s)**: sweeps back and forth between 10°-30° around the bottom end of the handle.
- **Body lean (1.5s)**: rotate 5°→15°, combined with translate(3px,1px) for a forceful horizontal sweep.
- **Right arm (1.5s)**: rotates from 0° to -20°.
- **Dust**: drifts along the ground from the broom's contact point at x=19 to x=25, then fades out.

## Expression
Clawd bends down and sweeps the floor forcefully, kicking up dust.
