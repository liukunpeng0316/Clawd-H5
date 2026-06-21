# clawd-disconnected.svg

6s infinite-loop animation of Clawd searching for a Bluetooth connection signal. The whole thing is mirrored horizontally.

## Body
Standard standing posture; the torso, arms, legs, and ground shadow are all at default positions and sizes.

## Animation
- **6s sequence**: first looks left (torso shifts left 1px, eyes shift left 2px) → looks right → quick side-to-side head shake (anxious searching) → gazes up to the right (target found)
- **Question mark**: a white pixel question mark fades in from below and rises during confusion
- **Exclamation mark**: a blue (#0082FC) pixel exclamation mark pops out when the signal is found
- **BLE icon**: the Bluetooth symbol (right side of the frame, x=26) floats up and down on a 3s cycle, with its own blue glow pulse
- **Blink**: about 3 quick blinks within the 6s cycle

## Expression
Clawd stands looking left and right until it spots the BLE connection icon floating in the upper right. It simulates searching for a signal source after a device disconnects.
