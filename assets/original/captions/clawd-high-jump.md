# clawd-high-jump.svg

A bouncing animation of Clawd jumping high with all its might, on a 1.4-second loop, featuring a charge-up crouch, mid-air hang time, and landing-impact effects.

## Body
Standard upright pose, with the torso 11x7 located at (2,6), #DE886D. The four legs are each 1x2 at the standard positions (3,13)/(5,13)/(9,13)/(11,13). Both arms are each 2x2 at y=9 (left arm (0,9) transform-origin right-center, right arm (13,9) transform-origin left-center), spreading/retracting with the jump. The eyes are in a happy ^^ form, drawn with polyline (stroke #000000, 0.8px), with a scaleY animation simulating a hard squint and a landing squint. The ground shadow 9x1 is located at (3,15), #000000 opacity 0.5.

## Animation
- **high-jump (1.4s loop, ease-in-out)**: 0-12% standing still → 18% deep crouch compression (translateY(1px) scaleY(0.7)) → 22% launch stretch (scaleY(1.15)) → 38% rising (translateY(-24px) scaleY(1.08)) → 46-52% peak hang time (translateY(-26px) scaleY(1)) → 62% descent stretch (translateY(-24px) scaleY(1.08)) → 78% landing squash (scaleY(0.72)) → 85% rebound overshoot (scaleY(1.05)) → 92% fine-tune (scaleY(0.97)) → 100% recover. transform-origin: 50% 100% (bottom center).
- **arm-left (1.4s loop, ease-in-out)**: 0-12% reset → 18% charge-up tuck-in (rotate(-10deg)) → 30% spread (rotate(60deg)) → 46-52% wide open at peak (rotate(85deg)) → 70% retract (rotate(50deg)) → 78% landing tuck-in (rotate(-15deg)) → 92-100% reset. transform-origin: 100% 50%.
- **arm-right (1.4s loop, ease-in-out)**: mirror of arm-left, direction reversed. 46-52% peak rotate(-85deg). transform-origin: 0% 50%.
- **eyes-squint (1.4s loop, ease-in-out)**: 0-15% scaleY(1) → 18% hard squint scaleY(0.6) → 30-70% recover scaleY(1) → 78% landing squint scaleY(0.5) → 90-100% recover.
- **shadow-shrink (1.4s loop, ease-in-out)**: 18% crouch enlargement (scale(1.2) opacity 0.6) → 46-52% extremely small at peak (scale(0.2) opacity 0.06) → 78% landing-impact spread (scale(1.3) opacity 0.65).
- **speed-show (1.4s loop, ease-out)**: briefly shows speed lines during the rising phase (24% opacity 0.6 → 44% disappears), 4 vertical lines stroke #000000 0.4px distributed on either side of the character.
- **impact-burst (1.4s loop, ease-out)**: at landing, gold (#FFC107) cross pixel stars appear at 78%, enlarging from scale(0.5) to scale(1.5) then disappearing. The left star is at (1,14), the right star at (14,14), with the right star delayed 0.03s.
- **puff-burst (1.4s loop, ease-out)**: at the moment of takeoff, gray dust puffs appear at 20% (3 clumps of #000000 low-opacity rounded rectangles), drifting downward translateY(5px) and enlarging to scale(2) then disappearing.

## Expression
Clawd crouches down with all its might then leaps up, rocketing to a 26px height with both arms spread wide, accompanied by speed lines on the way up and gold impact stars on landing, with dust puffing out from underfoot.
