# clawd-surprised.svg

A surprised animation of Clawd recoiling in shock. 4s loop, including the body jumping back to the left, both arms spreading open, and a red exclamation mark popping out.

## Body
Standard torso 11x7 at (2,6). The eyes (1x2 each) at (4,8) and (10,8), enlarging when surprised with scaleY(1.35)+scaleX(1.1) and shifting right translateX(0.8px) to show widening and turning. The left arm (2x2) pivots around (2px,10px), spreading down and outward with rotate(-40deg)+translate(-1.5px,1px); the right arm (2x2) pivots around (13px,10px), spreading symmetrically with rotate(40deg)+translate(1.5px,1px). The left leg pair (x=3, x=5, each 1x4) follows the body translate(-5px) backward and jumps up -1.5px; the right leg pair (x=9, x=11, each 1x4) pivots around (10px,15px) with rotate(-35deg)+translate(-3.5px), tilting and stretching to connect to the body.

## Props
- Exclamation mark bar: fill=#FF3D00 (1.5x3) rx=0.3, located above the head with transform translate(6.5,2)
- Exclamation mark dot: fill=#FF3D00 (1x1) rx=0.2, located below the bar at (6.75,5.5)

## Animation
- **breathe (3.2s loop)**: Centered on (7.5px,13px), a faint breathing rise and fall of scale(1.02,0.98)+translateY(0.3px)
- **body-surprise (4s loop)**: Centered on (7.5px,15px), at 15% translate(-5px,-1.5px)+scaleX(0.85) jumping back to the left, holding the recoil pose translate(-5px,0)+scaleX(0.85) during 20%-48%, springing back to original position at 58%
- **legs-left (4s loop)**: The left leg pair follows the body, at 15% translate(-5px,-1.5px) jumping back, holding translate(-5px,0) during 20%-48%, returning at 58%
- **legs-right (4s loop)**: The right leg pair pivots around (10px,15px), at 15% translate(-3.5px,-1.5px)+rotate(-35deg) tilting widely, holding during 20%-48%, returning at 58%
- **eyes-surprise (4s loop)**: 12%-13% quick close scaleY(0) to simulate a startled blink, 16%-48% enlarging scaleY(1.35)+scaleX(1.1)+translateX(0.8px) widening and shifting right
- **arm-l-surprise (4s loop)**: Left arm at 16% translate(-1.5px,1px)+rotate(-35deg) spreading down and outward, holding rotate(-40deg) during 20%-48%, returning at 58%
- **arm-r-surprise (4s loop)**: Right arm mirrored, at 16% translate(1.5px,1px)+rotate(35deg) spreading open, holding rotate(40deg) during 20%-48%, returning at 58%
- **exclaim-pop (4s loop)**: At 16% scale(1.3) pops out with overshoot, at 18% shrinks back to scale(1) to settle, holds at 42%, at 50% floats up translate(0,-3px)+scale(0.7) and fades out
- **shadow-surprise (4s loop)**: Follows the body translate(-5px,0)+scaleX(0.85)+opacity(0.4) contracting to the left, returning at 58%

## Expression
Clawd is suddenly startled, his body abruptly jumping back to the rear-left, both arms spreading to the sides, his eyes going wide, a red exclamation mark popping out above his head, and then he slowly recovers his standing posture.
